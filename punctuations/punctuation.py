import yaml
import torch
from torch import package

class Punctuation(object):
    def __init__(self, yml_path, model_path, text_val):
        self.yml_path = yml_path
        self.model_path = model_path
        self.text_val = text_val
        with open(self.yml_path, 'r') as yaml_file:
            self.models = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        self.model_conf = self.models.get('te_models').get('latest')
        self.imp = package.PackageImporter(self.model_path)
        self.model = self.imp.load_pickle("te_model", "model")

    def apply_te(self):
        self.lan = "ru"
        self.text_with_punctuation = self.model.enhance_text(self.text_val, self.lan)
        return self.text_with_punctuation

if __name__ == "__main__":
    yml_path = "latest_silero_models.yml"
    model_path = "v1_4lang_q.pt"
    text_val = "ехали цигане кошку потеряли кошка сдохла хвост облез кто слово скажет тот ее и съест"

    punctuation = Punctuation(yml_path, model_path, text_val).apply_te()