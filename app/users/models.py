from app import db
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    last_accessed = db.Column(db.DateTime)
    role = db.Column(db.String(120), nullable=False)
    avatar_url = db.Column(db.String(120), nullable=True, default='')
    songs = db.relationship('Song', backref='creator', lazy=True)
    categories = db.relationship('Category', backref='creator', lazy=True)
    playlist = db.relationship('Playlist', backref='creator', lazy=True)

    def __init__(self, username, email, password, first_name, last_name, role):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.last_accessed = datetime.utcnow()-timedelta(hours=3)
        self.avatar_url = 'https://gravatar.com/avatar/8aec9a741d3d00fc127210a085df99b1?s=200&d=mp&r=x'
        self.role = role

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'last_accessed': self.last_accessed.strftime('%d/%m/%Y %H:%M:%S'),
            'role': self.role,
            'avatar_url': self.avatar_url,
            'songs': [song.id for song in self.songs],
            'categories': [category.json() for category in self.categories]
        }

    def updateLastAcessed(self):
        self.last_accessed = datetime.utcnow()-timedelta(hours=3)
        db.session.commit()

    def update(self, username, email, password, firstName, lastName, role):
        self.username = username
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.role = role
        db.session.commit()

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
