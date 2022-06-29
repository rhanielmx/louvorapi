from app import db

from slugify import slugify

song_category = db.Table('song_category',
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
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
    # category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


    def __init__(self, title, artist, lyrics, video_url):#, category_id):
        self.title = title
        self.slugified_title = slugify(title)
        self.artist = artist
        self.slugified_artist = slugify(artist)
        self.lyrics = lyrics
        self.video_url = video_url
        # self.category_id = category_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'lyrics': self.lyrics,
            'video_url': self.video_url#,
            # 'category_id': self.category_id
        }
        
    def __repr__(self):
        return f"{self.title} - {self.artist}"

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    songs = db.relationship('Song', secondary=song_category, backref="categories")#backref='category', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name) -> None:
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
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
