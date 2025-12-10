from flask import Flask, render_template, flash
from .extensions import db, login_manager
from .routes.main import main_bp
from .routes.auth import auth_bp
from .routes.auth_security import twofa_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(twofa_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        flash("La page que vous recherchez n'existe pas.", 'error')
        return render_template("error/404.html")
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        flash("Méthode non autorisée pour cette ressource.", 'error')
        return render_template("error/405.html")

    return app
