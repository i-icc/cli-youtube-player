import subprocess

class CliPlayer:
    def __init__(self, texts_dir_path):
        self.texts_dir_path = texts_dir_path
        
    def play(self, fps):
        i = 0
        start_time = 0
        while True:
            # 表示フレームの決定
            i += 1
            subprocess.run(["clear"])
            subprocess.run(["cat", f"{self.texts_dir_path}/{i:09d}.txt"])
            subprocess.run(["sleep", str(1 / fps)])