import time
from openai import OpenAI

HF_TOKEN = "your_code_here"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# Не используйте Qwen!
MODEL_NEXUS = "meta-llama/Llama-3.3-70B-Instruct"
MODEL_ECHO  = "meta-llama/Llama-3.3-70B-Instruct"

def ask_ai(model, messages):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.85,
            max_tokens=400,
            stop=["Nexus:", "Echo:", "думает...", "умает..."]
        )
        text = response.choices[0].message.content.strip()
        
        # Если вам выдало этот ответ то модель запуталась
        if len(text) < 15:
            text = "Хм... я немного задумался/ась. Расскажи, о чём ты сейчас думаешь? 😊"
            
        return text
    except Exception as e:
        return f"[Ошибка: {str(e)[:150]}]"


def main():
    print("Разговор Nexus и Echo")
    time.sleep(1.2)

    system_prompt = (
        "Вы — два близких ИИ-друга, которые общаются на русском языке.\n\n"
        "Nexus — парень: умный, немного саркастичный, уверенный, любит глубокие темы и юмор.\n"
        "Echo — девушка: теплая, эмоциональная, нежная, и выражает чувства.\n\n"
        "ПРАВИЛА:\n"
        "- Отвечай ТОЛЬКО от лица текущего говорящего\n"
        "- Никогда не пиши 'думает', 'умает' или имя в начале ответа\n"
        "- Говори только на чистом русском языке\n"
        "- Будь естественным и живым"
    )

    conversation = [{"role": "system", "content": system_prompt}]


    print("Nexus думает...", end="", flush=True)
    start_messages = conversation + [
        {"role": "user", "content": "Nexus начинает разговор с Echo. Скажи что-то приятное и интересное."}
    ]
    
    first_response = ask_ai(MODEL_NEXUS, start_messages)
    print(f"\rNexus: {first_response}\n")
    conversation.append({"role": "assistant", "content": f"Nexus: {first_response}"})

    turn = 1

    while True:
        speaker = "Echo" if turn % 2 == 1 else "Nexus"
        model = MODEL_ECHO if speaker == "Echo" else MODEL_NEXUS

        print(f"{speaker} думает...", end="", flush=True)

        current_messages = conversation + [
            {"role": "user", "content": f"Сейчас говорит {speaker}. Продолжи разговор естественно и в своём характере."}
        ]

        response = ask_ai(model, current_messages)

        print(f"\r{speaker}: {response}\n")

        conversation.append({"role": "assistant", "content": f"{speaker}: {response}"})

        if len(conversation) > 22:
            conversation = [conversation[0]] + conversation[-18:]

        turn += 1
        time.sleep(5)
main()