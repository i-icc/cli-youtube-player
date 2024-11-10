import subprocess

class YoutubeDlownloader:
    def __init__(self):
        self.base_url = "https://www.youtube.com/watch?v="

    def execute(self, id, output_path):
        try:
            # youtube-dlで動画をダウンロード
            commands = ["yt-dlp", "-o", output_path ,"-f", "mp4", f"https://www.youtube.com/watch?v={id}"]
            subprocess.run(" ".join(commands), shell=True, check=True)
            pass
        except FileNotFoundError as e:
            print("Error: youtube-dl が見つかりません。インストールしてください。")
            raise e
            return
        except subprocess.CalledProcessError as e:
            print("Error: youtube-dl で動画のダウンロードに失敗しました。", e)
            raise e
            return
