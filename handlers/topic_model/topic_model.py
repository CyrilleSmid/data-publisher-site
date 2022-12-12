from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
import json

class TopicModelFactory(ABCMeta):
    @abstractmethod
    def get_topic_model(self):
        pass

class TopicModel(ABCMeta):
    @abstractmethod
    def predict_topic(self):
        pass

class KerasNNTopicModel(TopicModel):
    model, tok = None
    maxlen = 500
    def __init__(self, model, tok):
        self.model, self.tok = model, tok
    def predict_topic(self, abstract_text):
        text_seq = tf.keras_preprocessing.sequence.pad_sequences(
            self.tok.texts_to_sequences([abstract_text]), maxlen = self.maxlen)
        return np.argmax(self.model.predict(text_seq)[0])

class KerasNNTopicModelFactory(TopicModelFactory):
    def get_topic_model(self):
        model = keras.models.load_model('keras-topic-model.h5')
        with open('tokenizer.json') as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)
        return KerasNNTopicModel(model, tokenizer)