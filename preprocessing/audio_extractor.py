import os
import moviepy.editor as mp

__version__ = "0.0.5"


class AudioExtractor(object):
    def __init__(self, path):
        self.path = path
        self.dir = os.path.split(path)[0]
        filename, file_ext = os.path.splitext(path)
        self.filename = filename
        self.file_ext = file_ext[1:]
        self.sr = 16000

        self.video_ext = ('mp4', 'avi', 'mkv')
        self.audio_ext = ('mp3', 'wav')

    def get_audio(self, output_ext):
        if self.file_ext in self.video_ext:
            self.extract_audio(output_ext)
        elif self.file_ext in self.audio_ext:
            self.convert_audio(output_ext)

    def extract_audio(self, output_ext):
        clip = mp.VideoFileClip(f"{self.path}")
        if output_ext == 'wav':
            clip.audio.write_audiofile(f"output.{output_ext}",
                                       codec="pcm_s16le",
                                       fps=self.sr,
                                       ffmpeg_params=["-ac", "1"])
        elif output_ext == 'mp3':
            clip.audio.write_audiofile(f"output.{output_ext}")
        clip.close()

    def convert_audio(self, output_ext):
        clip = mp.AudioFileClip(f"{self.path}")
        if output_ext == 'wav':
            clip.write_audiofile(f"output.{output_ext}",
                                 codec="pcm_s16le",
                                 fps=self.sr,
                                 ffmpeg_params=["-ac", "1"])
        elif output_ext == 'mp3':
            clip.write_audiofile(f"output.{output_ext}")
        clip.close()

def multiple_extraction(filename, formats=[], remove_original=False):
    # name = filename.split('.')[0]
    # for format in formats:
    #     if os.path.exists('' + name + '.' + format):
    #         os.remove('' + name + '.' + format)

    extractor = AudioExtractor(filename)
    for format in formats:
        extractor.get_audio(output_ext=format)

    if remove_original:
        os.remove(''+filename)


if __name__ == "__main__":
    path = input("Введите путь к файлу: ")
    extractor = AudioExtractor(path)
    extractor.get_audio(output_ext='wav')
