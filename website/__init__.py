from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_required
import os


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask("__name__", template_folder='website/templates', static_folder='website/static')
    app.config['SECRET_KEY'] = 'jfpamcoakr ncldprnkea'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    UPLOAD_FOLDER = 'website/static/sneat/assets/img/avatars'
    ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Bank, Post, Day_report

    with app.app_context():
        db.create_all()
        try:
            User.create_admin()
            User.create_random_staffs()
            Bank.create_bank_data()
            User.create_random_staffs()
            Post.create_random_post()
        except Exception as e:
            print(f'Exception: {e}')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = ""
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/upload', methods=['POST'])
    @login_required
    def upload_file():
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['image']
        user_id = request.form.get('user_id')

        if not user_id:
            return jsonify({'error': 'Missing user_id in the request'}), 400

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Extract file extension
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        
        # Rename file to user_id.filetype
        new_filename = f"{user_id}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)

        return jsonify({'message': 'File uploaded successfully', 'filename': new_filename}), 200

    return app