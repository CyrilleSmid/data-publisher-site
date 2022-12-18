from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras_preprocessing.sequence import pad_sequences
import json
import os

class TopicModelFactory(ABC):
    @abstractmethod
    def get_topic_model(self):
        pass

class TopicModel(ABC):
    @abstractmethod
    def predict_topic(self):
        pass

class KerasNNTopicModel(TopicModel):
    maxlen = 500
    def __init__(self, model, tok):
        self.model, self.tok = model, tok
    def predict_topic(self, abstract_text):
        abstract_text = abstract_text.lower()
        text_seq = pad_sequences(
            self.tok.texts_to_sequences([abstract_text]), maxlen = self.maxlen)
        return np.argmax(self.model.predict(text_seq)[0])

class KerasNNTopicModelFactory(TopicModelFactory):
    def get_topic_model(self):
        
        model_dir = os.path.join(os.path.abspath(os.curdir),'software_design_lab\\topic_model') 
        model = keras.models.load_model(os.path.join(model_dir, 'keras-topic-model.h5'))
        with open(os.path.join(model_dir,'tokenizer.json')) as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)
        return KerasNNTopicModel(model, tokenizer)