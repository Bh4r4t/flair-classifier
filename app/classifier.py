import torch
import transformers
from transformers import DistilBertForSequenceClassification, DistilBertConfig, DistilBertTokenizer
from . import scrapper

def loadModel(filepath):
    """
    -Function to load model with saved states(parameters)
    -Args:
        filpath (str): path to the saved model
    """
    # load saved model dictionary
    saved = torch.load(filepath, map_location='cpu')
    state_dict = saved['state_dict']
    # load the numberical decoding for the Flair catgory

    # inialize model
    config = DistilBertConfig(num_labels = 9)
    model = DistilBertForSequenceClassification(config)
    # loading the trained parameters with model
    model.load_state_dict(state_dict)

    cat_dict = saved['category']
    return model, cat_dict

class First:
    def __init__(self, path, max_len=120):
        # load model and category decoder
        print('start')
        self.model, self.cat_dict = loadModel(path)
        self.maxlen = max_len
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

    def getTokens(self, text):
        tokens_dict = self.tokenizer.encode_plus(text = text,
                            add_special_tokens=True,
                            max_length = self.maxlen,
                            pad_to_max_length=True,
                            return_attention_mask=True)

        token_id = torch.tensor(tokens_dict['input_ids'])
        attn_mask = torch.tensor(tokens_dict['attention_mask'])

        return token_id, attn_mask

def predict(text, preload):
    """
    Functiion to predict category(Flair) of the post.
    Args:
        text (str): text extracted from reddit post
        preload (class): A class having mathods to 
    Returns:
        prediction (str): predicted Flair of the post

    Note: currently the model is trained on only 9 Flair categories
        
    """
    # get tokens and attention mask for text
    tokens, attn_mask = preload.getTokens(text)
    # initializing model
    # get tokens and attention mask for text
    tokens, attn_mask = preload.getTokens(text)
    # feed the tokens and attn_mask into the model
    output = preload.model(tokens.unsqueeze(0),
                        attention_mask = attn_mask.unsqueeze(0))
    prediction = output[0].argmax()
    flair = [key for key in preload.cat_dict if preload.cat_dict[key]==prediction]
    return flair[0]
