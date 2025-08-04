import pytest
from langchain.docstore.document import Document
from app.processing.splitter import split_html_with_headers

@pytest.fixture
def sample_html_data():
    """
    Фикстура Pytest, предоставляющая тестовые HTML-данные.
    Это позволяет переиспользовать одни и те же данные в разных тестах.
    """
    return """
    <html>
    <body>
        <p>Текст до первого заголовка.</p>
        <h1>Главный заголовок</h1>
        <p>Это вводный параграф под H1.</p>
        <h2>Раздел 1: Введение</h2>
        <p>Текст первого раздела.</p>
        <h3>Подраздел 1.1: Детали</h3>
        <p>Этот подраздел предоставляет дополнительные сведения.</p>
        <h2>Раздел 2: Заключение</h2>
        <p>Текст второго раздела.</p>
    </body>
    </html>
    """

def test_split_basic_functionality(sample_html_data):
    """
    Тест: Проверяет базовое разделение и корректное количество чанков.
    """
    chunks = split_html_with_headers(sample_html_data)

    # Ожидаем 5 чанков: (1) до H1, (2) H1, (3) H2, (4) H3, (5) второй H2
    assert len(chunks) == 5
    # Проверяем, что все элементы в списке - это объекты Document
    assert all(isinstance(chunk, Document) for chunk in chunks)

def test_metadata_correctness(sample_html_data):
    """
    Тест: Проверяет правильность формирования метаданных для каждого чанка.
    Это самый важный тест, т.к. он проверяет основную логику сплиттера.
    """
    chunks = split_html_with_headers(sample_html_data)

    # Чанк 1: Текст до первого заголовка, без метаданных
    assert chunks[0].metadata == {}
    assert chunks[0].page_content == "Текст до первого заголовка."

    # Чанк 2: Контент под H1
    assert chunks[1].metadata == {"Header 1": "Главный заголовок"}
    assert chunks[1].page_content == "Это вводный параграф под H1."

    # Чанк 3: Контент под H2 (внутри H1)
    assert chunks[2].metadata == {
        "Header 1": "Главный заголовок",
        "Header 2": "Раздел 1: Введение"
    }
    assert chunks[2].page_content == "Текст первого раздела."

    # Чанк 4: Контент под H3 (внутри H2 и H1)
    assert chunks[3].metadata == {
        "Header 1": "Главный заголовок",
        "Header 2": "Раздел 1: Введение",
        "Header 3": "Подраздел 1.1: Детали"
    }

    # Чанк 5: Контент под вторым H2. Метаданные H3 должны исчезнуть.
    assert chunks[4].metadata == {
        "Header 1": "Главный заголовок",
        "Header 2": "Раздел 2: Заключение"
    }

def test_edge_cases():
    """
    Тест: Проверяет поведение функции на граничных случаях.
    """
    # Случай 1: Пустая строка на входе
    assert split_html_with_headers("") == []

    # Случай 2: HTML без заголовков из списка
    html_no_headers = "<p>Просто текст.</p><div>И еще текст.</div>"
    chunks = split_html_with_headers(html_no_headers)
    assert len(chunks) == 1
    assert chunks[0].page_content == "Просто текст. И еще текст."
    assert chunks[0].metadata == {}

def test_custom_headers_parameter(sample_html_data):
    """
    Тест: Проверяет работу с кастомным списком заголовков для разделения.
    """
    # Разделяем только по H1 и даем ему другое имя в метаданных
    custom_headers = [("h1", "Title")]
    chunks = split_html_with_headers(sample_html_data, headers_to_split_on=custom_headers)

    # Ожидаем 2 чанка: (1) до H1, (2) весь контент после H1 (т.к. H2, H3 игнорируются)
    assert len(chunks) == 2
    assert chunks[0].metadata == {}
    assert chunks[1].metadata == {"Title": "Главный заголовок"}
    # Проверим, что контент H2 и H3 теперь внутри чанка H1
    assert "Раздел 1: Введение" in chunks[1].page_content
    assert "Подраздел 1.1: Детали" in chunks[1].page_content