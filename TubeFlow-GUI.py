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

# Function to toggle theme
def toggle_theme(root, theme_var, theme_type):
    theme_var.set(theme_type)
    if theme_type == 'Dark':
        root.configure(bg='gray20')
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg='gray20', fg='white')
            elif isinstance(widget, tk.Frame):
                widget.configure(bg='gray20')
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, tk.Label):
                        subwidget.configure(bg='gray20', fg='white')
                    elif isinstance(subwidget, tk.Button):
                        subwidget.configure(bg='gray30', fg='white')
                    elif isinstance(subwidget, tk.Entry):
                        subwidget.configure(bg='gray30', fg='white', insertbackground='white')
                    elif isinstance(subwidget, tk.Checkbutton):
                        subwidget.configure(bg='gray20', fg='white', selectcolor='gray30')
                    elif isinstance(subwidget, ttk.Combobox):
                        widget.configure(style='TCombobox')
    elif theme_type == 'Light':
        root.configure(bg='SystemButtonFace')
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg='SystemButtonFace', fg='black')
            elif isinstance(widget, tk.Frame):
                widget.configure(bg='SystemButtonFace')
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, tk.Label):
                        subwidget.configure(bg='SystemButtonFace', fg='black')
                    elif isinstance(subwidget, tk.Button):
                        subwidget.configure(bg='SystemButtonFace', fg='black')
                    elif isinstance(subwidget, tk.Entry):
                        subwidget.configure(bg='SystemButtonFace', fg='black', insertbackground='black')
                    elif isinstance(subwidget, tk.Checkbutton):
                        subwidget.configure(bg='SystemButtonFace', fg='black', selectcolor='SystemButtonFace')
                    elif isinstance(subwidget, ttk.Combobox):
                        widget.configure(style='TCombobox')

# Function to open settings window
def open_settings(root, theme_var, console_text):
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("400x400")

    tk.Label(settings_win, text="Theme:").pack(pady=5)
    theme_radio = tk.StringVar(value=theme_var.get())
    tk.Radiobutton(settings_win, text="Light", variable=theme_radio, value='Light', command=lambda: [toggle_theme(root, theme_var, 'Light'), theme_var.set('Light')]).pack()
    tk.Radiobutton(settings_win, text="Dark", variable=theme_radio, value='Dark', command=lambda: [toggle_theme(root, theme_var, 'Dark'), theme_var.set('Dark')]).pack()

    tk.Label(settings_win, text="Console:").pack(pady=5)
    console_area = scrolledtext.ScrolledText(settings_win, width=50, height=10)
    console_area.pack(pady=5)
    console_area.insert(tk.END, console_text.get(1.0, tk.END))

# Function to start download
def start_download(url_var, folder_var, playlist_var, progress_bar, download_button, folder_button, url_entry, playlist_check):
    url = url_var.get().strip()
    folder = folder_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    if not folder:
        messagebox.showerror("Error", "Please select a download folder.")
        return
    threading.Thread(target=do_download, args=(url, folder, playlist_var.get(), progress_bar, download_button, folder_button, url_entry, playlist_check)).start()

# Main GUI setup
def main():
    global format_var, quality_var
    install_yt_dlp()

    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("600x450")

    # Top frame for settings button
    top_frame = tk.Frame(root)
    top_frame.pack(fill=tk.X, pady=5)

    # Settings button on the left
    theme_var = tk.StringVar(value='Light')
    settings_button = tk.Button(top_frame, text="Settings", command=lambda: open_settings(root, theme_var, console_text))
    settings_button.pack(side=tk.LEFT, padx=10)

    # URL input
    tk.Label(root, text="YouTube URL:").pack(pady=5)
    url_var = tk.StringVar()
    url_entry = tk.Entry(root, textvariable=url_var, width=50)
    url_entry.pack(pady=5)

    # Playlist checkbox
    playlist_var = tk.BooleanVar()
    playlist_check = tk.Checkbutton(root, text="Download as playlist", variable=playlist_var)
    playlist_check.pack(pady=5)

    # Folder selection
    tk.Label(root, text="Download Folder:").pack(pady=5)
    folder_var = tk.StringVar()
    folder_frame = tk.Frame(root)
    folder_frame.pack(pady=5)
    folder_entry = tk.Entry(folder_frame, textvariable=folder_var, width=40)
    folder_entry.pack(side=tk.LEFT)
    folder_button = tk.Button(folder_frame, text="Browse", command=lambda: select_folder(folder_var))
    folder_button.pack(side=tk.RIGHT)

    # Format selection
    tk.Label(root, text="Format:").pack(pady=5)
    format_var = tk.StringVar(value='MP4')
    format_combo = ttk.Combobox(root, textvariable=format_var, values=['MP4', 'WebM'], state='readonly')
    format_combo.pack(pady=5)

    # Quality selection
    tk.Label(root, text="Quality:").pack(pady=5)
    quality_var = tk.StringVar(value='Best')
    quality_combo = ttk.Combobox(root, textvariable=quality_var, values=['Best', '720p', '1080p'], state='readonly')
    quality_combo.pack(pady=5)



    # Progress bar
    progress_bar = ttk.Progressbar(root, mode='determinate', maximum=100)
    progress_bar.pack(pady=10, fill=tk.X, padx=20)

    # Download button
    download_button = tk.Button(root, text="Download", command=lambda: start_download(url_var, folder_var, playlist_var, progress_bar, download_button, folder_button, url_entry, playlist_check))
    download_button.pack(pady=10)

    # Social media buttons
    social_frame = tk.Frame(root)
    social_frame.pack(pady=10)
    github_button = tk.Button(social_frame, text="GitHub", command=lambda: webbrowser.open("https://www.github.com/el-guemra-br"))
    github_button.pack(side=tk.LEFT, padx=5)
    instagram_button = tk.Button(social_frame, text="Instagram", command=lambda: webbrowser.open("https://www.instagram.com/el_guemra_br"))
    instagram_button.pack(side=tk.LEFT, padx=5)

    # Console area
    tk.Label(root, text="Console:").pack(pady=5)
    console_text = scrolledtext.ScrolledText(root, width=80, height=10)
    console_text.pack(pady=5, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
