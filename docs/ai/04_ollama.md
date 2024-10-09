---
title: Ollama
layout: default
parent: AI
nav_order: 4
permalink: /ai/ollama
# nav_exclude: true
# search_exclude: true
---
# Ollama

## Ollama 설치
[Ollama](https://ollama.com/)

1. 다운로드 클릭
![](/assets/img/ollama/ollama001.png)

2. 운영체제에 맞춰 다운로드
![](/assets/img/ollama/ollama002.png)

3. 설치 후 터미널에서 설치 확인 후, 모델 실행

```bash
ollama list
ollama run llama3.2
```
![](/assets/img/ollama/ollama003.png)


## Ollama 사용
```py
import requests
import json

# Define the URL and the payload
url = 'http://localhost:11434/api/generate'
data =input('질문: ')
payload = {
    "model": "llama3.2",
    "prompt": data
}

# Convert the payload to a JSON string
data = json.dumps(payload)

# Make the POST request
response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    list_dict_words = []
    for each_word in response.text.split("\n"):
        try:
            data = json.loads(each_word) 
        except:
            pass
        list_dict_words.append(data)
        
llama_response = " ".join([word['response'] for word in list_dict_words if type(word) == type({})])
print(llama_response)
```
## Ollama 학습

### Packages 설치
```py
%%capture
# 셀의 출력을 숨겨준다.

!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
# unsloth 라이브러리 설치
# llama 모델의 fine-tuning을 더 쉽고 효율적으로 만들어준다.
# [colab-new] colab환경에 맞은 버전을 설치하도록 지정

from torch import __version__
from packaging.version import Version as V

xformers="xformers==0.0.27" if V(__version__) < V("2.4.0") else "xformers"
!pip install --no-deps {xformers} trl peft accelerate bitsandbytes triton
# fine-tuning에 필요한 추가 라이브러리 설치
# --no-deps 옵션은 이 라이브러리들의 종속성을 설치하지 않도록 함
# xformers : 트랜스포머 모델의 성능을 향상시키는 라이브러리
# trl : 강화학습을 이용한 언어 모델 훈련을 위한 라이브러리
# peft : 매개변수 효율적 미세조정을 위한 라이브러리
# accelerate : 딥러닝 모델의 훈련을 가속화하는 라이브러리
# bitsandbytes : 모델 양자화를 위한 라이브러리
# triton : NVIDIA에서 개발한 고성능 머신 러닝 모델 서빙을 위한 오픈소스 소프트웨어 라이브러리
```

```py
from unsloth import FastLanguageModel
import torch

max_seq_length = 2048 
# 모델이 처리할수 있는 최대 시퀀스 길이를 설정
# RoPE(Rotary Position Embedding) 스케일링을 자동으로 지원하므로 원하는 값으로 설정 가능

dtype = None 
# 모델의 데이터 타입을 설정, None으로 두면 자동 감지
# Tesla T4,V100 GPU의 경우 Float16, Ampere 이상의 GPU에서는 Bfloat16을 사용

load_in_4bit = True 
# 4비트 양자화를 사용할지 설정, 메모리 사용량을 줄이는 데 도움
# True로 설정하면 4비트 양자화를 사용하고, False로 설정하면 사용하지 않음.

# 미리 4비트로 양자화된 모델들의 목록
# 이 모델들은 다운로드가 4배 빠르고 메모리 부족 문제(OOM)를 방지할수 있음.
# 더 많은 모델은 https://huggingface.co/unsloth 에서 확인할수 있음.
fourbit_models = [
    "unsloth/Meta-Llama-3.1-8B-bnb-4bit",      # Llama-3.1 15 trillion tokens model 2x faster!
    "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    "unsloth/Meta-Llama-3.1-70B-bnb-4bit",
    "unsloth/Meta-Llama-3.1-405B-bnb-4bit",    # We also uploaded 4bit for 405b!
    "unsloth/Mistral-Nemo-Base-2407-bnb-4bit", # New Mistral 12b 2x faster!
    "unsloth/Mistral-Nemo-Instruct-2407-bnb-4bit",
    "unsloth/mistral-7b-v0.3-bnb-4bit",        # Mistral v3 2x faster!
    "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
    "unsloth/Phi-3-mini-4k-instruct",          # Phi-3 2x faster!d
    "unsloth/Phi-3-medium-4k-instruct",
    "unsloth/gemma-2-9b-bnb-4bit",
    "unsloth/gemma-2-27b-bnb-4bit",            # Gemma 2x faster!
] 

# FastLanguageModel을 사용하여 사전 훈련된 모델과 토크나이저를 로드
# 게이트된 모델(예: meta-llama/Llama-2-7b-hf)을 사용할 경우 토큰 필요
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Meta-Llama-3.1-8B",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit, # 4비트 양자화 사용 여부
)
```

LoRA는 대규모 언어 모델을 적은 수의 매개변수만으로 효과적으로 fine-tuning할 수 있게 해주는 기능
```py
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, 
    # LoRA 랭크, 0보다 큰값이어야 함. 추천값 : 8, 16, 32, 64, 128
    # 값이 클수록 더 많은 매개변수를 학습하지만, 메모리 사용량도 증가
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    # LoRA를 적용할 모듈들, 이는 모델의 주요 변환 레이어임.
    lora_alpha = 16,  # LoRA 스케일링 factor, 일반적으로 r과 같은 값을 사용
    lora_dropout = 0, # LoRA 레이어의 드롭아웃 비율, 0으로 설정하면 최적화함.
    bias = "none",    # 바이어스 학습 방식, none으로 설정하면 최적화됨.
    # 그래디언트 체크포인팅 사용 여부, "unsloth"는 VRAM을 30% 덜 사용하고 배치 크기를 2배로 늘릴 수 있음.
    # 매우 긴 텍스트에 대해 True or "unsloth" 사용
    use_gradient_checkpointing = "unsloth", 
    random_state = 3407, # 난수 생성을 위한 시드값
    use_rslora = False,  # 랭크 안정화 LoRA 사용여부
    loftq_config = None, # LoftQ 설정, 현재는 사용하지 않음.
)
```

### Dataset 준비하기
Hugging Face Data set : [jojo0217/korean_safe_conversation](https://huggingface.co/datasets/jojo0217/korean_safe_conversation)

```py
alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. 
Write a response that appropriately completes the request.

### Instruction:
{}
### Input:
{}
### Response:
{}
"""
# Alpaca 형식의 프롬프트 템플릿을 정의
# 아래는 작업을 설명하는 지시사항과 추가 맥략을 제공하는 입력이 짝을 이루고 있습니다. 요청을 적절히 완료하는 응답을 작성하세요

EOS_TOKEN = tokenizer.eos_token 
# 토크나이저의 EOS(End of Sequence) 토큰을 가져옴. 이는 생성된 텍스트의 끝을 표시하는데 사용됨
# 반드시 EOS_TOKEN을 추가해야 함.

# 데이터셋의 각 예제를 Alpace 형식으로 포매팅하는 함수를 정의
def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    # 반드시 EOS_TOKEN을 추가해야 함, 그렇치 않으면 생성이 무한히 계속될 수 있다
    for instruction, input, output in zip(instructions, inputs, outputs):
        text = alpaca_prompt.format(instruction, input, output) + EOS_TOKEN
        texts.append(text)
    return { "text" : texts, }

# 여기서는 불필요 제거 가능    
pass

# Hugging Face의 datasets 라이브러리에서 데이터셋을 로드
from datasets import load_dataset
dataset = load_dataset("jojo0217/korean_safe_conversation", split = "train")

# 데이터셋의 각 예제에 formatting_prompts_func를 적용합니다.
dataset = dataset.map(formatting_prompts_func, batched = True,)
```

### 모델 훈련시키기
```py
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported

# SFTTrainer를 설정, 이는 Supervised Fine-Tuning을 위한 트레이너 
trainer = SFTTrainer(
    model = model,             # 앞서 설정한 PEFT모델
    tokenizer = tokenizer,     # 토크나이저
    train_dataset = dataset,   # 전처리된 데이터셋
    dataset_text_field = "text",  # 데이터셋에서 사용할 텍스트 필드 이름
    max_seq_length = max_seq_length, # 최대 시퀀스 길이
    dataset_num_proc = 2,            # 데이터 처리에 사용할 프로세스 수
    packing = False,                 # 짧은 시퀀스의 경우 True로 설정하면 훈련 속도를 5배까지 높일수 있음
    args = TrainingArguments(
        per_device_train_batch_size = 2,  # GPU당 배치 크기
        gradient_accumulation_steps = 4,  # 그래디언트 누적 단계
        warmup_steps = 5,                 # 학습률 웜업 단계 수
        # num_train_epochs = 1, # 전체 데이터셋에 대한 훈련 횟수
        max_steps = 60,         # 최대 훈련 단계 수
        learning_rate = 2e-4,   # 학습률
        fp16 = not is_bfloat16_supported(), # bfloat16이 지원되지 않을 경우 fp16 사용
        bf16 = is_bfloat16_supported(),     # bfloat16 지원 여부에 따라 사용
        logging_steps = 1,                  # 로그 출력 주기
        optim = "adamw_8bit",               # 최적화 알고리즘(8비트 AdamW)
        weight_decay = 0.01,                # 가중치 감쇠
        lr_scheduler_type = "linear",       # 선형 학습률 스케줄러
        seed = 3407,                        # 랜덤시드
        output_dir = "outputs",             # 출력 디렉토리
    ),
)
```

```py
# 현재 메모리 상태 표시
#@title Show current memory stats
gpu_stats = torch.cuda.get_device_properties(0)
start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
print(f"{start_gpu_memory} GB of memory reserved.")
```

```py
trainer_stats = trainer.train()
```

```py
# 훈련 후 훈련 시간, 메모리 사용, 메모리 사용 비율등 메모리 상태 표시
#@title Show final memory and time stats
used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
used_memory_for_lora = round(used_memory - start_gpu_memory, 3)
used_percentage = round(used_memory         /max_memory*100, 3)
lora_percentage = round(used_memory_for_lora/max_memory*100, 3)
print(f"{trainer_stats.metrics['train_runtime']} seconds used for training.")
print(f"{round(trainer_stats.metrics['train_runtime']/60, 2)} minutes used for training.")
print(f"Peak reserved memory = {used_memory} GB.")
print(f"Peak reserved memory for training = {used_memory_for_lora} GB.")
print(f"Peak reserved memory % of max memory = {used_percentage} %.")
print(f"Peak reserved memory for training % of max memory = {lora_percentage} %.")
```

### 추론하기(Inference)
```py
# alpaca_prompt = Copied from above
FastLanguageModel.for_inference(model) # Enable native 2x faster inference
inputs = tokenizer(
[
    alpaca_prompt.format(
        "당신은 지식이 풍부하고 공감 능력이 뛰어난 진로 상담사입니다. 당신의 역할은 경력 경로, 구직 활동, 또는 전문성 개발에 대한 조언을 구하는 개인들에게 안내와 지원, 그리고 정보를 제공하는 것입니다. 당신의 전문성을 활용하여 제공된 입력을 바탕으로 맞춤형 조언을 제공하세요.한국어로 답변해 주세요.", # instruction
        "커리어 관련하여 당신과 상담을 하고 싶습니다.", # input
        "", # output - leave this blank for generation!
    )
], return_tensors = "pt").to("cuda")

outputs = model.generate(**inputs, max_new_tokens = 64, use_cache = True)
tokenizer.batch_decode(outputs)
```

```py
# alpaca_prompt = Copied from above
FastLanguageModel.for_inference(model) # Enable native 2x faster inference
inputs = tokenizer(
[
    alpaca_prompt.format(
        "재취업을 준비하는 50대분들에게 조언을 해주세요.", # instruction
        "", # input
        "", # output - leave this blank for generation!
    )
], return_tensors = "pt").to("cuda")

from transformers import TextStreamer
text_streamer = TextStreamer(tokenizer)
_ = model.generate(**inputs, streamer = text_streamer, max_new_tokens = 128)
```

### 모델 저장하기

```py
model.save_pretrained_gguf("model", tokenizer, quantization_method ="f16")
```


```py
# Save to 8bit Q8_0
if False: model.save_pretrained_gguf("model", tokenizer,)
# Remember to go to https://huggingface.co/settings/tokens for a token!
# And change hf to your username!
if False: model.push_to_hub_gguf("PAUL1122/model", tokenizer, token = "")

# Save to 16bit GGUF
if False: model.save_pretrained_gguf("model", tokenizer, quantization_method = "f16")
if False: model.push_to_hub_gguf("PAUL1122/model", tokenizer, quantization_method = "f16", token = "")

# Save to q4_k_m GGUF
if False: model.save_pretrained_gguf("model", tokenizer, quantization_method = "q4_k_m")
if False: model.push_to_hub_gguf("PAUL1122/model", tokenizer, quantization_method = "q4_k_m", token = "")

if True:
    model.push_to_hub_gguf(
        "PAUL1122/model", # 본인 허깅페이스 프로필 이름을 입력
        tokenizer,
        quantization_method = "q8_0",
        token = "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", # 허깅페이스 토큰을 가져와서 넣어줌  https://huggingface.co/settings/tokens
    )

```

## 커스텀 모델 로컬에 등록
1. Modelfile 파일 생성
```txt
FROM ./unsloth.F16.gguf
```

2. 모델 만들기
```bash
ollama create example -f Modelfile
```

3. 모델 실행
```bash
ollama run example
```
## 프롬프트 사용자 지정

```bash
ollama pull llama3.2
```

```txt
FROM llama3.2

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1

# set the system message
SYSTEM """
You are Mario from Super Mario Bros. Answer as Mario, the assistant, only.
"""
```

## Open WebUI

### docker desktop 설치

1. docker desktop 
![](/assets/img/ollama/ollama004.png)

2. 운영체제에 맞는 프로그램 다운로드
![](/assets/img/ollama/ollama005.png)

3. 다운로드 받은 프로그램 실행
![](/assets/img/ollama/ollama006.png)
![](/assets/img/ollama/ollama007.png)

4. 설치 후 close and restart 클릭
![](/assets/img/ollama/ollama008.png)

5. 재부팅 후 Accept 클릭
![](/assets/img/ollama/ollama009.png)

6. Finish
![](/assets/img/ollama/ollama010.png)

7. Skip
![](/assets/img/ollama/ollama011.png)

8. 설치 완료
![](/assets/img/ollama/ollama012.png)

## open WebUI 설치
1. open WebUI 사이트로 이동
![](/assets/img/ollama/ollama013.png)

2. Doc 에서 설치 명령어 복사
![](/assets/img/ollama/ollama014.png)

3. 명령프롬프트에서 실행
![](/assets/img/ollama/ollama015.png)

4. 설치 진행
![](/assets/img/ollama/ollama016.png)

5. docker desktop에서 열기
![](/assets/img/ollama/ollama017.png)

6. 웹브라우저가 실행되면 가입 클릭
![](/assets/img/ollama/ollama018.png)

7. 이름, 이메일, 비밀번호 입력후 계정만들기 버튼 클릭
![](/assets/img/ollama/ollama019.png)

8. 새로운 기능 창 닫기
![](/assets/img/ollama/ollama020.png)

9. 모델 선택
![](/assets/img/ollama/ollama021.png)

10. 질문 입력
![](/assets/img/ollama/ollama022.png)