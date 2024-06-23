# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# DB_URI = "mysql://root:@localhost:3306/bee"

# def configure_database(app):
#     try:
#         app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

#         db.init_app(app)

#         with app.app_context():
#             db.create_all()
#             db.session.commit()

#         print("Database connection established.")
#     except Exception as e:
#         print(f"Error while establishing the database connection: {str(e)}")
#         #db = None

#     return db