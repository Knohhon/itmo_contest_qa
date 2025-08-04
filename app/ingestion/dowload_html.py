# scrapers.py
import time
from playwright.sync_api import sync_playwright, Page, Error
from bs4 import BeautifulSoup
from os import getenv
import os
from dotenv import load_dotenv

load_dotenv()

def get_page_content_with_scroll(page: Page, url: str) -> str:
    """
    Переходит по URL на уже существующей странице, прокручивает ее
    и возвращает HTML-код.
    """
    print(f"Перехожу на страницу: {url}")

    page.goto(url, timeout=30000, wait_until="domcontentloaded")

    print("Прокручиваю страницу для подгрузки всего контента...")
    for _ in range(5):
        page.keyboard.press("End")

        page.wait_for_timeout(500)

    print("Получаю финальный HTML...")
    return page.content()


def get_full_page_html(url: str) -> str:
    """
    Полный цикл: запускает Playwright, вызывает логику получения страницы
    и возвращает HTML-код.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        html_content = ""
        try:
            html_content = get_page_content_with_scroll(page, url)
        except Error as e:
            # Playwright выбрасывает свои типизированные ошибки
            print(f"Произошла ошибка Playwright: {e}")
            # Возвращаем пустую строку, как и в оригинале
            return ""
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            return ""
        finally:
            browser.close()
    return html_content


def save_to_html():
    target_url = getenv('PAGES_URLS')

    for url in target_url:
    
        full_html = get_full_page_html(url)

        if full_html:

            with open(f"./app/data/{url}.html", "w", encoding="utf-8") as f:
                f.write(full_html)
            print("Полный HTML страницы сохранен в файл ./data/ai_page_content.html")