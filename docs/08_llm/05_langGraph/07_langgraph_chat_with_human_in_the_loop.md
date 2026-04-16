---
title: 6. LangGraph 챗봇에 사람의 개입 통합하기
layout: default
grand_parent: LLM
parent: LangGraph
nav_order: 7
permalink: /llm/langgraph/chat_human
--- 
# LangGraph 챗봇에 사람의 개입 통합하기

본 강의에서는 LangGraph를 활용하여 챗봇 워크플로우에 인간의 개입(Human-in-the-loop)을 통합하는 방법을 단계별로 안내합니다. 이러한 통합은 복잡한 질문이나 모델의 불확실한 응답 시, 인간이 직접 개입하여 대화의 품질과 정확성을 향상시키는 데 도움이 됩니다.

## 학습 목표
- 챗봇 워크플로우에 인간 검토 노드 추가하기
- LangGraph의 `interrupt` 기능을 이용해 인간 개입 요청하기
- 인간 개입 후 워크플로우 중단 및 재개하기

### 학습 내용 요약

1. **인간 검토 노드 추가:**
   - 챗봇이 처리하기 어려운 질문을 받았을 때, 이를 인간 검토 노드로 라우팅하여 사람이 직접 응답할 수 있도록 합니다.

2. **LangGraph의 `interrupt` 기능 활용:**
   - `interrupt` 함수를 사용하여 그래프 실행을 일시 중지하고, 인간의 입력을 기다릴 수 있습니다. 이 기능을 통해 특정 지점에서 인간의 개입을 요청하고, 입력을 받은 후 실행을 재개할 수 있습니다.

3. **체크포인팅을 통한 상태 관리:**
   - 인간의 입력을 기다리는 동안 현재 상태를 저장하여, 이후 실행을 원활하게 재개할 수 있도록 합니다.

이러한 방식을 통해, 챗봇은 자동화된 응답과 인간의 개입을 효과적으로 결합하여 보다 정확하고 신뢰성 있는 서비스를 제공할 수 있습니다.

<a id="toc"></a>

## 진행 순서

1. [환경 설정](#part1)
2. [코드 설명](#part2)
3. [챗봇 실행](#part3)
4. [도구 호출 승인 게이트 (Approval Gate)](#part4)
5. [Time Travel: 과거 상태로 되돌리기](#part5)

<a id="part1"></a>

## 1. 환경 설정 [↑](#toc)


### 환경변수 설정
환경변수 파일 `.env`를 생성하여 다음의 내용을 설정합니다.
```bash
OPENAI_API_KEY=본인의_OpenAI_API키
OPENAI_MODEL=gpt-4o-mini
TAVILY_API_KEY=본인의_tavily_api_key
```
환경변수를 로드하기 위해 Python의 `python-dotenv` 라이브러리를 사용합니다.

<a id="part2"></a>

## 2. 코드 설명 [↑](#toc)
### 라이브러리 임포트

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated, List
from dotenv import load_dotenv
import os
```

### 환경변수 로딩

```python
load_dotenv()

openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
```

### 도구 정의

Tavily 검색 도구를 설정합니다.

```python
from langchain_tavily import TavilySearch

search_tool = TavilySearch(max_results=2)
search_tool.invoke("LangGraph가 무엇인가요?")
```

Human-in-the-loop 도구를 설정합니다.
- LangGraph에서 Human-in-the-loop 기능을 구현할 때 LLM의 요청에 따라 사람이 직접 개입하여 응답을 제공할 수 있도록 하는 **도구(tool)**를 정의합니다.

- 이 도구는 사용자가 입력한 질문에 대해 LLM이 직접 응답할 수 없는 경우, 사람에게 질문을 전달하고 답변을 받을 수 있도록 합니다.

```python
from langchain_core.tools import tool
from langgraph.types import interrupt

@tool
def human_assist(query):
    """Human assist tool"""
    human_response = interrupt({"query": query})
    return human_response["data"]
```

① `@tool` 데코레이터

```python
@tool
```

- LangChain의 도구(tool)로 해당 함수를 자동 등록합니다.
- LLM이 해당 도구를 호출할 수 있도록 합니다.
- 데코레이터를 통해 명시적 `name` 및 `description`을 제공하지 않으면, 함수 이름(`human_assist`)과 Docstring(`"Human assist tool"`)이 자동으로 사용됩니다.


② 함수 정의 (`human_assist`)

```python
def human_assist(query):
```

- 함수 이름: `human_assist`
- 입력 인자:
  - `query` (필수): 사용자가 입력한 질문 또는 LLM이 추가 정보가 필요하다고 판단한 내용을 전달합니다.


③ 함수의 Docstring (설명 문자열)

```python
"""Human assist tool"""
```

- 함수가 수행하는 역할을 간략하게 설명합니다.
- LLM이 이 도구의 기능을 쉽게 이해할 수 있도록 도와줍니다.


④ `interrupt` 함수 호출

```python
human_response = interrupt({"query": query})
```

- **`interrupt` 함수의 역할**:
  - LangGraph에서 워크플로우의 실행을 **일시적으로 중단**하고, 외부(인간)의 입력을 기다리는 데 사용됩니다.
  - 이 함수를 호출하면 LangGraph는 즉시 실행을 중단하고, 호출된 곳에서 지정한 데이터를 외부로 전달하여 인간의 개입을 요청합니다.
  - 외부에서 제공한 입력이 도착할 때까지 상태를 저장하고 대기합니다.

- **입력 형태**:
  ```json
  {
      "query": "LLM이 물어본 질문 또는 요청 내용"
  }
  ```
  이 형태로 인간에게 전달됩니다.


⑤ 인간 입력의 반환 및 처리

```python
return human_response["data"]
```

- 인간이 제공한 입력(응답)을 받으면, LangGraph는 해당 응답을 `interrupt` 호출의 반환값으로 전달합니다.
- `human_response`는 다음과 같은 구조를 가집니다:
  ```json
  {
      "data": "인간이 입력한 실제 응답 내용"
  }
  ```
- 따라서 이 코드는 인간이 제공한 실제 데이터를 반환하여 LLM의 최종 응답에 사용할 수 있도록 합니다.

### 상태(State) 정의

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
```

### LLM 모델 설정 및 도구 바인딩

```python
llm = ChatOpenAI(model=openai_model)
tools = [search_tool, human_assist]
llm_with_tools = llm.bind_tools(tools)
```

> 💡 **Ollama 사용 시:** `from langchain_ollama import ChatOllama` 후 `llm = ChatOllama(model="gemma3:1b")`로 교체할 수 있습니다.

① 도구 목록 준비 (`tools`)

```python
tools = [search_tool, human_assist]
```

- LLM이 활용할 수 있는 도구들을 **리스트 형태로 정의**합니다.
- 이 리스트는 이전에 정의된 함수나 클래스 기반 도구를 포함할 수 있습니다.
- **`search_tool`**: 웹 검색 등의 자동화 도구
- **`human_assist`**: 챗봇이 답하기 어려울 때, 인간의 판단을 요청하는 도구

도구는 보통 `@tool` 데코레이터로 정의하거나 클래스 형태로 정의할 수 있습니다.

### 챗봇 노드 정의

챗봇이 도구를 이용하여 사용자 메시지에 응답하도록 설정합니다.

```python
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}
```

- `chatbot(state: State)`: 챗봇 노드 함수로, 상태에서 받은 메시지를 기반으로 도구를 활용하여 응답을 생성하고 상태를 업데이트합니다.

### 체크포인터 설정
체크포인팅을 위한 메모리 체크포인터를 생성합니다.

```python
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()
```

- `InMemorySaver`: 메모리 기반의 체크포인터로, 각 대화의 상태를 메모리에 임시로 저장하고 관리합니다. 이를 통해 챗봇은 이전 대화 내용을 기억하고 다음 번 상호작용 시에도 맥락을 유지한 상태로 대화를 진행할 수 있습니다. 실제 운영 환경에서는 더 영구적인 상태 관리를 위해 데이터베이스 기반 체크포인터(예: SqliteSaver 또는 PostgresSaver)를 사용하는 것이 권장됩니다.

### 그래프 구성 및 컴파일
LangGraph의 ToolNode와 tools_condition을 사용하여 조건부로 도구 노드를 호출합니다.

```python
from langgraph.prebuilt import ToolNode, tools_condition

tool_node = ToolNode(tools)

workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")

graph = workflow.compile(checkpointer=memory)
```

> `ToolNode`와 `tools_condition`의 작동 원리는 [4단원 도구 사용](/llm/langgraph/chat_tool)에서 학습한 것과 동일합니다.

### 그래프 시각화
컴파일된 그래프를 이용해 시각화해봅니다.

```python
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))
```

```mermaid
graph TD
    __start__([__start__]) --> chatbot[chatbot]
    chatbot -.->|도구 호출| tools[tools]
    chatbot -.->|응답 완료| __end__([__end__])
    tools --> chatbot
```

<a id="part3"></a>

## 3. 챗봇 실행 [↑](#toc)
동일한 thread_id를 사용하여 이전 대화 맥락을 유지하는 예시입니다. 이 예시에서는 두 개의 서로 다른 thread_id를 사용하여 두 개의 독립된 대화를 관리하는 방법을 보여줍니다.

```python
config = {"configurable": {"thread_id": "user123"}}
```

`config`는 LangGraph의 그래프 실행 시 설정을 정의하는 딕셔너리입니다.
여기서 `configurable` 키는 실행 시 동적으로 설정할 수 있는 옵션을 포함합니다.

- `thread_id`: 대화의 고유 식별자 역할을 합니다.
- LangGraph는 상태 기반 그래프(StateGraph)를 사용하여 대화를 관리합니다.
- `thread_id`는 각 대화의 상태를 구분하는 데 사용됩니다.
- 동일한 `thread_id`를 사용하면 이전 대화의 맥락을 유지하며 대화를 이어갈 수 있습니다.
- 서로 다른 `thread_id`를 사용하면 독립된 대화를 관리할 수 있습니다.

예를 들어:
- `thread_id`가 "user123"인 경우, 해당 대화의 상태를 기반으로 응답을 생성합니다.
- 새로운 `thread_id`를 지정하면 이전 대화와는 별개의 새로운 대화가 시작됩니다.

이 설정은 LangGraph의 체크포인팅(checkpointing) 기능과 결합하여 다중 턴 대화에서 맥락을 유지하거나 독립적인 대화를 관리하는 데 유용합니다.

```python
from pprint import pprint
snapshot = graph.get_state(config)
if 'messages' in snapshot.values:
	pprint(snapshot.values['messages'])
else:
	print("No messages found in the snapshot.")
print(snapshot.next)
```

```python
user_input1 = "AI 에이전트 개발을 위한 LangGraph의 특징에 대해 설명해주세요."
state1 = {"messages": [HumanMessage(content=user_input1)]}
response1 = graph.invoke(state1, config)

print(response1["messages"][-1].content)
```

**실행 결과 (예시):**
```
LangGraph는 AI 에이전트 개발을 위한 프레임워크로, 다음과 같은 특징이 있습니다:
1. 상태 기반 그래프 구조로 복잡한 워크플로우 관리...
```

```python
snapshot = graph.get_state(config)
if 'messages' in snapshot.values:
	pprint(snapshot.values['messages'])
else:
	print("No messages found in the snapshot.")
print(snapshot.next)
```

```python
user_input2 = "AI 에이전트 개발을 위한 기술 선택에 대한 전문가의 지원이 필요해요. 지원 요청을 해도 될까요?"
state2 = {"messages": [HumanMessage(content=user_input2)]}
response2 = graph.invoke(state2, config)

print(response2["messages"][-1].content)
```

```python
snapshot = graph.get_state(config)
if 'messages' in snapshot.values:
	pprint(snapshot.values['messages'])
else:
	print("No messages found in the snapshot.")
print(snapshot.next)
```

**실행 결과 (예시):**
```
[기존 메시지들...]
('tools',)
```

> 📌 `snapshot.next`가 `('tools',)`를 반환하면 그래프가 **tools 노드에서 중단(interrupt)**된 상태입니다. 이 상태에서 사람의 입력을 받아 `Command(resume=...)`로 재개할 수 있습니다. `()`이 반환되면 그래프가 정상 종료된 상태입니다.

```python
from langgraph.types import Command

human_response = (
    "네, 물론입니다. AI 에이전트 개발을 위한 기술 선택에 대한 지원을 해드리겠습니다. "
    "우선 LangGraph를 사용하는 것에 대해 어떻게 생각하시나요? "
    "LangGraph는 AI 에이전트를 개발하는 데 매우 유용한 도구입니다. "
)

human_command = Command(resume={"data": human_response})
response = graph.invoke(human_command, config)
print(response["messages"][-1].content)
```

**실행 결과 (예시):**
```
네, LangGraph를 AI 에이전트 개발에 사용하는 것은 좋은 선택입니다.
전문가의 의견에 따르면, LangGraph는 상태 관리와 워크플로우 제어에 강점이 있어...
```

```python
snapshot = graph.get_state(config)
pprint(snapshot.values['messages'])
print(snapshot.next)
```

```python
user_input3 = "앞서 추천해주신 기술의 시장성은 어떤가요?"
state3 = {"messages": [HumanMessage(content=user_input3)]}
response3 = graph.invoke(state3, config)

print(response3["messages"][-1].content)
```

```python
snapshot = graph.get_state(config)
pprint(snapshot.values['messages'])
print(snapshot.next)
```

```python
user_input4 = "LangGraph의 메모리 기능 추가에 대한 전문가의 지원이 필요해요."
state4 = {"messages": [HumanMessage(content=user_input4)]}
response4 = graph.invoke(state4, config)

print(response4["messages"][-1].content)
```

```python
snapshot = graph.get_state(config)
if 'messages' in snapshot.values:
	pprint(snapshot.values['messages'])
else:
	print("No messages found in the snapshot.")
print(snapshot.next)
```

```python
human_response = (
    "MemorySaver는 메모리 기반의 체크포인터로, 각 대화의 상태를 메모리에 임시로 저장하고 관리합니다. "
    "이를 통해 챗봇은 이전 대화 내용을 기억하고 다음 번 상호작용 시에도 맥락을 유지한 상태로 대화를 진행할 수 있습니다. "
    "실제 운영 환경에서는 더 영구적인 상태 관리를 위해 데이터베이스 기반 체크포인터(예: SqliteSaver 또는 PostgresSaver)를 사용하는 것이 권장됩니다."
)

human_command = Command(resume={"data": human_response})
response = graph.invoke(human_command, config)
print(response["messages"][-1].content)
```

```python
snapshot = graph.get_state(config)
pprint(snapshot.values['messages'])
print(snapshot.next)
```

<a id="part4"></a>

## 4. 도구 호출 승인 게이트 (Approval Gate) [↑](#toc)

지금까지는 `interrupt()`를 **도구 함수 내부**에서 호출하여 사람의 개입을 요청했습니다. LangGraph는 이보다 더 간단한 방법도 제공합니다. 그래프 컴파일 시 `interrupt_before` 옵션을 지정하면, 특정 노드 실행 전에 **자동으로** 그래프가 멈춥니다.

### interrupt_before 설정

```python
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from typing import Annotated

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4o-mini")
search_tool = TavilySearch(max_results=2)
llm_with_tools = llm.bind_tools([search_tool])

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

memory = InMemorySaver()
tool_node = ToolNode([search_tool])

workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", tool_node)
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")

# interrupt_before=["tools"] — 도구 실행 전 자동으로 멈춤
graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["tools"]
)
```

> 💡 `interrupt_before=["tools"]`를 지정하면, LLM이 도구 호출을 결정한 직후, 실제 도구가 실행되기 **전에** 그래프가 자동으로 일시 정지합니다. 도구 함수 코드를 수정하지 않아도 됩니다.

### 승인 게이트 워크플로우

승인 게이트를 사용하는 전형적인 흐름은 다음과 같습니다.

```mermaid
flowchart TD
    A[사용자 질문 입력] --> B[chatbot 노드: LLM이 도구 호출 결정]
    B --> C{interrupt_before 게이트}
    C -->|사람이 검토| D[도구 호출 내용 확인]
    D -->|승인| E["graph.invoke(None, config) — 실행 재개"]
    D -->|거절| F[상태 수정 또는 다른 입력 제공]
    E --> G[tools 노드 실행]
    G --> H[chatbot 노드: 최종 응답 생성]
    F --> B
```

**1단계: 질문 입력 → 그래프 일시 정지**

```python
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "approval_demo"}}
user_input = "오늘 서울 날씨를 검색해 주세요."

result = graph.invoke(
    {"messages": [HumanMessage(content=user_input)]},
    config
)

# 그래프가 tools 노드 직전에 멈춤
snapshot = graph.get_state(config)
print("현재 다음 노드:", snapshot.next)  # ('tools',)
```

**실행 결과 (예시):**
```
현재 다음 노드: ('tools',)
```

**2단계: 도구 호출 내용 확인**

```python
# LLM이 어떤 도구를 어떤 인수로 호출하려는지 확인
last_message = snapshot.values["messages"][-1]
print("LLM이 호출하려는 도구:")
for tool_call in last_message.tool_calls:
    print(f"  도구: {tool_call['name']}")
    print(f"  인수: {tool_call['args']}")
```

**실행 결과 (예시):**
```
LLM이 호출하려는 도구:
  도구: tavily_search
  인수: {'query': '서울 날씨 오늘'}
```

**3단계A: 승인 → 실행 재개**

```python
# None을 전달하면 "중단된 지점에서 그대로 계속" 의미
result = graph.invoke(None, config)
print(result["messages"][-1].content)
```

**실행 결과 (예시):**
```
오늘 서울의 날씨는 맑고 기온은 약 18°C입니다...
```

**3단계B: 거절 → 상태 수정**

```python
from langgraph.types import Command

# 도구 호출을 취소하고 직접 응답을 주입
result = graph.invoke(
    Command(resume="죄송합니다. 날씨 검색 도구 사용을 승인하지 않겠습니다. 직접 확인해 주세요."),
    config
)
```

### interrupt() vs interrupt_before 비교

| 구분 | `interrupt()` | `interrupt_before` |
|---|---|---|
| 설정 위치 | 도구 함수 내부 | 그래프 컴파일 시 |
| 적용 범위 | 해당 도구만 | 지정한 모든 노드 |
| 유연성 | 조건부 인터럽트 가능 | 항상 멈춤 |
| 코드 변경 | 도구 함수 수정 필요 | 도구 함수 수정 불필요 |
| 주요 사용처 | 특정 상황에서만 사람 확인 필요 | 모든 도구 실행 전 일괄 승인 |

> ⚠️ `interrupt_before`는 지정한 노드 실행 전에 **항상** 멈춥니다. 특정 조건에서만 멈추게 하려면 `interrupt()` 함수를 노드 내부에서 조건부로 호출하세요.

---

<a id="part5"></a>

## 5. Time Travel: 과거 상태로 되돌리기 [↑](#toc)

LangGraph의 체크포인터는 대화 중 매 단계의 상태를 스냅샷으로 저장합니다. 이 스냅샷들을 이용하면 과거의 특정 시점으로 되돌아가서 대화를 다시 진행할 수 있습니다. 이를 **Time Travel**이라고 합니다.

### 언제 필요한가?

> LLM이 잘못된 도구를 선택했거나, 엉뚱한 방향으로 응답을 생성했을 때, 한 단계 전으로 되돌려서 다시 시도할 수 있습니다.

마치 게임의 "세이브 포인트"처럼, 중요한 분기점으로 돌아가 다른 선택을 해볼 수 있습니다.

### 과거 상태 목록 조회

```python
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from typing import Annotated

class State(TypedDict):
    messages: Annotated[list, add_messages]

memory = InMemorySaver()
llm = ChatOpenAI(model="gpt-4o-mini")
search_tool = TavilySearch(max_results=2)
llm_with_tools = llm.bind_tools([search_tool])

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", ToolNode([search_tool]))
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")
graph = workflow.compile(checkpointer=memory)

# 몇 차례 대화를 진행하여 체크포인트 쌓기
config = {"configurable": {"thread_id": "time_travel_demo"}}
for msg in ["안녕하세요!", "LangGraph란 무엇인가요?", "LangGraph의 장점을 알려주세요."]:
    graph.invoke({"messages": [HumanMessage(content=msg)]}, config)

# 저장된 모든 상태(체크포인트) 조회
print("=== 저장된 상태 이력 ===")
for state in graph.get_state_history(config):
    step = state.metadata.get("step", "?")
    next_nodes = state.next
    msg_count = len(state.values.get("messages", []))
    print(f"Step: {step:>3} | 다음 노드: {str(next_nodes):<20} | 메시지 수: {msg_count}")
    print(f"  체크포인트 ID: {state.config['configurable']['checkpoint_id']}")
    print()
```

**실행 결과 (예시):**
```
=== 저장된 상태 이력 ===
Step:   6 | 다음 노드: ()                   | 메시지 수: 6
  체크포인트 ID: 1ef8a2b3-...

Step:   5 | 다음 노드: ('chatbot',)          | 메시지 수: 5
  체크포인트 ID: 1ef8a2b2-...

Step:   4 | 다음 노드: ()                   | 메시지 수: 4
  체크포인트 ID: 1ef8a2b1-...

Step:   3 | 다음 노드: ('chatbot',)          | 메시지 수: 3
  체크포인트 ID: 1ef8a2b0-...
...
```

> 💡 `get_state_history()`는 가장 최근 상태부터 역순으로 반환합니다. `state.next`가 `()`이면 해당 단계에서 그래프가 정상 종료된 상태, `('chatbot',)` 등이면 해당 노드 실행 직전 상태입니다.

### 특정 시점으로 되돌아가기

```python
# 이력에서 되돌아갈 체크포인트 선택
all_states = list(graph.get_state_history(config))

# 메시지가 2개였던 시점(첫 번째 대화 직후)을 찾기
target_state = None
for state in all_states:
    if len(state.values.get("messages", [])) == 2 and state.next == ():
        target_state = state
        break

if target_state:
    checkpoint_id = target_state.config["configurable"]["checkpoint_id"]
    print(f"되돌아갈 체크포인트: {checkpoint_id}")

    # 해당 체크포인트를 기준으로 새 config 구성
    replay_config = {
        "configurable": {
            "thread_id": "time_travel_demo",
            "checkpoint_id": checkpoint_id
        }
    }

    # 해당 시점 이후 새로운 질문으로 다시 시작
    new_result = graph.invoke(
        {"messages": [HumanMessage(content="그 시점에서 파이썬이란 무엇인가요?")]},
        replay_config
    )
    print("\n=== 과거 시점에서 새로 이어간 응답 ===")
    print(new_result["messages"][-1].content)
```

**실행 결과 (예시):**
```
되돌아갈 체크포인트: 1ef8a2b0-c4d5-...

=== 과거 시점에서 새로 이어간 응답 ===
파이썬(Python)은 간결하고 읽기 쉬운 문법을 가진 프로그래밍 언어입니다...
```

### Time Travel 활용 시나리오

| 시나리오 | 방법 |
|---|---|
| LLM이 잘못된 도구를 선택한 경우 | 도구 호출 직전 체크포인트로 복원 후 재실행 |
| 잘못된 정보로 응답을 생성한 경우 | 해당 응답 이전 체크포인트로 복원 후 다른 질문 |
| A/B 테스트 | 동일한 체크포인트에서 두 가지 입력으로 분기 실행 |
| 디버깅 | 특정 단계의 상태를 정확히 재현하여 문제 분석 |

> ⚠️ `InMemorySaver`는 프로세스가 종료되면 모든 이력이 사라집니다. 이력을 영구 보존하려면 `SqliteSaver` 또는 `PostgresSaver`를 사용하세요.

---

### 🎯 실습 미션

1. `interrupt` 후 `snapshot.next`를 출력하여 `('tools',)` 상태를 직접 확인해보세요. 정상 응답 후에도 출력하여 `()`과 비교해보세요.
2. `Command(resume={"data": "다른 응답"})`에서 `"data"` 키 대신 다른 키(예: `"answer"`)를 사용하면 어떤 에러가 발생하는지 확인해보세요.
3. `human_assist` 도구의 docstring을 수정하여 LLM이 더 자주/드물게 사람에게 도움을 요청하도록 유도해보세요.
4. `interrupt_before=["tools"]`를 사용하여 도구 실행 전 승인 여부를 묻는 챗봇을 만들어 보세요. 승인 시에는 `graph.invoke(None, config)`, 거절 시에는 다른 메시지를 출력하도록 분기를 구현해 보세요.
5. `get_state_history()`를 사용하여 특정 시점으로 되돌아간 후, 원래와 다른 질문을 해보세요. 이전 대화 맥락이 어디까지 유지되는지 관찰해보세요.

→ **다음 장**: [8. 스트리밍 심화](/llm/langgraph/streaming)
