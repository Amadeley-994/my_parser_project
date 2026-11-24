import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import subprocess
import os
import sys
import urllib.request
from PIL import Image, ImageTk

# 👁️ Палитра "Men in Black / Epsilon"
BG_COLOR = "#000000"
PANEL_COLOR = "#0A0A0A"
EPSILON_RED = "#FF0000"
TEXT_MAIN = "#FFFFFF"
TEXT_DIM = "#888888"
INPUT_BG = "#222222" 

FONT_TITLE = ("Impact", 22) 
FONT_SUBTITLE = ("Courier New", 11, "bold")
FONT_BTN = ("Arial", 10, "bold") 
FONT_TEXT = ("Consolas", 10)

def paste_url():
    try:
        url_entry.delete(0, tk.END)
        url_entry.insert(0, root.clipboard_get())
    except tk.TclError:
        messagebox.showwarning("ОШИБКА", "БУФЕР ОБМЕНА ПУСТ!")

def run_parser():
    target_url = url_entry.get().strip()
    search_query = search_entry.get().strip()
    
    if not target_url:
        messagebox.showwarning("ВНИМАНИЕ", "ВВЕДИТЕ ССЫЛКУ НА САЙТ!")
        return

    parser_path = os.path.join(os.path.dirname(__file__), "..", "parser", "parser.py")
    subprocess.run([sys.executable, parser_path, target_url, search_query])
    messagebox.showinfo("MIB // ЭПСИЛОН", "ПРОТОКОЛ ВЫПОЛНЕН.\nДАННЫЕ ИЗВЛЕЧЕНЫ.")

def show_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.csv")
    try:
        with open(data_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
    except FileNotFoundError:
        messagebox.showerror("ОШИБКА", "ФАЙЛ НЕ НАЙДЕН.\nДОСТУП ЗАПРЕЩЕН.")
        return

    win = tk.Toplevel(root)
    win.title("MIB // АРХИВ ЭПСИЛОН")
    win.geometry("800x500") 
    win.configure(bg=BG_COLOR)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=BG_COLOR, foreground=TEXT_MAIN, fieldbackground=BG_COLOR, font=FONT_TEXT, rowheight=30, borderwidth=1, bordercolor=EPSILON_RED)
    style.configure("Treeview.Heading", background=PANEL_COLOR, foreground=EPSILON_RED, font=("Arial", 10, "bold"), relief="flat")
    
    tree = ttk.Treeview(win, columns=rows[0], show="headings")
    style.map("Treeview", background=[('selected', EPSILON_RED)], foreground=[('selected', BG_COLOR)])

    for col in rows[0]:
        tree.heading(col, text=col.upper())
        tree.column(col, anchor="w", width=750)

    for row in rows[1:]:
        tree.insert("", tk.END, values=row)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar.pack(side="right", fill="y", pady=15)

def on_enter(e):
    e.widget['background'] = EPSILON_RED
    e.widget['fg'] = "#000000"
def on_leave(e):
    e.widget['background'] = BG_COLOR
    e.widget['fg'] = TEXT_MAIN

# --- Главное окно ---
root = tk.Tk()
root.title("Epsilon Program // MIB Терминал")
root.geometry("500x520") # Увеличили высоту для нового поля
root.configure(bg=BG_COLOR)
root.resizable(False, False) 

tk.Frame(root, bg=EPSILON_RED, height=4).pack(fill="x", side="top")

# 🖼️ ЗАГРУЗКА КАРТИНКИ
image_frame = tk.Frame(root, bg=BG_COLOR)
image_frame.pack(pady=(10, 5))

url_img = "https://avatars.mds.yandex.net/i?id=a91b31ac53ff2f178f418c232e4219b8_l-10241101-images-thumbs&n=13"
try:
    req = urllib.request.Request(url_img, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        img_data = response.read()
    temp_img_path = os.path.join(os.path.dirname(__file__), "temp_logo.png")
    with open(temp_img_path, "wb") as f:
        f.write(img_data)
    img = Image.open(temp_img_path)
    img = img.resize((60, 60), Image.Resampling.LANCZOS) 
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(image_frame, image=photo, bg=BG_COLOR)
    img_label.image = photo
    img_label.pack()
except Exception as e:
    tk.Label(image_frame, text="▲", font=("Courier New", 50, "bold"), bg=BG_COLOR, fg=EPSILON_RED).pack()

title_label = tk.Label(root, text="ЭПСИЛОН", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_MAIN)
title_label.pack(pady=(0, 0))

subtitle_label = tk.Label(root, text="MIB // СБОР ДАННЫХ", font=FONT_SUBTITLE, bg=BG_COLOR, fg=EPSILON_RED)
subtitle_label.pack(pady=(0, 10))

url_frame = tk.Frame(root, bg=BG_COLOR)
url_frame.pack(pady=0)

# Ссылка
tk.Label(url_frame, text="ВВЕДИТЕ URL САЙТА:", font=("Arial", 9, "bold"), bg=BG_COLOR, fg=TEXT_MAIN).pack()
url_entry = tk.Entry(url_frame, font=("Arial", 10), bg=INPUT_BG, fg="#00FF00", insertbackground="white", width=35, bd=2, relief="solid")
url_entry.pack(pady=2)
url_entry.insert(0, "https://ru.wikipedia.org/wiki/Питон") 

# Слово для поиска
tk.Label(url_frame, text="ЧТО ИСКАТЬ (необязательно):", font=("Arial", 9, "bold"), bg=BG_COLOR, fg=TEXT_MAIN).pack(pady=(8, 0))
search_entry = tk.Entry(url_frame, font=("Arial", 10), bg=INPUT_BG, fg="#00FF00", insertbackground="white", width=35, bd=2, relief="solid")
search_entry.pack(pady=2)
search_entry.insert(0, "язык") # Пример

btn_paste = tk.Button(url_frame, text="📋 ВСТАВИТЬ URL ИЗ БУФЕРА", font=("Arial", 8, "bold"), 
                      bg=PANEL_COLOR, fg=TEXT_DIM, 
                      activebackground=EPSILON_RED, activeforeground="#000000",
                      bd=1, relief="solid", cursor="hand2", command=paste_url)
btn_paste.pack(pady=8)

btn_parse = tk.Button(root, text="[ СКАНИРОВАТЬ САЙТ ]", font=FONT_BTN, 
                      bg=BG_COLOR, fg=TEXT_MAIN, 
                      activebackground=EPSILON_RED, activeforeground="#000000",
                      bd=2, relief="solid", cursor="hand2", width=30, height=1, command=run_parser) 
btn_parse.pack(pady=8) 
btn_parse.bind("<Enter>", on_enter)
btn_parse.bind("<Leave>", on_leave)

btn_show = tk.Button(root, text="[ ДОСТУП К АРХИВУ ]", font=FONT_BTN, 
                     bg=BG_COLOR, fg=TEXT_MAIN, 
                     activebackground=EPSILON_RED, activeforeground="#000000",
                     bd=2, relief="solid", cursor="hand2", width=30, height=1, command=show_data)
btn_show.pack(pady=2)
btn_show.bind("<Enter>", on_enter)
btn_show.bind("<Leave>", on_leave)

tk.Frame(root, bg=EPSILON_RED, height=1).pack(side="bottom", fill="x", pady=(10, 0))

footer_label = tk.Label(root, text="STATUS: ONLINE // AGENT: Amadeley // EYES ONLY", font=("Courier New", 8), bg=BG_COLOR, fg=TEXT_DIM)
footer_label.pack(side="bottom", pady=5)

root.mainloop()