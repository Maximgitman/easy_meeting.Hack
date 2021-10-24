# -*- coding: utf-8 -*-

import os
import time
import keyboard
import streamlit as st
from PIL import Image
import youtube_dl
from youtube_dl import DownloadError

from preprocessing.audio_extractor import multiple_extraction
from preprocessing.audio_recorder import recording
from speech2text.ASR.asr import Gen_batch
from preprocessing_for_streamlit import main_asr_for_streamlit
from preprocessing_for_streamlit import postprocessing_text_for_streamlit
from preprocessing_for_streamlit import main_sum_for_streamlit
from preprocessing_for_streamlit import main_q_a_for_streamlit


__version__ = "0.0.7"

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #EA4825;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #ffffff;
    color:#ff0000;
    }
</style>""", unsafe_allow_html=True)

# if 'pid' not in st.session_state:
#     st.session_state.pid = None
if 'ready_upload' not in st.session_state:
    st.session_state.ready_upload = False
if 'ready_dl_youtube' not in st.session_state:
    st.session_state.ready_dl_youtube = False
if 'ready_record' not in st.session_state:
    st.session_state.ready_record = False
if 'show_process_btn' not in st.session_state:
    st.session_state.show_process_btn = False
if 'start_process' not in st.session_state:
    st.session_state.start_process = False
if 'speech_to_text' not in st.session_state:
    st.session_state.speech_to_text = False
if 'summarisation' not in st.session_state:
    st.session_state.summarisation = False
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'processed' not in st.session_state:
    st.session_state.processed = False

formats = ['wav', 'mp3']
for format in formats:
    if os.path.exists('input.' + format):
        os.remove('input.' + format)

image = Image.open('source/easy_meeting.jpg')
st.image(image, width=200)

st.markdown('#### Загрузите файл удобным вам способом')

st.write('')

col1, col2, col3 = st.columns(3)   

with col1:
    st.markdown('Загрузите файл с устройства')
    upload = st.button("Загрузить")

with col2:
    st.markdown('Укажите ссылку на youtube')
    youtube = st.button("Скачать с youtube")

with col3:
    st.markdown('Запишите с микрофона')
    record = st.button("Записать")

if upload:
    st.session_state.ready_upload = True
    st.session_state.ready_dl_youtube = False
    st.session_state.ready_record = False
    #st.session_state.show_process_btn = False

if youtube:
    st.session_state.ready_upload = False
    st.session_state.ready_dl_youtube = True
    st.session_state.ready_record = False
    #st.session_state.show_process_btn = False

if record:
    st.session_state.ready_upload = False
    st.session_state.ready_dl_youtube = False
    st.session_state.ready_record = True
    #st.session_state.show_process_btn = False

if st.session_state.ready_upload:
    uploaded_file = st.file_uploader("Выберите файл")

if st.session_state.ready_dl_youtube:
    url = st.text_input('Вставьте ссылку на видео с youtube')
    download = st.button("Скачать видео")

if st.session_state.ready_record:
    st.markdown('Запись с микрофона')
    start = st.button("Начать запись")
    st.markdown('Для остановки записи нажмите и удерживайте 5 секунд кнопку "S"')

st.write('')

if st.session_state.ready_upload:
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        ext = uploaded_file.name.split('.')[-1]
        filename = f'input.{ext}'

        with open(filename, mode='bw') as f:
            f.write(bytes_data)

        multiple_extraction(filename, formats=['wav', 'mp3'])

        for format in ['source/test_answer.txt','source/test_summary.txt','source/test_answer_Q.txt', 'source\test_text.txt']:
            if os.path.exists(format):
                os.remove(format)

        uploaded_file.close()
        st.success('Данные загружены! Теперь можно приступить к извлечению текста.')
        st.session_state.show_process_btn = True
        st.session_state.ready_upload = False

if st.session_state.ready_dl_youtube:
    if download:
        download_path = os.getcwd()
        filename = 'input.mp4'

        ydl_opts = {'outtmpl': os.path.join(download_path, filename)}
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            multiple_extraction(filename, formats=['wav', 'mp3'])
            st.success('Данные загружены! Теперь можно приступить к извлечению текста.')
            st.session_state.show_process_btn = True
        except DownloadError:
            st.error('Вы ввели некорректную ссылку для скачивания')

        for format in ['source/test_answer.txt','source/test_summary.txt', 'source/test_answer_Q.txt', 'source\test_text.txt']:
            if os.path.exists(format):
                os.remove(format)
        st.session_state.ready_dl_youtube = False

if st.session_state.ready_record:
    if start:
        recording()

    if keyboard.is_pressed('s'):

        multiple_extraction('input.wav', formats=['wav', 'mp3'], remove_original=False)

        for format in ['source/test_answer.txt','source/test_summary.txt', 'source/test_answer_Q.txt', 'source\test_text.txt']:
            if os.path.exists(format):
                os.remove(format)

        st.success('Данные загружены! Теперь можно приступить к извлечению текста.')
        st.session_state.show_process_btn = True
        st.session_state.ready_record = False

if st.session_state.show_process_btn:
    col4, col5, col6 = st.columns(3)
    with col5:
        process = st.button("Обработать аудио")
    if process:
        st.session_state.start_process = True


if st.session_state.start_process:
    st.markdown('#### Статус обработки')
    if not st.session_state.speech_to_text:
        bar = st.progress(0.0)
        with st.empty():

            data = Gen_batch('output.wav')
            text = ''
            k = 0
            for i, batch in enumerate(data.get_batch()):
                
                print(f'Батч - {i+1}/{len(data)}')
                text +=  main_asr_for_streamlit(batch)
                k+=float(1/len(data))
                st.write(f"Обработано {round(k*100, 2)}%")
                bar.progress(k)

            text = postprocessing_text_for_streamlit(text)
            with open('source/test_text.txt', mode='w', encoding='utf8') as f:
                f.write(text)
    else:
        bar = st.progress(100)
        with st.empty():
            st.write("Обработано 100%")

    st.success('Текст распознан! Теперь его можно посмотреть и при необходимости отредактировать.')
    st.session_state.speech_to_text = True

if st.session_state.speech_to_text:
    st.sidebar.title('Задайте вопрос по тексту')
    question = st.sidebar.text_input('Ваш вопрос:')
    ask = st.sidebar.button("Спросить")

    with open("source/test_text.txt", "r", encoding='utf8') as file:
        data = file.read()

    with st.expander("Распознанный текст"):
        new_text = st.text_input('', data)

        corr_text = st.button("Внести исправления в текст")
    if corr_text:
        with open("source/test_text.txt", "w", encoding='utf8') as file:
            file.write(new_text)

    col7, col8, col9 = st.columns(3)
    with open("output.mp3", "rb") as file:
        btn = col7.download_button(label="Скачать аудио в формате mp3",
                                   data=file,
                                   file_name="audio.mp3",
                                   mime="audio/wav")

    with open("source/test_text.txt", "r", encoding='utf8') as file:
        btn = col9.download_button(label="Скачать распознанный текст",
                                   data=file,
                                   file_name="text.txt",
                                   mime="text/plain")

    st.markdown('#### Получите краткое содержание распознанного текста')

    col10, col11, col12 = st.columns(3)
    with col11:
        summarize = st.button("Получить краткое содержание")
    if summarize:
        st.session_state.summarisation = True

    if ask:
        st.session_state.show_answer = True

if st.session_state.show_answer:

    try:
        with open("source/test_answer_Q.txt", "r", encoding='utf8') as file:
            last_question= file.read()
    except:
        last_question = ''

    with open("source/test_text.txt", "r", encoding='utf8') as file:
        text = file.read()

    if os.path.exists('source/test_answer.txt') and last_question==question:
        with open("source/test_answer.txt", "r", encoding='utf8') as file:
            text_Q_A = file.read()

    else:    
        text_Q_A =  main_q_a_for_streamlit(text, question)
        with open("source/test_answer.txt", "w", encoding='utf8') as file:
                file.write(text_Q_A)

    with open("source/test_answer_Q.txt", "w", encoding='utf8') as file:
        file.write(question)

    st.sidebar.markdown('#### Возможные варианты ответа:')
    st.sidebar.markdown(text_Q_A)

if st.session_state.summarisation:
    if not st.session_state.processed:
        with st.spinner('Идет суммаризация текста'):
            with open("source/test_text.txt", "r", encoding='utf8') as file:
                text = file.read()

            if os.path.exists('source/test_summary.txt'):
                with open("source/test_summary.txt", "r", encoding='utf8') as file:
                    text_summarizatuion = file.read()

            else:
                text_summarizatuion = main_sum_for_streamlit(text)
                with open("source/test_summary.txt", "w", encoding='utf8') as file:
                        file.write(text_summarizatuion)
                    
    st.session_state.processed = True


    with st.expander("Краткое содержание"):
        new_summarization = st.text_input('', text_summarizatuion)
        corr_summ = st.button("Внести исправления в краткое содержание")
    if corr_summ:
        with open("source/test_summary.txt", "w", encoding='utf8') as file:
            file.write(new_summarization)


    col13, col14, col15 = st.columns(3)
    with open("source/test_summary.txt", "r", encoding='utf8') as file:
        btn = col14.download_button(label="Скачать краткое содержание",
                                    data=file,
                                    file_name="summary.txt",
                                    mime="text/plain")
