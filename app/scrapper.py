import re
import emoji
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def scrape(url, reddit):
    """
    Function to scrape data from url of a reddit post
    Args:
        url (str): url to reddit post
        reddit 
    Return:
        dictionary object containing title, author, post's selftext, top 10 comments.
    """
    post = reddit.submission(url = url)
    try:
        headline = post.title
        postBody = post.selftext
    except:
        return None

    return {'headline':headline,
            'postBody':postBody}


def textPreProcess(text, rem_stop=True):
    """
    Function to process text data and remove non neccessary information
    1. converting emojis to text
    2. lower casing
    3. removing punctuations, urls
    4. removing stop words
    5. lemmatization 
    Args:
        text (str): text data
        rem_stop (bool): whether to remove stopping words or not
    Return:
        text (str): processed text data
    """
    # converting emojis to text
    text = emoji.demojize(text)
    # removing empty space at start and end of text and lower casing
    text = text.strip().lower()
    # removing punctuation
    PUNCTUATIONS = r'[!()\-[\]{};:"\,<>/?@#$%^&.*_~]'
    text = re.sub(PUNCTUATIONS, "", text)
    # removing url links
    urlPattern = re.compile(r'https?://\S+|www\.\S+')
    urlPattern.sub('', text)

    # updating stopping words list
    if rem_stop:
        stopWords = list(stopwords.words('english'))
    else:
        stopWords = []

    # lemmatizing, removing stop word, removing emojis
    lemmaWords=[]
    Lemma=WordNetLemmatizer()
    for word in text.split():
        # removing stop words
        if word not in stopWords:
            lemmaWords.append(Lemma.lemmatize(word.strip()))
    text = " ".join(lemmaWords)

    return text



def preProcess(scraped_data):
    """
    Function to preprocess scraped data for inference
    Args:
        scraped_data (dict): scraped data containing 
                            headline, postbody
    Return:
        text (str) : preprocessed text data
    """
    scraped = scraped_data
    # appending all the text features except author name
    text = " ".join([scraped['headline'], scraped['postBody']])
    # preprocess text data for inference
    text = textPreProcess(text)

    return text
