#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ControlS - Windows Control Panel
Графическая версия с GUI и веб-интерфейсом
"""

import os
import sys
import subprocess
import threading
import webbrowser
import random
import time
import json
from datetime import datetime

# Try to import tkinter for GUI
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("Tkinter не установлен. Графический интерфейс недоступен.")

# Try to import flask for web version
try:
    from flask import Flask, send_from_directory, send_file, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask не установлен. Веб-интерфейс недоступен.")

# =====================
# ACTIONS DEFINITIONS
# =====================

ACTIONS = [
    {"id": 1, "title": "Открыть Paint", "category": "Программы", "cmd": "mspaint", "icon": "paint"},
    {"id": 2, "title": "Открыть Блокнот", "category": "Программы", "cmd": "notepad", "icon": "notepad"},
    {"id": 3, "title": "Выход", "category": "Система", "cmd": "exit", "icon": "exit"},
    {"id": 4, "title": "Настройки Windows", "category": "Настройки", "cmd": "start ms-settings:", "icon": "settings"},
    {"id": 5, "title": "Настройки дисплея", "category": "Настройки", "cmd": "start ms-settings:display", "icon": "monitor"},
    {"id": 6, "title": "Отключить обои", "category": "Персонализация", "cmd": "wallpaper_off", "icon": "wallpaper"},
    {"id": 7, "title": "Создать новую папку", "category": "Файлы", "cmd": "new_folder", "icon": "folder"},
    {"id": 8, "title": "Включить темную тему", "category": "Персонализация", "cmd": "dark_theme", "icon": "moon"},
    {"id": 9, "title": "Включить светлую тему", "category": "Персонализация", "cmd": "light_theme", "icon": "sun"},
    {"id": 10, "title": "Информация о системе", "category": "Система", "cmd": "systeminfo", "icon": "info"},
    {"id": 11, "title": "Пинг", "category": "Сеть", "cmd": "ping google.com -n 4", "icon": "globe"},
    {"id": 12, "title": "Панель управления", "category": "Настройки", "cmd": "control", "icon": "sliders"},
    {"id": 13, "title": "Параметры сетевых адаптеров", "category": "Сеть", "cmd": "ncpa.cpl", "icon": "network"},
    {"id": 14, "title": "Управление аккаунтами", "category": "Система", "cmd": "netplwiz", "icon": "users"},
    {"id": 15, "title": "Открыть поиск", "category": "Система", "cmd": "explorer.exe shell:::{2559a1f8-21d7-11d4-bdaf-00c04f60b9f0}", "icon": "search"},
    {"id": 16, "title": "Симуляция матрицы", "category": "Развлечения", "cmd": "matrix", "icon": "terminal"},
    {"id": 17, "title": "Стать мамкиным хацкером", "category": "Развлечения", "cmd": "hacker", "icon": "skull"},
    {"id": 18, "title": "Статус диска", "category": "Система", "cmd": "wmic diskdrive get status", "icon": "hdd"},
    {"id": 19, "title": "Сброс сетевых настроек", "category": "Сеть", "cmd": "ipconfig /release & ipconfig /renew & ipconfig /flushdns", "icon": "refresh"},
    {"id": 20, "title": "Удаление или изменение программ", "category": "Программы", "cmd": "appwiz.cpl", "icon": "trash"},
    {"id": 21, "title": "Очистить память", "category": "Система", "cmd": "clean_memory", "icon": "clean"},
    {"id": 22, "title": "Информация о системе (msinfo32)", "category": "Система", "cmd": "msinfo32", "icon": "cpu"},
    {"id": 23, "title": "Настройка мыши и тачпада", "category": "Панель управления", "cmd": "main.cpl", "icon": "mouse"},
    {"id": 24, "title": "Свойства системы", "category": "Панель управления", "cmd": "sysdm.cpl", "icon": "system"},
    {"id": 25, "title": "Электропитание", "category": "Панель управления", "cmd": "powercfg.cpl", "icon": "battery"},
    {"id": 26, "title": "Звуковые устройства", "category": "Панель управления", "cmd": "mmsys.cpl", "icon": "volume"},
    {"id": 27, "title": "Диспетчер устройств", "category": "Панель управления", "cmd": "devmgmt.msc", "icon": "wrench"},
    {"id": 28, "title": "Конфигурация системы", "category": "Панель управления", "cmd": "msconfig", "icon": "layers"},
]

CATEGORIES = ["Все", "Программы", "Настройки", "Персонализация", "Файлы", "Система", "Сеть", "Развлечения", "Панель управления"]

# PowerShell commands
PS_WALLPAPER_OFF = '''powershell -command "Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name WallPaper -Value ''; Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Wallpapers' -Name BackgroundType -Type DWORD -Value 1; Set-ItemProperty -Path 'HKCU:\\Control Panel\\Colors' -Name Background -Value '0 0 0'; Add-Type -MemberDefinition '[DllImport(\\"user32.dll\\")] public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);' -Name Win32Utils -Namespace Win32; [Win32.Win32Utils]::SystemParametersInfo(20, 0, '', 3)"'''

PS_DARK_THEME = '''powershell -command "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'SystemUsesLightTheme' -Value 0; Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'AppsUseLightTheme' -Value 0"'''

PS_LIGHT_THEME = '''powershell -command "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'SystemUsesLightTheme' -Value 1; Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'AppsUseLightTheme' -Value 1"'''

# =====================
# EXECUTE ACTION
# =====================

def execute_action(action, output_callback=None):
    """Execute a Windows action"""
    cmd = action["cmd"]

    if output_callback:
        output_callback(f"Выполняется: {action['title']}")

    try:
        if cmd == "exit":
            if output_callback:
                output_callback("Выход из приложения...")
            return "exit"

        elif cmd == "wallpaper_off":
            if os.name == 'nt':
                subprocess.run(PS_WALLPAPER_OFF, shell=True)
                if output_callback:
                    output_callback("Обои отключены, установлен черный фон")
            else:
                if output_callback:
                    output_callback("Доступно только в Windows")

        elif cmd == "new_folder":
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            new_folder = os.path.join(desktop, "New_folder")
            try:
                os.makedirs(new_folder, exist_ok=True)
                if output_callback:
                    output_callback(f"Папка создана: {new_folder}")
            except Exception as e:
                if output_callback:
                    output_callback(f"Ошибка: {e}")

        elif cmd == "dark_theme":
            if os.name == 'nt':
                subprocess.run(PS_DARK_THEME, shell=True)
                if output_callback:
                    output_callback("Темная тема включена")
            else:
                if output_callback:
                    output_callback("Доступно только в Windows")

        elif cmd == "light_theme":
            if os.name == 'nt':
                subprocess.run(PS_LIGHT_THEME, shell=True)
                if output_callback:
                    output_callback("Светлая тема включена")
            else:
                if output_callback:
                    output_callback("Доступно только в Windows")

        elif cmd == "matrix":
            return "matrix_simulation"

        elif cmd == "hacker":
            return "hacker_simulation"

        elif cmd == "clean_memory":
            if os.name == 'nt':
                if output_callback:
                    output_callback("Закрываем браузеры...")
                subprocess.run("taskkill /f /im chrome.exe /im browser.exe /im msedge.exe", shell=True, capture_output=True)

                if output_callback:
                    output_callback("Очистка системных папок Temp...")
                subprocess.run('del /f /s /q "C:\\Windows\\Temp\\*.*"', shell=True, capture_output=True)

                if output_callback:
                    output_callback("Очистка кэша профилей...")
                subprocess.run('del /f /s /q "%TEMP%\\*.*"', shell=True, capture_output=True)

                if output_callback:
                    output_callback("ОЧИСТКА УСПЕШНО ЗАВЕРШЕНА!")
            else:
                if output_callback:
                    output_callback("Доступно только в Windows")

        elif cmd in ["systeminfo", "ping google.com -n 4", "wmic diskdrive get status"]:
            if os.name == 'nt':
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if output_callback:
                    output_callback(result.stdout or result.stderr)
            else:
                if output_callback:
                    output_callback("Доступно только в Windows")

        else:
            # Generic command execution
            if os.name == 'nt':
                subprocess.run(cmd, shell=True)
                if output_callback:
                    output_callback(f"Выполнено: {action['title']}")
            else:
                if output_callback:
                    output_callback("Доступно только в Windows")

    except Exception as e:
        if output_callback:
            output_callback(f"Ошибка: {e}")

    return None


# =====================
# TKINTER GUI
# =====================

class ControlSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ControlS - Панель управления Windows")
        self.root.geometry("900x700")
        self.root.configure(bg="#0f172a")

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.setup_ui()
        self.create_menu()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#1e293b", pady=15)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="ControlS",
            font=("Arial", 24, "bold"),
            fg="#06b6d4",
            bg="#1e293b"
        )
        title_label.pack(side=tk.LEFT, padx=20)

        subtitle_label = tk.Label(
            header_frame,
            text="Панель управления системой",
            font=("Arial", 10),
            fg="#94a3b8",
            bg="#1e293b"
        )
        subtitle_label.pack(side=tk.LEFT)

        time_label = tk.Label(
            header_frame,
            text=datetime.now().strftime("%d/%m/%Y %H:%M"),
            font=("Arial", 10),
            fg="#64748b",
            bg="#1e293b"
        )
        time_label.pack(side=tk.RIGHT, padx=20)

        # Category buttons
        cat_frame = tk.Frame(self.root, bg="#0f172a", pady=10)
        cat_frame.pack(fill=tk.X)

        self.selected_category = tk.StringVar(value="Все")

        for cat in CATEGORIES:
            btn = tk.Button(
                cat_frame,
                text=cat,
                command=lambda c=cat: self.filter_category(c),
                bg="#1e293b" if cat == "Все" else "#334155",
                fg="white",
                font=("Arial", 9),
                relief=tk.FLAT,
                padx=15,
                pady=5,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=3)

        # Action buttons grid
        self.actions_frame = tk.Frame(self.root, bg="#0f172a")
        self.actions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.render_actions(ACTIONS)

        # Output area
        output_frame = tk.Frame(self.root, bg="#0f172a")
        output_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=6,
            bg="#1e293b",
            fg="#06b6d4",
            font=("Consolas", 9),
            relief=tk.FLAT
        )
        self.output_text.pack(fill=tk.X)

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Запустить веб-версию", command=self.launch_web)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menubar)

    def render_actions(self, actions):
        # Clear existing buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        # Create canvas with scrollbar for many items
        canvas = tk.Canvas(self.actions_frame, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.actions_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f172a")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Render items in grid
        col = 0
        row = 0
        for action in actions:
            btn_frame = tk.Frame(
                scrollable_frame,
                bg="#1e293b",
                padx=15,
                pady=10
            )
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

            # Category label
            cat_label = tk.Label(
                btn_frame,
                text=action["category"].upper(),
                font=("Arial", 8),
                fg="#64748b",
                bg="#1e293b"
            )
            cat_label.pack(anchor="w")

            # Title button
            btn = tk.Button(
                btn_frame,
                text=action["title"],
                font=("Arial", 10, "bold"),
                fg="white",
                bg="#334155",
                activebackground="#06b6d4",
                activeforeground="white",
                relief=tk.FLAT,
                width=20,
                height=2,
                cursor="hand2",
                command=lambda a=action: self.run_action(a)
            )
            btn.pack(fill=tk.X, pady=(5, 0))

            col += 1
            if col >= 3:
                col = 0
                row += 1

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def filter_category(self, category):
        self.selected_category.set(category)
        if category == "Все":
            filtered = ACTIONS
        else:
            filtered = [a for a in ACTIONS if a["category"] == category]
        self.render_actions(filtered)

    def log(self, message):
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)

    def run_action(self, action):
        result = execute_action(action, self.log)

        if result == "exit":
            self.root.quit()
        elif result == "matrix_simulation":
            self.show_matrix()
        elif result == "hacker_simulation":
            self.show_hacker()

    def show_matrix(self):
        matrix_win = tk.Toplevel(self.root)
        matrix_win.title("Matrix")
        matrix_win.geometry("800x600")
        matrix_win.configure(bg="black")

        canvas = tk.Canvas(matrix_win, bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789"

        def draw_matrix():
            canvas.delete("all")
            w = canvas.winfo_width()
            h = canvas.winfo_height()

            for x in range(0, w, 20):
                text = "".join(random.choice(chars) for _ in range(h // 15))
                y = random.randint(0, h)
                canvas.create_text(
                    x, y,
                    text=text,
                    fill="#00ff00",
                    font=("Consolas", 12),
                    anchor="nw"
                )

            matrix_win.after(100, draw_matrix)

        canvas.update()
        draw_matrix()

        btn = tk.Button(
            matrix_win,
            text="Закрыть",
            command=matrix_win.destroy,
            bg="#00ff00",
            fg="black",
            font=("Arial", 12)
        )
        btn.place(relx=0.5, rely=0.9, anchor="center")

    def show_hacker(self):
        hacker_win = tk.Toplevel(self.root)
        hacker_win.title("Hacker Mode")
        hacker_win.geometry("600x400")
        hacker_win.configure(bg="black")

        text = tk.Text(
            hacker_win,
            bg="black",
            fg="#ff0000",
            font=("Consolas", 12),
            relief=tk.FLAT
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        messages = [
            "[СИСТЕМА]: Подключение к удаленному серверу...",
            "[УСПЕШНО]: Обход брандмауэра пройден.",
            "[СТАТУС]: Скачивание базы данных... 12%",
            "[СТАТУС]: Скачивание базы данных... 48%",
            "[СТАТУС]: Скачивание базы данных... 89%",
            "[ГОТОВО]: Все данные успешно скопированы на ваш ПК.",
            "Шутка! Ваши файлы в безопасности. :^)",
        ]

        def show_messages(index=0):
            if index < len(messages):
                text.insert(tk.END, messages[index] + "\n")
                text.see(tk.END)
                if index == len(messages) - 1:
                    text.config(fg="#00ff00")
                    btn = tk.Button(
                        hacker_win,
                        text="Закрыть",
                        command=hacker_win.destroy,
                        bg="#00ff00",
                        fg="black",
                        font=("Arial", 10)
                    )
                    btn.pack(pady=10)
                else:
                    hacker_win.after(1200, lambda: show_messages(index + 1))

        show_messages()

    def launch_web(self):
        if FLASK_AVAILABLE:
            webbrowser.open("http://localhost:5000")
            threading.Thread(target=run_web_server, daemon=True).start()
            self.log("Веб-сервер запущен на http://localhost:5000")
        else:
            messagebox.showerror("Ошибка", "Flask не установлен. Веб-версия недоступна.")

    def show_about(self):
        messagebox.showinfo(
            "О ControlS",
            "ControlS v1.0\nПанель управления Windows\n\nГрафическая версия Batch-скрипта\nс веб-интерфейсом"
        )


# =====================
# FLASK WEB SERVER
# =====================

def create_flask_app():
    """Create Flask app with embedded HTML template"""

    app = Flask(__name__)

    # Embedded HTML template
    HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ControlS - Панель управления Windows</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes fall {
            0% { transform: translateY(-100%); opacity: 1; }
            100% { transform: translateY(100vh); opacity: 0; }
        }
        @keyframes slide-in {
            0% { transform: translateX(100%); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        .animate-fall { animation: fall linear infinite; }
        .animate-slide-in { animation: slide-in 0.3s ease-out; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
    <div id="app"></div>

    <script>
        const ACTIONS = {{ actions_json }};

        const CATEGORIES = ["Все", "Программы", "Настройки", "Персонализация", "Файлы", "Система", "Сеть", "Развлечения", "Панель управления"];

        let selectedCategory = "Все";
        let notification = null;
        let matrixMode = false;
        let hackerMode = false;

        function App() {
            const filtered = selectedCategory === "Все"
                ? ACTIONS
                : ACTIONS.filter(a => a.category === selectedCategory);

            return `
                ${notification ? `
                    <div class="fixed top-4 right-4 z-50 animate-slide-in">
                        <div class="flex items-center gap-3 px-6 py-4 rounded-xl shadow-2xl backdrop-blur-sm ${
                            notification.type === 'success' ? 'bg-emerald-500/90' :
                            notification.type === 'warning' ? 'bg-amber-500/90' : 'bg-blue-500/90'
                        }">
                            <span class="font-medium">${notification.message}</span>
                            <button onclick="closeNotification()" class="ml-2 hover:opacity-70">✕</button>
                        </div>
                    </div>
                ` : ''}

                ${matrixMode ? `<div class="fixed inset-0 z-50 bg-black overflow-hidden">${MatrixRain()}</div>` : ''}

                ${hackerMode ? `<div class="fixed inset-0 z-50 bg-black flex items-center justify-center">${HackerSimulation()}</div>` : ''}

                <header class="border-b border-slate-700/50 bg-slate-900/80 backdrop-blur-xl sticky top-0 z-40">
                    <div class="max-w-7xl mx-auto px-6 py-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/30">
                                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h1 class="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">ControlS</h1>
                                    <p class="text-xs text-slate-400">Панель управления Windows</p>
                                </div>
                            </div>
                            <div class="text-sm text-slate-400">${new Date().toLocaleString('ru-RU')}</div>
                        </div>
                    </div>
                </header>

                <main class="max-w-7xl mx-auto px-6 py-8">
                    <div class="flex flex-wrap gap-2 mb-8">
                        ${CATEGORIES.map(cat => `
                            <button
                                onclick="selectCategory('${cat}')"
                                class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                                    selectedCategory === cat
                                        ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30'
                                        : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 border border-slate-700/50'
                                }"
                            >
                                ${cat}
                            </button>
                        `).join('')}
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                        ${filtered.map(item => `
                            <button
                                onclick="executeAction(${item.id})"
                                class="group relative p-5 rounded-2xl border transition-all duration-300 hover:scale-[1.02] hover:shadow-xl text-left bg-gradient-to-br from-slate-800/50 to-slate-900/50 border-slate-700/50 hover:border-cyan-500/50 hover:shadow-cyan-900/30"
                            >
                                <div class="flex items-start gap-4">
                                    <div class="w-12 h-12 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 text-cyan-400">
                                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                        </svg>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <span class="text-xs font-medium text-slate-500 uppercase tracking-wider">${item.category}</span>
                                        <h3 class="font-semibold text-white mt-1 group-hover:text-cyan-400 transition-colors">${item.title}</h3>
                                    </div>
                                </div>
                                <div class="mt-3 pt-3 border-t border-slate-700/30">
                                    <p class="text-sm text-slate-400">${item.cmd}</p>
                                </div>
                            </button>
                        `).join('')}
                    </div>
                </main>

                <footer class="border-t border-slate-700/50 bg-slate-900/50 mt-16">
                    <div class="max-w-7xl mx-auto px-6 py-4">
                        <p class="text-center text-sm text-slate-500">ControlS - Панель управления системой (Веб-версия)</p>
                    </div>
                </footer>
            `;
        }

        function MatrixRain() {
            const chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789';
            let columns = '';
            for (let i = 0; i < 50; i++) {
                let column = '';
                for (let j = 0; j < 20; j++) {
                    column += chars[Math.floor(Math.random() * chars.length)];
                }
                columns += `<div class="absolute text-green-500 font-mono animate-fall" style="left: ${i * 2}%; animation-delay: ${Math.random() * 2}s; animation-duration: ${2 + Math.random() * 3}s;">${column.split('').map((c, j) => `<div style="opacity: ${1 - j * 0.05}">${c}</div>`).join('')}</div>`;
            }
            return columns + `<div class="absolute inset-0 flex items-center justify-center"><button onclick="closeMatrix()" class="px-6 py-3 bg-green-500/20 border border-green-500 text-green-400 rounded-lg hover:bg-green-500/30 transition-colors">Закрыть</button></div>`;
        }

        function HackerSimulation() {
            return `
                <div class="max-w-xl w-full mx-4 bg-slate-900/80 rounded-xl border border-slate-700 p-6 font-mono text-sm">
                    <p class="text-red-400 mb-2">[СИСТЕМА]: Подключение к удаленному серверу...</p>
                    <p class="text-red-400 mb-2">[УСПЕШНО]: Обход брандмауэра пройден.</p>
                    <p class="text-red-400 mb-2">[СТАТУС]: Скачивание базы данных... 100%</p>
                    <p class="text-green-400 mb-2">[ГОТОВО]: Все данные скопированы.</p>
                    <p class="text-green-400">Шутка! Ваши файлы в безопасности. :^)</p>
                </div>
                <button onclick="closeHacker()" class="mt-4 px-6 py-3 bg-green-500/20 border border-green-500 text-green-400 rounded-lg hover:bg-green-500/30 transition-colors">Закрыть</button>
            `;
        }

        function render() {
            document.getElementById('app').innerHTML = App();
        }

        function selectCategory(cat) {
            selectedCategory = cat;
            render();
        }

        function closeNotification() {
            notification = null;
            render();
        }

        function closeMatrix() {
            matrixMode = false;
            render();
        }

        function closeHacker() {
            hackerMode = false;
            render();
        }

        async function executeAction(id) {
            const action = ACTIONS.find(a => a.id === id);

            if (action.cmd === 'matrix') {
                matrixMode = true;
                render();
                return;
            }

            if (action.cmd === 'hacker') {
                hackerMode = true;
                render();
                return;
            }

            if (action.cmd === 'exit') {
                notification = { show: true, message: 'Выход (демо)', type: 'warning' };
                render();
                setTimeout(() => { notification = null; render(); }, 3000);
                return;
            }

            // Send to server
            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id: id})
                });
                const result = await response.json();
                notification = { show: true, message: result.message, type: result.success ? 'success' : 'warning' };
            } catch (e) {
                notification = { show: true, message: action.title + ' - отправлено', type: 'success' };
            }

            render();
            setTimeout(() => { notification = null; render(); }, 3000);
        }

        render();
    </script>
</body>
</html>'''

    @app.route('/')
    def index():
        actions_json = json.dumps(ACTIONS, ensure_ascii=False)
        html = HTML_TEMPLATE.replace('{{ actions_json }}', actions_json)
        return html

    @app.route('/execute', methods=['POST'])
    def execute():
        data = request.get_json()
        action_id = data.get('id')
        action = next((a for a in ACTIONS if a['id'] == action_id), None)

        if not action:
            return {'success': False, 'message': 'Действие не найдено'}

        result_stream = []

        def log(msg):
            result_stream.append(msg)

        execute_action(action, log)

        return {
            'success': True,
            'message': '\n'.join(result_stream) or f'{action["title"]} - выполнено'
        }

    return app


def run_web_server():
    """Run Flask web server"""
    if not FLASK_AVAILABLE:
        print("Flask не установлен. Установите: pip install flask")
        return

    app = create_flask_app()
    print("\n" + "=" * 50)
    print("ControlS Web Server")
    print("=" * 50)
    print("Откройте в браузере: http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False)


# =====================
# MAIN ENTRY POINT
# =====================

def main():
    print("""
    ╔═══════════════════════════════════════╗
    ║        ControlS - Запуск системы      ║
    ╠═══════════════════════════════════════╣
    ║  1. Графический интерфейс (GUI)        ║
    ║  2. Веб-интерфейс                      ║
    ║  3. Оба режима                         ║
    ╚═══════════════════════════════════════╝
    """)

    choice = input("Выберите режим (1/2/3): ").strip()

    if choice == '1':
        # GUI only
        if TKINTER_AVAILABLE:
            root = tk.Tk()
            app = ControlSApp(root)
            root.mainloop()
        else:
            print("Tkinter недоступен. Запускаю веб-версию...")
            run_web_server()

    elif choice == '2':
        # Web only
        webbrowser.open("http://localhost:5000")
        run_web_server()

    elif choice == '3':
        # Both
        if TKINTER_AVAILABLE and FLASK_AVAILABLE:
            # Start web server in background
            threading.Thread(target=run_web_server, daemon=True).start()

            # Start GUI
            root = tk.Tk()
            app = ControlSApp(root)
            root.mainloop()
        elif TKINTER_AVAILABLE:
            print("Flask недоступен. Запускаю только GUI...")
            root = tk.Tk()
            app = ControlSApp(root)
            root.mainloop()
        elif FLASK_AVAILABLE:
            print("Tkinter недоступен. Запускаю только веб...")
            webbrowser.open("http://localhost:5000")
            run_web_server()
        else:
            print("Ни Tkinter, ни Flask не установлены!")
            print("Установите: pip install flask")
            sys.exit(1)
    else:
        print("Неверный выбор. Запускаю GUI по умолчанию...")
        if TKINTER_AVAILABLE:
            root = tk.Tk()
            app = ControlSApp(root)
            root.mainloop()


if __name__ == '__main__':
    # Check if running as web-only via command line
    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        webbrowser.open("http://localhost:5000")
        run_web_server()
    elif len(sys.argv) > 1 and sys.argv[1] == '--gui':
        if TKINTER_AVAILABLE:
            root = tk.Tk()
            app = ControlSApp(root)
            root.mainloop()
        else:
            print("Tkinter не установлен!")
            sys.exit(1)
    else:
        main()
