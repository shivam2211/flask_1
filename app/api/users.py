from app.api import bp
from flask import jsonify
from app.models import User, Post
from flask import request
from flask import url_for
from app import db
from app.api.errors import bad_request
from flask import g, abort
from app.api.auth import token_auth
from flask_login import logout_user, current_user
from app.forms import PostForm

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        abort(403)

    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/logout')
def logout():
    logout_user()
    return jsonify({'status':'Logged out'})
    
@bp.route('/post', methods=['GET'])
@token_auth.login_required
def posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(
        Post.query.order_by(Post.timestamp.desc()), 
        page, per_page, 'api.posts')
    return jsonify(data)


@bp.route('/post', methods=['POST'])
@token_auth.login_required
def post():
    data = request.get_json() or {}
    if 'post' not in data:
        return bad_request('must write something...')
    
    post = Post()
    post.from_dict(data)
    db.session.add(post)
    db.session.commit()
    return jsonify({'status':'Successfully Posted'})