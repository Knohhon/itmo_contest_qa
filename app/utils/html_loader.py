import os
from pathlib import Path
from typing import List

def get_file_contents_from_folder(folder_path: str) -> List[str]:
    """
    Считывает содержимое файлов из указанной папки в список строк.

    Args:
        folder_path: Строка с путем к папке.

    Returns:
        Список, где каждый элемент - это текстовое содержимое одного файла.
        
    Raises:
        FileNotFoundError: Если указанный путь не существует или не является папкой.
    """
    # Преобразуем строковый путь в объект Path для удобной работы
    path = Path(folder_path)

    # Проверяем, существует ли путь и является ли он папкой
    if not path.is_dir():
        raise FileNotFoundError(f"Путь '{folder_path}' не существует или не является папкой.")

    file_contents = []
    # Итерируемся по всем элементам в директории
    for entry in path.iterdir():
        # Убеждаемся, что это файл, а не поддиректория
        if entry.is_file():
            try:
                # Читаем содержимое файла с явным указанием кодировки UTF-8
                # и добавляем его в список
                content = entry.read_text(encoding='utf-8')
                file_contents.append(content)
            except (IOError, UnicodeDecodeError) as e:
                # Обрабатываем возможные ошибки чтения или декодирования
                # (например, для бинарных файлов или файлов с другой кодировкой)
                print(f"Предупреждение: Не удалось прочитать файл '{entry.name}': {e}")
                
    return file_contents