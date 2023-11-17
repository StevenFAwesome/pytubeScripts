import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube
import threading
import time  # Add the import for the time module

def select_download_location():
    download_path = filedialog.askdirectory()
    if download_path:
        download_path_label.config(text=f"Download location: {download_path}")

def simulate_download(stream):
    chunk_size = 1024 * 1024  # 1 MB
    total_bytes = stream.filesize
    bytes_downloaded = 0

    while bytes_downloaded < total_bytes:
        bytes_downloaded += chunk_size
        progress = (bytes_downloaded / total_bytes) * 100
        progress_bar['value'] = progress
        root.update_idletasks()
        # Simulate download progress by waiting (can be removed in actual usage)
        time.sleep(1)

def download_video():
    link = link_entry.get()
    try:
        youtubeObject = YouTube(link)
        video_stream = youtubeObject.streams.get_highest_resolution()

        download_path = download_path_label.cget("text").replace("Download location: ", "")
        download_label.config(text="Downloading...")
        download_button.config(state=tk.DISABLED)

        # Start the download in a separate thread
        download_thread = threading.Thread(target=start_download, args=(video_stream, download_path))
        download_thread.start()

        simulate_download(video_stream)
        
        download_label.config(text="Download completed")
        download_button.config(state=tk.NORMAL)
    except Exception as e:
        download_label.config(text=f"Error: {str(e)}")
        download_button.config(state=tk.NORMAL)

def start_download(video_stream, download_path):
    try:
        video_stream.download(download_path)
    except Exception as e:
        print(f"Download Error: {e}")

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create and place widgets
label = tk.Label(root, text="Enter YouTube video URL:")
label.pack()

link_entry = tk.Entry(root, width=50)
link_entry.pack()

select_location_button = tk.Button(root, text="Select Download Location", command=select_download_location)
select_location_button.pack()

download_path_label = tk.Label(root, text="Download location: Not selected")
download_path_label.pack()

progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack()

download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

download_label = tk.Label(root, text="")
download_label.pack()

# Start the GUI event loop
root.mainloop()
