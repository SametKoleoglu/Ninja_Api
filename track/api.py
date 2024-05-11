from django.http import JsonResponse
from ninja import NinjaAPI, ModelSchema,Schema
from .models import Track
from typing import List

api = NinjaAPI()

class TrackSchema(ModelSchema):
    class Meta:
        model = Track
        fields = "__all__"


class NotFoundSchema(Schema):
    message : str

@api.get("/tracks", response=List[TrackSchema])
def get_tracks(request,title=None):
    if title:
        return Track.objects.filter(title__icontains=title)
    else:
        return Track.objects.all()


@api.get("/tracks/{id}", response={200:TrackSchema, 404:NotFoundSchema})
def get_track(request, id):
    try:
        return Track.objects.get(id=id)
    except:
        return 404,{'message':'Track not found'}



@api.post("/tracks", response={201:TrackSchema})
def create_track(request, track: TrackSchema):
    track = Track.objects.create(**track.dict())
    return track

@api.put("/tracks/{id}", response={200:TrackSchema, 404:NotFoundSchema})
def update_track(request, id: int, data: TrackSchema):
    try:
        track = Track.objects.get(id=id)
        for attr, value in data.dict().items():
            setattr(track, attr, value)
        track.save()
        return 200, track
    except:
        return 404,{'message':'Track not found'}


@api.delete("/tracks/{id}", response={404:NotFoundSchema})
def delete_track(request, id: int):
    try:
        track = Track.objects.get(id=id)
        track.delete()
        return 204, JsonResponse({'message': 'Track deleted successfully'})
    except Track.DoesNotExist:
        return 404,{'message':'Track not found'}