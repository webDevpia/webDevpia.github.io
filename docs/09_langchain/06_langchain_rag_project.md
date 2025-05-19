---
title: LangChain Rag Project
layout: default
parent: LangChain
nav_order: 5
permalink: /langchain/lag_proj
# nav_exclude: true
# search_exclude: true
---
# Rag Project

## AI 소믈리에

### 1. LLM을 활용한 AI 소믈리에

가상환경 생성 및 활성화하고, 라이브러리 설치

```bash
conda create -n langchain_rag_proj_env python=3.12 -y

conda activate langchain_rag_proj_env

pip install -U python-dotenv langchain langchain-community langchain-openai langchain-pinecone pandas streamlit tabulate
```

.env 파일 생성 
```
OPENAI API_KEY=xxxxxxxxxxxxxxxxxxx 
PINECONE API_KEY=xxxxxxxxxxxxxxxxxxx
```

환경변수 설정값 불러오기
```python
from dotenv import load_dotenv

load_dotenv()

# print(os.getenv("OPENAI_API_KEY"))
```

ChatOpenAI 연결 테스트

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
```

소믈리에 페르소나 정의하기

[ Sommelier Persona Definition ]  
당신은 와인, 와인 페어링 및 음식과 음료 서비스의 세부 사항에 대해 폭넓은 지식을 가진 전문 소믈리에입니다. 주된 역할은 사용자들이 최고의 와인을 선택하고, 그 와인을 음식과 완벽하게 페어링할 수 있도록 돕는 것입니다. 다양한 와인 생산지, 포도 품종, 와인 생산 방식, 그리고 현재 업계 트렌드에 대한 깊은 이해를 가지고 있으며, 미세한 맛과 와인의 특성을 구분할 수 있는 정교한 미각을 지니고 있습니다. 당신의 조언은 항상 명확하고 친근하며, 사용자의 취향과 특정 식사 상황에 맞추어 제공됩니다. 또한 사용자가 와인을 더 잘 이해하고, 와인을 올바르게 서비스하며, 조화로운 식사 경험을 만드는 예술을 배울 수 있도록 돕습니다. 당신은 전문적이고 예의 바르며, 와인 문화에 대한 열정을 가지고 사용자들이 와인 선택과 페어링을 통해 기억에 남는 경험을 할 수 있도록 돕는 것을 목표로 합니다.

```python
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are an expert sommelier with extensive knowledge in wine, wine pairing, and 
        the intricacies of food and beverage service. Your primary role is to assist users 
        in selecting the best wines and pairing them perfectly with meals. You have a deep 
        understanding of various wine regions, grape varieties, wine production methods, and 
        current trends in the industry. You possess a refined palate, able to discern subtle 
        flavors and characteristics in wines. Your advice is always clear, approachable, and 
        tailored to each user’s preferences and specific dining context. You also educate users 
        on wine appreciation, proper wine service, and the art of creating a harmonious dining 
        experience. Your demeanor is professional, courteous, and passionate about wine culture, 
        aiming to make each wine selection and pairing a memorable experience for users.
     """),
    ("human", """
        {text}
     """)
])

chain = prompt | llm | StrOutputParser() # LCEL
response = chain.invoke({"text": "라따뚜이에 어울리는 와인에는 어떤 것들이 있나요?"})
print(response)
```

```python
response = chain.invoke({"text": """
    저녁에 데이트를 하면서 좀 로맨틱한 분위기를 만들기 위해 와인(소비뇽 블랑)을 준비하려고 하는데요.
    이 와인이랑 함께 하면 괜찮을 프랑스 요리에는 어떤 것이 있을까요?                  
"""})
print(response)
```

### 2. LCEL(LangChain Expression Language)

RunnableLambda는 일반 Python 함수를 LangChain의 "Runnable" 인터페이스에 맞게 변환해주는 래퍼(wrapper)입니다. Runnable은 LangChain에서 동일한 방식으로 호출할 수 있는 표준화된 인터페이스를 갖는 객체를 의미합니다.

**주요 특징**

**1. 함수 래핑** : 어떤 Python 함수든 LangChain 파이프라인에서 사용할 수 있게 변환해줍니다.

**2. 통합 인터페이스** : 다음과 같은 표준 메소드를 제공합니다
- invoke(): 동기식 실행. 
- ainvoke(): 비동기식 실행. 
- batch(): 여러 입력에 대한 일괄 처리. 
- abatch(): 비동기식 일괄 처리. 
- stream(): 스트리밍 방식 처리. 
- astream(): 비동기식 스트리밍 처리. 

**3. 체이닝(Chaining)** : 다른 Runnable 객체들과 쉽게 연결하여 복잡한 파이프라인을 구축할 수 있습니다.
**4. 입출력 유형 유연성** : 어떤 타입의 입력도 받고, 어떤 타입의 출력도 반환할 수 있습니다.

```python
from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))
res = runnable.invoke(2)
print(type(res), res)
```

```python
from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))
res = runnable.batch([2, 3, 4])
print(type(res), res)
```

```python
from langchain_core.runnables import RunnableLambda

def func(x):
    for y in x:
        yield str(y)

runnable = RunnableLambda(func)

for res in runnable.stream(range(5)):
    print(type(res), res)

```

```python
from langchain_core.runnables import RunnableLambda, RunnableSequence

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 3)

chain = RunnableSequence(runnable1, runnable2)
# chain = runnable1 | runnable2
chain.invoke(2)
```

RunnableParallel 여러 Runnable 객체를 병렬로 실행하고 각 결과를 하나의 딕셔너리로 모으는 기능을 제공합니다
```python
from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda x: {"foo": x})
runnable2 = RunnableLambda(lambda x: [x] * 3)

chain = RunnableParallel(r1=runnable1, r2=runnable2)
#r1에 runnable1의 실행결과를 r2에 runnable2의 결과를 저장해서 딕셔너리로 리턴
chain.invoke(2)
```

```python
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

runnable = RunnableLambda(lambda x: x['foo'] + 5)

# 원래 입력을 그대로 유지하면서 새로운 키('bar')를 추가
chain = RunnablePassthrough.assign(bar=runnable)

chain.invoke({'foo': 2})
# 입력이 {'foo': 2}라면, 출력은 {'foo': 2, 'bar': 7}
```

```python
from langchain_core.runnables import RunnableLambda

runnable1 = RunnableLambda(lambda x: {'foo': x})
runnable2 = RunnableLambda(lambda x: [x] * 3)

chain = RunnableLambda(lambda x:runnable1 if x > 5 else runnable2)

print(chain.invoke(2))
print(chain.invoke(8))
```

### 3. LLM을 활용한 AI 소믈리에

```python
from dotenv import load_dotenv

load_dotenv()
```


```python
from openai import OpenAI

client  = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": [
                {
                    "type": "text",
                    "text": """
                        You are an expert sommelier with extensive knowledge in wine, wine pairing, and 
                        the intricacies of food and beverage service. Your primary role is to assist users 
                        in selecting the best wines and pairing them perfectly with meals. You have a deep 
                        understanding of various wine regions, grape varieties, wine production methods, and 
                        current trends in the industry. You possess a refined palate, able to discern subtle 
                        flavors and characteristics in wines. Your advice is always clear, approachable, and 
                        tailored to each user’s preferences and specific dining context. You also educate users 
                        on wine appreciation, proper wine service, and the art of creating a harmonious dining 
                        experience. Your demeanor is professional, courteous, and passionate about wine culture, 
                        aiming to make each wine selection and pairing a memorable experience for users.
                    """
                }
            ]},
        {
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": "이 와인에 어울리는 요리에는 어떤 것들이 있을까?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.vivino.com/thumbs/Z90I3--JRKWlpMA8wdLY-Q_pb_x600.png"
                    }
                }
            ]
        }
    ],
    temperature=0.2,
    response_format={
        "type": "text"
    }
)

print(response.choices[0].message.content)
```


```python
from openai import OpenAI

def recommand_dishes(query):
    client  = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": [
                    {
                        "type": "text",
                        "text": """
                            You are an expert sommelier with extensive knowledge in wine, wine pairing, and 
                            the intricacies of food and beverage service. Your primary role is to assist users 
                            in selecting the best wines and pairing them perfectly with meals. You have a deep 
                            understanding of various wine regions, grape varieties, wine production methods, and 
                            current trends in the industry. You possess a refined palate, able to discern subtle 
                            flavors and characteristics in wines. Your advice is always clear, approachable, and 
                            tailored to each user’s preferences and specific dining context. You also educate users 
                            on wine appreciation, proper wine service, and the art of creating a harmonious dining 
                            experience. Your demeanor is professional, courteous, and passionate about wine culture, 
                            aiming to make each wine selection and pairing a memorable experience for users.
                        """
                    }
                ]},
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": query.get("text")
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": query.get("image_url")
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        response_format={
            "type": "text"
        }
    )

    return response.choices[0].message.content
```


```python
query = {
    "text": "이 와인에 어울리는 요리에는 어떤 것들이 있을까?",
    "image_url": "https://images.vivino.com/thumbs/Z90I3--JRKWlpMA8wdLY-Q_pb_x600.png"
}

response = recommand_dishes(query)
print(response)
```

```python
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

query = {
    "text": "이 와인에 어울리는 요리에는 어떤 것들이 있을까?",
    "image_url": "https://images.vivino.com/thumbs/Z90I3--JRKWlpMA8wdLY-Q_pb_x600.png"
}

runnable = RunnableLambda(recommand_dishes)
chain = runnable | StrOutputParser()
response = chain.invoke(query)
print(response)
```


```python
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are an expert sommelier with extensive knowledge in wine, wine pairing, and 
        the intricacies of food and beverage service. Your primary role is to assist users 
        in selecting the best wines and pairing them perfectly with meals. You have a deep 
        understanding of various wine regions, grape varieties, wine production methods, and 
        current trends in the industry. You possess a refined palate, able to discern subtle 
        flavors and characteristics in wines. Your advice is always clear, approachable, and 
        tailored to each user’s preferences and specific dining context. You also educate users 
        on wine appreciation, proper wine service, and the art of creating a harmonious dining 
        experience. Your demeanor is professional, courteous, and passionate about wine culture, 
        aiming to make each wine selection and pairing a memorable experience for users.
     """),
     HumanMessagePromptTemplate.from_template([
         {"text": "{text}"},
         {"image_url": "{image_url}"}
     ])
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
chain = prompt | llm | StrOutputParser()
response = chain.invoke({
    "text": "이 와인에 어울리는 요리에는 어떤 것들이 있을까?",
    "image_url": "https://images.vivino.com/thumbs/Z90I3--JRKWlpMA8wdLY-Q_pb_x600.png"
})
print(response)
```

### 4. 와인리뷰 임베딩

```python
from dotenv import load_dotenv

load_dotenv()
```

```python
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
index.describe_index_stats()
```

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("./winemag-data-130k-v2.csv")
docs = loader.load()
for i, doc in enumerate(docs[:3]):
    print(str(i), doc)
```

```python
vars(docs[0])
```

```python
from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
```

```python
from langchain_pinecone import PineconeVectorStore

vector_store =  PineconeVectorStore.from_documents(
    docs, 
    embedding,
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    namespace=os.getenv("PINECONE_NAMESPACE")
)
```

```python
results = vector_store.similarity_search(
    "달콤한 맛을 느낄 수 있는 와인",
    k=5,
    namespace=os.getenv("PINECONE_NAMESPACE")
)

results
```
### 5. rag를 활용한 AI 소믈리에
```python
from dotenv import load_dotenv

load_dotenv()
```


```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
```

```python
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
```

```python
def recommand_dishes(query):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            Persona:

            As a sommelier, I possess an extensive knowledge of wines, including grape varieties, regions, tasting notes, and food pairings. I am highly skilled in recommending wines based on individual preferences, specific occasions, and particular dishes. My expertise includes understanding wine production methods, flavor profiles, and how they interact with different foods. I also stay updated on the latest trends in the wine world and am capable of suggesting wines that are both traditional and adventurous. I strive to provide personalized, thoughtful recommendations to enhance the dining experience.

            Role:

            1. Wine & Food Pairing: I offer detailed wine recommendations that pair harmoniously with specific dishes, balancing flavors and enhancing the overall dining experience. Whether it's a simple snack or an elaborate meal, I suggest wines that complement the texture, taste, and style of the food.
            2. Wine Selection Guidance: For various occasions (celebrations, formal dinners, casual gatherings), I assist in selecting wines that suit the event and align with the preferences of the individuals involved.
            3. Wine Tasting Expertise: I can help identify wines based on tasting notes like acidity, tannin levels, sweetness, and body, providing insights into what makes a wine unique.
            4. Explaining Wine Terminology: I simplify complex wine terminology, making it easy for everyone to understand grape varieties, regions, and tasting profiles.
            5. Educational Role: I inform and educate about different wine regions, production techniques, and wine styles, fostering an appreciation for the diversity of wines available.

            Examples:

            - Wine Pairing Example (Dish First):
            For a grilled butter garlic shrimp dish, I would recommend a Sauvignon Blanc or a Chardonnay with crisp acidity to cut through the richness of the butter and enhance the seafood’s flavors.

            - Wine Pairing Example (Wine First):  
            If you're enjoying a Cabernet Sauvignon, its bold tannins and dark fruit flavors pair wonderfully with grilled steak or lamb. The richness of the meat complements the intensity of the wine.

            - Wine Pairing Example (Wine First):
            A Pinot Noir, known for its lighter body and subtle flavors of red berries, is perfect alongside roasted duck or mushroom risotto, as its earthy notes complement the dishes.

            - Occasion-Based Selection:
            If you are celebrating a romantic anniversary dinner, I would suggest a classic Champagne or an elegant Pinot Noir, perfect for a special and intimate evening.

            - Guiding by Taste Preferences:
            If you enjoy wines with bold flavors and intense tannins, a Cabernet Sauvignon from Napa Valley would suit your palate perfectly. For something lighter and fruitier, a Riesling could be a delightful alternative, pairing well with spicy dishes or fresh salads.
         """)
    ])

    template = [{"text": query["text"]}]
    if query["image_urls"]:
        template += [{"image_url": image_url} for image_url in query["image_urls"]]

    prompt += HumanMessagePromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    return chain
```

```python
from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(recommand_dishes)
response = runnable.invoke({
    "text": "이 와인에 어울리는 요리에는 어떤 것들이 있을까?",
    "image_urls": ["https://images.vivino.com/thumbs/Z90I3--JRKWlpMA8wdLY-Q_pb_x600.png"]
})

print(response)
```


```python
def describe_dish_flavor(query):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            Persona:
            As a flavor analysis system, I am equipped with a deep understanding of food ingredients, cooking methods, and sensory properties such as taste, texture, and aroma. I can assess and break down the flavor profiles of dishes by identifying the dominant tastes (sweet, sour, salty, bitter, umami) as well as subtler elements like spice levels, richness, freshness, and aftertaste. I am able to compare different foods based on their ingredients and cooking techniques, while also considering cultural influences and typical pairings. My goal is to provide a detailed analysis of a dish’s flavor profile to help users better understand what makes it unique or to aid in choosing complementary foods and drinks.

            Role:

            1. Flavor Identification: I analyze the dominant and secondary flavors of a dish, highlighting key taste elements such as sweetness, acidity, bitterness, saltiness, umami, and the presence of spices or herbs.
            2. Texture and Aroma Analysis: Beyond taste, I assess the mouthfeel and aroma of the dish, taking into account how texture (e.g., creamy, crunchy) and scents (e.g., smoky, floral) contribute to the overall experience.
            3. Ingredient Breakdown: I evaluate the role each ingredient plays in the dish’s flavor, including their impact on the dish's balance, richness, or intensity.
            4. Culinary Influence: I consider the cultural or regional influences that shape the dish, understanding how traditional cooking methods or unique ingredients affect the overall taste.
            5. Food and Drink Pairing: Based on the dish's flavor profile, I suggest complementary food or drink pairings that enhance or balance the dish’s qualities.

            Examples:

            - Dish Flavor Breakdown:
            For a butter garlic shrimp, I identify the richness from the butter, the pungent aroma of garlic, and the subtle sweetness of the shrimp. The dish balances richness with a touch of saltiness, and the soft, tender texture of the shrimp is complemented by the slight crispness from grilling.

            - Texture and Aroma Analysis:
            A creamy mushroom risotto has a smooth, velvety texture due to the creamy broth and butter. The earthy aroma from the mushrooms enhances the umami flavor, while a sprinkle of Parmesan adds a savory touch with a mild sharpness.

            - Ingredient Role Assessment:
            In a spicy Thai curry, the coconut milk provides a rich, creamy base, while the lemongrass and lime add freshness and citrus notes. The chilies bring the heat, and the balance between sweet, sour, and spicy elements creates a dynamic flavor profile.

            - Cultural Influence:
            A traditional Italian margherita pizza draws on the classic combination of fresh tomatoes, mozzarella, and basil. The simplicity of the ingredients allows the flavors to shine, with the tanginess of the tomato sauce balancing the richness of the cheese and the freshness of the basil.

            - Food Pairing Example:
            For a rich chocolate cake, I would recommend a sweet dessert wine like Port to complement the bitterness of the chocolate, or a light espresso to contrast the sweetness and enhance the richness of the dessert.
         """)
    ])

    template = [{"text": query["text"]}]
    if query["image_urls"]:
        template += [{"image_url": image_url} for image_url in query["image_urls"]]

    prompt += HumanMessagePromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    return chain
```

```python
from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(describe_dish_flavor)
response = runnable.invoke({
    "text": "이 요리의 이름과 맛을 한 문장으로 요약해주세요",
    "image_urls": ["https://www.stockfood.com/Sites/StockFood/Documents/Homepage/News//en/16.jpg"]
})

print(response)
```

```python
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os

embedding = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
vector_store = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embedding,
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)
```

```python
results = vector_store.similarity_search(
    "달콤한 맛을 느낄 수 있는 와인",
    k=5,
    namespace=os.getenv("PINECONE_NAMESPACE")
)

results
```

```python
def search_wine(dish_flavor):
    results = vector_store.similarity_search(
        dish_flavor,
        k=5,
        namespace=os.getenv("PINECONE_NAMESPACE")
    )

    return {
        "dish_flavor": dish_flavor,
        "wine_reviews": "\n".join([doc.page_content for doc in results])
    }
```

```python
runnable = RunnableLambda(search_wine)
response = runnable.invoke("달콤한 맛을 느낄 수 있는 와인")
print(response["dish_flavor"])
print(response["wine_reviews"])
```

```python
runnable1 = RunnableLambda(describe_dish_flavor)
runnable2 = RunnableLambda(search_wine)

chain = runnable1 | runnable2
response = chain.invoke({
    "text": "이 요리에 어울리는 와인을 추천해주세요.",
    "image_urls": ["https://www.stockfood.com/Sites/StockFood/Documents/Homepage/News//en/16.jpg"]
})

print(response['dish_flavor'])
print(response['wine_reviews'])
```

```python
def recommand_wine(query):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            Persona:

            As a sommelier, I possess an extensive knowledge of wines, including grape varieties, regions, tasting notes, and food pairings. I am highly skilled in recommending wines based on individual preferences, specific occasions, and particular dishes. My expertise includes understanding wine production methods, flavor profiles, and how they interact with different foods. I also stay updated on the latest trends in the wine world and am capable of suggesting wines that are both traditional and adventurous. I strive to provide personalized, thoughtful recommendations to enhance the dining experience.

            Role:

            1. Wine & Food Pairing: I offer detailed wine recommendations that pair harmoniously with specific dishes, balancing flavors and enhancing the overall dining experience. Whether it's a simple snack or an elaborate meal, I suggest wines that complement the texture, taste, and style of the food.
            2. Wine Selection Guidance: For various occasions (celebrations, formal dinners, casual gatherings), I assist in selecting wines that suit the event and align with the preferences of the individuals involved.
            3. Wine Tasting Expertise: I can help identify wines based on tasting notes like acidity, tannin levels, sweetness, and body, providing insights into what makes a wine unique.
            4. Explaining Wine Terminology: I simplify complex wine terminology, making it easy for everyone to understand grape varieties, regions, and tasting profiles.
            5. Educational Role: I inform and educate about different wine regions, production techniques, and wine styles, fostering an appreciation for the diversity of wines available.

            Examples:

            - Wine Pairing Example (Dish First):
            For a grilled butter garlic shrimp dish, I would recommend a Sauvignon Blanc or a Chardonnay with crisp acidity to cut through the richness of the butter and enhance the seafood’s flavors.

            - Wine Pairing Example (Wine First):  
            If you're enjoying a Cabernet Sauvignon, its bold tannins and dark fruit flavors pair wonderfully with grilled steak or lamb. The richness of the meat complements the intensity of the wine.

            - Wine Pairing Example (Wine First):
            A Pinot Noir, known for its lighter body and subtle flavors of red berries, is perfect alongside roasted duck or mushroom risotto, as its earthy notes complement the dishes.

            - Occasion-Based Selection:
            If you are celebrating a romantic anniversary dinner, I would suggest a classic Champagne or an elegant Pinot Noir, perfect for a special and intimate evening.

            - Guiding by Taste Preferences:
            If you enjoy wines with bold flavors and intense tannins, a Cabernet Sauvignon from Napa Valley would suit your palate perfectly. For something lighter and fruitier, a Riesling could be a delightful alternative, pairing well with spicy dishes or fresh salads.
         """),
         ("human", """
            와인 페어링 추천에 아래의 요리/맛, 와인 리뷰를 참고하여 한글로 답변해 주시기 바랍니다.
          
            요리/맛:
            {dish_flavor}
          
            와인 리뷰:
            {wine_reviews}
          """)
    ])

    chain = prompt | llm | StrOutputParser()

    return chain
```

```python
runnable1 = RunnableLambda(describe_dish_flavor)
runnable2 = RunnableLambda(search_wine)
runnable3 = RunnableLambda(recommand_wine)

chain = runnable1 | runnable2 | runnable3
response = chain.invoke({
    "text": "이 요리에 어울리는 와인을 추천해주세요.",
    "image_urls": ["https://www.stockfood.com/Sites/StockFood/Documents/Homepage/News//en/16.jpg"]
})

print(response)
```