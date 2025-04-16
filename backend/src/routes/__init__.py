from src.routes.auth_routes.auth_route import auth_bp
from src.routes.project_route import project_bp 

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
