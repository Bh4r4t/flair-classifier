# flair-classifier
A webapp using django to predict the flair on a post from r/india subreddit.

## Notebooks
This folder contains the code for scraping and cleaning of the reddit data. Then applying text classification to predict flair on a post.
* ```Data_Scrapping.ipynb``` downloads the posts data from r'india' subreddit using ```PRAW API``` and ```PSAW API```.<br>
* ```Data Exploration.ipynb``` Cleans the scraped data and include some visualisations of relevant details about the data scraped.
* ```final_distilbert.ipynb``` contains the code for text preprocessing and text classification.<br>
  DistilBERT architechture has been used for classification task.
  
## app
This folder contains the files related to the webapp.
* ```scrapper.py``` scrapes post from subreddit r'india' based on URL of the post
* ```classifier.py``` loads the pretrained weights on the model and runs through the scraped text data to predict the flair.
