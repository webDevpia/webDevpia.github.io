---
title: 6-2. Streamlit 기초
layout: default
parent: DeepLearning
nav_order: 6.5
permalink: /deeplearning/streamlit-basics
# nav_exclude: true
# search_exclude: true
---
# 6-2. Streamlit 기초 — Python만으로 웹 앱 만들기

## 학습 목표

1. Streamlit의 개념과 실행 방법을 설명할 수 있다
2. Streamlit의 실행 모델(스크립트 재실행)을 이해할 수 있다
3. 핵심 위젯(slider, button, selectbox 등)을 사용하여 인터랙티브 앱을 만들 수 있다
4. columns, sidebar를 활용하여 레이아웃을 구성할 수 있다
5. 캐싱의 필요성을 이해하고 @st.cache_data를 적용할 수 있다

<a id="toc"></a>
## 진행 순서

1. [Streamlit이란?](#part1)
2. [실행 모델 이해](#part2)
3. [핵심 위젯 5종](#part3)
4. [레이아웃](#part4)
5. [캐싱 맛보기](#part5)
6. [미니 프로젝트: BMI 계산기](#part6)
7. [통합 정리](#part7)

> **실습 안내**: 이 수업의 실습은 Jupyter 노트북이 아니라 **`.py` 파일**을 로컬에서 실행합니다. `uv`로 프로젝트 환경을 만들고, 각 실습 코드를 `.py` 파일로 저장한 뒤 터미널에서 실행합니다.

---

<a id="part1"></a>
## 1. Streamlit이란? [↑](#toc)

**학습목표**: Streamlit의 개념과 실행 방법을 설명할 수 있다

### 한 줄 요약

> **Streamlit = Python 코드만으로 웹 앱을 만드는 프레임워크**

HTML, CSS, JavaScript를 전혀 몰라도 Python만 알면 브라우저에서 동작하는 인터랙티브 웹 앱을 만들 수 있습니다.

### 왜 Streamlit인가?

| 방법 | 필요 지식 | 코드량 | 용도 |
|------|----------|--------|------|
| HTML + Flask | Python + HTML + CSS + JS | 많음 | 범용 웹 서비스 |
| Django | Python + 템플릿 + ORM | 매우 많음 | 대규모 웹 서비스 |
| **Streamlit** | **Python만** | **최소** | **데이터/ML 앱, 프로토타입** |
| Gradio | Python만 | 최소 | ML 데모 특화 |

### 환경 설정 — uv로 프로젝트 만들기

이 수업부터는 **uv**를 사용하여 프로젝트 환경을 관리합니다.

> **uv란?** Python 패키지와 가상환경을 초고속으로 관리하는 도구입니다. pip보다 10~100배 빠르고, 프로젝트별로 환경을 자동 격리합니다. Python이 설치되어 있지 않아도 uv가 알아서 설치해 줍니다.

#### Step 1: uv 설치 (최초 1회)

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치 확인:
```bash
uv --version
```

```
# 보안 오류 발생 시: 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope currentuser 
# 입력 후 실행
```

> 설치가 안 되면 대안: `winget install astral-sh.uv` (Windows) 또는 `brew install uv` (Mac)

#### Step 2: 프로젝트 생성

```bash
uv init streamlit-basics
cd streamlit-basics
uv sync
```

이 명령으로 다음이 자동 생성됩니다:
- `.venv/` — 가상환경 (프로젝트별 독립 공간)
- `pyproject.toml` — 프로젝트 설정 파일

> **가상환경이란?** 프로젝트마다 별도의 Python 패키지 공간을 만드는 것입니다. A 프로젝트에서 설치한 패키지가 B 프로젝트에 영향을 주지 않습니다. uv는 이것을 **자동으로** 해줍니다.

#### Step 3: Streamlit 설치

```bash
uv add streamlit
```

> pip이면 ~20초 걸리는 설치가 uv는 **~2초**면 끝납니다.

### Hello World

아래 코드를 `hello.py`로 저장합니다.

```python
# hello.py
import streamlit as st

st.title("안녕하세요!")
st.write("Streamlit으로 만든 첫 번째 웹 앱입니다.")
```

터미널에서 실행합니다.

```bash
uv run streamlit run hello.py
# 또는
streamlit run hello.py
```

> `uv run` = "이 프로젝트 환경에서 실행하라"는 의미입니다. 뒤의 `streamlit run`은 Streamlit 실행 명령입니다.

브라우저가 자동으로 열리고 `http://localhost:8501`에서 앱이 실행됩니다.

> **3줄의 Python 코드만으로 웹 페이지가 만들어졌습니다!**

### uv 명령어 정리

| 명령어 | 역할 |
|--------|------|
| `uv init 프로젝트명` | 프로젝트 폴더 + 가상환경 + 설정 파일 생성 |
| `uv add 패키지명` | 패키지 설치 (가상환경에 자동 격리) |
| `uv run 명령어` | 프로젝트 환경에서 명령어 실행 |
| `uv remove 패키지명` | 패키지 제거 |
| `uv pip freeze > requirements.txt` | 파일 생성 |
| `uv add -r requirements.txt` | 패키지 설치 |


> **Colab 실습과의 차이**: DeepLearning 수업에서는 Colab(클라우드)에서 실습했습니다. Streamlit은 **로컬 PC**에서 실행해야 하므로, uv로 로컬 환경을 직접 만듭니다.

### st.write() — 만능 출력 함수

`st.write()`는 텍스트, 숫자, 데이터프레임, 차트 등 거의 모든 것을 출력합니다.

```python
import streamlit as st
import pandas as pd

st.write("## 텍스트도 되고")
st.write(1 + 2 + 3)  # 숫자도 되고
st.write(pd.DataFrame({  # 데이터프레임도 되고
    "이름": ["철수", "영희", "민수"],
    "점수": [85, 92, 78]
}))
```

**핵심**: Streamlit은 Python 코드만으로 웹 앱을 만든다. `uv add streamlit` → 코드 작성 → `streamlit run app.py`가 전부다.

> **확인**: `st.title()`과 `st.write("# 제목")`의 결과가 같아 보입니다. 차이가 있을까요? 직접 실행해서 비교해 보세요.

---

<a id="part2"></a>
## 2. 실행 모델 이해 [↑](#toc)

**학습목표**: Streamlit의 실행 모델(스크립트 재실행)을 이해할 수 있다

### Streamlit의 핵심 규칙

> **사용자가 위젯을 조작할 때마다 Python 스크립트가 위에서 아래로 전체 재실행된다.**

이것은 Jupyter 노트북과 **완전히 다른** 실행 방식입니다.

```
Jupyter 노트북:           Streamlit:
┌─────────────┐          ┌─────────────┐
│ 셀 1 실행    │          │ 전체 스크립트  │
├─────────────┤          │ 위→아래      │
│ 셀 2 실행    │  ←→     │ 한 번에 실행   │
├─────────────┤          │              │
│ 셀 3 실행    │          │ 위젯 변경 시   │
└─────────────┘          │ 처음부터 재실행 │
  개별 실행                └─────────────┘
                           전체 재실행
```

### 직접 체험하기

아래 코드를 `rerun_demo.py`로 저장하고 실행해 보세요.

```python
# rerun_demo.py
import streamlit as st
import datetime

st.title("재실행 모델 체험")

# 이 줄은 스크립트가 실행될 때마다 현재 시각을 표시합니다
st.write(f"스크립트 실행 시각: {datetime.datetime.now().strftime('%H:%M:%S')}")

# 슬라이더를 움직여 보세요 → 시각이 바뀝니다!
value = st.slider("숫자를 선택하세요", 0, 100, 50)
st.write(f"선택한 값: {value}")

st.info("👆 슬라이더를 움직일 때마다 '실행 시각'이 바뀌는 것을 관찰하세요. 스크립트 전체가 다시 실행되기 때문입니다!")
```

### 왜 이렇게 설계했을까?

- **장점**: 상태 관리가 단순. Python 스크립트처럼 위에서 아래로 읽으면 됨
- **장점**: 위젯 값이 바뀌면 그에 의존하는 모든 계산이 자동으로 갱신
- **주의**: 매번 재실행되므로 **무거운 연산**은 캐싱이 필요 → §5에서 학습

### Jupyter vs Streamlit 비교

| 항목 | Jupyter 노트북 | Streamlit |
|------|---------------|-----------|
| 실행 단위 | 셀 단위 | 스크립트 전체 |
| 실행 시점 | 사용자가 셀 실행 | 위젯 조작 시 자동 |
| 출력 위치 | 셀 아래 | 브라우저 전체 |
| 상태 보존 | 셀 실행 순서에 의존 | 매번 초기화 (session_state 제외) |
| 공유 | .ipynb 파일 | URL 링크 |

**핵심**: Streamlit은 위젯이 변경될 때마다 스크립트 전체를 재실행한다. 이것이 Streamlit의 가장 중요한 특성이며, 캐싱이 필요한 이유다.

> **확인**: `rerun_demo.py`에서 슬라이더를 움직일 때마다 실행 시각이 변하는 것을 확인했나요? 브라우저를 새로고침(F5)하면 어떻게 되나요?

---

<a id="part3"></a>
## 3. 핵심 위젯 5종 [↑](#toc)

**학습목표**: 핵심 위젯(slider, button, selectbox 등)을 사용하여 인터랙티브 앱을 만들 수 있다

Streamlit 위젯은 **함수 호출 = 화면 표시 + 값 반환**이 동시에 일어납니다.

```python
# 위젯을 화면에 표시하고, 사용자가 선택한 값을 변수에 저장
name = st.text_input("이름을 입력하세요")
# name에는 사용자가 입력한 문자열이 들어감
```

### 위젯 1: st.text_input — 텍스트 입력

```python
name = st.text_input("이름을 입력하세요", value="홍길동")
st.write(f"안녕하세요, {name}님!")
```

### 위젯 2: st.slider — 슬라이더

```python
age = st.slider("나이를 선택하세요", min_value=1, max_value=100, value=25)
st.write(f"선택한 나이: {age}세")
```

### 위젯 3: st.selectbox — 드롭다운 선택

```python
color = st.selectbox("좋아하는 색은?", ["빨강", "파랑", "초록", "노랑"])
st.write(f"선택한 색: {color}")
```

### 위젯 4: st.button — 버튼

```python
if st.button("인사하기"):
    st.balloons()  # 풍선 애니메이션!
    st.write("버튼을 눌렀습니다!")
```

> **주의**: 버튼은 클릭 시 `True`를 반환하지만, 재실행 후에는 다시 `False`가 됩니다. 버튼 클릭 결과를 유지하려면 `st.session_state`가 필요합니다 (심화 내용).

### 위젯 5: st.file_uploader — 파일 업로드

```python
uploaded = st.file_uploader("이미지를 선택하세요", type=["png", "jpg", "jpeg"])
if uploaded is not None:
    st.image(uploaded, caption="업로드한 이미지", width=300)
```

> 이 위젯은 [6-3. 웹서비스 배포](/deeplearning/streamlit-mnist-deploy)에서 모델 추론 앱에 바로 사용됩니다.

### 한 파일에 모아보기

아래 코드를 `widgets.py`로 저장하고 실행하면 모든 위젯을 한 번에 체험할 수 있습니다.

```python
# widgets.py
import streamlit as st

st.title("위젯 놀이터")

# 텍스트 입력
name = st.text_input("이름", value="학생")

# 슬라이더
score = st.slider("점수", 0, 100, 75)

# 드롭다운
grade = st.selectbox("학년", ["1학년", "2학년", "3학년", "4학년"])

# 결과 표시
st.divider()
st.write(f"**{name}**님은 {grade}이고, 점수는 **{score}점**입니다.")

if score >= 90:
    st.success("우수합니다!")
elif score >= 70:
    st.info("양호합니다.")
else:
    st.warning("더 노력이 필요합니다.")

# 버튼
if st.button("축하 버튼"):
    st.balloons()
```

### 위젯 정리

| 위젯 | 반환값 | 용도 |
|------|--------|------|
| `st.text_input()` | 문자열 | 이름, 검색어 등 텍스트 입력 |
| `st.slider()` | 숫자 | 범위 값 선택 |
| `st.selectbox()` | 선택 항목 | 목록에서 하나 선택 |
| `st.button()` | True/False | 동작 트리거 |
| `st.file_uploader()` | 파일 객체 또는 None | 이미지/데이터 파일 업로드 |

**핵심**: 위젯은 화면에 UI를 표시하면서 동시에 사용자 입력값을 변수로 반환한다. 위젯 값이 바뀌면 스크립트가 재실행되어 결과가 자동 갱신된다.

> **확인**: `widgets.py`에서 점수 슬라이더를 90 이상으로 올리면 메시지가 어떻게 바뀌나요? 왜 그렇게 되나요?

---

<a id="part4"></a>
## 4. 레이아웃 [↑](#toc)

**학습목표**: columns, sidebar를 활용하여 레이아웃을 구성할 수 있다

### st.columns — 나란히 배치

```python
import streamlit as st

col1, col2 = st.columns(2)  # 2개의 동일 너비 컬럼

with col1:
    st.header("왼쪽")
    st.write("여기는 왼쪽 컬럼입니다.")

with col2:
    st.header("오른쪽")
    st.write("여기는 오른쪽 컬럼입니다.")
```

비율을 조정할 수도 있습니다.

```python
col1, col2 = st.columns([2, 1])  # 왼쪽이 2배 넓음
```

### st.sidebar — 사이드바

```python
import streamlit as st

# 사이드바에 위젯 배치
st.sidebar.title("설정")
name = st.sidebar.text_input("이름")
theme = st.sidebar.selectbox("테마", ["밝음", "어두움"])

# 메인 영역
st.title(f"안녕하세요, {name}님!")
st.write(f"선택한 테마: {theme}")
```

### st.tabs — 탭

```python
import streamlit as st

tab1, tab2, tab3 = st.tabs(["데이터", "차트", "설명"])

with tab1:
    st.write("데이터를 보여주는 탭")

with tab2:
    st.write("차트를 보여주는 탭")

with tab3:
    st.write("설명을 보여주는 탭")
```

### 출력 위젯 정리

화면에 정보를 표시하는 위젯들도 알아둡시다.

| 위젯 | 용도 | 예시 |
|------|------|------|
| `st.write()` | 범용 출력 | `st.write("텍스트", df, 숫자)` |
| `st.title()` | 제목 | `st.title("앱 제목")` |
| `st.header()` | 중제목 | `st.header("섹션")` |
| `st.subheader()` | 소제목 | `st.subheader("하위 섹션")` |
| `st.image()` | 이미지 | `st.image("photo.jpg", width=300)` |
| `st.success()` | 성공 메시지 (초록) | `st.success("완료!")` |
| `st.info()` | 정보 메시지 (파랑) | `st.info("참고사항")` |
| `st.warning()` | 경고 메시지 (노랑) | `st.warning("주의!")` |
| `st.error()` | 에러 메시지 (빨강) | `st.error("오류 발생")` |
| `st.divider()` | 구분선 | `st.divider()` |
| `st.bar_chart()` | 막대 차트 | `st.bar_chart(data)` |
| `st.line_chart()` | 꺾은선 차트 | `st.line_chart(data)` |

**핵심**: `st.columns()`로 나란히, `st.sidebar`로 사이드에, `st.tabs()`로 탭으로 구분하여 레이아웃을 구성할 수 있다.

---

<a id="part5"></a>
## 5. 캐싱 맛보기 [↑](#toc)

**학습목표**: 캐싱의 필요성을 이해하고 @st.cache_data를 적용할 수 있다

### 문제 상황

§2에서 배웠듯이 Streamlit은 **위젯이 변경될 때마다 스크립트 전체를 재실행**합니다. 그런데 스크립트에 시간이 오래 걸리는 작업이 있다면?

```python
# cache_problem.py — 캐싱 없음
import streamlit as st
import time

def load_data():
    """3초 걸리는 데이터 로드를 시뮬레이션"""
    time.sleep(3)
    return {"data": [1, 2, 3, 4, 5]}

st.title("캐싱 없는 앱")
data = load_data()  # 슬라이더를 움직일 때마다 3초 대기!
value = st.slider("값 선택", 1, 10, 5)
st.write(f"선택: {value}, 데이터: {data}")
```

슬라이더를 움직일 때마다 **3초씩 기다려야** 합니다. 데이터는 바뀌지 않았는데 말이죠.

### 해결: @st.cache_data

`@st.cache_data`를 붙이면 함수의 결과를 **메모리에 저장(캐시)**합니다. 같은 입력으로 다시 호출하면 함수를 실행하지 않고 저장된 결과를 바로 반환합니다.

```python
# cache_solution.py — 캐싱 적용
import streamlit as st
import time

@st.cache_data   # ← 이 한 줄만 추가!
def load_data():
    """3초 걸리는 데이터 로드를 시뮬레이션"""
    time.sleep(3)
    return {"data": [1, 2, 3, 4, 5]}

st.title("캐싱 있는 앱")
data = load_data()  # 첫 실행만 3초, 이후는 즉시!
value = st.slider("값 선택", 1, 10, 5)
st.write(f"선택: {value}, 데이터: {data}")
```

### 캐싱 2종류

| 데코레이터 | 용도 | 예시 |
|-----------|------|------|
| `@st.cache_data` | **데이터** 캐싱 (복사본 반환) | CSV 로드, API 호출, 계산 결과 |
| `@st.cache_resource` | **리소스** 캐싱 (원본 참조 반환) | ML 모델 로드, DB 연결 |

[6-3. 웹서비스 배포](/deeplearning/streamlit-mnist-deploy)에서 학습된 모델을 로드할 때 `@st.cache_resource`를 사용합니다.

```python
# 웹서비스 배포에서 사용할 CNN 모델 로드 예시
@st.cache_resource
def load_model():
    model = CNN()
    model.load_state_dict(torch.load("mnist_cnn.pt", map_location="cpu"))
    model.eval()
    return model
```

> `@st.cache_resource`를 쓰지 않으면 이미지를 업로드할 때마다 모델을 처음부터 다시 로드합니다!

**핵심**: Streamlit은 매번 스크립트를 재실행하므로, 무거운 연산에는 `@st.cache_data`(데이터)나 `@st.cache_resource`(모델, 연결)를 붙여 캐싱해야 한다.

> **확인**: `cache_problem.py`와 `cache_solution.py`를 각각 실행하고 슬라이더를 움직여 보세요. 체감 속도 차이가 느껴지나요?

---

<a id="part6"></a>
## 6. 미니 프로젝트: BMI 계산기 [↑](#toc)

지금까지 배운 모든 요소를 조합하여 BMI 계산기를 만들어 봅시다.

### 완성 앱

```python
# bmi_app.py
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="BMI 계산기", page_icon="⚖️")

# 사이드바 — 입력
st.sidebar.title("신체 정보 입력")
name = st.sidebar.text_input("이름", value="사용자")
height = st.sidebar.slider("키 (cm)", 100, 220, 170)
weight = st.sidebar.slider("몸무게 (kg)", 30, 200, 70)

# 메인 — 결과
st.title("⚖️ BMI 계산기")
st.write(f"**{name}**님의 BMI를 계산합니다.")

# BMI 계산
height_m = height / 100
bmi = weight / (height_m ** 2)

# 2단 컬럼 레이아웃
col1, col2 = st.columns(2)

with col1:
    st.metric("키", f"{height} cm")
    st.metric("몸무게", f"{weight} kg")

with col2:
    st.metric("BMI", f"{bmi:.1f}")

    # BMI 판정
    if bmi < 18.5:
        st.info("저체중")
    elif bmi < 23:
        st.success("정상")
    elif bmi < 25:
        st.warning("과체중")
    else:
        st.error("비만")

# 구분선 + BMI 기준표
st.divider()
st.subheader("BMI 판정 기준")
st.write("""
| 범위 | 판정 |
|------|------|
| 18.5 미만 | 저체중 |
| 18.5 ~ 22.9 | 정상 |
| 23 ~ 24.9 | 과체중 |
| 25 이상 | 비만 |
""")
```

### 사용된 Streamlit 요소 정리

```
st.set_page_config()   ← 페이지 제목, 아이콘 설정
st.sidebar             ← 사이드바 레이아웃
st.text_input()        ← 텍스트 위젯
st.slider()            ← 슬라이더 위젯
st.columns()           ← 2단 컬럼 레이아웃
st.metric()            ← 숫자 강조 표시
st.success/info/...()  ← 상태 메시지
st.divider()           ← 구분선
st.write()             ← 마크다운 테이블 출력
```

### 도전 과제

BMI 계산기를 확장해 보세요.

1. `st.radio()`로 성별 선택을 추가하고, 성별에 따라 다른 판정 기준 적용
2. `st.number_input()`으로 키와 몸무게를 더 정밀하게 입력
3. `st.bar_chart()`로 BMI 범위별 막대 차트 추가
4. 여러 사람의 BMI를 비교하는 기능 추가 (힌트: `st.session_state` 활용)

---

<a id="part7"></a>
## 7. 통합 정리 [↑](#toc)

### 이 수업에서 배운 것

| 개념 | 핵심 내용 |
|------|----------|
| **Streamlit이란** | Python만으로 웹 앱을 만드는 프레임워크 |
| **실행 모델** | 위젯 변경 → 스크립트 전체 재실행 |
| **입력 위젯** | text_input, slider, selectbox, button, file_uploader |
| **출력 위젯** | write, title, image, success/info/warning/error |
| **레이아웃** | columns, sidebar, tabs |
| **캐싱** | @st.cache_data (데이터), @st.cache_resource (모델) |

### 다음 시간 연결

다음 시간([6-3. 웹서비스 배포](/deeplearning/streamlit-mnist-deploy))에서 이 지식을 활용하여 CNN 수업에서 만든 MNIST 모델을 **숫자 인식 웹 앱**으로 만들고 배포합니다.

```python
# 6-3에서 만들 앱의 구조 미리보기
import streamlit as st

st.title("MNIST 숫자 인식")           # ← 오늘 배운 st.title

uploaded = st.file_uploader(...)     # ← 오늘 배운 파일 업로드

col1, col2 = st.columns(2)          # ← 오늘 배운 레이아웃
with col1:
    st.image(uploaded)               # ← 오늘 배운 이미지 표시

model = load_model()                 # ← 오늘 배운 @st.cache_resource

st.success(f"결과: {prediction}")    # ← 오늘 배운 상태 메시지
st.bar_chart(probabilities)          # ← 오늘 배운 차트
```

### 복습 질문

1. Streamlit에서 위젯 값이 바뀌면 무슨 일이 일어나는가?
2. `@st.cache_data`를 사용하지 않으면 어떤 문제가 발생하는가?
3. `st.columns(2)`와 `st.columns([3, 1])`의 차이는 무엇인가?
4. `st.sidebar`에 위젯을 배치하는 이유는 무엇인가?
5. `@st.cache_data`와 `@st.cache_resource`는 각각 언제 사용하는가?

### 심화 과제

- BMI 계산기에 `st.tabs()`를 추가하여 "계산" 탭과 "설명" 탭으로 분리해 보기
- `st.line_chart()`를 사용하여 키/몸무게에 따른 BMI 변화 그래프 추가하기
- `st.session_state`를 활용하여 계산 히스토리를 저장하는 기능 만들어 보기
- Streamlit을 이용한 간단한 할 일 목록(To-Do) 앱 만들어 보기

### 참고 자료

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Streamlit 기본 개념](https://docs.streamlit.io/get-started/fundamentals/main-concepts)
- [Streamlit API 레퍼런스](https://docs.streamlit.io/develop/api-reference)
- [Streamlit 갤러리 (다른 사람들이 만든 앱)](https://streamlit.io/gallery)
- [Streamlit 치트 시트](https://docs.streamlit.io/develop/quick-references/api-cheat-sheet)
