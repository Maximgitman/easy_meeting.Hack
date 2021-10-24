from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from datetime import datetime

import sys
sys.path.append('../')
import config

class Summarization():
    def __init__(self, 
                model_path=config.model_path_summarization,
                tokenizer_path=config.tokenizer_path_summarization,
                device = config.device_summarization
                ):
        self.device = device
        chek_0 = datetime.now()
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        chek_1 = datetime.now()
        print(f'>>> Init class Summarization: {chek_1-chek_0}')

    def generate(self,
            text,
            do_sample=True, 
            max_length=100, 
            repetition_penalty=5.0,
            top_k=5, 
            top_p=0.9, 
            temperature=0.9,
            num_beams=None,
            no_repeat_ngram_size=3
            ):
        
            input_ids = self.tokenizer.encode(text, return_tensors="pt")
            
            out = self.model.generate(
                                input_ids.to(self.device),
                                max_length=max_length,
                                repetition_penalty=repetition_penalty,
                                do_sample=do_sample,
                                top_k=top_k, top_p=top_p, temperature=temperature,
                                num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
                                )
    
            return self.tokenizer.decode(out[0], skip_special_tokens=True)

    def inference(self,
                text,
                step=config.step_sum,
                max_length=config.max_length_sum
                ):
        
        chek_0 = datetime.now()
        text_sum = ''
        for i in range(0, len(text.split())//step+1):
            text_sum += self.generate(' '.join(text.split()[i*step:(i+1)*step]), max_length=max_length) + ' \n'
        chek_1 = datetime.now()

        print(f'predict model: {chek_1-chek_0}')

        return text_sum