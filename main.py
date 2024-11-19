import subprocess
import sys
import os
from src.dir_manager import DirManager
from src.youtube_downloader import YoutubeDlownloader
from src.cli_player import CliPlayer

def main(id):
    """
    YouTubeの動画をASCIIアートとビープ音でターミナルに表示する関数

    Args:
      url: YouTube動画のURL
    """

    base_path = "./output"
    fps = 30
    dr = DirManager(id, base_path)
    is_exist = dr.check_exit_dir()
    
    if not is_exist:
        _create_files(id, dr, fps)
        
    while True:
        is_play = input("再生を始めますか？(y/n):")
        if is_play == "y":
            break
        if is_play == "n":
            return
    
    # AA表示
    text_path = dr.get_text_path()
    cp = CliPlayer(text_path)
    cp.play(fps)


def _create_files(id, dr, fps):
    dr.create_template_dir()
    filename = dr.get_target_path() + "/tmp_video.mp4"
    try:
        # youtube-dlで動画をダウンロード
        yd = YoutubeDlownloader()
        yd.execute(id, filename)
    except:
        return

    flame_path = dr.get_flame_path()
    try:
        # ffmpegで動画をフレームに分割
        commands = ["ffmpeg", "-i", filename, "-r", str(fps), f"{flame_path}/frame%09d.png"]
        print(" ".join(commands))
        subprocess.run(" ".join(commands), shell=True, check=True)
    except FileNotFoundError:
        print("Error: ffmpeg が見つかりません。インストールしてください。")
        return
    except subprocess.CalledProcessError:
        print("Error: ffmpeg で動画のフレーム分割に失敗しました。")
        return

    try:
        text_path = dr.get_text_path()
        file_count = os.listdir(flame_path)
        # jp2aでフレームをASCIIアートに変換
        for i in range(1, file_count): 
            commands = ["jp2a", "--width=128", f"{flame_path}/frame{i:09d}.png", ">", f"{text_path}/{i:09d}.txt"]
            subprocess.run(" ".join(commands), shell=True, check=True)
    except FileNotFoundError:
        print("Error: jp2a が見つかりません。インストールしてください。")
        return
    except subprocess.CalledProcessError:
        print("Error: jp2a でASCIIアートへの変換に失敗しました。")
        return

if __name__ == "__main__":
    # YouTube動画のURLを入力
    url = sys.argv[1]
    main(url)
