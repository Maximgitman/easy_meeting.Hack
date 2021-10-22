# Этот кусок кода вставить в скрипт стримлита где прогрес бар

from speech2text.ASR.asr import Gen_batch
from preprocessing_for_streamlit import main_asr_for_streamlit
from preprocessing_for_streamlit import postprocessing_text_for_streamlit
from preprocessing_for_streamlit import main_sum_for_streamlit
from preprocessing_for_streamlit import main_q_a_for_streamlit


path_wav = r'C:\Users\Yuriy\Desktop\project\Chat-API\easy_meeting\data\1.wav'

data = Gen_batch(path_wav)


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

text_summarizatuion = main_sum_for_streamlit(text_)
text_Q_A =  main_q_a_for_streamlit(text_, question)


print()
print('>>> Text: ', text_[:1000])
print()
print('>>> summarizatuion: ', text_summarizatuion)
print()
print('>>> Q_A: ', text_Q_A)
print()


