from app import db

from slugify import slugify

song_category = db.Table('song_category',
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)

song_playlist = db.Table('song_playlist',
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'))
)

class Song(db.Model):
    __tablename__ = 'songs'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    slugified_title=db.Column(db.String(100), nullable=False)
    artist=db.Column(db.String(100), nullable=False)
    slugified_artist=db.Column(db.String(100), nullable=False)
    lyrics=db.Column(db.String, nullable=False)
    video_url=db.Column(db.String(100), nullable=False)
    created_by=db.Column(db.Integer, db.ForeignKey('users.id'))
    access_count = db.Column(db.Integer, default=0)

    def __init__(self, title, artist, lyrics, video_url, created_by):#, category_id):
        self.title = title
        self.slugified_title = slugify(title)
        self.artist = artist
        self.slugified_artist = slugify(artist)
        self.lyrics = lyrics
        self.video_url = video_url
        self.created_by = created_by
        self.access_count = 0
       
        # db.session.query(Song).filter(
        #     or_(
        #         func.similarity(Song.title, "Marcos") > 0.6,
        #         func.similarity(Song.artist, "Marcos") > 0.4,
        #     ),
        #     and_(Song.title != '0'),
        # ).order_by(Song.title).limit(20).all()
    def increment_access_count(self):
        self.access_count += 1
        db.session.commit()        

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, artist, lyrics, video_url, categories):
        self.title = title
        self.slugified_title = slugify(title)
        self.artist = artist
        self.slugified_artist = slugify(artist)
        self.lyrics = lyrics
        self.video_url = video_url
        self.categories = Category.query.filter(Category.name.in_(categories)).all()
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'lyrics': self.lyrics,
            'video_url': self.video_url,
            'slug_title': self.slugified_title,
            'slug_artist': self.slugified_artist,
            'created_by': self.created_by,
            'access_count': self.access_count,
            'categories': [category.json() for category in self.categories]
        }
        
    def __repr__(self):
        return f"{self.title} - {self.artist}"

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    slug = db.Column(db.String)
    songs = db.relationship('Song', secondary=song_category, backref="categories")#backref='category', lazy=True, cascade="all, delete-orphan")
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, created_by) -> None:
        self.name = name
        self.slug = slugify(name)
        self.created_by = created_by

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    slug = db.Column(db.String)
    songs = db.relationship('Song', secondary=song_playlist, backref="playlists")
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, created_by) -> None:
        self.name = name
        self.slug = slugify(name)
        self.created_by = created_by