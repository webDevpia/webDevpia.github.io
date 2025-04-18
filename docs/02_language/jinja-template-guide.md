# Jinja 템플릿 엔진 기초 가이드

## 개요

Jinja는 Python 웹 애플리케이션에서 많이 사용되는 강력한 템플릿 엔진입니다. Django의 템플릿 시스템에서 영감을 받았으며, Python과 유사한 문법을 사용합니다.

## Jinja 템플릿이란?

Jinja 템플릿은 기본적으로 **텍스트 파일**입니다. 이 템플릿은 다양한 형식(HTML, XML, CSV, LaTeX 등)을 생성할 수 있으며, 특정 확장자를 가질 필요는 없습니다(`.html`, `.xml` 등 모두 가능).

## 템플릿의 주요 구성 요소

Jinja 템플릿은 다음과 같은 요소로 구성됩니다:

1. **변수(Variables)** - 템플릿이 렌더링될 때 실제 값으로 대체됩니다.
2. **표현식(Expressions)** - 평가되어 출력으로 변환됩니다.
3. **태그(Tags)** - 템플릿의 로직을 제어합니다.

## 기본 문법

Jinja의 기본 구분 기호(delimiters)는 다음과 같습니다:

* `{% ... %}` - **문장(Statements)** - 제어 구조(for 루프, if 조건문 등)
* `{{ ... }}` - **표현식(Expressions)** - 출력으로 인쇄될 표현식
* `{# ... #}` - **주석(Comments)** - 템플릿 출력에 포함되지 않는 주석

## 기본 템플릿 예제

아래는 기본 Jinja 구성을 사용한 간단한 템플릿 예제입니다:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Webpage</title>
</head>
<body>
    <ul id="navigation">
    {% for item in navigation %}
        <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
    </ul>

    <h1>My Webpage</h1>
    {{ a_variable }}

    {# 이것은 출력되지 않는 주석입니다 #}
</body>
</html>
```

## 주요 기능 설명

### 1. 변수와 표현식

변수는 `{{ variable_name }}`와 같이 이중 중괄호 안에 표현되며, 템플릿이 렌더링될 때 해당 변수의 값으로 대체됩니다.

```html
<h1>안녕하세요, {{ user_name }}님!</h1>
```

### 2. 제어 구조

Jinja는 다양한 제어 구조를 지원합니다:

#### For 루프

```html
<ul>
{% for user in users %}
    <li>{{ user.username }}</li>
{% endfor %}
</ul>
```

#### If 조건문

```html
{% if user.is_authenticated %}
    <p>환영합니다, {{ user.username }}!</p>
{% else %}
    <p>로그인해주세요.</p>
{% endif %}
```

### 3. 필터

필터는 파이프(`|`) 기호를 사용하여 변수의 출력을 수정할 수 있습니다:

```html
{{ name|capitalize }}
{{ list|join(', ') }}
{{ text|truncate(100) }}
```

### 4. 주석

주석은 출력에 포함되지 않습니다:

```html
{# 이 주석은 HTML 출력에 포함되지 않습니다 #}
```

## 구성 변경하기

애플리케이션 개발자는 Jinja 문법 구성을 변경할 수 있습니다. 예를 들어 `{% foo %}`를 `<% foo %>`로 변경할 수 있습니다. 또한 줄 구문(Line Statements)과 줄 주석(Line Comments)을 활성화하려면 `Environment`를 생성할 때 `line_statement_prefix`와 `line_comment_prefix`를 설정하면 됩니다.

## 사용 예제

### 데이터 전달하기

Python 코드에서 템플릿에 데이터를 전달하는 기본 예제:

```python
from jinja2 import Template

template = Template('안녕하세요, {{ name }}님!')
result = template.render(name='홍길동')
# 결과: '안녕하세요, 홍길동님!'
```

### 웹 애플리케이션에서의 사용

Flask와 같은 웹 프레임워크에서는 다음과 같이 사용할 수 있습니다:

```python
@app.route('/')
def index():
    return render_template('index.html', 
                          title='홈페이지',
                          users=['홍길동', '김철수', '이영희'])
```

템플릿 파일 (index.html):

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>사용자 목록</h1>
    <ul>
    {% for user in users %}
        <li>{{ user }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

## 정리

Jinja 템플릿 엔진은:
- 텍스트 기반 템플릿을 사용합니다
- 변수, 표현식, 태그를 포함할 수 있습니다
- 다양한 제어 구조(for, if 등)를 지원합니다
- 필터를 통해 출력을 변환할 수 있습니다
- 주석을 사용할 수 있습니다
- 문법을 커스터마이징할 수 있습니다

Jinja 템플릿은 웹 개발에서 HTML을 동적으로 생성하는 데 매우 유용하며, Python 웹 프레임워크(Flask, Django 등)와 함께 자주 사용됩니다.
