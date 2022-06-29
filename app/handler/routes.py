from email import message
from app import app, db
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.models import Category, Song

from slugify import slugify

handler_bp = Blueprint('handler',__name__)
api = Api(handler_bp)

song_model = api.model('Song',{
    'title': fields.String,
    'artist': fields.String,
    'lyrics': fields.String,
    'video_url': fields.String,
    'category_id':fields.Integer
})

category_model = api.model('Category',{
    'name': fields.String
})

@api.route('/songs/new', methods=['POST'])
class CreateSongs(Resource):
    @api.expect(song_model)
    def post(self):
        categories = []
        msg = request.json
        song = Song(msg['title'], msg['artist'], msg['lyrics'], msg['video_url'])        
        for name in msg['categories']:
            category = Category.query.filter_by(name=name).first()
            if category:
                categories.append(category)      
        song.categories.extend(categories)
        song.save()
        return {'Status':'OK', 'message':msg}, 200

@api.route('/songs/list', methods=['GET'])
class ListSongs(Resource):
    def get(self):
        songs = Song.query.all()
        return {'Status':'OK', 'songs':[song.json() for song in songs]}, 200

@api.route('/categories/new', methods=['POST'])
class CreateCategories(Resource):
    @api.expect(category_model)
    def post(self):
        category = Category(**request.json)
        category.save()
        return {'Status':'OK', 'category':category.json()}, 200

@api.route('/categories/list', methods=['GET'])
class ListCategories(Resource):
    def get(self):
        categories = Category.query.order_by(Category.name).all()
        return {'Status':'OK', 'categories':[category.json() for category in categories]}, 200

@api.route('/title/<title>', methods=['GET'])
class GetSongByTitle(Resource):
    def get(self,title):
        songs = Song.query.filter_by(slugified_title=slugify(title)).all()
        if songs:
            return {'status':'OK', 'songs':[song.json() for song in songs]}, 200
        else:
            return {'status':'Error', 'songs':[], 'message':'Song not found'}

@api.route('/artist/<artist>', methods=['GET'])
class GetSongsByArtist(Resource):
    def get(self,artist):     
        songs = Song.query.filter_by(slugified_artist=slugify(artist)).all()
        if songs:
            return {'status':'OK', 'songs':[song.json() for song in songs]}, 200
        else:
            return {'status':'Error', 'message':'No songs found'}

@api.route('/<artist>/<title>', methods=['GET'])
class GetSongByTitleAndArtist(Resource):
    def get(self,artist,title):
        data = []
        print(slugify(artist), slugify(title))
        song = Song.query.filter_by(slugified_artist=slugify(artist),slugified_title=slugify(title)).first()
        print('song',song)
        if song:
            data=song.json()        
            return {'status':'OK', 'song':data}, 200
        else:
            return {'status':'Error', 'song':[],'message':'Song not found'}


