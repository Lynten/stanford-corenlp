## Prerequisites
Java 1.8+

Stanford CoreNLP 3.7.0 ([Download Page](https://stanfordnlp.github.io/CoreNLP/download.html))

## Installation

`pip install stanfordcorenlp`

## Example
### Simple Usage
```python
# Simple usage
nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/')

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
print 'Tokenize:', nlp.word_tokenize(sentence)
print 'Part of Speech:', nlp.pos_tag(sentence)
print 'Named Entities:', nlp.ner(sentence)
print 'Constituency Parsing:', nlp.parse(sentence)
print 'Dependency Parsing:', nlp.dependency_parse(sentence)
```

### General Stanford CoreNLP API
```python
 # General json output
print nlp.annotate(sentence)
```

### Other Human Languages Support
Note: you must download addditinal model files and place it in the `.../stanford-corenlp-full-2016-10-31/` folder. For example, you should [download](http://nlp.stanford.edu/software/stanford-chinese-corenlp-2016-10-31-models.jar) the `stanford-chinese-corenlp-2016-10-31-models.jar` file if you want to process Chinese.
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

print nlp.word_tokenize(sentence)
print nlp.pos_tag(sentence)
print nlp.ner(sentence)
print nlp.parse(sentence)
print nlp.dependency_parse(sentence)

print nlp.annotate(sentence)
```

### Use an Existing Server
```python
# Use an existing server
nlp = StanfordCoreNLP('http://corenlp.run', port=80)
```