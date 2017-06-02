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

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],

    license="MIT License",

)
