#!/usr/bin/env python3
"""04_cloud 챕터 → 학생 배포용 단일 PDF 생성.

흐름: _site의 렌더링된 HTML을 추출 → 강사 전용 섹션 제거 →
페이지 브레이크 + 표지 + 목차 추가 → Chrome 헤드리스로 PDF 출력 → pdfunite 로 표지+본문 결합.
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
SERVE_URL = "http://127.0.0.1:4000"
SITE_HTML = SITE / "handout.html"  # Jekyll 서버가 서빙 → http://127.0.0.1:4000/handout.html
OUT_DIR = ROOT / "build" / "handout"
OUT_HTML = OUT_DIR / "handout.html"
OUT_PDF = OUT_DIR / "AWS_클라우드_입문_수강생자료.pdf"
OUT_DOCX = OUT_DIR / "AWS_클라우드_입문_수강생자료.docx"
MERMAID_DIR = OUT_DIR / "mermaid"  # 사전 렌더링한 PNG 캐시

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# (제목, 파일경로). nav_order 1~8 순서.
CHAPTERS = [
    ("01. 클라우드와 AWS 소개", SITE / "cloud" / "intro.html"),
    ("02. AWS 가입 따라하기", SITE / "cloud" / "signup.html"),
    ("03. AWS 콘솔과 비용 관리", SITE / "cloud" / "console-billing.html"),
    ("04. EC2 생성과 접속", SITE / "cloud" / "ec2.html"),
    ("05. 리눅스 기초 명령어", SITE / "cloud" / "linux-basics.html"),
    ("06. 웹서버 Nginx 설치", SITE / "cloud" / "nginx.html"),
    ("07. GitHub에서 정적 사이트 배포", SITE / "cloud" / "github-deploy.html"),
    ("08. 리소스 정리와 다음 단계", SITE / "cloud" / "cleanup.html"),
]


def extract_main(html_path: Path) -> Tag:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")
    main = soup.select_one("div.main-content")
    if main is None:
        raise RuntimeError(f"main-content not found in {html_path}")
    return main


def strip_instructor_blocks(content: Tag) -> None:
    """공통 패턴: 🎤 가 들어간 blockquote = 강사 운영 안내. 일괄 제거."""
    for bq in content.find_all("blockquote"):
        text = bq.get_text(" ", strip=True)
        if "🎤" in text:
            bq.decompose()
            continue
        if "강사 운영 노트" in text or "강사용" in text and "수강생은 읽지 않아도" in text:
            bq.decompose()


def strip_section_by_heading(content: Tag, heading_text_match: str) -> None:
    """특정 H2 헤딩과 그 뒤 형제 노드를 다음 H2 만날 때까지 제거."""
    target = None
    for h in content.find_all(["h2"]):
        if heading_text_match in h.get_text(" ", strip=True):
            target = h
            break
    if target is None:
        return

    # H2 직전에 <hr>이 있으면 같이 제거 (Just-the-Docs는 챕터 사이 hr를 넣음)
    prev = target.find_previous_sibling()
    while prev and prev.name in ("hr",):
        nxt = prev.find_previous_sibling()
        prev.decompose()
        prev = nxt

    # H2부터 다음 H2 직전까지 제거
    nxt = target.find_next_sibling()
    while nxt and not (isinstance(nxt, Tag) and nxt.name == "h2"):
        following = nxt.find_next_sibling()
        nxt.decompose()
        nxt = following
    target.decompose()


def fix_image_paths(content: Tag) -> None:
    """이미지 src를 file:// 절대경로로 변환.
    Pandoc(HTML→DOCX)과 Chrome 헤드리스 모두에서 동일하게 작동.
    """
    for img in content.find_all("img"):
        src = img.get("src", "")
        if src.startswith("/"):
            abs_path = SITE / src.lstrip("/")
            if abs_path.exists():
                img["src"] = "file://" + str(abs_path)


def strip_jtd_footer(content: Tag) -> None:
    """Just-the-Docs가 main-content 마지막에 붙이는 'Back to top', 'Edit this page on GitHub' 링크/푸터 제거."""
    for el_id in ("back-to-top", "edit-this-page"):
        el = content.find(id=el_id)
        if el is not None:
            # 부모 wrapper(div / footer)까지 찾아 제거
            parent = el.parent
            while parent and parent.name in ("p", "div") and len(parent.find_all(True, recursive=False)) <= 2:
                grand = parent.parent
                if grand is None or grand.get("class") == ["main-content"]:
                    break
                parent = grand
            (parent or el).decompose()


def fix_internal_links(content: Tag) -> None:
    """절대/상대 사이트 내부 링크는 PDF에서는 작동 안 하므로 텍스트로 둠.

    페이지 내부 #앵커 링크는 그대로 둠 (PDF에서도 동작).
    /cloud/... 형태 링크는 텍스트로 변환.
    """
    for a in content.find_all("a"):
        href = a.get("href", "")
        if href.startswith("/"):
            # 사이트 내부 절대 링크 → 텍스트만 남김
            a.unwrap()


def render_mermaid_png(mermaid_src: str) -> Path:
    """mermaid 코드를 PNG로 렌더링. SHA 기반 캐시."""
    MERMAID_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(mermaid_src.encode("utf-8")).hexdigest()[:16]
    png_path = MERMAID_DIR / f"{digest}.png"
    if png_path.exists():
        return png_path

    mmd_path = MERMAID_DIR / f"{digest}.mmd"
    mmd_path.write_text(mermaid_src, encoding="utf-8")
    cmd = [
        "mmdc",
        "-i", str(mmd_path),
        "-o", str(png_path),
        "-b", "white",
        "-w", "1400",  # 충분한 해상도
        "-s", "2",     # 2배 스케일
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    mmd_path.unlink(missing_ok=True)
    if res.returncode != 0 or not png_path.exists():
        print(f"  [warn] mmdc 실패 (digest={digest}): {res.stderr[-300:]}")
        return None
    return png_path


def transform_mermaid(content: Tag) -> None:
    """Just-the-Docs ```mermaid``` 블록 → mmdc로 PNG 사전 렌더링 → <img>로 교체.

    Word/PDF 모두에서 안정적으로 표시되며, Chrome 헤드리스 timing 이슈도 우회.
    """
    soup_factory = BeautifulSoup("", "lxml")  # new_tag()용
    for code in content.find_all("code", class_="language-mermaid"):
        mermaid_src = code.get_text()
        wrapper = code
        for ancestor in code.parents:
            if not isinstance(ancestor, Tag):
                break
            cls = ancestor.get("class") or []
            if ancestor.name in ("pre", "figure") or "highlight" in cls or "language-mermaid" in cls or "highlighter-rouge" in cls:
                wrapper = ancestor
            else:
                break

        png_path = render_mermaid_png(mermaid_src)
        if png_path is None:
            # 폴백: 코드를 그대로 둠
            continue
        # Pandoc/Chrome 모두에서 작동하도록 file:// URI 사용
        img = soup_factory.new_tag(
            "img",
            attrs={
                "src": "file://" + str(png_path),
                "alt": "diagram",
                "class": "mermaid-img",
            },
        )
        figure = soup_factory.new_tag("figure", attrs={"class": "mermaid-fig"})
        figure.append(img)
        wrapper.replace_with(figure)


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    chapter_htmls = []
    for title, path in CHAPTERS:
        if not path.exists():
            sys.exit(f"missing: {path}")
        main = extract_main(path)

        # 챕터별 강사 전용 제거
        strip_instructor_blocks(main)
        if "07. GitHub" in title:
            strip_section_by_heading(main, "강사용: 레포 사전 준비")
        # 02장은 본문 어딘가에 별도 강사 안내 박스가 있을 수 있는데 strip_instructor_blocks 이 처리

        fix_image_paths(main)
        fix_internal_links(main)
        strip_jtd_footer(main)
        transform_mermaid(main)

        # 챕터 래퍼
        wrapper = BeautifulSoup(
            f'<section class="chapter"><div class="chapter-content"></div></section>',
            "lxml",
        ).section
        wrapper.div.append(main)
        chapter_htmls.append(str(wrapper))

    cover = """
    <section class="cover">
      <div class="cover-inner">
        <h1>AWS 클라우드 1일 입문</h1>
        <h2>수강생 배포 자료</h2>
        <p class="cover-meta">실습 가이드 · 01~08장</p>
        <p class="cover-foot">EC2 · Nginx · GitHub 배포 · 비용 관리</p>
      </div>
    </section>
    """

    toc_items = "".join(
        f'<li><span class="toc-title">{title}</span></li>' for title, _ in CHAPTERS
    )
    toc = f"""
    <section class="toc-page">
      <h1>목차</h1>
      <ol class="toc-list">
        {toc_items}
      </ol>
      <p class="toc-note">본 자료는 학습 흐름상 <strong>01장 → 08장 순서</strong>로 진행하도록 구성되었습니다.</p>
    </section>
    """

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<title>AWS 클라우드 1일 입문 — 수강생 자료</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<!-- Mermaid는 mmdc로 사전 PNG 렌더링되어 <img>로 임베드되므로 런타임 스크립트 불필요 -->
<style>
  @page {{ size: A4; margin: 18mm 16mm 22mm 16mm; }}
  @page :left {{ @bottom-left {{ content: counter(page); }} }}
  @page :right {{ @bottom-right {{ content: counter(page); }} }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1f2937;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  h1, h2, h3, h4 {{ color: #111827; line-height: 1.3; page-break-after: avoid; }}
  h1 {{ font-size: 18pt; margin: 0 0 12pt; border-bottom: 2px solid #1e40af; padding-bottom: 6pt; }}
  h2 {{ font-size: 14pt; margin: 18pt 0 8pt; color: #1e40af; }}
  h3 {{ font-size: 12pt; margin: 12pt 0 6pt; }}
  h4 {{ font-size: 11pt; margin: 10pt 0 4pt; }}
  p {{ margin: 6pt 0; }}
  ul, ol {{ margin: 6pt 0; padding-left: 22pt; }}
  li {{ margin: 2pt 0; }}
  code {{ font-family: 'JetBrains Mono', Menlo, Consolas, monospace; font-size: 9.5pt; }}
  p code, li code, td code {{
    background: #f3f4f6; padding: 1pt 4pt; border-radius: 3pt;
  }}
  pre {{
    background: #f8fafc !important;
    border: 0.5pt solid #cbd5e1;
    padding: 7pt 9pt; border-radius: 3pt;
    font-family: 'JetBrains Mono', Menlo, monospace; font-size: 9pt;
    white-space: pre-wrap; word-break: break-all;
    page-break-inside: avoid;
    margin: 6pt 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  pre, pre code, pre code * {{
    color: #0f172a !important;
    background-color: transparent !important;
  }}
  pre {{ background-color: #f8fafc !important; }}
  /* Just-the-Docs syntax highlight 토큰 색 (어두운 글자, 인쇄 친화) */
  pre .k, pre .kn, pre .kc, pre .kt {{ color: #7c3aed !important; }}
  pre .s, pre .s1, pre .s2 {{ color: #b91c1c !important; }}
  pre .c, pre .c1 {{ color: #6b7280 !important; font-style: italic; }}
  pre .nf, pre .nb {{ color: #1d4ed8 !important; }}
  pre .err {{ color: #0f172a !important; background: transparent !important; }}
  div.highlighter-rouge, figure.highlight, div.highlight {{
    background: transparent !important;
  }}
  blockquote {{
    margin: 8pt 0;
    padding: 8pt 12pt;
    border-left: 4pt solid #3b82f6;
    background: #eff6ff !important;
    border-radius: 2pt;
    page-break-inside: avoid;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  blockquote > :first-child {{ margin-top: 0; }}
  blockquote > :last-child {{ margin-bottom: 0; }}
  table {{
    border-collapse: collapse; width: 100%; margin: 8pt 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  th, td {{ border: 0.5pt solid #cbd5e1; padding: 4pt 6pt; text-align: left; vertical-align: top; }}
  th {{
    background: #f1f5f9 !important; font-weight: 600;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  img {{
    max-width: 70%;         /* 가로 폭 축소 → 비례적으로 height도 축소 */
    max-height: 36vh;       /* 짧은 섹션이 한 페이지 빈 공간에 들어가도록 */
    height: auto;
    width: auto;
    display: block;
    margin: 6pt auto;
    object-fit: contain;
  }}
  hr {{ border: none; border-top: 0.5pt solid #cbd5e1; margin: 12pt 0; }}
  figure.mermaid-fig {{
    text-align: center;
    margin: 10pt 0;
    page-break-inside: avoid;
  }}
  img.mermaid-img {{
    max-width: 55%;         /* 다이어그램이 페이지 빈 공간에 들어가도록 */
    max-height: 42vh;
    height: auto;
    width: auto;
  }}

  /* 표지 */
  .cover {{
    height: 100vh;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%);
    color: white;
    page-break-after: always;
  }}
  .cover-inner {{ text-align: center; padding: 40pt; }}
  .cover h1 {{
    font-size: 32pt; border: none; color: white; font-weight: 700;
    margin: 0 0 14pt;
  }}
  .cover h2 {{
    font-size: 18pt; color: #dbeafe; font-weight: 400;
    margin: 0 0 30pt;
  }}
  .cover-meta {{ font-size: 13pt; color: #bfdbfe; margin: 8pt 0; }}
  .cover-foot {{ font-size: 11pt; color: #93c5fd; margin-top: 30pt; letter-spacing: 0.5pt; }}

  /* 목차 */
  .toc-page {{ page-break-after: always; padding-top: 10pt; }}
  .toc-page h1 {{ font-size: 22pt; margin-bottom: 24pt; }}
  .toc-list {{
    list-style: none; padding: 0;
    counter-reset: toc;
  }}
  .toc-list li {{
    counter-increment: toc;
    padding: 10pt 12pt;
    margin: 4pt 0;
    border-bottom: 0.5pt dashed #cbd5e1;
    font-size: 12pt;
  }}
  .toc-list li::before {{
    content: counter(toc, decimal-leading-zero) ". ";
    color: #1e40af; font-weight: 600; margin-right: 6pt;
  }}
  .toc-title {{ font-weight: 500; }}
  .toc-note {{
    margin-top: 24pt; padding: 10pt; background: #fef3c7;
    border-left: 3pt solid #f59e0b; font-size: 10pt;
  }}

  /* 챕터 */
  .chapter {{
    page-break-before: always;
  }}
  .chapter:first-of-type {{ page-break-before: auto; }}

  /* Just-the-Docs 잔재 클래스 정리 */
  .anchor-heading, .copy-button {{ display: none !important; }}
  .highlight {{ background: transparent !important; }}
  details summary {{ cursor: default; }}
  details[open] {{ }}

  /* 인쇄 시 링크 색 */
  a {{ color: #1e40af; text-decoration: none; }}
</style>
</head>
<body>
{cover}
{toc}
{''.join(chapter_htmls)}
</body>
</html>
"""

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[ok] merged HTML → {OUT_HTML}")
    print(f"     size: {OUT_HTML.stat().st_size / 1024:.1f} KB")

    # Chrome 헤드리스 → PDF (file:// 직접 — Mermaid 의존 제거됨)
    handout_url = "file://" + str(OUT_HTML)
    cmd = [
        CHROME,
        "--headless=new",
        "--no-pdf-header-footer",
        "--no-sandbox",
        f"--print-to-pdf={OUT_PDF}",
        "--virtual-time-budget=10000",
        "--disable-gpu",
        "--allow-file-access-from-files",
        handout_url,
    ]
    print(f"[run] chrome --headless --print-to-pdf  {OUT_HTML.name}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDERR:", res.stderr[-2000:])
        sys.exit(f"chrome exited with {res.returncode}")
    print(f"[ok] PDF → {OUT_PDF}")
    print(f"     size: {OUT_PDF.stat().st_size / 1024 / 1024:.2f} MB")

    # DOCX 생성은 사용자 요청에 따라 비활성. 재활성하려면 아래 주석 해제.
    # cmd = ["pandoc", str(OUT_HTML), "-f", "html", "-t", "docx", "-o", str(OUT_DOCX), "--standalone"]
    # subprocess.run(cmd, check=True)


if __name__ == "__main__":
    build()
