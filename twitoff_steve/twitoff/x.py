from os import getenv
import not_tweepy as tweepy
from .models import User, DB, Post
import spacy

# get API keys from .env file
key = getenv('X_API_KEY')
secret = getenv('X_API_KEY_SECRET')

X_AUTH = tweepy.OAuthHandler(key, secret)
X = tweepy.API(X_AUTH)


def add_or_update_user(username):
    '''
    Take a username and pull that user's data and posts from the API
    If this user already exists in db, then we will just check to see if there
    are any new posts from that user that we don't already have and we will
    add any new posts to the db.
    '''
    try:
        # get the user information from X
        x_user = X.get_user(screen_name=username)

        # check to see if this user is already in the database
        # is there a user with the same id already in the db
        # if we don't already have that user, then we'll create a new one
        db_user = (User.query.get(x_user.id)) or User(id=x_user.id, username=username)

        # add the user to the db
        # this won't re-add a user if they've already been added
        DB.session.add(db_user)

        # get the user's posts (in a list)
        posts = x_user.timeline(count=200, 
                                exclude_replies=True, 
                                include_rts=False, 
                                tweet_mode='extended',
                                since_id=db_user.newest_post_id)
        
        # update the newest_post_id if there have been new posts
        # since the last time this user posted
        if posts:
            db_user.newest_post_id = posts[0].id
        
        # add all of the individual posts to the database

        for post in posts:
            post_vector = vectorize_post(post.full_text)
            db_post = Post(id=post.id,
                            text=post.full_text[:300],
                            vect = post_vector,
                            user_id=db_user.id)
            DB.session.add(db_post)
    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e
    
    else:
        # save the changes to the db
        DB.session.commit()


nlp = spacy.load('my_model/')
# we have the same tool we used in the flask shell
def vectorize_post(post_text):
    '''
    Give the function some text
    Returns a word embedding
    '''
    return nlp(post_text).vector
