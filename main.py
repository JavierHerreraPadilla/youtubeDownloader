import time

from flask import Flask, render_template, url_for, redirect, request, send_from_directory
import os
import pytube
from pathlib import Path


app = Flask(__name__)

songPath = Path(r'./static/songs/')

@app.route("/", methods=['POST', 'GET'])
def home():
# DELETING EXISTING SONGS BASED ON TIME
    global songPath
    savedSongs = os.listdir(songPath)
    if len(savedSongs) > 0:
        for song in savedSongs:
            songs_path = songPath / song
            if time.time() - os.path.getmtime(songs_path) > 60:
                print(f'{song} se ha borrado')
                os.remove(songs_path)

    yt = None
    result_list = None
    if request.method == 'POST':
        req_url = request.form.get('url')
        req_search = request.form.get('buscar')

        if req_url:
            yt = pytube.YouTube(req_url)
            vid_id = yt.vid_info.get('videoDetails').get('videoId')
            print(type(yt.vid_info.get('videoDetails').get('videoId')))
            #return redirect(url_for('unique', vid_id=vid_id))
        elif req_search:
            print(request.form.get('buscar'))
            print(type(request.form.get('buscar')))
            s = pytube.Search(req_search)
            result_list = s.results
            print(result_list)
            print([result.title for result in result_list])
            #result_ids = [result.vid_info.get('videoDetails').get('videoId') for result in result_list]
            #ids_dict=dict()
            #for i in range(len(result_ids)):
            #    ids_dict[f"{i}"] = result_ids[i]
            #json_dict = json.dumps(ids_dict)
            #print('result_id ', result_ids)
            #return redirect(url_for('search_list', id_list=json_dict))
    return render_template('home.html', yt=yt, list=result_list)


@app.route('/unique-by-id')
def unique():
    vid = pytube.YouTube.from_id(request.args.get('vid_id'))
    video = vid.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=r'./static/songs')
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(new_file)
    file_name = Path(new_file).name
    print(file_name)
    print(type(file_name))
    #return render_template('unique.html', yt=vid)
    return send_from_directory(r'./static/songs', file_name, as_attachment=True)
    #send_from_directory(r'./static/songs', file_name, as_attachment=True)
    #os.remove(Path(new_file))
    #return redirect(url_for('home'))
    #try:
    #    return send_from_directory(r'./static/songs', file_name, as_attachment=True)
    #finally:
    #    os.remove(new_file)

if __name__ == '__main__':
    app.run(debug=True)