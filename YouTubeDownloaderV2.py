import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube  # Import necessary libraries
import threading
import os
import time

# using https://www.freecodecamp.org/news/python-program-to-download-youtube-videos/ method to download youtube videos

# Function to select download location
def select_download_location():
    download_path = filedialog.askdirectory()  # Open folder selection dialog
    if download_path:
        download_path_label.config(text=f"Download location: {download_path}")  # Update label with selected path

# Function to initiate video download
# The progress bar is simulated because I don't think pytube has a built-in progress bar
def download_video():
    link = link_entry.get()  # Get URL input from entry field
    try:
        youtubeObject = YouTube(link)  # Create YouTube object with the given link
        if audio_only_var.get():  # Check if the checkbox for audio-only is selected
            video_stream = youtubeObject.streams.filter(only_audio=True).first()  # Get audio-only stream
        else:
            video_stream = youtubeObject.streams.get_highest_resolution()  # Get highest resolution video stream

        download_path = download_path_label.cget("text").replace("Download location: ", "")  # Get download path
        download_label.config(text="Downloading...")  # Update label to show download initiation
        download_button.config(state=tk.DISABLED)  # Disable download button

        download_thread = threading.Thread(target=start_download, args=(video_stream, download_path))
        download_thread.start()  # Start download in a separate thread

        simulate_download(video_stream)  # Simulate download progress
        
        download_label.config(text="Download completed")  # Update label to show download completion
        download_button.config(state=tk.NORMAL)  # Enable download button
    except Exception as e:
        download_label.config(text=f"Error: {str(e)}")  # Display error message
        download_button.config(state=tk.NORMAL)  # Enable download button

# Function to handle the download process
def start_download(video_stream, download_path):
    try:
        file_name = video_stream.default_filename  # Get default filename from the stream
        video_stream.download(download_path)  # Download the video/audio stream
        if audio_only_var.get() and file_name.endswith('.mp4'):
            # If audio-only download is successful, rename the file with change to '.mp3' extension
            new_file_name = os.path.join(download_path, f"{os.path.splitext(file_name)[0]}.mp3")
            os.rename(os.path.join(download_path, file_name), new_file_name)
    except Exception as e:
        print(f"Download Error: {e}")

# Function to simulate download progress
def simulate_download(stream):
    chunk_size = 1024 * 1024  # Define chunk size for simulation
    total_bytes = stream.filesize if stream else 0  # Get total bytes to simulate progress
    bytes_downloaded = 0

    while bytes_downloaded < total_bytes:
        bytes_downloaded += chunk_size
        progress = (bytes_downloaded / total_bytes) * 100
        progress_bar['value'] = progress  # Update progress bar value
        root.update_idletasks()  # Update GUI
        time.sleep(1)  # Simulate download progress every second

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create and place widgets (Labels, Entry, Buttons, Checkbutton, Progressbar)
label = tk.Label(root, text="Enter YouTube video URL:")
label.pack()

link_entry = tk.Entry(root, width=50)
link_entry.pack()

select_location_button = tk.Button(root, text="Select Download Location", command=select_download_location)
select_location_button.pack()

download_path_label = tk.Label(root, text="Download location: Not selected")
download_path_label.pack()

audio_only_var = tk.BooleanVar()
audio_only_checkbox = tk.Checkbutton(root, text="Download Audio Only", variable=audio_only_var)
audio_only_checkbox.pack()

progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack()

download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

download_label = tk.Label(root, text="")
download_label.pack()

# Start the GUI event loop
root.mainloop()
