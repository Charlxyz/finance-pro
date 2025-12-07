mon_site/
├── intance/
|   └── bdd.db
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # routes générales (accueil, pages publiques)
│   │   └── auth.py          # login/logout/register
│   │
│   ├── models.py            # modèles SQLAlchemy (User, etc.)
│   ├── extensions.py        # init des extensions (db, login_manager...)
│   │
│   ├── templates/
|   |   ├── auth/
|   |   |   ├── login.html
|   |   |   └── register.html
│   │   ├── index.html
│   │   ├── about.html
|   |   └── account.html 
│   │
│   └── static/
│       ├── css/
|       |   └── acceuil.css
│       ├── js/
|       |   └── auth.js
│       └── img/
|           └── image.jpg
│
├── config.py                # classes de configuration
├── server.py                   # point d’entrée
├── requirements.txt
└── README.md
