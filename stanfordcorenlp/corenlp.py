# _*_coding:utf-8_*_
from __future__ import print_function

import glob
import json
import logging
import os
import re
import signal
import socket
import subprocess
import sys
import time

import psutil

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import requests


class StanfordCoreNLP:
    def __init__(self, path_or_host, port=8000, memory='4g', lang='en', timeout=1500, quiet=True,
                 logging_level=logging.WARNING):
        self.path_or_host = path_or_host
        self.port = port
        self.memory = memory
        self.lang = lang
        self.timeout = timeout
        self.quiet = quiet
        self.logging_level = logging_level

        logging.basicConfig(level=self.logging_level)

        # Check args
        self._check_args()

        if path_or_host.startswith('http'):
            self.url = path_or_host + ':' + str(port)
            logging.info('Using an existing server {}'.format(self.url))
        else:

            # Check Java
            if not subprocess.call(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) == 0:
                raise RuntimeError('Java not found.')

            # Check if the dir exists
            if not os.path.isdir(self.path_or_host):
                raise IOError(str(self.path_or_host) + ' is not a directory.')
            directory = os.path.normpath(self.path_or_host) + os.sep

            # Check if the language specific model file exists
            switcher = {
                'en': 'stanford-corenlp-[0-9].[0-9].[0-9]-models.jar',
                'zh': 'stanford-chinese-corenlp-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-models.jar',
                'ar': 'stanford-arabic-corenlp-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-models.jar',
                'fr': 'stanford-french-corenlp-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-models.jar',
                'de': 'stanford-german-corenlp-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-models.jar',
                'es': 'stanford-spanish-corenlp-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-models.jar'
            }
            jars = {
                'en': 'stanford-corenlp-x.x.x-models.jar',
                'zh': 'stanford-chinese-corenlp-yyyy-MM-dd-models.jar',
                'ar': 'stanford-arabic-corenlp-yyyy-MM-dd-models.jar',
                'fr': 'stanford-french-corenlp-yyyy-MM-dd-models.jar',
                'de': 'stanford-german-corenlp-yyyy-MM-dd-models.jar',
                'es': 'stanford-spanish-corenlp-yyyy-MM-dd-models.jar'
            }
            if len(glob.glob(directory + switcher.get(self.lang))) <= 0:
                raise IOError(jars.get(
                    self.lang) + ' not exists. You should download and place it in the ' + directory + ' first.')

            # Check if the port is in use
            if self.port in [conn.laddr[1] for conn in psutil.net_connections()]:
                raise IOError('Port ' + str(self.port) + ' is already in use.')

            # Start native server
            logging.info('Initializing native server...')
            cmd = "java"
            java_args = "-Xmx{}".format(self.memory)
            java_class = "edu.stanford.nlp.pipeline.StanfordCoreNLPServer"
            path = '"{}*"'.format(directory)

            args = [cmd, java_args, '-cp', path, java_class, '-port', str(self.port)]

            args = ' '.join(args)

            logging.info(args)

            # Silence
            with open(os.devnull, 'w') as null_file:
                out_file = None
                if self.quiet:
                    out_file = null_file

                self.p = subprocess.Popen(args, shell=True, stdout=out_file, stderr=subprocess.STDOUT)
                logging.info('Server shell PID: {}'.format(self.p.pid))

            self.url = 'http://localhost:' + str(self.port)

        # Wait until server starts
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = urlparse(self.url).hostname
        while sock.connect_ex((host_name, self.port)):
            logging.info('Waiting until the server is available.')
            time.sleep(1)
        logging.info('The server is available.')

    def __del__(self):
        logging.info('Cleanup...')
        if hasattr(self, 'p'):
            try:
                parent = psutil.Process(self.p.pid)
            except psutil.NoSuchProcess:
                logging.info('No process: {}'.format(self.p.pid))
                return
            children = parent.children(recursive=True)
            for process in children:
                logging.info('Killing pid: {} cmdline: {}'.format(process.pid, process.cmdline()))
                process.send_signal(signal.SIGTERM)

            logging.info('Killing shell pid: {}'.format(parent.pid))
            parent.send_signal(signal.SIGTERM)

    def annotate(self, text, properties=None):
        if sys.version_info.major >= 3:
            text = text.encode('utf-8')

        r = requests.post(self.url, params={'properties': str(properties)}, data=text,
                          headers={'Connection': 'close'})
        return r.text

    def word_tokenize(self, sentence):
        r_dict = self._request('ssplit,tokenize', sentence)
        return [token['word'] for s in r_dict['sentences'] for token in s['tokens']]

    def pos_tag(self, sentence):
        r_dict = self._request('pos', sentence)
        words = []
        tags = []
        for s in r_dict['sentences']:
            for token in s['tokens']:
                words.append(token['word'])
                tags.append(token['pos'])
        return list(zip(words, tags))

    def ner(self, sentence):
        r_dict = self._request('ner', sentence)
        words = []
        ner_tags = []
        for s in r_dict['sentences']:
            for token in s['tokens']:
                words.append(token['word'])
                ner_tags.append(token['ner'])
        return list(zip(words, ner_tags))

    def parse(self, sentence):
        r_dict = self._request('pos,parse', sentence)
        return [s['parse'] for s in r_dict['sentences']][0]

    def dependency_parse(self, sentence):
        r_dict = self._request('depparse', sentence)
        return [(dep['dep'], dep['governor'], dep['dependent']) for s in r_dict['sentences'] for dep in
                s['basicDependencies']]

    def _request(self, annotators=None, data=None):
        if sys.version_info.major >= 3:
            data = data.encode('utf-8')

        properties = {'annotators': annotators, 'pipelineLanguage': self.lang, 'outputFormat': 'json'}
        r = requests.post(self.url, params={'properties': str(properties)}, data=data,
                          headers={'Connection': 'close'})
        r_dict = json.loads(r.text)

        return r_dict

    def _check_args(self):
        if self.lang not in ['en', 'zh', 'ar', 'fr', 'de', 'es']:
            raise ValueError(
                'lang=' + self.lang + ' not supported. Use English(en), Chinese(zh), Arabic(ar), French(fr), German(de), Spanish(es).')
        if not re.match('\dg', self.memory):
            raise ValueError('memory=' + self.memory + ' not supported. Use 4g, 6g, 8g and etc. ')

    def dcorf(self,sentence):
        text=[]
        cluster_no=[]
        position=[]
        r_dict=self._request('dcoref',sentence)
        for key,value in r_dict['corefs'].items():
            for i in range(len(value)):
                position.append(value[i]['position']),cluster_no.append(key),text.append(value[i]['text'])
        return position,cluster_no,text
