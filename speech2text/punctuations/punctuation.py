import yaml
import torch
from torch import package

import sys
sys.path.append('../../')

import config


class Punctuation(object):
    def __init__(self, 
                    model_path=config.model_path_punctuation, 
                    step=config.step_punctuation):

        self.model_path = model_path
        self.imp = package.PackageImporter(self.model_path)
        self.model = self.imp.load_pickle("te_model", "model")
        self.step =step

    def apply_te(self, text_val):
        self.lan = "ru"

        len_text = len(text_val.split())

        if len_text > self.step:

            temp_pred = ''
            for i in range(0, len_text, self.step):
                temp_text = self.model.enhance_text(' '.join(text_val.split()[i:i+self.step]), self.lan)[:-1] + ' ' 
                temp_pred += temp_text[0].lower() + temp_text[1:]

            self.text_with_punctuation = temp_pred
        else:
            self.text_with_punctuation = self.model.enhance_text(text_val, self.lan)

        return self.text_with_punctuation

