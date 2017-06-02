# _*_coding:utf-8_*_

from __future__ import print_function

from stanfordcorenlp import StanfordCoreNLP

# Simple usage
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/')

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
print('Tokenize:', nlp.word_tokenize(sentence))
print('Part of Speech:', nlp.pos_tag(sentence))
print('Named Entities:', nlp.ner(sentence))
print('Constituency Parsing:', nlp.parse(sentence))
print('Dependency Parsing:', nlp.dependency_parse(sentence))

del nlp
# Other human languages support, e.g. Chinese
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/', lang='zh', quiet=False)

sentence = '清华大学位于北京。'
print(nlp.word_tokenize(sentence))
print(nlp.pos_tag(sentence))
print(nlp.ner(sentence))
print(nlp.parse(sentence))
print(nlp.dependency_parse(sentence))

del nlp
# General Stanford CoreNLP API
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/', memory='8g', lang='zh')
print(nlp.annotate(sentence))

del nlp
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/')

text = 'Guangdong University of Foreign Studies is located in Guangzhou. ' \
       'GDUFS is active in a full range of international cooperation and exchanges in education. '
print(nlp.annotate(text,
                   properties={'annotators': 'tokenize,ssplit,pos', 'pinelineLanguage': 'en', 'outputFormat': 'xml'}))

del nlp
# Use an existing server
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
