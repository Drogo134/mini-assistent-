import os
from dotenv import load_dotenv
from sambanova import SambaNova
from rag_utils import get_context_from_docs
from prompt_examples import PROMPT_TEMPLATE

# Загружаем .env
load_dotenv()

# Получаем ключ из .env
API_KEY = os.getenv("SAMBANOVA_API_KEY")
if not API_KEY:
    raise ValueError("❌ Не найден SAMBANOVA_API_KEY в .env файле")

# Инициализация клиента
client = SambaNova(
    api_key=API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

def run_assistant(user_query: str):
    """Основная функция общения с ассистентом."""
    # Получаем контекст из документов
    context = get_context_from_docs(user_query)

    # Формируем полный промт
    prompt = PROMPT_TEMPLATE.format(
        user_query=user_query,
        context=context
    )

    # Отправляем запрос в модель
    response = client.chat.completions.create(
        model="DeepSeek-R1-Distill-Llama-70B",
        messages=[
            {"role": "system", "content": "Ты умный помощник, использующий контекст из документов."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        top_p=0.9
    )

    # Печатаем ответ
    answer = response.choices[0].message.content
    print("\nОтвет ассистента:\n", answer)

if __name__ == "__main__":
    print("=== RAG-Ассистент (SambaNova) ===")
    query = input("Введите ваш запрос: ")
    run_assistant(query)
