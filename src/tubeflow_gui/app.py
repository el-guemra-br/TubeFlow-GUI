"""
YouTube Downloader GUI Application

This application allows users to download YouTube videos and playlists using yt-dlp.

Features include:
- Single video or playlist download
- Real-time progress bar
- Customizable format (MP4, WebM) and quality (Best, 720p, 1080p)
- Dark/Light theme toggle

- It allows you to change the source code as you wish as long as you mention the developer or the owner of the program.

Developed by el-guemra-br

"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import subprocess
import sys
import os
import threading
import webbrowser


# Function to install yt-dlp if not present
def install_yt_dlp():
    try:
        import yt_dlp
    except ImportError:
        messagebox.showinfo("Installing yt-dlp", "yt-dlp is not installed. Installing now...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yt-dlp'])
            messagebox.showinfo("Success", "yt-dlp installed successfully.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to install yt-dlp. Please install it manually using 'pip install yt-dlp'")
            sys.exit(1)
            
import yt_dlp

THEMES = {
    'Light': {
        'bg': '#f4f6f8',
        'surface': '#ffffff',
        'text': '#1f2937',
        'muted': '#5b6470',
        'accent': '#1264a3',
        'accent_active': '#0e4f81',
        'console_bg': '#ffffff',
        'console_fg': '#1f2937',
        'entry_bg': '#ffffff',
    },
    'Dark': {
        'bg': '#161a1d',
        'surface': '#20262b',
        'text': '#e6edf3',
        'muted': '#9eaab6',
        'accent': '#3a86ff',
        'accent_active': '#2f6fce',
        'console_bg': '#0f1419',
        'console_fg': '#dbe4ee',
        'entry_bg': '#2b333b',
    },
}


def configure_styles(style, theme_type):
    colors = THEMES[theme_type]
    style.theme_use('clam')
    style.configure('App.TFrame', background=colors['bg'])
    style.configure('Card.TLabelframe', background=colors['surface'], borderwidth=1)
    style.configure('Card.TLabelframe.Label', background=colors['surface'], foreground=colors['text'])
    style.configure('App.TLabel', background=colors['bg'], foreground=colors['text'])
    style.configure('Card.TLabel', background=colors['surface'], foreground=colors['text'])
    style.configure('Muted.TLabel', background=colors['bg'], foreground=colors['muted'])
    style.configure('App.TButton', padding=6)
    style.configure('Accent.TButton', background=colors['accent'], foreground='white', padding=7)
    style.map('Accent.TButton', background=[('active', colors['accent_active'])])
    style.configure('App.TCheckbutton', background=colors['surface'], foreground=colors['text'])
    style.configure('App.TCombobox', fieldbackground=colors['entry_bg'])
    style.configure('App.Horizontal.TProgressbar', troughcolor=colors['entry_bg'], background=colors['accent'])
    return colors


def apply_theme(root, style, theme_var, console_text, theme_type):
    theme_var.set(theme_type)
    colors = configure_styles(style, theme_type)
    root.configure(bg=colors['bg'])
    console_text.configure(
        background=colors['console_bg'],
        foreground=colors['console_fg'],
        insertbackground=colors['console_fg'],
    )

# Function to handle download
def do_download(url, folder, is_playlist, progress_bar, download_button, folder_button, url_entry, playlist_check, format_var, quality_var):
    try:
        # Disable buttons during download
        download_button.config(state='disabled')
        folder_button.config(state='disabled')
        url_entry.config(state='disabled')
        playlist_check.config(state='disabled')

        # Reset progress bar
        progress_bar['value'] = 0

        format_choice = format_var.get()
        quality_choice = quality_var.get()

        if quality_choice == 'Best':
            format_str = 'bestvideo+bestaudio/best'
        elif quality_choice == '720p':
            format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality_choice == '1080p':
            format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'

        merge_format = 'mp4' if format_choice == 'MP4' else 'webm'

        ydl_opts = {
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'format': format_str,
            'merge_output_format': merge_format,
            'progress_hooks': [lambda d: update_progress(d, progress_bar)],
        }
        if not is_playlist:
            ydl_opts['noplaylist'] = True

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Download completed successfully!")
    except yt_dlp.utils.DownloadError as e:
        if "javascript" in str(e).lower():
            messagebox.showerror("Error", "JavaScript runtime required. Please install Node.js from https://nodejs.org/")
        else:
            messagebox.showerror("Download Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        # Re-enable buttons
        download_button.config(state='normal')
        folder_button.config(state='normal')
        url_entry.config(state='normal')
        playlist_check.config(state='normal')

# update_progress
def update_progress(d, progress_bar):
    if d['status'] == 'downloading':
        if 'total_bytes' in d and d['total_bytes'] is not None:
            progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
            progress_bar['value'] = progress
    elif d['status'] == 'finished':
        progress_bar['value'] = 100

# Function to select folder
def select_folder(folder_var):
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

# Function to open settings window
def open_settings(root, style, theme_var, console_text):
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("380x260")
    settings_win.resizable(False, False)
    settings_win.configure(bg=THEMES[theme_var.get()]['bg'])

    container = ttk.Frame(settings_win, style='App.TFrame', padding=16)
    container.pack(fill=tk.BOTH, expand=True)

    ttk.Label(container, text="Appearance", style='App.TLabel', font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 8))
    theme_radio = tk.StringVar(value=theme_var.get())
    ttk.Radiobutton(
        container,
        text="Light",
        variable=theme_radio,
        value='Light',
        command=lambda: apply_theme(root, style, theme_var, console_text, 'Light'),
    ).pack(anchor=tk.W)
    ttk.Radiobutton(
        container,
        text="Dark",
        variable=theme_radio,
        value='Dark',
        command=lambda: apply_theme(root, style, theme_var, console_text, 'Dark'),
    ).pack(anchor=tk.W, pady=(4, 12))

    ttk.Label(container, text="Console Preview", style='App.TLabel').pack(anchor=tk.W, pady=(2, 5))
    console_area = scrolledtext.ScrolledText(settings_win, width=46, height=7)
    console_area.pack(padx=16, pady=(0, 12), fill=tk.BOTH, expand=True)
    console_area.configure(state='normal')
    console_area.insert(tk.END, console_text.get(1.0, tk.END))
    apply_theme(settings_win, style, tk.StringVar(value=theme_var.get()), console_area, theme_var.get())
    console_area.configure(state='disabled')

# Function to start download
def start_download(url_var, folder_var, playlist_var, progress_bar, download_button, folder_button, url_entry, playlist_check, format_var, quality_var):
    url = url_var.get().strip()
    folder = folder_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    if not folder:
        messagebox.showerror("Error", "Please select a download folder.")
        return
    threading.Thread(
        target=do_download,
        args=(
            url,
            folder,
            playlist_var.get(),
            progress_bar,
            download_button,
            folder_button,
            url_entry,
            playlist_check,
            format_var,
            quality_var,
        ),
        daemon=True,
    ).start()

# Main GUI setup
def main():
    install_yt_dlp()

    root = tk.Tk()
    root.title("TubeFlow GUI")
    root.geometry("760x620")
    root.minsize(680, 560)

    style = ttk.Style(root)
    theme_var = tk.StringVar(value='Light')

    app = ttk.Frame(root, style='App.TFrame', padding=14)
    app.pack(fill=tk.BOTH, expand=True)

    header = ttk.Frame(app, style='App.TFrame')
    header.pack(fill=tk.X, pady=(0, 10))
    ttk.Label(header, text="TubeFlow GUI", style='App.TLabel', font=('Segoe UI', 16, 'bold')).pack(side=tk.LEFT)
    ttk.Label(header, text="Download YouTube videos with yt-dlp", style='Muted.TLabel').pack(side=tk.LEFT, padx=(10, 0))
    settings_button = ttk.Button(
        header,
        text="Settings",
        style='App.TButton',
        command=lambda: open_settings(root, style, theme_var, console_text),
    )
    settings_button.pack(side=tk.RIGHT)

    form_card = ttk.LabelFrame(app, text='Download Options', style='Card.TLabelframe', padding=14)
    form_card.pack(fill=tk.X, pady=(0, 10))
    form_card.columnconfigure(1, weight=1)

    ttk.Label(form_card, text="YouTube URL", style='Card.TLabel').grid(row=0, column=0, sticky='w', padx=(0, 8), pady=4)
    url_var = tk.StringVar()
    url_entry = ttk.Entry(form_card, textvariable=url_var)
    url_entry.grid(row=0, column=1, sticky='ew', pady=4)

    playlist_var = tk.BooleanVar()
    playlist_check = ttk.Checkbutton(form_card, text="Download as playlist", variable=playlist_var, style='App.TCheckbutton')
    playlist_check.grid(row=1, column=1, sticky='w', pady=4)

    ttk.Label(form_card, text="Download Folder", style='Card.TLabel').grid(row=2, column=0, sticky='w', padx=(0, 8), pady=4)
    folder_var = tk.StringVar(value=os.path.join(os.path.expanduser('~'), 'Downloads'))
    folder_frame = ttk.Frame(form_card, style='Card.TLabelframe')
    folder_frame.grid(row=2, column=1, sticky='ew', pady=4)
    folder_frame.columnconfigure(0, weight=1)
    folder_entry = ttk.Entry(folder_frame, textvariable=folder_var)
    folder_entry.grid(row=0, column=0, sticky='ew', padx=(0, 8))
    folder_button = ttk.Button(folder_frame, text="Browse", style='App.TButton', command=lambda: select_folder(folder_var))
    folder_button.grid(row=0, column=1)

    ttk.Label(form_card, text="Format", style='Card.TLabel').grid(row=3, column=0, sticky='w', padx=(0, 8), pady=4)
    format_var = tk.StringVar(value='MP4')
    format_combo = ttk.Combobox(form_card, textvariable=format_var, values=['MP4', 'WebM'], state='readonly', style='App.TCombobox')
    format_combo.grid(row=3, column=1, sticky='w', pady=4)

    ttk.Label(form_card, text="Quality", style='Card.TLabel').grid(row=4, column=0, sticky='w', padx=(0, 8), pady=4)
    quality_var = tk.StringVar(value='Best')
    quality_combo = ttk.Combobox(form_card, textvariable=quality_var, values=['Best', '720p', '1080p'], state='readonly', style='App.TCombobox')
    quality_combo.grid(row=4, column=1, sticky='w', pady=4)

    progress_card = ttk.LabelFrame(app, text='Progress', style='Card.TLabelframe', padding=12)
    progress_card.pack(fill=tk.X, pady=(0, 10))
    progress_bar = ttk.Progressbar(progress_card, mode='determinate', maximum=100, style='App.Horizontal.TProgressbar')
    progress_bar.pack(fill=tk.X)

    actions = ttk.Frame(app, style='App.TFrame')
    actions.pack(fill=tk.X, pady=(0, 10))
    download_button = ttk.Button(
        actions,
        text="Start Download",
        style='Accent.TButton',
        command=lambda: start_download(
            url_var,
            folder_var,
            playlist_var,
            progress_bar,
            download_button,
            folder_button,
            url_entry,
            playlist_check,
            format_var,
            quality_var,
        ),
    )
    download_button.pack(side=tk.LEFT)

    social_frame = ttk.Frame(actions, style='App.TFrame')
    social_frame.pack(side=tk.RIGHT)
    github_button = ttk.Button(social_frame, text="GitHub", style='App.TButton', command=lambda: webbrowser.open("https://www.github.com/el-guemra-br"))
    github_button.pack(side=tk.LEFT, padx=(0, 6))
    instagram_button = ttk.Button(social_frame, text="Instagram", style='App.TButton', command=lambda: webbrowser.open("https://www.instagram.com/el_guemra_br"))
    instagram_button.pack(side=tk.LEFT)

    console_card = ttk.LabelFrame(app, text='Console', style='Card.TLabelframe', padding=10)
    console_card.pack(fill=tk.BOTH, expand=True)
    console_text = scrolledtext.ScrolledText(console_card, width=80, height=11)
    console_text.pack(fill=tk.BOTH, expand=True)

    apply_theme(root, style, theme_var, console_text, theme_var.get())

    root.mainloop()

if __name__ == "__main__":
    main()
