from ASR.asr import ASR
from ASR.asr import Gen_batch
from punctuations.punctuation import Punctuation
from word2number.extractor import NumberExtractor





def main_asr(path_wav,
        model_path_asr='/content/drive/MyDrive/easy_meeting/models/ru_3_norm/wav2vec2-large-xlsr-russian-demo/checkpoint-3540',
        processor_path_asr='jonatasgrosman/wav2vec2-large-xlsr-53-russian',
        yml_path_punctuation='/content/drive/MyDrive/easy_meeting/models/maks/latest_silero_models.yml',
        model_path_punctuation='/content/drive/MyDrive/easy_meeting/models/maks/v1_4lang_q.pt',
        device='cpu',
        min_len_sec=100,
        max_len_sec=150,
        step_punctuation=30,
        ):

    asr = ASR(model_path=model_path_asr,
                processor_path=processor_path_asr,
                device=device)

    data = Gen_batch(path_wav, 
                        min_len=min_len_sec, 
                        max_len=max_len_sec)
    text = ''
    for name, i in enumerate(data.get_batch()):
        text +=  asr.inference(i) + ' '


    punct = Punctuation(yml_path=yml_path_punctuation, 
                        model_path= model_path_punctuation,
                        step=step_punctuation)

    text_ = punct.apply_te(text)


    ext = NumberExtractor()
    text_with_num = ext.replace_groups(text_)

    return text_with_num



# if __name__ == "__main__":
#     path_wav = ''
#     text_with_num = main_asr(path_wav)
#     print(text_with_num)