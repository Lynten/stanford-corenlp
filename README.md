## stanfordcorenlp
[![PyPI](https://img.shields.io/pypi/v/stanfordcorenlp.svg)]()
[![GitHub release](https://img.shields.io/github/release/Lynten/stanford-corenlp.svg)]()
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stanfordcorenlp.svg)]()


`stanfordcorenlp` is a Python wrapper for [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/). It provides a simple API for text processing tasks such as Tokenization, Part of Speech Tagging, Named Entity Reconigtion, Constituency Parsing, Dependency Parsing, and more.

## Prerequisites
Java 1.8+ (Check with command: `java -version`) ([Download Page](http://www.oracle.com/technetwork/cn/java/javase/downloads/jdk8-downloads-2133151-zhs.html))

Stanford CoreNLP ([Download Page](https://stanfordnlp.github.io/CoreNLP/history.html))

| Py Version | CoreNLP Version |
| --- | --- |
|v3.7.0.1 v3.7.0.2 | CoreNLP 3.7.0 |
|v3.8.0.1 | CoreNLP 3.8.0 |
|v3.9.1.1 | CoreNLP 3.9.1 |

## Installation

`pip install stanfordcorenlp`

## Example
### Simple Usage
```python
# Simple usage
from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'G:\JavaLibraries\stanford-corenlp-full-2018-02-27')

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou. It is a beautiful university.'
print('Tokenize:', nlp.word_tokenize(sentence))
print('Part of Speech:', nlp.pos_tag(sentence))
print('Named Entities:', nlp.ner(sentence))
print('Constituency Parsing:', nlp.parse(sentence))
print('Dependency Parsing:', nlp.dependency_parse(sentence))
print('Coreferce Resolution:', nlp.coref(sentence))

nlp.close() # Do not forget to close! The backend server will consume a lot memery.
```

Output format:
```python
# Tokenize
[u'Guangdong', u'University', u'of', u'Foreign', u'Studies', u'is', u'located', u'in', u'Guangzhou', u'.']

# Part of Speech
[(u'Guangdong', u'NNP'), (u'University', u'NNP'), (u'of', u'IN'), (u'Foreign', u'NNP'), (u'Studies', u'NNPS'), (u'is', u'VBZ'), (u'located', u'JJ'), (u'in', u'IN'), (u'Guangzhou', u'NNP'), (u'.', u'.')]

# Named Entities
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

# Coreference Resolution
[[(1, 1, 6, 'Guangdong University of Foreign Studies'), (2, 1, 2, 'It')]]

```

### Other Human Languages Support
Note: you must download an additional model file and place it in the `.../stanford-corenlp-full-2018-02-27` folder. For example, you should download the `stanford-chinese-corenlp-2018-02-27-models.jar` file if you want to process Chinese.
```python
# _*_coding:utf-8_*_

# Other human languages support, e.g. Chinese
sentence = '清华大学位于北京。它是一所综合性大学。'

with StanfordCoreNLP(r'G:\JavaLibraries\stanford-corenlp-full-2018-02-27', lang='zh') as nlp:
    print(nlp.word_tokenize(sentence))
    print(nlp.pos_tag(sentence))
    print(nlp.ner(sentence))
    print(nlp.parse(sentence))
    print(nlp.dependency_parse(sentence))
    print(nlp.coref(sentence))
```

### General Stanford CoreNLP API
Since this will load all the models which require more memory, initialize the server with more memory. 8GB is recommended.

```python
 # General json output
nlp = StanfordCoreNLP(r'path_to_corenlp', memory='8g')
print(nlp.annotate(sentence))
nlp.close()
```
You can specify properties:

- `annotators`: `tokenize, ssplit, pos, lemma, ner, parse, depparse, dcoref` ([See Detail](https://stanfordnlp.github.io/CoreNLP/annotators.html))

- `pipelineLanguage`: `en, zh, ar, fr, de, es` (English, Chinese, Arabic, French, German, Spanish) ([See Annotator Support Detail](https://stanfordnlp.github.io/CoreNLP/human-languages.html)) 

- `outputFormat`: `json, xml, text`
```python
text = 'Guangdong University of Foreign Studies is located in Guangzhou. ' \
       'GDUFS is active in a full range of international cooperation and exchanges in education. '

props={'annotators': 'tokenize,ssplit,pos','pipelineLanguage':'en','outputFormat':'xml'}
print(nlp.annotate(text, properties=props))
nlp.close()
```


### Use an Existing Server
Start a [CoreNLP Server](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) with command:
```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```
And then:
```python
# Use an existing server
nlp = StanfordCoreNLP('http://localhost', port=9000)
```

## Debug
```python
import logging
from stanfordcorenlp import StanfordCoreNLP

# Debug the wrapper
nlp = StanfordCoreNLP(r'path_or_host', logging_level=logging.DEBUG)

# Check more info from the CoreNLP Server 
nlp = StanfordCoreNLP(r'path_or_host', quiet=False, logging_level=logging.DEBUG)
nlp.close()
```

## Build

We use `setuptools` to package our project. You can build from the latest source code with the following command:
```
$ python setup.py bdist_wheel --universal
```

You will see the `.whl` file under `dist` directory.

## Common Error
```python
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/psutil/_psosx.py", line 339, in wrapper
    return fun(self, *args, **kwargs)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/psutil/_psosx.py", line 528, in connections
    rawlist = cext.proc_connections(self.pid, families, types)
PermissionError: [Errno 1] Operation not permitted

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/USERNAME/Stanford-OpenIE-Python/stanford-corenlp/simple_usage.py", line 4, in <module>
    nlp = StanfordCoreNLP(r'../stanford-corenlp-full-2018-10-05')
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/stanfordcorenlp/corenlp.py", line 79, in __init__
    if port_candidate not in [conn.laddr[1] for conn in psutil.net_connections()]:
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/psutil/__init__.py", line 2263, in net_connections
    return _psplatform.net_connections(kind)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/psutil/_psosx.py", line 252, in net_connections
    cons = Process(pid).connections(kind)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/psutil/_psosx.py", line 344, in wrapper
    raise AccessDenied(self.pid, self._name)
psutil.AccessDenied: psutil.AccessDenied (pid=2059)
```

The solution to the error is to run the file as Root User and run with Terminal on MacOS or other command line tools in other OS.
