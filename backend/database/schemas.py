from pydantic import BaseModel

class TweetBase(BaseModel):
    message: str
    is_depressed: int
    char_count: int
    word_count: int
    hashtag_count: int
    mention_count: int

class TweetCreate(TweetBase):
    pass

class TweetUpdate(TweetBase):
    pass

class Tweet(TweetBase):
    id: int
    class Config:
        orm_mode = True
    pass
