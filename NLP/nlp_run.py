from Q_A import Q_A
from summarization import Summarization



def main_nlp(text,
            question,
            model_path_summarization='/content/drive/MyDrive/easy_meeting/models/ivan/checkpoint-10000/',
            tokenizer_path_summarization='sberbank-ai/ruT5-large',
            model_path_Q_A='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru',
            tokenizer_Q_A='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru',
            max_length=50,
            step=450,
            device_summarization='cpu',
            device_Q_A='cpu',
            ):

    summarization = Summarization(model_path=model_path_summarization,
                                    tokenizer_path=tokenizer_path_summarization,
                                    device=device_summarization )

    rez_sum = summarization.inference(text, 
                                        max_length=max_length, 
                                        step=step)

    model_q_a = Q_A(model_path=model_path_Q_A,
                    tokenizer_path=tokenizer_Q_A,
                    device=device_Q_A)   

    prob_list = model_q_a.inference(text, question)

    return rez_sum, '\nvs\n'.join(prob_list)


# if __name__ == "__main__":
#     text = ''
#     question = ''
#     list_text = main_nlp(text, question)
#     print(list_text)