from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
import rang
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions
import datetime
from mutagen.mp3 import MP3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/Music'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SECRET_KEY'] = 'aaaa'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg', 'mp4', 'mp3'}


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    album = db.relationship("Album", backref="users", order_by="Album.id")
    music = db.relationship("Music", backref="users", order_by="Music.id")
    play = db.relationship("Playlist", backref="users", order_by="Playlist.id")
    like = relationship("Album", backref="liked_by", secondary="like", order_by="Album.id")
    name = Column(String)
    password = Column(String)
    gmail = Column(String)
    photo = Column(String)
    admin = Column(Boolean)
    artist = Column(Boolean)
    check = Column(Boolean)


class Genre(db.Model):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    albums = db.relationship("Album", backref="genre", order_by="Album.id")
    rgba = Column(String)
    photo = Column(String)


class Album(db.Model):
    __tablename__ = 'album'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(String)
    caption = Column(String)
    genrea = Column(Integer, ForeignKey('genre.id'))
    photo = Column(String)
    user = Column(Integer, ForeignKey('users.id'))
    rgba = Column(String)
    music = db.relationship("Music", backref="album", order_by="Music.id")


class Playlist(db.Model):
    __tablename__ = 'play'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    caption = Column(String)
    photo = Column(String)
    user = Column(Integer, ForeignKey('users.id'))
    musicscha = relationship("Music", backref="play", secondary="musics", order_by="Music.id")


class Music(db.Model):
    __tablename__ = 'music'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(String)
    albom = Column(Integer, ForeignKey('album.id'))
    user = Column(Integer, ForeignKey('users.id'))
    duration = Column(String)
    genreas = Column(Integer, ForeignKey('genre.id'))
    text = Column(String)
    audio = Column(String)
    data = Column(String)


db.Table('like',
         db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

db.Table('musics',
         db.Column('music_id', db.Integer, db.ForeignKey('music.id')),
         db.Column('play_id', db.Integer, db.ForeignKey('play.id')))


def current_user():
    user_now = None
    if 'gmail' in session:
        user_get = Users.query.filter(Users.gmail == session['gmail']).first()
        user_now = user_get

    return user_now


def users_folder():
    upload_folder = 'static/img/'
    return upload_folder


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
    return value and type_file


@app.route('/')
def hello_world():
    genres = Genre.query.all()
    artist = Users.query.filter(Users.artist).all()
    albums = Album.query.all()
    user = current_user()
    if user:
        playlist = Playlist.query.filter(Playlist.user == user.id).all()
        my_album = Album.query.filter(Album.user == user.id).all()
        return render_template('index.html', user=user, genres=genres, artist=artist, albums=my_album,
                               playlist=playlist)
    return render_template('index.html', user=user, genres=genres, artist=artist, albums=albums)


@app.route('/album')
def album():
    user = current_user()
    return render_template('album.html', user=user)


@app.route('/search', methods=['POST', 'GET'])
def search():
    user = current_user()
    genres = Genre.query.order_by(Genre.id.desc()).all()
    if request.method == 'POST':
        name = request.form.get('name')
        photo = request.files.get('photo')
        if photo and checkFile(photo.filename):
            folder = users_folder()
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            get_photo_url = folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            rang2 = rang.get_average_color(get_photo_url)
            ranag = ", ".join(map(str, rang2))
            add = Genre(name=name, photo=photo_url, rgba=ranag)
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('search'))
    return render_template('search.html', user=user, genres=genres)


@app.route('/send')
def send():
    user = current_user()
    genres = Genre.query.order_by(Genre.id.desc()).all()
    serialized_genres = []
    for genre in genres:
        serialized_genre = {
            'id': genre.id,
            'name': genre.name,
            'rgba': genre.rgba,
            'photo': genre.photo,
        }
        serialized_genres.append(serialized_genre)
    if user:
        if user.admin:
            return jsonify({"result": serialized_genres})
    return jsonify()


@app.route('/edit_genre', methods=["POST", "GET"])
def edit_genre():
    if request.method == "POST":
        photo = request.files.get('image')
        name = request.form.get('name')
        ids = request.form.get('id')
        folder = users_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            get_photo_url = folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            rang2 = rang.get_average_color(get_photo_url)
            ranag = ", ".join(map(str, rang2))
            Genre.query.filter(Genre.id == ids).update({
                "name": name,
                "rgba": ranag,
                "photo": photo_url,
            })
            db.session.commit()
        else:
            Genre.query.filter(Genre.id == ids).update({
                "name": name,
            })
            db.session.commit()
    genres = Genre.query.order_by(Genre.id.desc()).all()
    serialized_genres = []
    for genre in genres:
        serialized_genre = {
            "id": genre.id,
            "name": genre.name,
            "rgba": genre.rgba,
            "photo": genre.photo,
        }
        serialized_genres.append(serialized_genre)
    return jsonify({"result": serialized_genres})


@app.route('/login', methods=["POST", "GET"])
def login():
    user = current_user()
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        username = Users.query.filter(Users.gmail == name).first()
        if username:
            if check_password_hash(username.password, password):
                session["gmail"] = username.gmail
                return redirect(url_for('hello_world'))
            else:
                return render_template('login.html', error='Username or password incorect')
    return render_template('login.html')


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == "POST":
        name = request.form.get('name')
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        checkbox = request.form.get('checkbox')
        username = Users.query.filter(Users.gmail == gmail).first()
        if username:
            return redirect(url_for('login'))
        else:
            hashed = generate_password_hash(password=password, method='sha256')
            if password == 'Admin':
                add = Users(name=name, password=hashed, admin=True,
                            gmail=gmail, photo='static/img/1.jpg', check=True)
            else:
                if checkbox == "on":
                    chek = True
                else:
                    chek = False
                add = Users(name=name, password=hashed,
                            gmail=gmail, photo='static/img/1.jpg', check=chek)
            db.session.add(add)
            db.session.commit()
            session["gmail"] = gmail
            return redirect(url_for('hello_world'))
    return render_template('reg.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    user = current_user()
    return render_template('add.html', user=user)


@app.route('/mymus', methods=['POST', 'GET'])
def mymus():
    genres = Genre.query.all()
    artist = Users.query.filter(Users.artist).all()
    user = current_user()
    if user:
        my_album = Album.query.filter(Album.user == user.id).all()
        musics = Music.query.filter(Music.user == user.id).all()
        return render_template('mus.html', user=user, genres=genres, artist=artist, albums=my_album, music=musics)
    return render_template('mus.html', user=user)


@app.route('/add_mus', methods=['POST', 'GET'])
def add_mus():
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        genre = request.form.get('genre')
        album = request.form.get('album')
        texta = request.form.get('text')
        music = request.files.get('music')
        photo = request.files.get('photo')
        folder = users_folder()
        music_file = secure_filename(music.filename)
        music_url = '/' + folder + music_file
        music_url2 = folder + music_file
        app.config['UPLOAD_FOLDER'] = folder
        music.save(os.path.join(app.config["UPLOAD_FOLDER"], music_file))
        mp3_file = MP3(music_url2)
        duration_seconds = mp3_file.info.length
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        mus = f'{minutes}:{seconds}'
        bugun = datetime.datetime.now()
        sana = bugun.strftime("%Y-%m-%d")
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            add = Music(name=name, genreas=genre,
                        albom=album, photo=photo_url, text=texta, duration=mus, user=user.id, audio=music_url,
                        data=sana)
            db.session.add(add)
            db.session.commit()
            return redirect(url_for('mymus'))
        else:
            add = Music(name=name, genreas=genre,
                        albom=album, text=text, duration=mus, user=user.id, audio=music_url, data=sana)
            db.session.add(add)
            db.session.commit()
            return redirect(url_for('mymus'))
    return render_template('mus.html')


@app.route('/delete_genre/<int:id>')
def delete_genre(id):
    filter = Genre.query.filter(Genre.id == id).delete()
    db.session.commit()
    return redirect(url_for('search'))


@app.route('/album_add', methods=["POST", "GET"])
def album_add():
    user = current_user()
    genres = Genre.query.order_by(Genre.id.desc()).all()
    artist = Users.query.filter(Users.artist).all()
    if request.method == 'POST':
        name = request.form.get('name')
        caption = request.form.get('caption')
        genre = request.form.get('genre')
        artist = request.form.get('artist')
        photo = request.files.get('photo')
        bugun = datetime.datetime.now()
        sana = bugun.strftime("%Y-%m-%d")
        if photo and checkFile(photo.filename):
            folder = users_folder()
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            get_photo_url = folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            rang2 = rang.get_average_color(get_photo_url)
            ranag = ", ".join(map(str, rang2))
            add = Album(name=name, photo=photo_url, rgba=ranag, user=artist, genrea=genre, caption=caption, data=sana)
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('album_add'))
    return redirect(url_for('hello_world', user=user, genres=genres, artist=artist))


@app.route('/delete_album/<int:id>')
def delete_album(id):
    filter = Album.query.filter(Album.id == id).first()
    db.session.delete(filter)
    db.session.commit()
    return redirect(url_for('hello_world'))


@app.route('/edit_album', methods=["POST", "GET"])
def edit_album():
    user = current_user()
    if request.method == "POST":
        photo = request.files.get('image')
        name = request.form.get('name')
        caption = request.form.get('caption')
        ids = request.form.get('id')
        folder = users_folder()
        print(caption, name, ids)
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            get_photo_url = folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            rang2 = rang.get_average_color(get_photo_url)
            ranag = ", ".join(map(str, rang2))
            Album.query.filter(Album.id == ids).update({
                "name": name,
                'caption': caption,
                "rgba": ranag,
                "photo": photo_url,
            })
            db.session.commit()
        else:
            Album.query.filter(Album.id == ids).update({
                'caption': caption,
                "name": name,
            })
            db.session.commit()
    genres = Album.query.filter(Album.user == user.id).all()
    serialized_genres = []
    for genre in genres:
        serialized_genre = {
            "id": genre.id,
            "name": genre.name,
            "user": genre.users.name,
            "caption": genre.caption,
            "photo": genre.photo,
        }
        serialized_genres.append(serialized_genre)
    return jsonify({"result": serialized_genres})


@app.route('/api')
def api():
    user = current_user()
    musics = Music.query.filter(Music.user == user.id).all()
    serialized_genres = []
    for music in musics:
        filter = Users.query.filter(Users.id == music.user).first()
        print(filter)
        serialized_genre = {
            'number': music.id,
            'photo': music.photo,
            'song': music.name,
            'artist': filter.name,
            'text': music.text,
            'music': music.audio,
            'album': music.album.name,
            'data': music.data,
            'duration': music.duration
        }
        serialized_genres.append(serialized_genre)
    if user:
        if user.admin or user.artist:
            return jsonify(serialized_genres)
    return jsonify()


@app.route('/edit_music', methods=["POST", "GET"])
def edit_music():
    user = current_user()
    if request.method == "POST":
        photo = request.files.get('image')
        name = request.form.get('name')
        caption = request.form.get('caption')
        ids = request.form.get('id')
        folder = users_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            Music.query.filter(Music.id == ids).update({
                "name": name,
                'text': caption,
                "photo": photo_url,
            })
            db.session.commit()
        else:
            Music.query.filter(Music.id == ids).update({
                'text': caption,
                "name": name,
            })
            db.session.commit()
    musics = Music.query.filter(Music.user == user.id).all()
    serialized_genres = []
    for music in musics:
        filter = Users.query.filter(Users.id == music.user).first()
        print(filter)
        serialized_genre = {
            'number': music.id,
            'photo': music.photo,
            'song': music.name,
            'artist': filter.name,
            'text': music.text,
            'music': music.audio,
            'album': music.album.name,
            'data': music.data,
            'duration': music.duration
        }
        serialized_genres.append(serialized_genre)
    return jsonify(serialized_genres)


@app.route('/genres/<string:genre>')
def genres(genre):
    user = current_user()
    filter = Genre.query.filter(Genre.name == genre).first()
    albums = Album.query.filter(Album.genrea == filter.id).all()
    return render_template('genre.html', albums=albums, user=user)


@app.route('/album/<string:name>')
def album_name(name):
    user = current_user()
    playlists = Playlist.query.filter(Playlist.user == user.id).all()
    filter = Album.query.filter(Album.name == name).first()
    musics = Music.query.filter(Music.albom == filter.id).all()
    api_music(name)
    return render_template('album.html', musics=musics, user=user, album=filter, playlist=playlists)


@app.route('/api_music/<string:name>')
def api_music(name):
    user = current_user()
    filter = Album.query.filter(Album.name == name).first()
    musics = Music.query.filter(Music.albom == filter.id).all()
    vount = Music.query.filter(Music.albom == filter.id).count()
    albumss = {
        'name': filter.name,
        'caption': filter.caption,
        'songs': vount,
        'photo': filter.photo,
        'rgba': filter.rgba

    }
    serialized_genres = []
    for music in musics:
        filter = Users.query.filter(Users.id == music.user).first()
        serialized_genre = {
            'number': music.id,
            'photo': music.photo,
            'song': music.name,
            'artist': filter.name,
            'text': music.text,
            'music': music.audio,
            'album': music.album.name,
            'data': music.data,
            'duration': music.duration
        }
        serialized_genres.append(serialized_genre)
    result = {
        'music': serialized_genres,
        'album': albumss
    }
    return jsonify(result)


@app.route('/delete_mus/<int:id>')
def delete_mus(id):
    user = current_user()
    filter = Music.query.filter(Music.id == id).first()
    db.session.delete(filter)
    db.session.commit()
    return redirect(url_for('mymus'), user=user)


@app.route('/play_add', methods=["POST", "GET"])
def play_add():
    user = current_user()
    if request.method == 'POST':
        name = request.form.get('name')
        caption = request.form.get('caption')
        photo = request.files.get('photo')
        if photo and checkFile(photo.filename):
            folder = users_folder()
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = Playlist(name=name, photo=photo_url, caption=caption, user=user.id)
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('play_add'))
    return redirect(url_for('hello_world', user=user))


@app.route('/delete_play/<int:id>')
def delete_play(id):
    filter = Playlist.query.filter(Playlist.id == id).first()
    db.session.delete(filter)
    db.session.commit()
    return redirect(url_for('hello_world'))


@app.route('/edit_play', methods=["POST", "GET"])
def edit_play():
    user = current_user()
    if request.method == "POST":
        photo = request.files.get('image')
        name = request.form.get('name')
        caption = request.form.get('caption')
        ids = request.form.get('id')
        folder = users_folder()
        print(caption, name, ids)
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            Playlist.query.filter(Playlist.id == ids).update({
                "name": name,
                'caption': caption,
                "photo": photo_url,
            })
            db.session.commit()
        else:
            Playlist.query.filter(Playlist.id == ids).update({
                'caption': caption,
                "name": name,
            })
            db.session.commit()
    genres = Playlist.query.filter(Playlist.user == user.id).all()
    serialized_genres = []
    for genre in genres:
        serialized_genre = {
            "id": genre.id,
            "name": genre.name,
            "user": genre.users.name,
            "caption": genre.caption,
            "photo": genre.photo,
        }
        serialized_genres.append(serialized_genre)
    return jsonify({"result": serialized_genres})


@app.route('/like', methods=["POST", "GET"])
def like():
    user = current_user()
    if request.method == "POST":
        ids = request.form.get('idssa')
        post_now = Album.query.filter(Album.id == ids).first()
        user_now = Users.query.filter(Users.gmail == session['gmail']).first()
        user_now.like.append(post_now)
        db.session.commit()
    return jsonify()


@app.route('/dislike', methods=["POST", "GET"])
def dislike():
    user = current_user()
    if request.method == "POST":
        ids = request.form.get('idssa')
        post_now = Album.query.filter(Album.id == ids).first()
        user_now = Users.query.filter(Users.gmail == user.gmail).first()
        user_now.like.remove(post_now)
        db.session.commit()
    return jsonify()


@app.route('/liked')
def liked():
    user = current_user()
    albums = user.like
    user = current_user()
    playlists = Playlist.query.filter(Playlist.user == user.id).all()
    return render_template('genre.html', albums=albums, user=user, playlist=playlists)


@app.route('/playlist/<string:name>')
def playlist_name(name):
    user = current_user()
    playlists = Playlist.query.filter(Playlist.user == user.id).all()
    # filter = Playlist.query.filter(Playlist.name == name).first()
    # musics = Music.query.filter(Music.albom == 3).all()
    api_play(name)
    return render_template('playlist.html', user=user, album=playlists, playlist=playlists)


@app.route('/api_play/<string:name>')
def api_play(name):
    user = current_user()
    filter = Playlist.query.filter(Playlist.name == name).first()
    musics = filter.musicscha
    albumss = {
        'name': filter.name,
        'caption': filter.caption,
        'photo': filter.photo,

    }
    serialized_genres = []
    for music in musics:
        filter = Users.query.filter(Users.id == music.user).first()
        serialized_genre = {
            'number': music.id,
            'photo': music.photo,
            'song': music.name,
            'artist': filter.name,
            'text': music.text,
            'music': music.audio,
            'album': music.album.name,
            'data': music.data,
            'duration': music.duration
        }
        serialized_genres.append(serialized_genre)
    result = {
        'music': serialized_genres,
        'album': albumss
    }
    return jsonify(result)


@app.route('/del_play/<int:id>/<string:id2>', methods=["POST", "GET"])
def del_play(id, id2):
    user = current_user()
    post_now = Music.query.filter(Music.id == id).first()
    user_now = Playlist.query.filter(Playlist.name == id2).first()
    user_now.musicscha.remove(post_now)
    db.session.commit()
    return redirect(url_for('playlist_name', name=id2))


@app.route('/search_music', methods=['POST', "GET"])
def search_music():
    user = current_user()
    if request.method == "POST":
        text = request.form.get('text')
        musics = Music.query.filter(Music.name == text).all()
        serialized_genres = []
        for genre in musics:
            serialized_genre = {
                "id": genre.id,
                "name": genre.name,
                "user": genre.users.name,
                "photo": genre.photo,
            }
            serialized_genres.append(serialized_genre)
    return jsonify(serialized_genres)


@app.route('/add_play/<int:id>/<string:id2>', methods=["POST", "GET"])
def add_play(id, id2):
    user = current_user()
    post_now = Music.query.filter(Music.id == id).first()
    user_now = Playlist.query.filter(Playlist.name == id2).first()
    user_now.musicscha.append(post_now)
    db.session.commit()
    return redirect(url_for('api_play', name=id2))


@app.route('/signout')
def singout():
    user = current_user()
    session['gmail'] = ""
    return redirect(url_for('login'))


@app.route('/profile', methods=["POST", "GET"])
def profile():
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        photo = request.files['photo']
        folder = users_folder()
        hashed = generate_password_hash(password=password, method='sha256')
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            Users.query.filter(Users.id == user.id).update({
                "name": name,
                "password": hashed,
                "gmail": username,
                "photo": photo_url,
            })
            db.session.commit()
        else:
            Users.query.filter(Users.id == user.id).update({
                "name": name,
                "password": hashed,
                "gmail": username,
            })
            db.session.commit()
            return redirect(url_for('profile'))
    return redirect(url_for('hello_world'))


@app.route('/admin')
def admin():
    user = current_user()
    all_user = Users.query.all()
    return render_template('admin.html', user=user, all_user=all_user)


@app.route('/check_user_ok/<int:user_id_for_check>', methods=['POST', 'GET'])
def check_user_ok(user_id_for_check):
    if request.method == "POST":
        check = request.form.get('check')
        if check == 'True':
            Users.query.filter(Users.id == user_id_for_check).update({
                "artist": True,
                "admin": True,
                "check": False
            })
            db.session.commit()
        else:
            Users.query.filter(Users.id == user_id_for_check).update({
                "artist": False,
                "admin": False,
                "check": False
            })
            db.session.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))




if __name__ == '__main__':
    app.run()
