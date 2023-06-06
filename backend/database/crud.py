from sqlalchemy.orm import Session

from . import models, schemas

def create_tweet(db: Session, tweet: schemas.TweetCreate):
    db_tweet = models.Tweet(message = tweet.message)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


# Get a tweet by ID
def get_tweet(db: Session, tweet_id: int):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    return tweet


# Update a tweet by ID
def update_tweet(db: Session, tweet_id: int, tweet: schemas.TweetUpdate):
    tweet_db = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if tweet_db:
        for field, value in tweet.items():
            setattr(tweet_db, field, value)
        db.commit()
        db.refresh(tweet_db)
    return tweet_db


# Delete a tweet by ID
def delete_tweet(db: Session, tweet_id: int):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if tweet:
        db.delete(tweet)
        db.commit()
    return tweet