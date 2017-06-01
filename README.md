## stanfordcorenlp
`stanfordcorenlp` is a Python wrapper for [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/). It provides a simple API for text processing tasks such as Tokenization, Part of Speech Tagging, Named Entity Reconigtion, Constituency Parsing, Dependency Parsing, and more.

## Prerequisites
Java 1.8+ (Check with command: `java -version`) ([Download Page](http://www.oracle.com/technetwork/cn/java/javase/downloads/jdk8-downloads-2133151-zhs.html))

Stanford CoreNLP 3.7.0 ([Download Page](https://stanfordnlp.github.io/CoreNLP/download.html))

## Installation

`pip install stanfordcorenlp`

## Example
### Simple Usage
```python
# Simple usage
from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/')

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
print 'Tokenize:', nlp.word_tokenize(sentence)
print 'Part of Speech:', nlp.pos_tag(sentence)
print 'Named Entities:', nlp.ner(sentence)
print 'Constituency Parsing:', nlp.parse(sentence)
print 'Dependency Parsing:', nlp.dependency_parse(sentence)
```

Output format:
```python
# Tokenize
[u'Guangdong', u'University', u'of', u'Foreign', u'Studies', u'is', u'located', u'in', u'Guangzhou', u'.']

# Part of Speech
[(u'Guangdong', u'NNP'), (u'University', u'NNP'), (u'of', u'IN'), (u'Foreign', u'NNP'), (u'Studies', u'NNPS'), (u'is', u'VBZ'), (u'located', u'JJ'), (u'in', u'IN'), (u'Guangzhou', u'NNP'), (u'.', u'.')]

# Named Entities:
 [(u'Guangdong', u'ORGANIZATION'), (u'University', u'ORGANIZATION'), (u'of', u'ORGANIZATION'), (u'Foreign', u'ORGANIZATION'), (u'Studies', u'ORGANIZATION'), (u'is', u'O'), (u'located', u'O'), (u'in', u'O'), (u'Guangzhou', u'LOCATION'), (u'.', u'O')]

# Constituency Parsing
 (ROOT
  (S
    (NP
      (NP (NNP Guangdong) (NNP University))
      (PP (IN of)
        (NP (NNP Foreign) (NNPS Studies))))
    (VP (VBZ is)
      (ADJP (JJ located)
        (PP (IN in)
          (NP (NNP Guangzhou)))))
    (. .)))

# Dependency Parsing
[(u'ROOT', 0, 7), (u'compound', 2, 1), (u'nsubjpass', 7, 2), (u'case', 5, 3), (u'compound', 5, 4), (u'nmod', 2, 5), (u'auxpass', 7, 6), (u'case', 9, 8), (u'nmod', 7, 9), (u'punct', 7, 10)]

```

### Other Human Languages Support
Note: you must download addditinal model file and place it in the `.../stanford-corenlp-full-2016-10-31/` folder. For example, you should [download](http://nlp.stanford.edu/software/stanford-chinese-corenlp-2016-10-31-models.jar) the `stanford-chinese-corenlp-2016-10-31-models.jar` file if you want to process Chinese.
```python
# Other human languages support, e.g. Chinese
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/',
                      lang='zh')

sentence = '清华大学位于北京。'
print nlp.word_tokenize(sentence)
print nlp.pos_tag(sentence)
print nlp.ner(sentence)
print nlp.parse(sentence)
print nlp.dependency_parse(sentence)
```

### General Stanford CoreNLP API
```python
 # General json output
print nlp.annotate(sentence)
```
You can specify properties:

- annotators: `tokenize, ssplit, pos, lemma, ner, parse, depparse, dcoref` ([See Detail](https://stanfordnlp.github.io/CoreNLP/annotators.html))

- pinelineLanguage: `en, zh, fr, de, es` (English, Chinese, French, German, Spanish) ([See Annotator Support Detail](https://stanfordnlp.github.io/CoreNLP/human-languages.html)) 

- outputFormat: `json, xml, text`
```python
text = 'Guangdong University of Foreign Studies is located in Guangzhou. ' \
       'GDUFS is active in a full range of international cooperation and exchanges in education. '
print nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos','pinelineLanguage':'en','outputFormat':'xml'})
```


### Use an Existing Server
```python
# Use an existing server
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
```