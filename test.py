# _*_coding:utf-8_*_

from stanfordcorenlp.corenlp import StanfordCoreNLP

# Simple usage
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/',memory='7g')

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
print 'Tokenize:', nlp.word_tokenize(sentence)
print 'Part of Speech:', nlp.pos_tag(sentence)
print 'Named Entities:', nlp.ner(sentence)
print 'Constituency Parsing:', nlp.parse(sentence)
print 'Dependency Parsing:', nlp.dependency_parse(sentence)

# General Stanford CoreNLP API
print nlp.annotate(sentence)

# Other human languages support, e.g. Chinese
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/',
                      lang='zh')

sentence = '清华大学位于北京。'
print nlp.word_tokenize(sentence)
print nlp.pos_tag(sentence)
print nlp.ner(sentence)
print nlp.parse(sentence)
print nlp.dependency_parse(sentence)

print nlp.word_tokenize(sentence)
print nlp.pos_tag(sentence)
print nlp.ner(sentence)
print nlp.parse(sentence)
print nlp.dependency_parse(sentence)

# Use an existing server
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
