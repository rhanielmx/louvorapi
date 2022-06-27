from app import app, db
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.models import Song

from slugify import slugify

songs_bp = Blueprint('songs',__name__)
api = Api(songs_bp)

song_model = api.model('Song',{
    'title': fields.String,
    'artist': fields.String,
    'lyrics': fields.String,
    'video_url': fields.String,
    'category_id':fields.Integer
})

@api.route('/new', methods=['POST'])
class CreateSongs(Resource):
    @api.expect(song_model)
    def post(self):
        msg = request.json
        data = Song(**request.json)
        data.save()
        return {'Status':'OK', 'message':msg}, 200

@api.route('/list', methods=['GET'])
class ListLyrics(Resource):
    def get(self):
        songs = Song.query.all()
        return {'Status':'OK', 'songs':[song.json() for song in songs]}, 200

@api.route('/title/<title>', methods=['GET'])
class GetSongByTitle(Resource):
    def get(self,title):
        songs = Song.query.filter_by(slugified_title=slugify(title)).all()
        if songs:
            return {'status':'OK', 'songs':[song.json() for song in songs]}, 200
        else:
            return {'status':'Error', 'message':'Song not found'}

@api.route('/artist/<artist>', methods=['GET'])
class GetSongsByArtist(Resource):
    def get(self,artist):
        print('artist',artist)
        print(slugify(artist))
        songs = Song.query.filter_by(slugified_artist=slugify(artist)).all()
        if songs:
            return {'status':'OK', 'songs':[song.json() for song in songs]}, 200
        else:
            return {'status':'Error', 'message':'No songs found'}

@api.route('/<artist>/<title>', methods=['GET'])
class GetSongByTitleAndArtist(Resource):
    def get(self,artist,title):
        print('caling get song')
        data = []
        print(slugify(artist))
        print(slugify(title))
        song = Song.query.filter_by(slugified_artist=slugify(artist),slugified_title=slugify(title)).first()
        print(song)
        if song:
            data=song.json()        
            return {'status':'OK', 'song':data}, 200
        else:
            return {'status':'Error', 'message':'Song not found'}


