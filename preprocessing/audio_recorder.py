import queue
import soundfile as sf
import sounddevice as sd


def recording():
    fs = 44100
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    try:
        with sf.SoundFile('output.wav',
                          mode='x',
                          samplerate=fs,
                          channels=2,
                          subtype='PCM_16') as file:
            with sd.InputStream(samplerate=fs,
                                channels=2,
                                callback=callback):
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished')