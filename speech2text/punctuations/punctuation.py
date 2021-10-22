import yaml
import torch
from torch import package

class Punctuation(object):
    def __init__(self, yml_path, model_path, step=20):
        self.yml_path = yml_path
        self.model_path = model_path
        # self.text_val = text_val
        with open(self.yml_path, 'r') as yaml_file:
            self.models = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        self.model_conf = self.models.get('te_models').get('latest')
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


# punct = Punctuation(yml_path='/content/drive/MyDrive/easy_meeting/models/maks/latest_silero_models.yml', 
#                     model_path= '/content/drive/MyDrive/easy_meeting/models/maks/v1_4lang_q.pt',
#                     step=30)
# text_ = punct.apply_te(text)
# text_