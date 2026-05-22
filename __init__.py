from flask import Flask, render_template
from flask_cors import CORS
from routes.auth import auth_bp
from routes.simulation import simulation_bp


def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    
    # Template routes
    @app.route('/')
    def index():
        return render_template('login.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        return render_template('register.html')
    
    @app.route('/game')
    def game():
        return render_template('game.html')
    
    return app
