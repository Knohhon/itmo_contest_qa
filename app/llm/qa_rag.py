from langchain.chains import RetrievalQA

def get_qa_answer(chain: RetrievalQA, question: str) -> str:
    """
    Принимает на вход созданную цепочку RetrievalQA и вопрос пользователя,
    а возвращает текстовый ответ от LLM.

    Args:
        chain (RetrievalQA): Готовая цепочка для ответов на вопросы.
        question (str): Вопрос от пользователя.

    Returns:
        str: Ответ, сгенерированный LLM.
    """
    print(f"Поиск ответа на вопрос: '{question}'")
    
    # В новых версиях LangChain рекомендуется использовать .invoke()
    # Входные данные передаются в виде словаря.
    result = chain.invoke({"query": question})
    
    # Ответ находится в ключе 'result'
    return result['result']
