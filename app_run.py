from multiprocessing import Process
import streamlit as st
import interface.SessionState as SessionState
import numpy as np
import psutil
from io import StringIO, BytesIO
import soundfile as sf
from preprocessing.audio_recorder import recording

from scipy.io.wavfile import read, write

__version__ = "0.0.1"

st.title('Easy Meeting')

st.sidebar.title("Controls")
start = st.sidebar.button("Record")
stop = st.sidebar.button("Stop")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    st.write(uploaded_file.__dict__)

    bytes_data = uploaded_file.getvalue()
    st.write(type(bytes_data))

    #with open('myfile.wav', mode='bx') as f:
    #    f.write(bytes_data)

    rate, data = read(BytesIO(bytes_data))
    st.write(type(rate))
    st.write(data.shape)

    #raw_data = BytesIO(bytes_data)
    #data = np.frombuffer(bytes_data, dtype=np.float32)

    #data, samplerate = sf.read(raw_data)
    #st.write(data.shape, samplerate)
    #sf.write('output.wav', data, samplerate, subtype='PCM_16')


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
