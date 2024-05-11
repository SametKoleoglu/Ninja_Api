from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
# Create your views here.

def index(request):
    response_track = requests.get('http://127.0.0.1:8000/api/tracks')
    if response_track.status_code == 200:
        tracks = response_track.json()
    else:
        tracks = None
        
    if request.method == 'POST':
        if request.POST.get('addTrack') == 'trackAdd':
            title = request.POST.get('title')
            artist = request.POST.get('artist')
            duration = request.POST.get('duration')
            last_play = request.POST.get('last_play')
            
            track = {
                "title": title,
                "artist": artist,
                "duration": duration,
                "last_play": last_play
            }
            
            new_track = requests.post('http://127.0.0.1:8000/api/tracks', json=track)
            
            if new_track.status_code == 201:
                return redirect('index')
            else:
                return "Something went wrong"
        
        
        if request.POST.get('updateTrack') == 'trackUpdate':
            track_id = request.POST.get('track_id')
            title = request.POST.get('title')
            artist = request.POST.get('artist')
            duration = request.POST.get('duration')
            last_play = request.POST.get('last_play')
            
            track = {
                "id": track_id,
                "title": title,
                "artist": artist,
                "duration": duration,
                "last_play": last_play
            }
            
            update_track = requests.put(f'http://127.0.0.1:8000/api/tracks/{track_id}', json=track)
            
            if update_track.status_code == 200:
                return redirect('index')
            else:
                return "Something went wrong"
            
    if "trackId" in request.GET and request.GET.get('trackId') != "":
        track_id = request.GET.get('trackId')
        
        delete_track = requests.delete(f'http://127.0.0.1:8000/api/tracks/{track_id}')
        
        return redirect('index')

    if "query" in request.GET and request.GET.get('query') != "":
        query = request.GET.get('query')
        title = {'title': query}
        filter_tracks = requests.get('http://127.0.0.1:8000/api/tracks', title)
        
        if filter_tracks.status_code == 200:
            tracks = filter_tracks.json()
        else:
            tracks = None
        
    context = {'tracks': tracks}
        
    return render(request, template_name='index.html',context=context)