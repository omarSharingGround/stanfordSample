from pytube import YouTube
import os

# saves a youtube video locally at the given path
def saveYTVideoAsAudio(link, path="."):
    yt = YouTube(link)

    video = yt.streams.filter(only_audio=True).first()

    out_file = video.download(output_path=path)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    return yt.title, base
