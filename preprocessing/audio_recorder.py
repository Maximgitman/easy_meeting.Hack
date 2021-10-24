import os
import queue
import soundfile as sf
import sounddevice as sd
import keyboard

__version__ = "0.0.5"


def recording(filename='input.wav', fs=16000, ch=1):
    name = filename.split('.')[0]
    if os.path.exists(name + '.wav'):
        os.remove(name + '.wav')

    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    try:
        with sf.SoundFile(filename,
                          mode='x',
                          samplerate=fs,
                          channels=ch,
                          subtype='PCM_16') as file:
            with sd.InputStream(samplerate=fs,
                                channels=1,
                                callback=callback):
                while True:
                    file.write(q.get())
                    if keyboard.is_pressed('s'):
                        break
    except KeyboardInterrupt:
        print('\nRecording finished')
