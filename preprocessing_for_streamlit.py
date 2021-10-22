from speech2text.ASR.asr import ASR
from speech2text.punctuations.punctuation import Punctuation
from speech2text.word2number.extractor import NumberExtractor
from NLP.Q_A import Q_A
from NLP.summarization import Summarization


# -----
model_path_asr='/content/drive/MyDrive/easy_meeting/models/ru_3_norm/wav2vec2-large-xlsr-russian-demo/checkpoint-3540',
processor_path_asr='jonatasgrosman/wav2vec2-large-xlsr-53-russian',
device_asr = 'cpu'
# -----
yml_path_punctuation='/content/drive/MyDrive/easy_meeting/models/maks/latest_silero_models.yml',
model_path_punctuation='/content/drive/MyDrive/easy_meeting/models/maks/v1_4lang_q.pt',
step_punctuation=30,
# -----
model_path_summarization='/content/drive/MyDrive/easy_meeting/models/ivan/checkpoint-10000/',
tokenizer_path_summarization='sberbank-ai/ruT5-large',
max_length=50,
step=450,
device_summarization='cpu',
# -----
model_path_Q_A='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru',
tokenizer_Q_A='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru',
device_Q_A='cpu',
# -----


# ==============
# speech2text
# ==============

asr = ASR(model_path=model_path_asr,
                processor_path=processor_path_asr,
                device=device_asr)

def main_asr_for_streamlit(X):
    return asr.inference(X) + ' '



punct = Punctuation(yml_path=yml_path_punctuation, 
                    model_path= model_path_punctuation,
                    step=step_punctuation)
ext = NumberExtractor()

def postprocessing_text_for_streamlit(text):
    text_ = punct.apply_te(text)
    text_with_num = ext.replace_groups(text_)
    return text_with_num





# ==============
# NLP
# ==============

summarization = Summarization(model_path=model_path_summarization,
                                tokenizer_path=tokenizer_path_summarization,
                                device=device_summarization )

model_q_a = Q_A(model_path=model_path_Q_A,
                tokenizer_path=tokenizer_Q_A,
                device=device_Q_A)   

def main_nlp_for_streamlit(text,question):
    rez_sum = summarization.inference(text, 
                                    max_length=max_length, 
                                    step=step)

    prob_list = model_q_a.inference(text, question)
    return rez_sum, '\nvs\n'.join(prob_list)