import os
import sys
import subprocess
import time


#time.sleep(3600)

backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Backend')
main_script = os.path.join(backend_dir, 'main.py')

# Build command with required arguments
command = [
    sys.executable,
    main_script,
    '--language', "English",
    '--type', "Supernatural",
    '--duration', "shortsVideos",
    '--model', "gemini-2.0-flash",
    '--api-key', "AIzaSyAHMRaTIXBT5vBqK7eKRS5u858_BCxBEBI",
    '--output-path', "E:\Youtube\Stories"
]

# while True:
for i in range(10):
    subprocess.run(command, check=True)

    # if result.returncode == 0:
    #     print("Command completed successfully.")
    #     break
