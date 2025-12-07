from app import create_app
from app.extensions import db

app = create_app()

# Création des tables de la base de donnee
with app.app_context():
    db.create_all()  # Crée les tables si elles n'existent pas

if __name__ == "__main__":
    app.run(debug=True)
