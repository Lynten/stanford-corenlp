# _*_coding:utf-8_*_

from __future__ import print_function

from stanfordcorenlp import StanfordCoreNLP

local_corenlp_path = r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/'
# local_corenlp_path = r'/home/gld/JavaLibs/stanford-corenlp-full-2016-10-31'

# Simple usage
nlp = StanfordCoreNLP(local_corenlp_path)

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
print('Tokenize:', nlp.word_tokenize(sentence))
print('Part of Speech:', nlp.pos_tag(sentence))
print('Named Entities:', nlp.ner(sentence))
print('Constituency Parsing:', nlp.parse(sentence))
print('Dependency Parsing:', nlp.dependency_parse(sentence))

nlp.__del__()
# Other human languages support, e.g. Chinese
nlp = StanfordCoreNLP(local_corenlp_path, lang='zh', quiet=False)

sentence = '清华大学位于北京。'
print(nlp.word_tokenize(sentence))
print(nlp.pos_tag(sentence))
print(nlp.ner(sentence))
print(nlp.parse(sentence))
print(nlp.dependency_parse(sentence))

nlp.__del__()
# General Stanford CoreNLP API
nlp = StanfordCoreNLP(local_corenlp_path, memory='8g', lang='zh')
print(nlp.annotate(sentence))

nlp.__del__()
nlp = StanfordCoreNLP(local_corenlp_path)

text = 'Guangdong University of Foreign Studies is located in Guangzhou. ' \
       'GDUFS is active in a full range of international cooperation and exchanges in education. '
print(nlp.annotate(text,
                   properties={'annotators': 'tokenize,ssplit,pos', 'pinelineLanguage': 'en', 'outputFormat': 'xml'}))

nlp.__del__()
# Use an existing server
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
