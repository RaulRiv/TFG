from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import nltk
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

class TweetProcessor:

    ## These functions will give us some more insight into the tweets
    def calc_char_count(self, message_column):
        return message_column.apply(len)

    def calc_word_count(self, message_column):
        return message_column.apply(lambda x: len(x.split(' ')))    

    def calc_hashtag_count(self, message_column):
        return message_column.apply(lambda x: len([word for word in x.split(' ') if word.startswith('#')]))

    def calc_mention_count(self, message_column):
        return message_column.apply(lambda x: len([word for word in x.split(' ') if word.startswith('@')]))

    def update_features(self, message_column):
        return self.calc_char_count(message_column), self.calc_word_count(message_column), self.calc_hashtag_count(message_column), self.calc_mention_count(message_column)

    # These functions filter the tweet content

    def filter_stopwords(self, tweet):
        nltk.download('stopwords')
        return ' '.join(word for word in tweet.split(' ') if word not in set(stopwords.words("english")))

    def filter_hashtags(self, tweet):
        return ' '.join(word for word in tweet.split(' ') if not word.startswith('#'))

    def filter_mentions(self, tweet):
        return ' '.join(word for word in tweet.split(' ') if not word.startswith('@'))

    def filter_urls(self, tweet):
        return ' '.join(word for word in tweet.split(' ') if not (word.startswith('http') or word.startswith('www')))

    def filter_everything(self, tweet):
        tweet = self.filter_stopwords(tweet)
        tweet = self.filter_hashtags(tweet)
        tweet = self.filter_mentions(tweet)
        tweet = self.filter_urls(tweet)
        return tweet

    # These functions process the tweet so the NN can work with it

    def load_tokenizer():
        # Load the tokenizer JSON from a file
        with open('tokenizer.json', 'r', encoding='utf-8') as f:
            tokenizer_json = json.load(f)

        # Create a tokenizer from the loaded JSON
        tokenizer = Tokenizer.from_json(tokenizer_json)
        return tokenizer

    def tokenize_tweet(self, tweet):
        tokenizer = self.load_tokenizer()
        tweet_tokens = tokenizer.texts_to_sequences(tweet)
        return tweet_tokens

    def pad_tweet(tweet_tokens):
        padded_tweet = pad_sequences(tweet_tokens, maxlen=25, padding='post', truncating='post')
        return padded_tweet
    
    def pre_process_tweet(self, tweet):
        return self.pad_tweet((self.tokenize_tweet(tweet)))

    # These functions interact with the model
    def load_model():
        model = tf.keras.models.load_model('./model/')
        return model
    
    def model_info(model):
        summary_str = []
        model.summary(print_fn=lambda x: summary_str.append(x))
        return {"summary": summary_str}
    
    def predict_tweet(padded_tweet, model):
        return model.predict(padded_tweet)