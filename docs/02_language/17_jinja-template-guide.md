---
title: Jinja
layout: default
parent: Language
nav_order: 17
permalink: /language/jinja
has_children: false
# nav_exclude: true
# search_exclude: true
---
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

{% raw %}
* `{% ... %}` - **문장(Statements)** - 제어 구조(for 루프, if 조건문 등)
* `{{ ... }}` - **표현식(Expressions)** - 출력으로 인쇄될 표현식
* `{# ... #}` - **주석(Comments)** - 템플릿 출력에 포함되지 않는 주석
{% endraw %} 

## 기본 템플릿 예제

아래는 기본 Jinja 구성을 사용한 간단한 템플릿 예제입니다:

```html
{% raw %}
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
{% endraw %}
```

## 주요 기능 설명

### 1. 변수와 표현식
{% raw %}
변수는 `{{ variable_name }}`와 같이 이중 중괄호 안에 표현되며, 템플릿이 렌더링될 때 해당 변수의 값으로 대체됩니다.
{% endraw %}

```html
{% raw %}
<h1>안녕하세요, {{ user_name }}님!</h1>
{% endraw %}
```

### 2. 제어 구조

Jinja는 다양한 제어 구조를 지원합니다:

#### For 루프

```html
{% raw %}
<ul>
{% for user in users %}
    <li>{{ user.username }}</li>
{% endfor %}
</ul>
{% endraw %}
```

#### If 조건문

```html
{% raw %}
{% if user.is_authenticated %}
    <p>환영합니다, {{ user.username }}!</p>
{% else %}
    <p>로그인해주세요.</p>
{% endif %}
{% endraw %}
```

### 3. 필터

필터는 파이프(`|`) 기호를 사용하여 변수의 출력을 수정할 수 있습니다:

```html
{% raw %}
{{ name|capitalize }}
{{ list|join(', ') }}
{{ text|truncate(100) }}
{% endraw %}
```

### 4. 주석

주석은 출력에 포함되지 않습니다:

```html
{% raw %}
{# 이 주석은 HTML 출력에 포함되지 않습니다 #}
{% endraw %}
```
## 사용 예제

### 데이터 전달하기

Python 코드에서 템플릿에 데이터를 전달하는 기본 예제:

```python
from jinja2 import Template

template = Template('안녕하세요, {% raw %}{{ name }}{% endraw %}님!')
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
 {% raw %}<!DOCTYPE html>
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
</html>{% endraw %}
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
