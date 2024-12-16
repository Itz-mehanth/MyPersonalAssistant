import os
import subprocess

def search_and_open_file(search_path, file_name_substring):
    video_audio_extensions = ['.mp4', '.mkv', '.avi', '.mp3', '.wav', '.flac', '.aac']  # Supported media formats
    vlc_path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"

    print(f"Searching for files containing '{file_name_substring}' in '{search_path}'...")
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file_name_substring.lower() in file.lower():  # Case-insensitive substring match
                file_path = os.path.join(root, file)
                print(f"File found: {file_path}")
                try:
                    # Check if the file is a video or audio file
                    if any(file.lower().endswith(ext) for ext in video_audio_extensions):
                        # Open in VLC media player
                        subprocess.Popen([vlc_path, file_path])
                        return f"Media file opened in VLC: {file_path}"
                    else:
                        # Open non-media file with default program
                        subprocess.Popen(["start", file_path], shell=True)
                        return f"File opened: {file_path}"
                except Exception as e:
                    return f"Error opening file: {e}"
    return f"No file containing '{file_name_substring}' found in '{search_path}'."

# Example Usage
search_path = "C:\\Users\\mehan\\Downloads"  # Change this to the directory you want to search in
file_name_substring = "sir"  # Substring to search for in file names
