from app import db, app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1969@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'htnethnet'
db = SQLAlchemy(app)

# Create an application context
with app.app_context():
    # Raw SQL query
    query = "DELETE FROM Users WHERE id = 49"

    try:
        # Create a connection
        connection = db.engine.connect()

        # Execute the query
        connection.execute(text(query))

        # Commit the changes
        db.session.commit()
        print("Query executed successfully")
    except Exception as e:
        # Rollback the changes
        db.session.rollback()
        print(f"Error: {str(e)}")
    finally:
        # Close the connection
        connection.close()