import subprocess
import sys

def play_youtube_with_ascii_art_and_beep(url, is_sound=False):
    """
    YouTubeの動画をASCIIアートとビープ音でターミナルに表示する関数

    Args:
      url: YouTube動画のURL
    """

    filename = "tmp_video.mp4"

    try:
        # youtube-dlで動画をダウンロード
        commands = ["yt-dlp", "-o", filename ,"-f", "mp4", url]
        subprocess.run(" ".join(commands), shell=True, check=True)
        pass
    except FileNotFoundError:
        print("Error: youtube-dl が見つかりません。インストールしてください。")
        return
    except subprocess.CalledProcessError:
        print("Error: youtube-dl で動画のダウンロードに失敗しました。")
        return

    try:
        # ffmpegで動画をフレームに分割
        subprocess.run(["ffmpeg", "-i", filename, "frame%09d.png"], check=True)
    except FileNotFoundError:
        print("Error: ffmpeg が見つかりません。インストールしてください。")
        return
    except subprocess.CalledProcessError:
        print("Error: ffmpeg で動画のフレーム分割に失敗しました。")
        return

    if is_sound:
        try:
            # ffmpegで動画から音声を抽出
            subprocess.run(["ffmpeg", "-i", filename, "audio.wav"], check=True)
        except subprocess.CalledProcessError:
            print("Error: ffmpeg で音声の抽出に失敗しました。")
            return

        try:
            # soxで音声の平均振幅を取得
            avg_amplitude = subprocess.check_output(["sox", "audio.wav", "-n", "stat", "2>&1", "|", "grep", "Mean    amplitude", "|", "awk", '{print $3}']).decode("utf-8").strip()
            # 平均振幅をビープ音の周波数に変換
            frequency = subprocess.check_output(["echo", "scale=4; " + avg_amplitude + " * 1000 + 440", "|", "bc"]).decode("utf-8").strip()
        except FileNotFoundError:
            print("Error: sox が見つかりません。インストールしてください。")
            return
        except subprocess.CalledProcessError:
            print("Error: sox で音声の分析に失敗しました。")
            return

    try:
        # jp2aでフレームをASCIIアートに変換
        for i in range(1, 2100): 
            commands = ["jp2a", "--width=128", f"frame{i:09d}.png", ">", f"frame{i:09d}.txt"]
            subprocess.run(" ".join(commands), shell=True, check=True)
    except FileNotFoundError:
        print("Error: jp2a が見つかりません。インストールしてください。")
        return
    except subprocess.CalledProcessError:
        print("Error: jp2a でASCIIアートへの変換に失敗しました。")
        return

    while True:
        is_play = input("再生を始めますか？(y/n):")
        if(is_play == "y"):
            break

    
    try:
        # ASCIIアートとビープ音を同期して表示
        fps = 30  # フレームレートを30fpsと仮定
        for i in range(1, 2100):
            subprocess.run(["clear"])
            subprocess.run(["cat", f"frame{i:09d}.txt"])
            if is_sound:
                subprocess.run(["beep", "-f", frequency, "-l", str(int(1000 / fps))])
            subprocess.run(["sleep", str(1 / fps)])
    except FileNotFoundError:
        print("Error: beep が見つかりません。インストールしてください。")
        return
    except subprocess.CalledProcessError:
        print("Error: beep でビープ音の生成に失敗しました。")
        return

if __name__ == "__main__":
    # YouTube動画のURLを入力
    url = sys.argv[1]
    play_youtube_with_ascii_art_and_beep(url)
