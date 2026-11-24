import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
import time

# Получаем URL и поисковый запрос
if len(sys.argv) > 2:
    URL = sys.argv[1]
    SEARCH_QUERY = sys.argv[2]
elif len(sys.argv) > 1:
    URL = sys.argv[1]
    SEARCH_QUERY = ""
else:
    URL = "https://example.com"
    SEARCH_QUERY = ""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
data_list = []

# --- ШАГ 1: Пробуем легкий и быстрый способ ---
try:
    response = requests.get(URL, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    if "turn on JavaScript" in response.text or "enable JavaScript" in response.text:
        use_selenium = True
    else:
        # Собираем все заголовки, параграфы и ссылки
        for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'a']):
            text = tag.text.strip()
            if text and len(text) < 150: # Берем только короткие осмысленные куски
                data_list.append(text)
        use_selenium = False if len(data_list) > 3 else True

except Exception:
    use_selenium = True

# --- ШАГ 2: Если сайт сложный, включаем Selenium ---
if use_selenium:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        print("Запуск невидимого браузера...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(URL)
        time.sleep(3)
        
        page_text = driver.find_element("tag name", "body").text
        driver.quit()
        
        data_list = [line.strip() for line in page_text.split("\n") if line.strip()]
        
    except Exception as e:
        data_list.append(f"Ошибка Selenium: {e}")

# --- ШАГ 3: Фильтрация и сохранение ---
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.csv")

with open(data_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Найденные данные"])
    
    if SEARCH_QUERY:
        writer.writerow([f"--- РЕЗУЛЬТАТЫ ПОИСКА: {SEARCH_QUERY} ---"])
        found = False
        for item in data_list:
            # Ищем без учета регистра (например, "питон" и "Питон")
            if SEARCH_QUERY.lower() in item.lower():
                writer.writerow([item])
                found = True
        
        if not found:
            writer.writerow([f"Слово '{SEARCH_QUERY}' не найдено на этой странице."])
    else:
        if data_list:
            for item in data_list:
                writer.writerow([item])
        else:
            writer.writerow(["[СИСТЕМА] Не удалось собрать данные."])

print("Готово! Данные сохранены.")