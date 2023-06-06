#Python and API imports
from fastapi import FastAPI, Depends, HTTPException
import starlette
import logging

#DL Tools
import tensorflow as tf

#Database imports
from sqlalchemy.orm import Session
from database.database import crud, models, schemas
from .database import SessionLocal, engine

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Load the model that we previously exported from the notebook
MODEL = tf.keras.models.load_model('./model/')

#Config and launch FastAPI app
logging.basicConfig(level=logging.INFO)
app = FastAPI(
    title = "Twit depression detector"
)

"""
Endpoints
"""

@app.get("/")
def ping(): 
    print("ping de print")
    logging.info("Ping de logging")
    return starlette.status.HTTP_200_OK

@app.get("/version")
def get_version():
    print('{"version": "0.1"}')
    return [{"version": "0.1"}]

@app.get("/model-info", tags=["Model"])
def get_model_info():
    summary_str = []
    MODEL.summary(print_fn=lambda x: summary_str.append(x))
    return {"summary": summary_str}

@app.post("/tweet", tags=["Evaluation"], response_model=schemas.Tweet)
def post_tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    logging.info("Storing tweet")
    ## store the tweet here
    db_tweet = crud.get_tweet_by_id(db, id=tweet.id)
    if db_tweet:
        ## I should manage this scenario, do I want dupes?
        logging.info("Tweet already exists")
        #raise HTTPException(status_code=400, detail="Tweet already stored")
    crud.create_tweet(db=db, tweet=tweet)
    logging.info("Predicting: \n")
    #prediction = MODEL.predict(processed_tweet)
    return 

# https://machinelearningmastery.com/update-neural-network-models-with-more-data/
# https://fastapi.tiangolo.com/tutorial/sql-databases/