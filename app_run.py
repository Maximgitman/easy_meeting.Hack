from multiprocessing import Process
import streamlit as st
import interface.SessionState as SessionState

import numpy as np

import psutil
from io import StringIO, BytesIO

import soundfile as sf

from preprocessing.audio_recorder import recording

st.title('Easy Meeting')

st.sidebar.title("Controls")
start = st.sidebar.button("Record")
stop = st.sidebar.button("Stop")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    st.write(uploaded_file.__dict__)

    bytes_data = uploaded_file.getvalue()
    st.write(type(bytes_data))
    with open('myfile.wav', mode='bx') as f:
        f.write(bytes_data)

    #raw_data = BytesIO(bytes_data)
    #data = np.frombuffer(bytes_data, dtype=np.float32)

    #data, samplerate = sf.read(raw_data)
    #st.write(data.shape, samplerate)
    #sf.write('output.wav', data, samplerate, subtype='PCM_16')

state = SessionState.get(pid=None)

if start:
    p = Process(target=recording)
    p.start()
    state.pid = p.pid
    st.write("Started process with pid:", state.pid)

if stop:
    p = psutil.Process(state.pid)
    p.terminate()
    st.write("Stopped process with pid:", state.pid)
    state.pid = None
