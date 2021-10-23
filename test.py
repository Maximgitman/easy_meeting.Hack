# -*- coding: utf-8 -*-

from NLP.summarization import Summarization

summarization = Summarization()


with open(r"C:\Users\Yuriy\Downloads\text (6).txt", "r") as file:
        text = file.read()

print('>>> ', summarization.inference(text))