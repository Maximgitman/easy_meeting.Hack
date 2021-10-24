from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch  
from datetime import datetime

import sys
sys.path.append('../')
import config

class Q_A:
    def __init__(self, 
                model_path=config.model_path_Q_A,
                tokenizer_path=config.tokenizer_Q_A,
                device = config.device_Q_A
                ):
        self.device = device
        chek_0 = datetime.now()
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_path).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

        chek_1 = datetime.now()
        print(f'>>> Init class Q_A: {chek_1-chek_0}')

    def inference(self,
                text,
                question,
                step = config.max_length_step_Q_A
                ):
        answer_prob = []
        chek_0 = datetime.now()

        for i in range(0, len(text.split())//step+1):

            inputs = self.tokenizer(question, ' '.join(text.split()[i*step:(i+1)*step]), add_special_tokens=True, return_tensors="pt")
            input_ids = inputs["input_ids"].tolist()[0]

            with torch.no_grad():
                outputs = self.model(**inputs.to(self.device))
                prob = torch.max(torch.nn.functional.softmax(outputs.start_logits, dim=-1))
           
            answer_start = torch.argmax(outputs.start_logits)
            answer_end = torch.argmax(outputs.end_logits) + 1

            answer = self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

            answer_prob.append({'answer': answer, 'prob': prob.numpy()})
        

        sorted_by_value =[i['answer'] for i in sorted(answer_prob, key=lambda x: x['prob'])[-3:]]

        chek_1 = datetime.now()
        print(f'predict model: {chek_1-chek_0}')
        
        return sorted_by_value