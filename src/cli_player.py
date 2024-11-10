import subprocess
from time import time

class CliPlayer:
    def __init__(self, texts_dir_path):
        self.texts_dir_path = texts_dir_path
        
    def play(self, fps):
        i = 0
        start_time = time()
        while True:
            # 表示フレームの決定
            current_time = time()
            s, ms = str(current_time - start_time).split(".")
            i = int(s) * fps + int(int(ms[:3]) * fps / 1000)
            # 表示用の時刻
            play_time = int(current_time - start_time)
            play_time_m = play_time//60
            play_time_s = play_time%60
            # 表示
            subprocess.run(["clear"])
            subprocess.run(["cat", f"{self.texts_dir_path}/{i:09d}.txt"])
            subprocess.run(["echo", f"{play_time_m:02}:{play_time_s:02}"])
            subprocess.run(["sleep", str(1 / fps)])