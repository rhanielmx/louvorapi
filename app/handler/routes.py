from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.handler.models import Category, Song

from slugify import slugify
from sqlalchemy import func

handler_bp = Blueprint('handler', __name__)
api = Api(handler_bp)

song_model = api.model('Song', {
    'title': fields.String,
    'artist': fields.String,
    'lyrics': fields.String,
    'video_url': fields.String,
    'category_id': fields.Integer
})

edit_song_model = api.model('EditSong', {
    'title': fields.String,
    'artist': fields.String,
    'lyrics': fields.String,
    'video_url': fields.String,
    'categories': fields.List(fields.String)
})

category_model = api.model('Category', {
    'name': fields.String
})


@api.route('/songs/new', methods=['POST'])
class CreateSongs(Resource):
    @api.expect(song_model)
    @jwt_required()
    def post(self):
        categories = []
        msg = request.json
        id=get_jwt_identity()
        print('hi',msg, id)
        song = Song(msg['title'], msg['artist'], msg['lyrics'],
                    msg['video_url'], id)
        for name in msg['categories']:
            category = Category.query.filter_by(name=name).first()
            if category:
                categories.append(category)
        song.categories.extend(categories)
        song.save()
        return {'Status': 'OK', 'message': msg}, 200


@api.route('/songs/list', methods=['GET'])
class ListSongs(Resource):
    def get(self):
        songs = Song.query.all()
        return {'Status': 'OK', 'songs': [song.json() for song in songs]}, 200


@api.route('/songs/<int:id>', methods=['PUT'])
class ListSongs(Resource):
    @api.expect(edit_song_model)
    @jwt_required()
    def put(self, id):
        song = Song.query.filter_by(id=id).first()
        if song:
            song.update(**request.json)
        return {'Status': 'OK', 'song': song.json() or []}, 200


@api.route('/categories/new', methods=['POST'])
class CreateCategories(Resource):
    @api.expect(category_model)
    @jwt_required
    def post(self):
        id = get_jwt_identity()
        category = Category(**request.json, created_by=id)
        category.save()
        return {'Status': 'OK', 'category': category.json()}, 200


@api.route('/categories/list', methods=['GET'])
class ListCategories(Resource):
    def get(self):
        categories = Category.query.order_by(Category.name).all()
        return {'Status': 'OK', 'categories': [category.json() for category in categories]}, 200


@api.route('/title/<title>', methods=['GET'])
class GetSongByTitle(Resource):
    def get(self, title):
        slug_ilike = Song.slugified_title.ilike(f"%%{slugify(title)}%%")
        slug_similar = func.similarity(
            Song.slugified_title, slugify(title)) > 0.5
        songs = Song.query.filter(
            slug_ilike | slug_similar).order_by(Song.title).all()
        if songs:
            return {'status': 'OK', 'songs': [song.json() for song in songs]}, 200
        else:
            return {'status': 'Error', 'songs': [], 'message': 'Song not found'}


@api.route('/artist/<artist>', methods=['GET'])
class GetSongsByArtist(Resource):
    def get(self, artist):
        slug_ilike = Song.slugified_artist.ilike(f"%%{slugify(artist)}%%")
        slug_similar = func.similarity(
            Song.slugified_artist, slugify(artist)) > 0.5
        songs = Song.query.filter(
            slug_ilike | slug_similar).order_by(Song.title).all()
        artists = {song.artist for song in songs}
        if songs:
            return {'status': 'OK', 'songs': [song.json() for song in songs], 'artists': list(artists)}, 200
        else:
            return {'status': 'Error', 'message': 'No songs found'}, 404


@api.route('/category/<category_slug>', methods=['GET'])
class GetSongsByCategory(Resource):
    def get(self, category_slug):
        name = Category.query.filter_by(slug=category_slug).first().name
        songs = Song.query.join(Category, Song.categories).filter(
            Song.categories.any(Category.slug == category_slug)).all()
        if songs:
            return {'status': 'OK', 'name': name, 'songs': [song.json() for song in songs]}, 200
        else:
            return {'status': 'Error', 'songs': [], 'message': 'Not found'}, 404


@api.route('/<artist>/<title>', methods=['GET'])
class GetSongByTitleAndArtist(Resource):
    def get(self, artist, title):
        data = []
        slug_artist_ilike = Song.slugified_artist.ilike(
            f"%%{slugify(artist)}%%")
        slug_artist_similar = func.similarity(
            Song.slugified_artist, slugify(artist)) > 0.5
        slug_title_ilike = Song.slugified_title.ilike(f"%%{slugify(title)}%%")
        slug_title_similar = func.similarity(
            Song.slugified_title, slugify(title)) > 0.5
        song = Song.query.filter(
            (slug_artist_ilike | slug_artist_similar) & (slug_title_ilike | slug_title_similar)).order_by(Song.title).first()
        if song:
            data = song.json()
            song.increment_access_count()
            return {'status': 'OK', 'song': data}, 200
        else:
            return {'status': 'Error', 'song': [], 'message': 'Song not found'}, 404


@api.route('/artist/list', methods=['GET'])
class GetSongByTitleAndArtist(Resource):
    def get(self):
        artists = {row.artist for row in db.session.query(
            Song.artist).order_by(Song.title).all()}
        if artists:
            return {'status': 'OK', 'artists': list(artists)}, 200
        else:
            return {'status': 'Error', 'artists': [], 'message': 'Song not found'}, 404


@api.route('/<query_string>', methods=['GET'])
class GetSongByGenericSearch(Resource):
    def get(self, query_string):
        slug_artist_ilike = Song.slugified_artist.ilike(
            f"%%{slugify(query_string)}%%")
        slug_artist_similar = func.similarity(
            Song.slugified_artist, slugify(query_string)) > 0.5
        slug_title_ilike = Song.slugified_title.ilike(
            f"%%{slugify(query_string)}%%")
        slug_title_similar = func.similarity(
            Song.slugified_title, slugify(query_string)) > 0.5
        query = Song.query.join(Category, Song.categories).filter(
            slug_artist_ilike | slug_artist_similar | slug_title_ilike | slug_title_similar)
        songs = query.all()
        artists = [song.artist for song in query.filter(
            slug_artist_ilike | slug_artist_similar).all()]

        return {'status': 'OK', 'songs': [song.json() for song in songs], 'artists': artists}, 200
        # else:
        #     return {'status':'Error', 'song':[],'message':'Song not found'}
