import pytest
from app import app, db, Post
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import logging

@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    with app.test_client() as client:
        with app.app_context():
            # Set up the database for testing
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_index(client):
    """Test the index page"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'No posts' in rv.data

def test_new_post(client):
    """Test creating a new post"""
    rv = client.post('/new-post', data=dict(
        title='Test Post',
        content='This is a test post.'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Test Post' in rv.data
    assert b'This is a test post.' in rv.data

def test_view_post(client):
    """Test viewing a post"""
    # First, create a post
    client.post('/new-post', data=dict(
        title='Test Post',
        content='This is a test post.'
    ), follow_redirects=True)
    # Then, view the post
    rv = client.get('/post/1')
    assert rv.status_code == 200
    assert b'Test Post' in rv.data
    assert b'This is a test post.' in rv.data

def test_edit_post(client):
    """Test editing a post"""
    # First, create a post
    client.post('/new-post', data=dict(
        title='Test Post',
        content='This is a test post.'
    ), follow_redirects=True)
    # Then, edit the post
    rv = client.post('/post/1/edit', data=dict(
        title='Updated Post',
        content='This is an updated test post.'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Updated Post' in rv.data
    assert b'This is an updated test post.' in rv.data

def test_delete_post(client):
    """Test deleting a post"""
    # First, create a post
    client.post('/new-post', data=dict(
        title='Test Post',
        content='This is a test post.'
    ), follow_redirects=True)
    # Then, delete the post
    rv = client.post('/post/1/delete', follow_redirects=True)
    assert rv.status_code == 200
    assert b'No posts' in rv.data
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Determine the database configuration based on the environment
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
