from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import logging
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the database configuration based on the environment
if os.getenv('ENV') == 'test':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    db_user = os.getenv('USER', 'user')
    db_password = os.getenv('PASSWORD', 'password')
    db_host = os.getenv('HOST', 'localhost')
    db_port = os.getenv('PORT', '5432')
    db_name = os.getenv('DATABASE', 'dbname')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory('assets', filename)

@app.route('/')
def index():
    posts = Post.query.all()
    posts_list = [{'id': post.id, 'title': post.title, 'content': post.content} for post in posts]
    return render_template('index.html', posts=posts_list)

@app.route('/post/<int:id>', methods=['GET'])
def view_post(id):
    post = db.session.get(Post, id)
    if post is None:
        return "Post not found", 404
    post_dict = {'id': post.id, 'title': post.title, 'content': post.content}
    return render_template('view_post.html', post=post_dict)

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = db.session.get(Post, id)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('view_post', id=id))
    post_dict = {'id': post.id, 'title': post.title, 'content': post.content}
    return render_template('edit_post.html', post=post_dict)

@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = db.session.get(Post, id)
    if post is None:
        return "Post not found", 404
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True, port=5000, host='0.0.0.0')