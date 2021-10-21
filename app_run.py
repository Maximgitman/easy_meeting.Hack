import time
from multiprocessing import Process
import streamlit as st
import psutil
from PIL import Image
from preprocessing.audio_extractor import AudioExtractor
from preprocessing.audio_recorder import recording


__version__ = "0.0.3"

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

image = Image.open('source/easy_meeting.jpg')
st.image(image, width=200)

st.markdown('#### Загрузить файл')

uploaded_file = st.file_uploader("Выберите файл")

st.write('')

col1, col2 = st.columns(2)

with col1:
    st.markdown('Укажите ссылку на youtube')
    url = st.text_input('')

with col2:
    st.markdown('Или запишите прямо сейчас')
    start = st.button("Начать запись")
    stop = st.button("Стоп")

st.write('')

col3, col4, col5 = st.columns(3)

with col4:
    process = st.button("Обработать")

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    ext = uploaded_file.name.split('.')[-1]
    filename = f'myfile.{ext}'

    with open(filename, mode='bx') as f:
        f.write(bytes_data)

    extractor = AudioExtractor(filename)
    extractor.get_audio()

if start:
    p = Process(target=recording)
    p.start()
    st.session_state.pid = p.pid
    st.write("Started process with pid:", st.session_state.pid)

if stop:
    p = psutil.Process(st.session_state.pid)
    p.kill()
    st.write("Stopped process with pid:", st.session_state.pid)
    st.session_state.pid = None

if process:
    st.markdown('#### Статус')
    my_bar = st.progress(0)
    with st.empty():
        for i in range(100):
            st.write(f"Обработано {i + 1}%")
            time.sleep(0.1)
            my_bar.progress(i + 1)

    st.success('Обработка завершена!')

    st.sidebar.title('Задайте вопрос по тексту')
    question = st.sidebar.text_input('Ваш вопрос:')

    with open("source/easy_meeting.jpg", "rb") as file:
        btn = st.download_button(label="Скачать файл",
                                 data=file,
                                 file_name="img.jpg",
                                 mime="image/png")
