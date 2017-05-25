from setuptools import setup

setup(
    name='stanfordcorenlp',
    packages=['stanfordcorenlp'],
    version='3.7.0.1',
    description='Python wrapper for Stanford CoreNLP.',

    author='Lynten Guo',
    author_email='1216920263@qq.com',

    url='https://github.com/Lynten/stanford-corenlp',
    keywords=['NLP', 'CL', 'natural language processing',
              'computational linguistics'],
    install_requires=['requests'],

    license="MIT License (SEE LICENSE)",

)
