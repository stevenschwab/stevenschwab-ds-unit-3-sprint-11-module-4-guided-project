"""Prediction of users based on posts"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .x import vectorize_post


def predict_user(user0_name, user1_name, hypo_post_text):
    """
    Determine and returns which user is more likely to say a given post
    Example run: predict_user("elonmusk", "jackblack", "Tesla cars go vroom")
    Returns a 0 (user0_name: "elonmusk") or a 1 (user1_name: "jackblack")
    """
    # Grabbing user from our DB
    # The user we want to compare has to be in our DB
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # Grabbing post vectors from each post for each user
    user0_vects = np.array([post.vect for post in user0.posts])
    user1_vects = np.array([post.vect for post in user1.posts])

    # Vertically stack tweet_vects to get one np array
    vects = np.vstack([user0_vects, user1_vects])

    # concatenate labels of 0 or 1 for each post
    labels = np.concatenate(
        [np.zeros(len(user0.posts)), np.ones(len(user1.posts))])

    # fit the model with our x's == vects & our y's == labels
    log_reg = LogisticRegression().fit(vects, labels)

    # vectorize the hypothetical tweet to pass into .predict()
    hypo_post_vect = vectorize_post(hypo_post_text)

    return log_reg.predict(hypo_post_vect.reshape(1, -1))[0]
