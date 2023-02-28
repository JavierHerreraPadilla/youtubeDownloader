from pytube import YouTube
import os
from pathlib import Path


def yt_dl(vid_url:str):
    yt = YouTube(vid_url)
    try:
        video = yt.streams.filter(only_audio=True).first()
        destination = Path('./static')
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return Path(new_file), yt
    except:
        return

#downloaded = False
#    file_name = None
#    yt = None
#    result_list = None
#    if request.method == "POST":
#        if request.form.get('url'):
#            file_name, yt = yt_dl(request.form.get('url'))
#            if file_name.name in os.listdir('./static'):
#                file_name = file_name.name #file_name es un Path
#                downloaded = True
#        elif request.form.get('buscar'):
#            s = pytube.Search(request.form.get('buscar'))
#            result_list = s.results