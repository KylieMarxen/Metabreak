from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import redis
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy import or_, func, desc
import json

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///metabreak.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads/covers'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# Initialize CORS
app.config['CORS_HEADERS'] = 'Content-Type'

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

app.after_request(add_cors_headers)

# Handle OPTIONS
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])

def handle_options(path):
    response = app.make_default_options_response()
    response = add_cors_headers(response)
    return response

# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"]
# )

# Redis for caching
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
except:
    redis_client = None
    app.logger.warning("Redis not available - caching disabled")

# Logging configuration
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/metabreak.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('MetaBreak startup')

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, moderator, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='author_rel', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author_rel', lazy='dynamic', cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='user_rel', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'review_count': self.reviews.count()
        }

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    studio = db.Column(db.String(200))
    release_year = db.Column(db.Integer)
    cover_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='game_rel', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_stats=True):
        data = {
            'id': self.id,
            'external_id': self.external_id,
            'title': self.title,
            'studio': self.studio,
            'release_year': self.release_year,
            'cover_url': self.cover_url,
            'description': self.description,
        }
        
        if include_stats:
            review_count = self.reviews.count()
            avg_score = db.session.query(func.avg(Review.score)).filter(Review.game_id == self.id).scalar() or 0
            data['review_count'] = review_count
            data['average_score'] = round(float(avg_score), 1) if avg_score else 0
        
        return data

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 0-100
    difficulty = db.Column(db.Integer, nullable=False)  # 1-5
    platform = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='review_rel', lazy='dynamic', cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='review_rel', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_author=True, include_game=True):
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'score': self.score,
            'difficulty': self.difficulty,
            'platform': self.platform,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'comment_count': self.comments.count(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_author:
            data['author'] = {
                'id': self.author_rel.id,
                'username': self.author_rel.username
            }
        
        if include_game:
            data['game'] = {
                'id': self.game_rel.id,
                'title': self.game_rel.title,
                'cover_url': self.game_rel.cover_url
            }
        
        return data

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author': {
                'id': self.author_rel.id,
                'username': self.author_rel.username
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Vote(db.Model):
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'review_id', name='unique_user_review_vote'),)

# ==================== HELPER FUNCTIONS ====================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_cache(key):
    if redis_client:
        try:
            return redis_client.get(key)
        except:
            return None
    return None

def set_cache(key, value, expiration=300):
    if redis_client:
        try:
            redis_client.setex(key, expiration, value)
        except:
            pass

def clear_cache_pattern(pattern):
    if redis_client:
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
        except:
            pass

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'Unhandled exception: {str(e)}')
    return jsonify({'error': 'An unexpected error occurred'}), 500

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
#@limiter.limit("5 per hour")
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    username = data['username'].strip()
    email = data['email'].strip().lower()
    password = data['password']
    
    if len(username) < 3 or len(username) > 80:
        return jsonify({'error': 'Username must be 3-80 characters'}), 400
    
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password_hash=hashed_password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))
        
        app.logger.info(f'New user registered: {username}')
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Registration error: {str(e)}')
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
#@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    access_token = create_access_token(identity=str(user.id))
    
    app.logger.info(f'User logged in: {user.username}')
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    # Serve HTML files
    if filename.endswith('.html'):
        return send_from_directory('.', filename)
    # Serve JS files
    elif filename.startswith('js/'):
        return send_from_directory('.', filename)
    # Serve other static files
    elif os.path.exists(filename):
        return send_from_directory('.', filename)
    # Default to index
    return send_from_directory('.', 'index.html')

# ==================== GAME ROUTES ====================

@app.route('/api/games', methods=['GET'])
def get_games():
    # Check cache first
    cache_key = 'games:all'
    cached = get_cache(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200
    
    games = Game.query.all()
    result = [game.to_dict() for game in games]
    
    # Cache for 5 minutes
    set_cache(cache_key, json.dumps(result), 300)
    
    return jsonify(result), 200

@app.route('/api/games/search', methods=['GET'])
def search_games():
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'error': 'Query must be at least 2 characters'}), 400
    
    # Check cache
    cache_key = f'games:search:{query.lower()}'
    cached = get_cache(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200
    
    games = Game.query.filter(
        or_(
            Game.title.ilike(f'%{query}%'),
            Game.studio.ilike(f'%{query}%')
        )
    ).limit(20).all()
    
    result = [game.to_dict() for game in games]
    
    # Cache for 10 minutes
    set_cache(cache_key, json.dumps(result), 600)
    
    return jsonify(result), 200

@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game.to_dict()), 200

# ==================== REVIEW ROUTES ====================

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    sort_by = request.args.get('sort', 'newest')
    game_id = request.args.get('game_id', type=int)
    
    # Build query
    query = Review.query
    
    if game_id:
        query = query.filter_by(game_id=game_id)
    
    # Apply sorting
    if sort_by == 'newest':
        query = query.order_by(desc(Review.created_at))
    elif sort_by == 'oldest':
        query = query.order_by(Review.created_at)
    elif sort_by == 'score-high':
        query = query.order_by(desc(Review.score))
    elif sort_by == 'score-low':
        query = query.order_by(Review.score)
    elif sort_by == 'difficulty-high':
        query = query.order_by(desc(Review.difficulty))
    elif sort_by == 'difficulty-low':
        query = query.order_by(Review.difficulty)
    elif sort_by == 'popular':
        query = query.order_by(desc(Review.upvotes - Review.downvotes))
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'reviews': [review.to_dict() for review in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200

@app.route('/api/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify(review.to_dict()), 200

@app.route('/api/reviews', methods=['POST'])
@jwt_required()
def create_review():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # Validation
    required_fields = ['title', 'content', 'score', 'difficulty', 'platform', 'game_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not (0 <= data['score'] <= 100):
        return jsonify({'error': 'Score must be between 0 and 100'}), 400
    
    if not (1 <= data['difficulty'] <= 5):
        return jsonify({'error': 'Difficulty must be between 1 and 5'}), 400
    
    # Check if game exists
    game = Game.query.get(data['game_id'])
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    review = Review(
        title=data['title'].strip(),
        content=data['content'].strip(),
        score=data['score'],
        difficulty=data['difficulty'],
        platform=data['platform'],
        user_id=user_id,
        game_id=data['game_id']
    )
    
    try:
        db.session.add(review)
        db.session.commit()
        
        # Clear relevant caches
        clear_cache_pattern('games:*')
        
        app.logger.info(f'New review created: {review.id} by user {user_id}')
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Review creation error: {str(e)}')
        return jsonify({'error': 'Failed to create review'}), 500

@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    review = Review.query.get_or_404(review_id)
    
    # Check permissions
    if review.user_id != user_id and user.role not in ['admin', 'moderator']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        review.title = data['title'].strip()
    if 'content' in data:
        review.content = data['content'].strip()
    if 'score' in data:
        if not (0 <= data['score'] <= 100):
            return jsonify({'error': 'Score must be between 0 and 100'}), 400
        review.score = data['score']
    if 'difficulty' in data:
        if not (1 <= data['difficulty'] <= 5):
            return jsonify({'error': 'Difficulty must be between 1 and 5'}), 400
        review.difficulty = data['difficulty']
    if 'platform' in data:
        review.platform = data['platform']
    
    try:
        db.session.commit()
        
        app.logger.info(f'Review updated: {review_id} by user {user_id}')
        
        return jsonify({
            'message': 'Review updated successfully',
            'review': review.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Review update error: {str(e)}')
        return jsonify({'error': 'Failed to update review'}), 500

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    review = Review.query.get_or_404(review_id)
    
    # Check permissions
    if review.user_id != user_id and user.role not in ['admin', 'moderator']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        db.session.delete(review)
        db.session.commit()
        
        # Clear caches
        clear_cache_pattern('games:*')
        
        app.logger.info(f'Review deleted: {review_id} by user {user_id}')
        
        return jsonify({'message': 'Review deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Review deletion error: {str(e)}')
        return jsonify({'error': 'Failed to delete review'}), 500

# ==================== VOTE ROUTES ====================

@app.route('/api/reviews/<int:review_id>/vote', methods=['POST'])
@jwt_required()
def vote_review(review_id):
    user_id = int(get_jwt_identity())
    review = Review.query.get_or_404(review_id)
    data = request.get_json()
    
    if not data or 'vote_type' not in data:
        return jsonify({'error': 'Vote type required'}), 400
    
    vote_type = data['vote_type']
    if vote_type not in ['upvote', 'downvote']:
        return jsonify({'error': 'Invalid vote type'}), 400
    
    # Check for existing vote
    existing_vote = Vote.query.filter_by(user_id=user_id, review_id=review_id).first()
    
    try:
        if existing_vote:
            # Update vote counts
            if existing_vote.vote_type == 'upvote':
                review.upvotes -= 1
            else:
                review.downvotes -= 1
            
            # Change vote or remove it
            if existing_vote.vote_type == vote_type:
                # Remove vote
                db.session.delete(existing_vote)
            else:
                # Change vote
                existing_vote.vote_type = vote_type
                if vote_type == 'upvote':
                    review.upvotes += 1
                else:
                    review.downvotes += 1
        else:
            # New vote
            vote = Vote(user_id=user_id, review_id=review_id, vote_type=vote_type)
            db.session.add(vote)
            
            if vote_type == 'upvote':
                review.upvotes += 1
            else:
                review.downvotes += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Vote recorded',
            'upvotes': review.upvotes,
            'downvotes': review.downvotes
        }), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Vote error: {str(e)}')
        return jsonify({'error': 'Failed to record vote'}), 500

# ==================== COMMENT ROUTES ====================

@app.route('/api/reviews/<int:review_id>/comments', methods=['GET'])
def get_comments(review_id):
    review = Review.query.get_or_404(review_id)
    comments = Comment.query.filter_by(review_id=review_id).order_by(Comment.created_at.desc()).all()
    
    return jsonify([comment.to_dict() for comment in comments]), 200

@app.route('/api/reviews/<int:review_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(review_id):
    user_id = int(get_jwt_identity())
    review = Review.query.get_or_404(review_id)
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Content required'}), 400
    
    content = data['content'].strip()
    if len(content) < 1:
        return jsonify({'error': 'Content cannot be empty'}), 400
    
    comment = Comment(
        content=content,
        user_id=user_id,
        review_id=review_id
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        
        app.logger.info(f'New comment created: {comment.id} by user {user_id}')
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Comment creation error: {str(e)}')
        return jsonify({'error': 'Failed to create comment'}), 500

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != user_id and user.role not in ['admin', 'moderator']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        db.session.delete(comment)
        db.session.commit()
        
        app.logger.info(f'Comment deleted: {comment_id} by user {user_id}')
        
        return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Comment deletion error: {str(e)}')
        return jsonify({'error': 'Failed to delete comment'}), 500

# ==================== FILE UPLOAD ROUTE ====================

@app.route('/api/upload/cover', methods=['POST'])
@jwt_required()
def upload_cover():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role not in ['admin', 'moderator']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        url = f"/uploads/covers/{unique_filename}"
        
        app.logger.info(f'File uploaded: {unique_filename} by user {user_id}')
        
        return jsonify({
            'message': 'File uploaded successfully',
            'url': url
        }), 201
    except Exception as e:
        app.logger.error(f'File upload error: {str(e)}')
        return jsonify({'error': 'Failed to upload file'}), 500

@app.route('/uploads/covers/<filename>')
def serve_cover(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==================== ANALYTICS ROUTES ====================

@app.route('/api/stats/dashboard', methods=['GET'])
def get_dashboard_stats():
    # Check cache
    cache_key = 'stats:dashboard'
    cached = get_cache(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200
    
    total_users = User.query.count()
    total_games = Game.query.count()
    total_reviews = Review.query.count()
    total_comments = Comment.query.count()
    
    # Top rated games
    top_games = db.session.query(
        Game,
        func.avg(Review.score).label('avg_score'),
        func.count(Review.id).label('review_count')
    ).join(Review).group_by(Game.id).order_by(desc('avg_score')).limit(5).all()
    
    result = {
        'total_users': total_users,
        'total_games': total_games,
        'total_reviews': total_reviews,
        'total_comments': total_comments,
        'top_games': [{
            'game': game.to_dict(include_stats=False),
            'average_score': round(float(avg_score), 1),
            'review_count': review_count
        } for game, avg_score, review_count in top_games]
    }
    
    # Cache for 5 minutes
    set_cache(cache_key, json.dumps(result), 300)
    
    return jsonify(result), 200

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        db.engine.connect()
        db_status = 'connected'
    except:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'cache': 'enabled' if redis_client else 'disabled'
    }), 200

# ==================== CLI COMMANDS ====================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@metabreak.com',
            password_hash=bcrypt.generate_password_hash('adminpass123').decode('utf-8'),
            role='admin'
        )
        db.session.add(admin)
    
    # Add games
    games_data = [
        {'external_id': 'g_minecraft', 'title': 'Minecraft', 'studio': 'Mojang Studios', 'release_year': 2011, 'cover_url': 'covers/minecraft.jpg'},
        {'external_id': 'g_tetris', 'title': 'Tetris', 'studio': 'Alexey Pajitnov', 'release_year': 1984, 'cover_url': 'covers/tetris.jpg'},
        {'external_id': 'g_gta5', 'title': 'Grand Theft Auto V', 'studio': 'Rockstar North', 'release_year': 2013, 'cover_url': 'covers/gta5.jpg'},
        {'external_id': 'g_wiisports', 'title': 'Wii Sports', 'studio': 'Nintendo EAD', 'release_year': 2006, 'cover_url': 'covers/wiisports.jpg'},
        {'external_id': 'g_pubg', 'title': 'PlayerUnknown\'s Battlegrounds', 'studio': 'PUBG Studios', 'release_year': 2017, 'cover_url': 'covers/pubg.jpg'},
        {'external_id': 'g_supermario', 'title': 'Super Mario Bros.', 'studio': 'Nintendo R&D4', 'release_year': 1985, 'cover_url': 'covers/smb.jpg'},
        {'external_id': 'g_zelda_oot', 'title': 'The Legend of Zelda: Ocarina of Time', 'studio': 'Nintendo EAD', 'release_year': 1998, 'cover_url': 'covers/oot.jpg'},
        {'external_id': 'g_thelastofus', 'title': 'The Last of Us', 'studio': 'Naughty Dog', 'release_year': 2013, 'cover_url': 'covers/tlou.jpg'},
        {'external_id': 'g_eldenring', 'title': 'Elden Ring', 'studio': 'FromSoftware', 'release_year': 2022, 'cover_url': 'covers/eldenring.jpg'},
        {'external_id': 'g_witcher3', 'title': 'The Witcher 3: Wild Hunt', 'studio': 'CD Projekt Red', 'release_year': 2015, 'cover_url': 'covers/witcher3.jpg'},
        {'external_id': 'g_rdr2', 'title': 'Red Dead Redemption 2', 'studio': 'Rockstar Studios', 'release_year': 2018, 'cover_url': 'covers/rdr2.jpg'},
        {'external_id': 'g_fortnite', 'title': 'Fortnite', 'studio': 'Epic Games', 'release_year': 2017, 'cover_url': 'covers/fortnite.jpg'},
        {'external_id': 'g_skyrim', 'title': 'The Elder Scrolls V: Skyrim', 'studio': 'Bethesda Game Studios', 'release_year': 2011, 'cover_url': 'covers/skyrim.jpg'},
        {'external_id': 'g_halo3', 'title': 'Halo 3', 'studio': 'Bungie', 'release_year': 2007, 'cover_url': 'covers/halo3.jpg'},
        {'external_id': 'g_acnh', 'title': 'Animal Crossing: New Horizons', 'studio': 'Nintendo EPD', 'release_year': 2020, 'cover_url': 'covers/acnh.jpg'},
        {'external_id': 'g_doom1993', 'title': 'DOOM (1993)', 'studio': 'id Software', 'release_year': 1993, 'cover_url': 'covers/doom.jpg'},
        {'external_id': 'g_hl2', 'title': 'Half-Life 2', 'studio': 'Valve', 'release_year': 2004, 'cover_url': 'covers/hl2.jpg'},
        {'external_id': 'g_overwatch', 'title': 'Overwatch', 'studio': 'Blizzard Entertainment', 'release_year': 2016, 'cover_url': 'covers/overwatch.jpg'},
        {'external_id': 'g_csgo', 'title': 'Counter-Strike: Global Offensive', 'studio': 'Valve / Hidden Path', 'release_year': 2012, 'cover_url': 'covers/csgo.jpg'}
    ]
    
    for game_data in games_data:
        if not Game.query.filter_by(external_id=game_data['external_id']).first():
            game = Game(**game_data)
            db.session.add(game)
    
    db.session.commit()
    print('Database seeded!')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
