"""
pymlrev2-main → Colab 호환 마이그레이션 스크립트

원본 노트북은 보존하고, 같은 폴더에 `<이름>_colab.ipynb`로 저장합니다.

대상 변환:
  - load_boston 제거 대응 (fetch_california_housing 대체 + 안내 주석)
  - DataFrame.append → pd.concat
  - OneHotEncoder(sparse=...) → sparse_output=...
  - .iteritems() → .items()
  - np.bool / np.int / np.float → 내장 타입
  - KMeans(...)에 n_init=10 명시
  - mean_squared_error(..., squared=False) → np.sqrt(mean_squared_error(...))
  - XGB/LGBM .fit(..., early_stopping_rounds=, eval_metric=) → ⚠️ 주석으로 안내(자동 변환은 셀별 의미가 달라 비활성)
  - 첫 셀에 Colab 환경 안내(데이터 경로/한글 폰트/필수 설치) 추가

사용법:
    python migrate_to_colab.py            # 기본 챕터(1,2,3,4,5,7,8) 일괄
    python migrate_to_colab.py 4 5        # 특정 챕터만
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_CHAPTERS = ["1장", "2장", "3장", "4장", "5장", "7장", "8장"]


# ---------- 셀 단위 패치 ----------

def patch_sparse(src: str) -> str:
    # OneHotEncoder(sparse=False) → OneHotEncoder(sparse_output=False)
    return re.sub(r"(OneHotEncoder\([^)]*?)\bsparse\s*=", r"\1sparse_output=", src)


def patch_iteritems(src: str) -> str:
    return re.sub(r"\.iteritems\(\)", ".items()", src)


def patch_np_aliases(src: str) -> str:
    # np.bool / np.int / np.float (단독 타입 참조)
    # dtype 인자나 isinstance 호출 등에서 자주 등장.
    src = re.sub(r"\bnp\.bool\b(?!_)", "bool", src)
    src = re.sub(r"\bnp\.int\b(?!_|8|16|32|64|p)", "int", src)
    src = re.sub(r"\bnp\.float\b(?!_|16|32|64|128)", "float", src)
    src = re.sub(r"\bnp\.object\b(?!_)", "object", src)
    return src


def patch_kmeans_ninit(src: str) -> str:
    """KMeans(...) 호출에 n_init=가 없으면 n_init=10 추가."""
    def add_ninit(m: re.Match) -> str:
        head, args = m.group(1), m.group(2)
        if "n_init" in args:
            return m.group(0)
        # 빈 인자거나 끝 공백만 있으면
        new_args = (args.rstrip()
                    + (", " if args.strip() else "")
                    + "n_init=10")
        return f"{head}({new_args})"
    return re.sub(r"(KMeans)\(([^()]*)\)", add_ninit, src)


def patch_mse_squared_false(src: str) -> str:
    """mean_squared_error(a, b, squared=False) → np.sqrt(mean_squared_error(a, b))

    sklearn 1.6에서 squared 인자가 제거됨. root_mean_squared_error로 가도 되지만
    구버전 호환을 위해 np.sqrt 래핑이 가장 안전.
    """
    pattern = re.compile(
        r"mean_squared_error\(([^()]*?),\s*squared\s*=\s*False\s*\)"
    )
    return pattern.sub(r"np.sqrt(mean_squared_error(\1))", src)


def patch_load_boston(src: str) -> str:
    """load_boston 사용 셀에 안내 + fetch_california_housing 대체.

    load_boston은 윤리적 문제로 sklearn 1.2부터 제거. 책 본문은 보스턴 데이터를 쓰지만
    Colab에서는 캘리포니아 주택 데이터로 대체. 컬럼/타깃 차이는 주석으로 명시.
    """
    if "load_boston" not in src:
        return src

    notice = (
        "# ⚠️ Colab 호환 안내: sklearn 1.2+에서 load_boston이 제거되었습니다.\n"
        "#   대체로 fetch_california_housing을 사용합니다.\n"
        "#   - 피처 개수/이름이 책과 다릅니다(13개 → 8개).\n"
        "#   - 타깃 단위도 다릅니다(가격 → 중위 주택 가격, 10만 달러 단위).\n"
        "#   - 회귀 모델 적용 흐름은 동일합니다.\n"
    )
    src = notice + src
    src = src.replace(
        "from sklearn.datasets import load_boston",
        "from sklearn.datasets import fetch_california_housing",
    )
    # boston = load_boston() / data = load_boston() 등을 일괄 치환
    src = re.sub(
        r"(\w+)\s*=\s*load_boston\(\)",
        r"\1 = fetch_california_housing()",
        src,
    )
    return src


def patch_df_append(src: str) -> str:
    """DataFrame.append(...) → pd.concat([...], ignore_index=True).

    완벽한 정적 분석은 어렵지만, 책 코드의 일반적 패턴(`df = df.append(...)`)을 처리.
    list.append(...)은 인자 형태로 구분: ignore_index= 가 있으면 거의 확실히 DataFrame.append.
    """
    # 패턴 1: df = df.append(other, ignore_index=True)
    src = re.sub(
        r"([A-Za-z_]\w*)\s*=\s*\1\.append\(([^()]*?ignore_index\s*=\s*True[^()]*?)\)",
        r"\1 = pd.concat([\1, \2.drop(columns=[]) if False else \2], ignore_index=True)",
        src,
    )
    # 위 치환은 너무 복잡 — 단순화 버전으로 다시
    return src


def patch_df_append_simple(src: str) -> str:
    """DataFrame.append → pd.concat 단순 치환.

    `<var> = <var>.append(<expr>, ignore_index=True)` 패턴만 처리.
    그 외의 경우는 주석 경고만 부착.
    """
    pattern = re.compile(
        r"^(\s*)([A-Za-z_]\w*)\s*=\s*\2\.append\((.+?),\s*ignore_index\s*=\s*True\s*\)\s*$",
        re.MULTILINE,
    )
    def repl(m: re.Match) -> str:
        indent, var, expr = m.group(1), m.group(2), m.group(3)
        return f"{indent}{var} = pd.concat([{var}, {expr}], ignore_index=True)"
    new_src = pattern.sub(repl, src)

    # 그 외 .append( with ignore_index 패턴은 안내 주석 부착
    remaining = re.search(
        r"(?<!\.)\.append\([^)]*ignore_index", new_src
    )
    if remaining and "pd.concat" not in new_src[max(0, remaining.start()-40):remaining.start()]:
        new_src = (
            "# ⚠️ DataFrame.append가 pandas 2.0에서 제거되었습니다. "
            "아래 .append(... ignore_index=...) 호출을 pd.concat([df1, df2], ignore_index=True)로 직접 바꿔주세요.\n"
            + new_src
        )
    return new_src


def _extract_kwargs_from_fit(fit_args: str) -> tuple[str, dict[str, str]]:
    """fit(...) 인자 문자열에서 early_stopping_rounds, eval_metric, verbose를 분리.

    반환: (정리된 fit 인자, 추출된 kwargs dict)
    문자열 파싱이므로 중첩 괄호 정도만 허용. 따옴표 안의 콤마는 처리하지 않음(책 코드 범위에선 안전).
    """
    # 콤마로 split (단, 괄호 깊이 0일 때만)
    parts: list[str] = []
    buf = ""
    depth = 0
    for ch in fit_args:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf)

    extracted: dict[str, str] = {}
    keep: list[str] = []
    for p in parts:
        stripped = p.strip()
        m = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.+)$", stripped, re.DOTALL)
        if m and m.group(1) in {"early_stopping_rounds", "eval_metric", "verbose"}:
            extracted[m.group(1)] = m.group(2).strip()
        else:
            keep.append(p)
    return ",".join(keep).strip().rstrip(","), extracted


def _find_balanced_call(src: str, start: int) -> int:
    """src[start]가 '(' 일 때 짝이 맞는 ')' 의 인덱스 반환. 없으면 -1.

    문자열 리터럴(따옴표) 안의 괄호도 무시.
    """
    depth = 0
    i = start
    in_str: str | None = None
    while i < len(src):
        ch = src[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
        else:
            if ch in ("'", '"'):
                in_str = ch
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def _iter_fit_calls(src: str):
    """소스에서 `<var>.fit(...)` 호출들을 순서대로 yield.

    각 항목: (start_index, end_index, var_name, args_str)
    중첩 괄호와 문자열을 안전하게 처리.
    """
    for m in re.finditer(r"([A-Za-z_]\w*)\.fit\(", src):
        open_paren = m.end() - 1
        close_paren = _find_balanced_call(src, open_paren)
        if close_paren == -1:
            continue
        args = src[open_paren + 1:close_paren]
        yield m.start(), close_paren + 1, m.group(1), args


def _rewrite_fit_calls(src: str, transform) -> str:
    """transform(var, args)이 새 .fit 인자 문자열(또는 None=변경없음)을 반환하도록 호출."""
    out_parts = []
    cursor = 0
    for start, end, var, args in _iter_fit_calls(src):
        new_args = transform(var, args)
        if new_args is None:
            continue
        out_parts.append(src[cursor:start])
        out_parts.append(f"{var}.fit({new_args})")
        cursor = end
    out_parts.append(src[cursor:])
    return "".join(out_parts)


def _is_xgb_var(src: str, var: str) -> bool:
    return re.search(rf"\b{re.escape(var)}\s*=\s*XGB(Classifier|Regressor)\(", src) is not None


def _is_lgbm_var(src: str, var: str) -> bool:
    return re.search(rf"\b{re.escape(var)}\s*=\s*LGBM(Classifier|Regressor)\(", src) is not None


def patch_xgb_fit(src: str) -> str:
    """XGBoost: .fit(...)의 early_stopping_rounds/eval_metric을 생성자로 이동.

    같은 셀의 생성자에 주입. 생성자가 같은 셀에 없으면 set_params 호출을 자동 삽입.
    """
    if not re.search(r"\.fit\(", src):
        return src
    # XGB 생성자가 같은 셀에 있거나, 변수명이 xgb 계열이면 처리
    has_xgb_ctor = bool(re.search(r"XGB(Classifier|Regressor)\(", src))
    has_xgb_varname = bool(re.search(r"\b[Xx][Gg][Bb]\w*\.fit\(", src))
    if not (has_xgb_ctor or has_xgb_varname):
        return src

    extracted_per_var: dict[str, dict[str, str]] = {}
    unsourced_extracts: list[tuple[str, dict[str, str]]] = []  # 생성자 못 찾은 경우

    def looks_like_xgb_var(name: str) -> bool:
        n = name.lower()
        return n.startswith("xgb") or n.startswith("xgboost") or "xgb" in n

    def transform(var: str, args: str):
        is_xgb_here = _is_xgb_var(src, var)
        if not is_xgb_here and not looks_like_xgb_var(var):
            return None
        new_args, kw = _extract_kwargs_from_fit(args)
        moved = {k: kw[k] for k in ("early_stopping_rounds", "eval_metric") if k in kw}
        if not moved and "verbose" not in kw:
            return None
        if moved:
            if is_xgb_here:
                extracted_per_var.setdefault(var, {}).update(moved)
            else:
                # 다른 셀에 생성자가 있는 경우 — set_params로 안내
                unsourced_extracts.append((var, moved))
        if "verbose" in kw:
            new_args = (new_args + (", " if new_args else "") + f"verbose={kw['verbose']}").strip(", ")
        return new_args

    new_src = _rewrite_fit_calls(src, transform)

    # 생성자에 주입
    for var, moved in extracted_per_var.items():
        ctor_re = re.compile(rf"(\b{re.escape(var)}\s*=\s*XGB(?:Classifier|Regressor))\(", re.MULTILINE)
        m = ctor_re.search(new_src)
        if not m:
            continue
        open_paren = m.end() - 1
        close_paren = _find_balanced_call(new_src, open_paren)
        if close_paren == -1:
            continue
        existing_args = new_src[open_paren + 1:close_paren]
        injections = []
        for k, v in moved.items():
            if re.search(rf"\b{k}\s*=", existing_args):
                continue
            injections.append(f"{k}={v}")
        if not injections:
            continue
        joined = ", ".join(injections)
        sep = ", " if existing_args.strip() else ""
        new_existing = existing_args.rstrip().rstrip(",")
        replacement = f"{new_src[m.start():open_paren+1]}{new_existing}{sep}{joined})"
        new_src = new_src[:m.start()] + replacement + new_src[close_paren + 1:]

    if unsourced_extracts:
        # 생성자가 다른 셀에 있는 경우 — set_params()로 동등 코드를 자동 삽입
        set_params_lines: list[str] = [
            "# Colab 호환: 생성자가 이전 셀에 있어 set_params로 옮겼습니다 (XGBoost 2.x)\n"
        ]
        seen: set[str] = set()
        for var, moved in unsourced_extracts:
            if var in seen:
                continue
            seen.add(var)
            kv = ", ".join(f"{k}={v}" for k, v in moved.items())
            set_params_lines.append(f"{var}.set_params({kv})\n")
        # 첫 fit 호출 직전에 삽입
        first_fit = re.search(r"^\s*[A-Za-z_]\w*\.fit\(", new_src, re.MULTILINE)
        injection = "".join(set_params_lines)
        if first_fit:
            new_src = new_src[:first_fit.start()] + injection + new_src[first_fit.start():]
        else:
            new_src = injection + new_src
    return new_src


def patch_lgbm_fit(src: str) -> str:
    """LightGBM: .fit(...)의 early_stopping_rounds/verbose → callbacks 이동.

    eval_metric은 fit에 유지(LGBM 4.x 허용).
    """
    if not re.search(r"\.fit\(", src):
        return src
    has_lgbm_ctor = bool(re.search(r"LGBM(Classifier|Regressor)\(", src))
    has_lgbm_varname = bool(re.search(r"\b[Ll][Gg][Bb][Mm]?\w*\.fit\(", src))
    if not (has_lgbm_ctor or has_lgbm_varname):
        return src

    needs_import_lgb = False

    def looks_like_lgbm_var(name: str) -> bool:
        n = name.lower()
        return n.startswith("lgbm") or n.startswith("lgb") or "lgbm" in n

    def transform(var: str, args: str):
        if not _is_lgbm_var(src, var) and not looks_like_lgbm_var(var):
            return None
        new_args, kw = _extract_kwargs_from_fit(args)
        callbacks: list[str] = []
        if "early_stopping_rounds" in kw:
            callbacks.append(f"lgb.early_stopping(stopping_rounds={kw['early_stopping_rounds']})")
        if "verbose" in kw:
            if kw["verbose"].strip() in {"False", "0"}:
                callbacks.append("lgb.log_evaluation(period=0)")
            else:
                callbacks.append("lgb.log_evaluation(period=100)")
        if not callbacks and "early_stopping_rounds" not in kw and "verbose" not in kw:
            return None
        if callbacks:
            nonlocal needs_import_lgb
            needs_import_lgb = True
            cb = "callbacks=[" + ", ".join(callbacks) + "]"
            new_args = (new_args + (", " if new_args else "") + cb).strip(", ")
        return new_args

    new_src = _rewrite_fit_calls(src, transform)

    if needs_import_lgb and "import lightgbm as lgb" not in new_src:
        lines = new_src.splitlines(keepends=True)
        for i, ln in enumerate(lines):
            if "from lightgbm" in ln or "import lightgbm" in ln:
                lines.insert(i + 1, "import lightgbm as lgb  # callbacks 사용을 위해 추가\n")
                break
        else:
            lines.insert(0, "import lightgbm as lgb  # callbacks 사용을 위해 추가\n")
        new_src = "".join(lines)
    return new_src


def patch_xgb_lgbm_fit(src: str) -> str:
    return patch_lgbm_fit(patch_xgb_fit(src))


def patch_old_imports(src: str) -> str:
    """seaborn/plot 임포트 정리는 건드리지 않음. 본 자리 표시자."""
    return src


CELL_PATCHES = [
    patch_load_boston,          # 가장 먼저(없으면 no-op)
    patch_sparse,
    patch_iteritems,
    patch_np_aliases,
    patch_kmeans_ninit,
    patch_mse_squared_false,
    patch_df_append_simple,
    patch_xgb_lgbm_fit,
]


def apply_patches(src: str) -> tuple[str, list[str]]:
    """모든 패치 적용 후 (새 소스, 변경된 패치 이름 리스트) 반환."""
    new = src
    applied: list[str] = []
    for fn in CELL_PATCHES:
        before = new
        new = fn(new)
        if new != before:
            applied.append(fn.__name__)
    return new, applied


# ---------- 노트북 단위 ----------

HEADER_MD = """# Colab 호환 버전

이 노트북은 원본 책 예제를 **Google Colab 최신 환경(2026)** 에 맞춰 자동 마이그레이션한 버전입니다.

## 적용된 변경
- `load_boston` → `fetch_california_housing` (sklearn 1.2+ 호환)
- `DataFrame.append` → `pd.concat` (pandas 2.0+ 호환)
- `OneHotEncoder(sparse=)` → `sparse_output=` (sklearn 1.2+)
- `.iteritems()` → `.items()` (pandas 2.0+)
- `np.bool / np.int / np.float` → 내장 타입 (numpy 1.20+)
- `KMeans()`에 `n_init=10` 명시 (sklearn 1.4+ 경고 회피)
- `mean_squared_error(..., squared=False)` → `np.sqrt(...)` 래핑 (sklearn 1.6+)
- XGBoost/LightGBM `.fit()` 파라미터는 자동 변환 대신 안내 주석을 달았습니다(셀별 의미 차이 때문).

## Colab 데이터 경로
원본은 같은 폴더의 csv/xlsx 파일을 가정합니다. Colab에서는 두 가지 방법 중 하나를 쓰세요.
1. **직접 업로드**: 좌측 파일 패널 → 업로드, 이후 경로는 `./파일명` 또는 `/content/파일명`.
2. **Drive 마운트**:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    # 이후 경로: /content/drive/MyDrive/...
    ```
"""

SETUP_CODE = """# Colab 환경 점검 (선택 실행)
import sys, platform
print('Python:', sys.version.split()[0], '| Platform:', platform.platform())
try:
    import numpy, pandas, sklearn
    print('numpy:', numpy.__version__, '| pandas:', pandas.__version__, '| sklearn:', sklearn.__version__)
except Exception as e:
    print('환경 점검 중 경고:', e)
"""

KOREAN_FONT_CODE = """# 한글 폰트 (matplotlib/seaborn) — Colab에서 한글이 깨질 때만 실행
# !sudo apt-get -qq install -y fonts-nanum > /dev/null
# !fc-cache -fv > /dev/null
# import matplotlib as mpl, matplotlib.font_manager as fm
# mpl.rcParams['font.family'] = 'NanumGothic'
# mpl.rcParams['axes.unicode_minus'] = False
"""


def make_code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def make_md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def get_source_str(cell: dict) -> str:
    s = cell.get("source", "")
    if isinstance(s, list):
        return "".join(s)
    return s


def set_source_str(cell: dict, new_src: str) -> None:
    cell["source"] = new_src.splitlines(keepends=True)


def needs_korean_font(nb_path: Path) -> bool:
    # 10장은 시각화 전용이라 항상 필요. 7~9장 일부도 한글 라벨 사용.
    name = nb_path.name
    return "한글" in name or "10장" in str(nb_path) or "Visualization" in name


def migrate_notebook(src_path: Path) -> tuple[Path, list[str]]:
    with src_path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    changes_summary: list[str] = []

    # 각 코드 셀에 패치 적용
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = get_source_str(cell)
        if not src.strip():
            continue
        new_src, applied = apply_patches(src)
        if applied:
            set_source_str(cell, new_src)
            # outputs/execution_count는 깨끗하게 비움(실행 결과 충돌 방지)
            cell["outputs"] = []
            cell["execution_count"] = None
            changes_summary.extend(applied)

    # 헤더 추가
    header_cells = [make_md_cell(HEADER_MD), make_code_cell(SETUP_CODE)]
    if needs_korean_font(src_path):
        header_cells.append(make_code_cell(KOREAN_FONT_CODE))
    nb["cells"] = header_cells + nb.get("cells", [])

    # 커널 메타데이터 (필요 시)
    nb.setdefault("metadata", {})
    nb["metadata"].setdefault("kernelspec", {"name": "python3", "display_name": "Python 3"})
    nb["metadata"].setdefault("language_info", {"name": "python"})

    out_path = src_path.with_name(src_path.stem + "_colab" + src_path.suffix)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return out_path, changes_summary


def iter_notebooks(chapter_dir: Path):
    for p in sorted(chapter_dir.glob("*.ipynb")):
        if p.stem.endswith("_colab"):
            continue
        yield p


def main(chapters: list[str]) -> None:
    grand_total = {}
    for ch in chapters:
        ch_dir = ROOT / ch
        if not ch_dir.is_dir():
            print(f"[skip] {ch} 폴더 없음")
            continue
        print(f"\n=== {ch} ===")
        for nb in iter_notebooks(ch_dir):
            out, changes = migrate_notebook(nb)
            tag = ", ".join(sorted(set(changes))) if changes else "헤더만 추가"
            print(f"  ✓ {nb.name}\n      → {out.name}\n      patches: {tag}")
            for c in changes:
                grand_total[c] = grand_total.get(c, 0) + 1

    print("\n=== 전체 패치 통계 ===")
    for k, v in sorted(grand_total.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    args = sys.argv[1:]
    chapters = [f"{n}장" if n.isdigit() else n for n in args] if args else DEFAULT_CHAPTERS
    main(chapters)
