import os

def get_context_from_docs(query: str, docs_path="docs"):
    """
    Простейшая реализация RAG:
    считывает все документы из docs/ и выбирает те,
    где встречаются слова из запроса.
    """
    context_parts = []
    keywords = query.lower().split()

    if not os.path.exists(docs_path):
        return "Документы не найдены."

    for file in os.listdir(docs_path):
        if file.endswith(".txt"):
            with open(os.path.join(docs_path, file), "r", encoding="utf-8") as f:
                text = f.read()
                if any(word in text.lower() for word in keywords):
                    context_parts.append(text[:500])  # ограничим контекст

    return "\n".join(context_parts) if context_parts else "Контекст не найден."
