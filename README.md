# Информационная система сбора данных

## Что делает
Программа собирает данные с сайта, сохраняет их в файл `data/data.csv`
и показывает в графическом интерфейсе.

## Состав проекта
- `parser/parser.py` — парсер (собирает данные с сайта)
- `data/data.csv` — база данных (файл с данными)
- `interface/interface.py` — интерфейс (окно с кнопками)

## Как запустить
1. Установить Python.
2. Установить библиотеки:
   pip install requests
   pip install beautifulsoup4
3. Запустить парсер:
   python parser/parser.py
4. Запустить интерфейс:
   python interface/interface.py

## Автор
Amadeley
