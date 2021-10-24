from speech2text.ASR.asr import ASR
from speech2text.punctuations.punctuation import Punctuation
from speech2text.word2number.extractor import NumberExtractor
from NLP.Q_A import Q_A
from NLP.summarization import Summarization

# ==============
# speech2text
# ==============

asr = ASR()

def main_asr_for_streamlit(X):
    return asr.inference(X) + ' '


punct = Punctuation()
ext = NumberExtractor()

def postprocessing_text_for_streamlit(text):
    text_ = punct.apply_te(text)
    text_with_num = ext.replace_groups(text_)
    return text_with_num

# ==============
# NLP
# ==============

summarization = Summarization()
model_q_a = Q_A()   


def main_sum_for_streamlit(text):
    return summarization.inference(text)

def main_q_a_for_streamlit(text, question):
    prob_list = model_q_a.inference(text, question)
    return ' '.join([f'{i+1}.  {text} \n' for i, text in enumerate(prob_list)])