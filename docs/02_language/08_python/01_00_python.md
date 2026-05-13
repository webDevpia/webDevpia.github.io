---
title: Python (8시간 재수강)
layout: default
parent: Language
nav_order: 8
has_children: true
permalink: /language/python
---

{% raw %}

# Python 문법 8시간 총정리

> "이전에 한 번 들었지만 막상 코드를 보면 막막한" 분을 위한 재수강 코스입니다.

---

## 이 강의가 다른 점

| | 일반 입문 강의 | 이 강의 |
|---|---|---|
| 대상 | Python을 처음 배우는 사람 | 한 번 들었지만 **실전이 안 되는** 사람 |
| 목표 | "코드를 따라 칠 수 있다" | "코드를 **읽고 고칠 수 있다**" |
| 시간 분배 | 강의 70 : 실습 30 | **강의 40 : 실습 60** |
| 강조점 | 새 개념 추가 | **흔한 실수 → 올바른 코드** 비교 |

> 💡 **중요한 메시지**: 처음 들었을 때 막막했던 건 정상입니다. 문법은 **두 번째 들어야 잡힙니다**. 자책하지 마세요.

---

## 학습 목표

이 코스를 마치면 다음을 할 수 있습니다.

- **read** — 다른 사람이 쓴 Python 코드를 읽고 흐름을 설명할 수 있다
- **fix** — 흔한 오류 메시지(IndexError, KeyError, TypeError)를 보고 원인을 찾을 수 있다
- **write** — 50줄 이내의 작은 프로그램을 처음부터 작성할 수 있다
- **search** — 모르는 함수/메서드를 검색해서 적용할 수 있다 (외울 필요 없음)

---

## 커리큘럼 (8시간 × 1단위 1시간)

| 단위 | 시간 | 챕터 | 핵심 |
|---|---|---|---|
| 0 | 10분 | 오리엔테이션 + **자가진단 10문항** | 본인 수준 확인 |
| 1 | 1h | [02. 변수·타입·연산자](/language/python/02-vars) | 동적 타이핑, `==` vs `is` |
| 2 | 1h | [03. 문자열](/language/python/03-string) | 슬라이싱, f-string, 메서드 |
| 3 | 1h | [04. 리스트·튜플 ★](/language/python/04-list-tuple) | mutable/immutable, 얕은 복사 |
| 4 | 1h | [05. 딕셔너리·세트 ★](/language/python/05-dict-set) | key-value 패턴, 중복 제거 |
| 5 | 1h | [06. 조건문·반복문](/language/python/06-control) | range/enumerate/zip |
| 6 | 1h | [07. 함수 ★](/language/python/07-function) | return, *args/**kwargs, 스코프 |
| 7 | 1h | [08. 컴프리헨션·입출력·예외](/language/python/08-misc) | `[x for ...]`, `with open`, `try/except` |
| 8 | 50분 | [09. 모듈·클래스·미니프로젝트 ★](/language/python/09-oop) | import, class, 통합 실습 |

★ = 상세 챕터 (학생이 가장 많이 막히는 부분)

---

## 단위 0 — 자가진단 10문항

> 본격 강의 전에 본인 수준을 확인하세요. **틀려도 됩니다**. 강사가 어느 챕터에 시간을 더 쓸지 정하는 자료입니다.

각 문항은 **결과를 예측 → 직접 실행** 순서로 진행하세요. 정답은 마지막에 있습니다.

### Q1 — 변수와 타입

```python
a = "5"
b = 3
print(a + b)
```
> 예상 결과는?  ① `8`  ② `"53"`  ③ 에러  ④ `"5" + 3`

### Q2 — `==` vs `is`

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)
print(a is b)
```
> 두 줄의 출력은 같을까 다를까? **왜?**

### Q3 — 문자열 슬라이싱

```python
s = "Hello, World!"
print(s[7:12])
print(s[-6:-1])
```
> 두 출력의 차이는?

### Q4 — 리스트 mutability

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```
> `a`는 어떻게 출력될까?  ① `[1, 2, 3]`  ② `[1, 2, 3, 4]`  ③ 에러

### Q5 — 딕셔너리 KeyError

```python
d = {"name": "Alice", "age": 30}
print(d["city"])
```
> 실행하면 무슨 일이 일어날까? **에러 메시지의 첫 단어**는?

### Q6 — for + range

```python
for i in range(2, 10, 2):
    print(i, end=" ")
```
> 출력은? (한 줄로)

### Q7 — 함수 return

```python
def add(a, b):
    print(a + b)

result = add(3, 4)
print(result)
```
> `result`에는 무엇이 들어 있을까?

### Q8 — 가변 기본값 함정

```python
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("apple"))
print(add_item("banana"))
```
> 두 번째 출력은?  ① `["banana"]`  ② `["apple", "banana"]`  ③ 에러

### Q9 — 리스트 컴프리헨션

```python
nums = [1, 2, 3, 4, 5]
result = [x * 2 for x in nums if x % 2 == 0]
print(result)
```
> 출력은?

### Q10 — try/except

```python
try:
    n = int("hello")
    print("OK")
except ValueError:
    print("값 변환 오류")
except Exception:
    print("기타 오류")
finally:
    print("종료")
```
> 출력은 모두 몇 줄? 각 줄의 내용은?

---

### 정답과 해설

<details>
<summary>👉 펼치기 (먼저 본인이 풀어본 뒤 확인)</summary>

| # | 정답 | 핵심 개념 | 챕터 |
|---|---|---|---|
| Q1 | ③ 에러 (TypeError: can only concatenate str to str) | 문자열과 숫자는 `+`로 못 더함. `int(a) + b` 또는 `a + str(b)` 로 형변환 | 02 |
| Q2 | `True` / `False`. `==`는 값 비교, `is`는 메모리 동일성 비교 | 리스트는 매번 새 객체로 만들어짐 | 02 |
| Q3 | `"World"` / `"World"`. 인덱스 `7~11`과 `-6~-2`는 같은 위치 | 음수 인덱스는 뒤에서부터 | 03 |
| Q4 | ② `[1, 2, 3, 4]`. `b = a` 는 **같은 리스트를 두 이름으로** 참조 | 별도 사본 원하면 `b = a.copy()` 또는 `b = a[:]` | 04 |
| Q5 | `KeyError`. 존재하지 않는 키 접근 | 안전한 접근: `d.get("city")` → `None` 반환 | 05 |
| Q6 | `2 4 6 8 ` (10은 제외) | `range(시작, 끝, 간격)` — 끝값 불포함 | 06 |
| Q7 | `None`. `print`는 화면 출력만, `return`이 없으면 함수는 `None` 반환 | `return a + b` 로 수정 | 07 |
| Q8 | ② `["apple", "banana"]`. 기본값 리스트는 **함수 정의 시 1회만 생성** | 함정 — 기본값은 `None`으로 두고 함수 안에서 새로 만들기 | 07 |
| Q9 | `[4, 8]`. 짝수만 골라(`if x % 2 == 0`) 2배 | 컴프리헨션 = `[변환식 for 변수 in 반복 if 조건]` | 08 |
| Q10 | 2줄: `값 변환 오류` / `종료` | `int("hello")` → ValueError. `except`가 잡으면 그 아래는 실행 안 됨, `finally`는 항상 실행 | 08 |

</details>

---

### 점수별 권장 학습 전략

| 맞춘 개수 | 상태 | 권장 |
|---|---|---|
| 9~10 | 사실 잘 알고 계심 | OOP·고급 함수(7장)에 시간 집중. 다른 챕터는 빠르게 |
| 6~8 | 평균 | 8단위 그대로 진행. 틀린 문항의 챕터에 표시 |
| 3~5 | 다시 잡아야 함 | 본 강의의 ★ 챕터(04, 05, 07, 09) 에 시간 1.5배 |
| 0~2 | 처음 듣는 것처럼 | 본 강의 + 추가 1~2시간 자율학습 권장 |

> 💡 **꿀팁**: 자가진단을 강사도 보세요. 학생 평균 점수가 5점 이하면 강의 속도를 늦추세요.

---

## 학습 방법 가이드

### 1. 코드는 반드시 직접 실행

```
읽기만 = 30% 이해
직접 타이핑 = 60% 이해
결과 예측 후 실행 = 85% 이해
누군가에게 설명 = 95% 이해
```

### 2. 실행 환경

Google Colab만으로 충분합니다 (설치 불필요).

[colab.research.google.com](https://colab.research.google.com) 접속 → **새 노트북** → 첫 셀:

```python
print("Hello, Python")
```

### 3. 에러 메시지는 친구

Python의 에러 메시지는 **거의 다 영어로 친절하게** 알려줍니다.

```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
└─ "타입 에러: +가 int랑 str을 더하는 건 지원 안 함"
```

에러 메시지를 그대로 검색하면 90%는 해결됩니다.

### 4. 검색 키워드 패턴

| 모르는 것 | 검색 |
|---|---|
| 리스트에서 최댓값 찾기 | `python list max value` |
| 딕셔너리 정렬 | `python dict sort by value` |
| 문자열에서 숫자만 추출 | `python extract numbers from string` |

영어로 검색하면 답이 훨씬 빠릅니다.

---

## 다음 단계

각 챕터는 다음 5단계로 구성됩니다:

1. **학습 목표** — 이 챕터 끝나면 뭘 할 수 있는지
2. **핵심 개념** — 1줄 정의 + 직관 비유
3. **코드와 예제** — 미니 코드 + 실행 결과
4. **흔한 실수 vs 올바른 코드** — 가장 중요한 부분
5. **자기 점검** — 5문항으로 확인

자, 시작합니다. 👉 [**02. 변수·타입·연산자**](/language/python/02-vars)

{% endraw %}
