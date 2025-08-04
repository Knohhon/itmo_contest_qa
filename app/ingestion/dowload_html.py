# scrapers.py
import time
from playwright.sync_api import sync_playwright, Page, Error
from bs4 import BeautifulSoup

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


#import time
#from playwright.sync_api import sync_playwright
#from bs4 import BeautifulSoup
#
#def get_full_page_html(url: str) -> str:
#    """
#    Запускает Playwright, переходит по URL, дожидается полной загрузки
#    и возвращает HTML-код страницы.
#    """
#    with sync_playwright() as p:
#
#
#        browser = p.chromium.launch(headless=True)
#        page = browser.new_page()
#
#        try:
#            
#            print(f"Перехожу на страницу: {url}")
#            page.goto(url, timeout=60000, wait_until="load")
#
#
#            print("Прокручиваю страницу для подгрузки всего контента...")
#            for _ in range(5):  
#                page.keyboard.press("End")
#                time.sleep(1) 
#
#            print("Получаю финальный HTML...")
#            html_content = page.content()
#            
#
#            return html_content
#
#        except Exception as e:
#            print(f"Произошла ошибка: {e}")
#            return ""
#        finally:
#
#            browser.close()

def save_to_html():
    target_url = "https://abit.itmo.ru/program/master/ai"
    
    full_html = get_full_page_html(target_url)

    soup = BeautifulSoup(full_html, 'html.parser')

    print(soup.prettify())

    if full_html:

        with open("./data/ai_page_content.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("Полный HTML страницы сохранен в файл ./data/ai_page_content.html")