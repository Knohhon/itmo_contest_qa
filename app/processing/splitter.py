from typing import List, Tuple
from langchain.docstore.document import Document
from langchain_text_splitters import HTMLHeaderTextSplitter # Примечание: Используем стандартный HTMLHeaderTextSplitter
from utils.html_loader import get_file_contents_from_folder

def splitter_func(
    html_string: str,
    max_chunk_size: int = 500,
    headers_to_split_on: List[Tuple[str, str]] = None
) -> List[Document]:
    """
    Разделяет HTML-строку на семантические чанки на основе заголовков.

    Эта функция использует HTMLHeaderTextSplitter из LangChain для разделения
    HTML-документа на более мелкие части, сохраняя при этом иерархию
    заголовков в метаданных каждого чанка. Это крайне полезно для
    RAG-систем, так как позволяет передавать в модель не только текст,
    но и его структурный контекст.

    Args:
        html_string (str): Строка, содержащая HTML-разметку для разделения.
        max_chunk_size (int, optional): Максимальный размер каждого чанка.
            Defaults to 500.
        headers_to_split_on (List[Tuple[str, str]], optional): Список
            кортежей, определяющих, по каким тегам заголовков выполнять
            разделение и как называть их в метаданных. Defaults to h1-h5.

    Returns:
        List[Document]: Список объектов Document, где каждый объект содержит
                        часть текста (page_content) и метаданные с иерархией
                        заголовков (metadata).
    """
    if headers_to_split_on is None:
        headers_to_split_on = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3"),
            ("h4", "Header 4"),
            ("h5", "Header 5"),
        ]

    # Инициализируем сплиттер
    # HTMLHeaderTextSplitter является стандартным и эффективным решением
    # для этой задачи в LangChain.
    html_splitter = HTMLHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        max_chunk_size=max_chunk_size
    )

    # Выполняем разделение
    # Метод .split_text() принимает строку с HTML
    html_header_splits = html_splitter.split_text(html_string)

    # Примечание: HTMLHeaderTextSplitter сам по себе не имеет chunk_size.
    # Для дальнейшего разделения крупных чанков можно использовать
    # RecursiveCharacterTextSplitter поверх этого результата.
    # Пример:
    # from langchain_text_splitters import RecursiveCharacterTextSplitter
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=30)
    # splits = text_splitter.split_documents(html_header_splits)
    # return splits

    return html_header_splits


def split_html_with_headers(folder_path):
    html_pages = get_file_contents_from_folder(folder_path)
    all_pages_html_documents = []

    for html_page in html_pages:
        html_documents = splitter_func(html_string=html_page)
        all_pages_html_documents += html_documents
    
    return all_pages_html_documents