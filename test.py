import os
import subprocess

search_path = "C:\\Users\\mehan\\Videos"
target_file = "ar today 23-09-24.mp4"
vlc_path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"

# Check if VLC path exists
if not os.path.exists(vlc_path):
    print(f"VLC not found at {vlc_path}")
    exit()

file_found = False

for root, dirs, files in os.walk(search_path):
    if target_file in files:
        file_path = os.path.join(root, target_file)
        try:
            print(f"Playing file: {file_path}")
            subprocess.Popen([vlc_path, file_path])
            file_found = True
            break
        except Exception as e:
            print(f"Error opening VLC: {e}")
            exit()

if not file_found:
    print(f"File '{target_file}' not found in '{search_path}'")
