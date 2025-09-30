import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("800x650")
        self.root.minsize(700, 550)
        
        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"
        self.success_color = "#5cb85c"
        self.error_color = "#d9534f"
        self.dark_text = "#2c3e50"
        
        self.root.configure(bg=self.bg_color)
        
        self.playlist_url = tk.StringVar()
        self.output_path = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.format_choice = tk.StringVar(value="mp3")
        self.quality_choice = tk.StringVar(value="1080p")
        self.is_downloading = False
        self.download_process = None
        
        self.setup_styles()
        self.create_widgets()
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       font=("Segoe UI", 18, "bold"), 
                       foreground=self.dark_text,
                       background=self.bg_color)
        
        style.configure('Header.TLabel', 
                       font=("Segoe UI", 11, "bold"), 
                       foreground=self.dark_text,
                       background=self.bg_color)
        
        style.configure('TLabel', 
                       font=("Segoe UI", 10), 
                       background=self.bg_color,
                       foreground=self.dark_text)
        
        style.configure('TFrame', background=self.bg_color)
        
        style.configure('Card.TFrame', 
                       background="white", 
                       relief="flat")
        
        style.configure('Download.TButton',
                       font=("Segoe UI", 11, "bold"),
                       foreground="white",
                       background=self.accent_color,
                       borderwidth=0,
                       focuscolor='none',
                       padding=10)
        
        style.map('Download.TButton',
                 background=[('active', '#357abd'), ('disabled', '#cccccc')])
        
        style.configure('Stop.TButton',
                       font=("Segoe UI", 10, "bold"),
                       foreground="white",
                       background=self.error_color,
                       borderwidth=0,
                       focuscolor='none',
                       padding=8)
        
        style.map('Stop.TButton',
                 background=[('active', '#c9302c'), ('disabled', '#cccccc')])
        
        style.configure('Browse.TButton',
                       font=("Segoe UI", 9),
                       padding=5)
        
        style.configure('TEntry',
                       fieldbackground="white",
                       borderwidth=1,
                       relief="solid")
        
        style.configure('TRadiobutton',
                       background=self.bg_color,
                       font=("Segoe UI", 10))
        
    def create_widgets(self):
        container = ttk.Frame(self.root, style='TFrame', padding="25")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        container.grid_rowconfigure(7, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        title_frame = ttk.Frame(container, style='TFrame')
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 25), sticky=tk.W)
        
        title_label = ttk.Label(title_frame, text="🎬 YouTube Playlist Downloader", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        url_card = ttk.Frame(container, style='Card.TFrame', padding="15")
        url_card.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        url_card.grid_columnconfigure(0, weight=1)
        
        ttk.Label(url_card, text="📎 Playlist URL", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        url_entry = ttk.Entry(url_card, textvariable=self.playlist_url, 
                             font=("Segoe UI", 10))
        url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), ipady=6)
        
        folder_card = ttk.Frame(container, style='Card.TFrame', padding="15")
        folder_card.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        folder_card.grid_columnconfigure(0, weight=1)
        
        ttk.Label(folder_card, text="📁 Output Folder", style='Header.TLabel').grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))
        
        ttk.Entry(folder_card, textvariable=self.output_path, 
                 font=("Segoe UI", 10), state="readonly").grid(
            row=1, column=0, sticky=(tk.W, tk.E), ipady=6, padx=(0, 10))
        
        ttk.Button(folder_card, text="Browse", style='Browse.TButton',
                  command=self.browse_folder).grid(row=1, column=1)
        
        format_card = ttk.Frame(container, style='Card.TFrame', padding="15")
        format_card.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(format_card, text="🎵 Format Selection", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        format_frame = ttk.Frame(format_card, style='Card.TFrame')
        format_frame.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(format_frame, text="🎵 MP3 (Audio Only)", 
                       variable=self.format_choice, 
                       value="mp3", command=self.on_format_change).pack(
            side=tk.LEFT, padx=(0, 30))
        
        ttk.Radiobutton(format_frame, text="🎬 MP4 (Video)", 
                       variable=self.format_choice, 
                       value="mp4", command=self.on_format_change).pack(side=tk.LEFT)
        
        self.quality_frame = ttk.Frame(format_card, style='Card.TFrame')
        self.quality_frame.grid(row=2, column=0, sticky=tk.W)
        
        ttk.Label(self.quality_frame, text="Quality:", 
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        qualities = ["2160p (4K)", "1440p", "1080p", "720p", "480p", "360p"]
        quality_menu = ttk.Combobox(self.quality_frame, textvariable=self.quality_choice, 
                                   values=qualities, state="readonly", width=15,
                                   font=("Segoe UI", 10))
        quality_menu.pack(side=tk.LEFT)
        quality_menu.current(2)
        
        self.quality_frame.grid_remove()
        
        button_frame = ttk.Frame(container, style='TFrame')
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.download_btn = ttk.Button(button_frame, text="⬇ Download Playlist", 
                                       style='Download.TButton',
                                       command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.stop_btn = ttk.Button(button_frame, text="⏹ Stop", 
                                   style='Stop.TButton',
                                   command=self.stop_download,
                                   state="disabled")
        self.stop_btn.pack(side=tk.LEFT)
        
        status_card = ttk.Frame(container, style='Card.TFrame', padding="15")
        status_card.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_card.grid_rowconfigure(1, weight=1)
        status_card.grid_columnconfigure(0, weight=1)
        
        ttk.Label(status_card, text="📊 Status Log", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(
            status_card, 
            height=12, 
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            relief="flat",
            padx=10,
            pady=10
        )
        self.status_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.status_text.config(state="disabled")
        
        self.status_text.tag_config("success", foreground="#5cb85c")
        self.status_text.tag_config("error", foreground="#d9534f")
        self.status_text.tag_config("info", foreground="#5bc0de")
        self.status_text.tag_config("warning", foreground="#f0ad4e")
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)
            
    def on_format_change(self):
        if self.format_choice.get() == "mp4":
            self.quality_frame.grid()
        else:
            self.quality_frame.grid_remove()
            
    def log_status(self, message, tag=""):
        self.status_text.config(state="normal")
        if tag:
            self.status_text.insert(tk.END, message + "\n", tag)
        else:
            self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.root.update()
        
    def start_download(self):
        if self.is_downloading:
            messagebox.showwarning("Download in Progress", 
                                 "Please wait for the current download to complete.")
            return
            
        url = self.playlist_url.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a playlist URL.")
            return
            
        output = self.output_path.get()
        if not os.path.exists(output):
            messagebox.showerror("Error", "Output folder does not exist.")
            return
            
        self.is_downloading = True
        self.download_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state="disabled")
        
        thread = threading.Thread(target=self.download_playlist, daemon=True)
        thread.start()
        
    def stop_download(self):
        if self.download_process:
            self.log_status("⏹ Stopping download...", "warning")
            self.download_process.terminate()
            self.is_downloading = False
            self.download_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.log_status("✗ Download stopped by user.", "error")
        
    def download_playlist(self):
        try:
            url = self.playlist_url.get().strip()
            output = self.output_path.get()
            format_type = self.format_choice.get()
            
            self.log_status("=" * 60, "info")
            self.log_status(f"🚀 Starting download...", "info")
            self.log_status(f"📎 URL: {url}", "info")
            self.log_status(f"📁 Output: {output}", "info")
            self.log_status(f"🎵 Format: {format_type.upper()}", "info")
            
            yt_dlp_path = resource_path("yt-dlp.exe")
            ffmpeg_path = resource_path("ffmpeg.exe")
            
            cmd = [yt_dlp_path, "--ffmpeg-location", ffmpeg_path]
            
            if format_type == "mp3":
                cmd.extend([
                    "-x",
                    "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "-o", os.path.join(output, "%(title)s.%(ext)s")
                ])
                self.log_status("🎵 Downloading audio only (MP3)...", "info")
            else:
                quality = self.quality_choice.get().split()[0]
                cmd.extend([
                    "-f", f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]",
                    "--merge-output-format", "mp4",
                    "-o", os.path.join(output, "%(title)s.%(ext)s")
                ])
                self.log_status(f"🎬 Downloading video (MP4 - {quality})...", "info")
            
            self.log_status("=" * 60, "info")
            cmd.append(url)
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            self.download_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            for line in self.download_process.stdout:
                if not self.is_downloading:
                    break
                self.log_status(line.strip())
            
            self.download_process.wait()
            
            if self.download_process.returncode == 0 and self.is_downloading:
                self.log_status("=" * 60, "success")
                self.log_status("✓ Download completed successfully!", "success")
                self.log_status("=" * 60, "success")
                messagebox.showinfo("Success", "Playlist downloaded successfully!")
            elif self.is_downloading:
                self.log_status("=" * 60, "error")
                self.log_status("✗ Download failed. Check the URL and try again.", "error")
                self.log_status("=" * 60, "error")
                messagebox.showerror("Error", "Download failed. Please check the status log.")
                
        except FileNotFoundError:
            self.log_status("=" * 60, "error")
            self.log_status("✗ Error: yt-dlp not found!", "error")
            self.log_status("=" * 60, "error")
            messagebox.showerror("Error", 
                               "yt-dlp is not installed or not in PATH.\n\n"
                               "Install it using:\npip install yt-dlp")
        except Exception as e:
            self.log_status("=" * 60, "error")
            self.log_status(f"✗ Error: {str(e)}", "error")
            self.log_status("=" * 60, "error")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.is_downloading = False
            self.download_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.download_process = None

def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()