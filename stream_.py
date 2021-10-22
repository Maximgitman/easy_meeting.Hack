# Этот кусок кода вставить в скрипт стримлита где прогрес бар

from speech2text.ASR.asr import Gen_batch
from preprocessing_for_streamlit import main_asr_for_streamlit
from preprocessing_for_streamlit import postprocessing_text_for_streamlit
from preprocessing_for_streamlit import main_nlp_for_streamlit


path_wav = './file_1.wav'
data = Gen_batch(path_wav, min_len=100, max_len=150)


text = ''

# Сам прогрес бар ==================

for name, i in enumerate(data.get_batch()):
    text +=  main_asr_for_streamlit(i)

#====================================

text_ = postprocessing_text_for_streamlit(text)

# text_ - готовый текст



#===============
# Дополнительно
#===============

question = ''
text_summarizatuion, text_Q_A =  main_nlp_for_streamlit(text_, question)

