import collections
import contextlib
import wave
import webrtcvad
import torchaudio
from datetime import datetime
from transformers import Wav2Vec2ForCTC 
from transformers import Wav2Vec2Processor
import torch
from datetime import datetime

import sys
sys.path.append('../../')
import config


class ASR:
    def __init__(self, 
                model_path=config.model_path_asr,
                processor_path=config.processor_path_asr,
                device = config.device_asr
                ):
        self.device = device
        chek_0 = datetime.now()
        self.model = model = Wav2Vec2ForCTC.from_pretrained(model_path).to(self.device)
        self.processor = Wav2Vec2Processor.from_pretrained(processor_path)
        chek_1 = datetime.now()
        print(f'>>> Init class ASR: {chek_1-chek_0}')

    def inference(self,
                    X
                ):
        chek_0 = datetime.now()
        inputs = self.processor(X, sampling_rate=16_000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = self.model(inputs.input_values.to(self.device), attention_mask=inputs.attention_mask.to(self.device)).logits

        predicted_ids = torch.argmax(logits, dim=-1)[0]
        predicted_sentences = self.processor.decode(predicted_ids) # processor.batch_decode
        # text = [i.lower() for i in predicted_sentences]
        
        text = predicted_sentences.lower()
        chek_1 = datetime.now()
        print(f'predict model: {chek_1-chek_0}')
        return text



class Pause_audio():
    def read_wave(self, path):
        # """Reads a .wav file.
        # Takes the path, and returns (PCM audio data, sample rate).
        # """
        with contextlib.closing(wave.open(path, 'rb')) as wf:
            num_channels = wf.getnchannels()
            assert num_channels == 1
            sample_width = wf.getsampwidth()
            assert sample_width == 2
            sample_rate = wf.getframerate()
            assert sample_rate in (8000, 16000, 32000, 48000)
            pcm_data = wf.readframes(wf.getnframes())
            return pcm_data, sample_rate

    class Frame(object):
        """Represents a "frame" of audio data."""
        def __init__(self, bytes, timestamp, duration):
            self.bytes = bytes
            self.timestamp = timestamp
            self.duration = duration


    def frame_generator(self, frame_duration_ms, audio, sample_rate):
        """Generates audio frames from PCM audio data.
        Takes the desired frame duration in milliseconds, the PCM data, and
        the sample rate.
        Yields Frames of the requested duration.
        """
        n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
        offset = 0
        timestamp = 0.0
        duration = (float(n) / sample_rate) / 2.0
        while offset + n < len(audio):
            yield self.Frame(audio[offset:offset + n], timestamp, duration)
            timestamp += duration
            offset += n


    def vad_collector(self, sample_rate, frame_duration_ms,
                    padding_duration_ms, vad, frames):
        """Filters out non-voiced audio frames.
        Given a webrtcvad.Vad and a source of audio frames, yields only
        the voiced audio.
        Uses a padded, sliding window algorithm over the audio frames.
        When more than 90% of the frames in the window are voiced (as
        reported by the VAD), the collector triggers and begins yielding
        audio frames. Then the collector waits until 90% of the frames in
        the window are unvoiced to detrigger.
        The window is padded at the front and back to provide a small
        amount of silence or the beginnings/endings of speech around the
        voiced frames.
        Arguments:
        sample_rate - The audio sample rate, in Hz.
        frame_duration_ms - The frame duration in milliseconds.
        padding_duration_ms - The amount to pad the window, in milliseconds.
        vad - An instance of webrtcvad.Vad.
        frames - a source of audio frames (sequence or generator).
        Returns: A generator that yields PCM audio data.
        """
        num_padding_frames = int(padding_duration_ms / frame_duration_ms)
        # We use a deque for our sliding window/ring buffer.
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
        # NOTTRIGGERED state.
        triggered = False
        for frame in frames:
            is_speech = vad.is_speech(frame.bytes, sample_rate)
            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                # If we're NOTTRIGGERED and more than 90% of the frames in
                # the ring buffer are voiced frames, then enter the
                # TRIGGERED state.
                if num_voiced > 0.9 * ring_buffer.maxlen:
                    triggered = True
                    ring_buffer.clear()
            else:
                # We're in the TRIGGERED state, so collect the audio data
                # and add it to the ring buffer.
                # voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                # If more than 90% of the frames in the ring buffer are
                # unvoiced, then enter NOTTRIGGERED and yield whatever
                # audio we've collected.
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    triggered = False
                    yield (frame.timestamp + frame.duration)
                    ring_buffer.clear()

        yield (frame.timestamp + frame.duration)



    def get_time_step(self,
                           path):
        
        audio, sample_rate = self.read_wave(path)
        vad = webrtcvad.Vad(3) # 0-3
        frames = self.frame_generator(30, audio, sample_rate)
        frames = list(frames)
        segments = self.vad_collector(sample_rate, 30, 40, vad, frames)
        time_step = []
        for i, segment in enumerate(segments):
            time_step.append(segment)
        return time_step


class Gen_batch():
    def __init__(self, 
                 path,
                 min_len=config.min_len_sec, 
                 max_len=config.max_len_sec,
                 ):
        chek_0 = datetime.now()
        self.min_len = min_len
        self.max_len = max_len
        self.path = path

        pause_audio = Pause_audio()
        self.time_step = pause_audio.get_time_step(self.path)
        self.sound = torchaudio.load(self.path)[0][0]
        chek_1 = datetime.now()
        print(f'>>> Init class Gen_batch: {chek_1-chek_0}')

    def gen_ind_batch(self, 
                  ):
        t_ind = 0
        while t_ind < self.time_step[-1]:
            for i in self.time_step:
                if i > t_ind+self.min_len and i < t_ind+self.max_len:
                    t_ind = i
                    yield t_ind
            if t_ind <= self.time_step[-1]-0.03:
                t_ind += self.max_len
                yield t_ind

    def __len__(self, 
                  ):
        j = 0
        t_ind = 0
        while t_ind < self.time_step[-1]:
            for i in self.time_step:
                if i > t_ind+self.min_len and i < t_ind+self.max_len:
                    t_ind = i
                    j+=1
            
            if t_ind <= self.time_step[-1]-0.03:
                t_ind += self.max_len
                j+=1
        return j
    
    def get_batch(self):

        p = 0
        for name, i in enumerate(self.gen_ind_batch()):
            speech_array = self.sound[int(p*16_000):int(i*16_000)]
            p = i
            yield speech_array

