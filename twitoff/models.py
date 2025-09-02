from flask_sqlalchemy import SQLAlchemy

# create a DB object from the SQLAlchemy class

DB = SQLAlchemy()


class User(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column
    username = DB.Column(DB.String, nullable=False)
    # most recent post id
    newest_post_id = DB.Column(DB.BigInteger)
    # backref is as-if we had added a posts list to the user class
    # posts = []

    def __repr__(self):
        return f"User: {self.username}"


class Post(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column
    text = DB.Column(DB.Unicode(300))
    # store our word embeddings "vectorization"
    # store numpy arrays in db
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id column (foreign / secondary key)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # user column creates a two-way link between a user object and a post
    user = DB.relationship('User', backref=DB.backref('posts', lazy=True))

    def __repr__(self):
        return f"Post: {self.text}"