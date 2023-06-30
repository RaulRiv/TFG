#Python and API imports
from fastapi import FastAPI, Depends, HTTPException
import starlette
import logging

#DL Tools
import tensorflow as tf

#Database imports
from sqlalchemy.orm import Session
from database import crud, schemas, database
from .tweet_processor import TweetProcessor

#Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Config and launch FastAPI app
logging.basicConfig(level=logging.INFO)
app = FastAPI(
    title = "Twit depression detector"
)

#Initialize model on server start
model = None
@app.on_event("startup")
def startup_event():
    global model
    model = TweetProcessor.load_model()

"""
Endpoints
"""

@app.get("/")
def ping(): 
    print("ping de print")
    logging.info("Logging de ping")
    return starlette.status.HTTP_200_OK

@app.get("/version", tags=["Model"])
def get_version():
    print('{"version": "0.1"}')
    return [{"version": "0.1"}]

@app.get("/model-info", tags=["Model"])
def get_model_info():
    return TweetProcessor.model_info()

# Store, process and make a prediction with a given tweet
@app.post("/tweet", tags=["Evaluation"], response_model=schemas.Tweet)
def post_tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    logging.info("Storing tweet")
    ## store the tweet here
    db_tweet = crud.get_tweet_by_id(db, id=tweet.id)
    if db_tweet:
        logging.info("Tweet already exists")
        raise HTTPException(status_code=400, detail="Tweet already stored")
    crud.create_tweet(db=db, tweet=tweet)
    logging.info("Predicting... \n")
    processed_tweet = TweetProcessor.pre_process_tweet([tweet.message])
    prediction = TweetProcessor.predict_tweet(processed_tweet)
    return prediction

# https://machinelearningmastery.com/update-neural-network-models-with-more-data/
# https://fastapi.tiangolo.com/tutorial/sql-databases/