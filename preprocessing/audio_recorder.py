import queue
import soundfile as sf
import sounddevice as sd

__version__ = "0.0.2"


def recording(fs=16000, ch=1):
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    try:
        with sf.SoundFile('output.wav',
                          mode='x',
                          samplerate=fs,
                          channels=ch,
                          subtype='PCM_16') as file:
            with sd.InputStream(samplerate=fs,
                                channels=1,
                                callback=callback):
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished')
