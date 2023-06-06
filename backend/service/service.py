def calc_char_count(message_column):
    return message_column.apply(len)

def calc_word_count(message_column):
    return message_column.apply(lambda x: len(x.split(' ')))    

def calc_hashtag_count(message_column):
    return message_column.apply(lambda x: len([word for word in x.split(' ') if word.startswith('#')]))

def calc_mention_count(message_column):
    return message_column.apply(lambda x: len([word for word in x.split(' ') if word.startswith('@')]))

def update_features(message_column):
    return calc_char_count(message_column), calc_word_count(message_column), calc_hashtag_count(message_column), calc_mention_count(message_column)