import os
from dotenv import load_dotenv
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

load_dotenv()

def create_rag_chain(
    documents: List[Document],
    embedding_model_name: str = 'all-MiniLM-L6-v2',
    llm_model_name: str = "openai/gpt-4o-mini",
    temperature: float = 0.0
) -> RetrievalQA:
    """
    Создает и настраивает цепочку для вопросно-ответной системы с использованием RAG.

    Эта функция выполняет следующие шаги:
    1. Инициализирует модель для создания эмбеддингов (векторных представлений) текста.
    2. Создает векторное хранилище FAISS из предоставленных документов.
    3. Инициализирует языковую модель (LLM) через OpenRouter.
    4. Собирает все компоненты в единую цепочку RetrievalQA.

    Args:
        documents (List[Document]): Список документов LangChain для индексации.
        embedding_model_name (str, optional): Название модели эмбеддингов от Sentence Transformers.
                                            Defaults to 'all-MiniLM-L6-v2'.
        llm_model_name (str, optional): Название модели LLM, доступной через OpenRouter.
                                      Defaults to "openai/gpt-4o-mini".
        temperature (float, optional): "Температура" модели для контроля креативности ответов.
                                     0.0 для наиболее детерминированных ответов. Defaults to 0.0.

    Returns:
        RetrievalQA: Готовая к использованию цепочка LangChain для ответов на вопросы.
        
    Raises:
        ValueError: Если ключи API для OpenRouter не найдены в переменных окружения.
    """
    # --- Шаг 1: Проверка наличия ключей API ---
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    openrouter_base_url = os.getenv('OPENROUTER_BASE_URL', "https://openrouter.ai/api/v1")
    
    if not openrouter_api_key:
        raise ValueError("Переменная окружения OPENROUTER_API_KEY не установлена. "
                         "Пожалуйста, добавьте ее в ваш .env файл.")

    # --- Шаг 2: Создание модели для эмбеддингов ---
    # Эта модель будет работать локально на вашем CPU/GPU
    print("Инициализация модели эмбеддингов...")
    embed_model = SentenceTransformerEmbeddings(model_name=embedding_model_name)

    # --- Шаг 3: Создание векторного хранилища ---
    # Документы преобразуются в векторы и сохраняются в быстрой in-memory базе FAISS
    # для семантического поиска.
    print(f"Создание векторного хранилища FAISS из {len(documents)} документов...")
    vector_store = FAISS.from_documents(documents, embed_model)

    # --- Шаг 4: Инициализация языковой модели (LLM) ---
    # Используем OpenRouter для доступа к различным моделям
    print(f"Инициализация LLM: {llm_model_name}...")
    qa_model = ChatOpenAI(
        model=llm_model_name,
        temperature=temperature,
        api_key=openrouter_api_key,
        base_url=openrouter_base_url
    )

    # --- Шаг 5: Сборка цепочки RetrievalQA ---
    # Это стандартная цепочка для вопросно-ответных систем. [github.com](https://github.com/the-ogre/LLM-ChatbotAdvancedRAGContextualCompressorReranking)
    # chain_type="stuff" означает, что все найденные документы будут "запихнуты" (stuffed)
    # в один промпт к LLM.
    print("Создание цепочки RetrievalQA...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=qa_model,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    print("Цепочка успешно создана!")
    return qa_chain

# --- Пример использования ---
def example_usage():
    """
    Демонстрирует, как использовать функцию create_rag_chain.
    """
    # 1. Подготовьте ваши документы.
    # В реальном приложении вы бы загружали их из файлов (PDF, TXT, HTML).
    # Здесь мы используем простые строки для примера.
    # `html_header_splits` из вашего примера — это список таких документов.
    example_docs = [
        Document(page_content="LangChain - это фреймворк для разработки приложений на базе больших языковых моделей."),
        Document(page_content="Ключевая особенность LangChain - возможность создавать цепочки (chains) из разных компонентов."),
        Document(page_content="OpenRouter предоставляет единый API для доступа к множеству LLM, включая модели от OpenAI, Google и Anthropic."),
        Document(page_content="FAISS - это библиотека для эффективного поиска по сходству и кластеризации плотных векторов.")
    ]

    try:
        # 2. Создайте цепочку, передав ей документы
        rag_chain = create_rag_chain(documents=example_docs)

        # 3. Задайте вопрос
        query = "Что такое LangChain?"
        print(f"\nЗапрос: {query}")
        
        # 4. Получите ответ
        # Метод invoke используется в новых версиях LangChain
        response = rag_chain.invoke(query)
        
        print("\nОтвет:")
        print(response['result'])
        
        # --- Другой вопрос ---
        query_2 = "Как OpenRouter связан с LLM?"
        print(f"\nЗапрос: {query_2}")
        response_2 = rag_chain.invoke(query_2)
        print("\nОтвет:")
        print(response_2['result'])

    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    example_usage()