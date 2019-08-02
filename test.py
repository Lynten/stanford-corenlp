# _*_coding:utf-8_*_

from __future__ import print_function

import logging

from stanfordcorenlp import StanfordCoreNLP

# local_corenlp_path = r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/'
# local_corenlp_path = r'G:\JavaLibraries\stanford-corenlp-full-2017-06-09'
local_corenlp_path = r'G:\JavaLibraries\stanford-corenlp-full-2018-01-31'
# local_corenlp_path = r'/home/gld/JavaLibs/stanford-corenlp-full-2016-10-31'

# Simple usage
nlp = StanfordCoreNLP(local_corenlp_path, quiet=False, logging_level=logging.DEBUG)

sentence = 'Guangdong University of Foreign Studies (GDUFS) is located in Guangzhou.'
print('Tokenize:', nlp.word_tokenize(sentence))
print('Part of Speech:', nlp.pos_tag(sentence))
print('Named Entities:', nlp.ner(sentence))
print('Constituency Parsing:', nlp.parse(sentence))
print('Dependency Parsing:', nlp.dependency_parse(sentence))
print('Coreference Resolution:', nlp.coref(sentence))

nlp.close()

# Other human languages support, e.g. Chinese
sentence = '清华大学位于北京。'

with StanfordCoreNLP(local_corenlp_path, lang='zh', quiet=False) as nlp:
    print(nlp.word_tokenize(sentence))
    print(nlp.pos_tag(sentence))
    print(nlp.ner(sentence))
    print(nlp.parse(sentence))
    print(nlp.dependency_parse(sentence))
    print(nlp.coref(sentence))

# General Stanford CoreNLP API
nlp = StanfordCoreNLP(local_corenlp_path, memory='8g', lang='zh')
print(nlp.annotate(sentence))
nlp.close()

nlp = StanfordCoreNLP(local_corenlp_path)
text = 'Guangdong University of Foreign Studies is located in Guangzhou. ' \
       'GDUFS is active in a full range of international cooperation and exchanges in education. '
pros = {'annotators': 'tokenize,ssplit,pos', 'pinelineLanguage': 'en', 'outputFormat': 'xml'}
print(nlp.annotate(text, properties=pros))
nlp.close()

# Use an existing server
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
