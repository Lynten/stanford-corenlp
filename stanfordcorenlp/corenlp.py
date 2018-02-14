# _*_coding:utf-8_*_
from __future__ import print_function

import glob
import json
import logging
import os
import re
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
    def __init__(self, path_or_host, port=None, memory='4g', lang='en', timeout=1500, quiet=True,
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
            self.class_path_dir = directory

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

            # If port not set, auto select
            if self.port is None:
                for port_candidate in range(9000, 65535):
                    if port_candidate not in [conn.laddr[1] for conn in psutil.net_connections()]:
                        self.port = port_candidate
                        break

            # Check if the port is in use
            if self.port in [conn.laddr[1] for conn in psutil.net_connections()]:
                raise IOError('Port ' + str(self.port) + ' is already in use.')

            # Start native server
            logging.info('Initializing native server...')
            cmd = "java"
            java_args = "-Xmx{}".format(self.memory)
            java_class = "edu.stanford.nlp.pipeline.StanfordCoreNLPServer"
            class_path = '"{}*"'.format(directory)

            args = [cmd, java_args, '-cp', class_path, java_class, '-port', str(self.port)]

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
        time.sleep(1)  # OSX, not tested
        while sock.connect_ex((host_name, self.port)):
            logging.info('Waiting until the server is available.')
            time.sleep(1)
        logging.info('The server is available.')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        logging.info('Cleanup...')
        if hasattr(self, 'p'):
            try:
                parent = psutil.Process(self.p.pid)
            except psutil.NoSuchProcess:
                logging.info('No process: {}'.format(self.p.pid))
                return

            if self.class_path_dir not in ' '.join(parent.cmdline()):
                logging.info('Process not in: {}'.format(parent.cmdline()))
                return

            children = parent.children(recursive=True)
            for process in children:
                logging.info('Killing pid: {}, cmdline: {}'.format(process.pid, process.cmdline()))
                # process.send_signal(signal.SIGTERM)
                process.kill()

            logging.info('Killing shell pid: {}, cmdline: {}'.format(parent.pid, parent.cmdline()))
            # parent.send_signal(signal.SIGTERM)
            parent.kill()

    def annotate(self, text, properties=None):
        if sys.version_info.major >= 3:
            text = text.encode('utf-8')

        r = requests.post(self.url, params={'properties': str(properties)}, data=text,
                          headers={'Connection': 'close'})
        return r.text

    def tregex(self, sentence, pattern):
        tregex_url = self.url + '/tregex'
        r_dict = self._request(tregex_url, pattern, "tokenize,ssplit,depparse,parse", sentence)
        return r_dict

    def tokensregex(self, sentence, pattern):
        tokensregex_url = self.url + '/tokensregex'
        r_dict = self._request(tokensregex_url, pattern, "tokenize,ssplit,depparse", sentence)
        return r_dict

    def semgrex(self, sentence, pattern):
        semgrex_url = self.url + '/semgrex'
        r_dict = self._request(semgrex_url, pattern, "tokenize,ssplit,depparse", sentence)
        return r_dict

    def word_tokenize(self, sentence, span=False):
        r_dict = self._request('ssplit,tokenize', sentence)
        tokens = [token['word'] for s in r_dict['sentences'] for token in s['tokens']]

        # Whether return token span
        if span:
            spans = [(token['characterOffsetBegin'], token['characterOffsetEnd']) for s in r_dict['sentences'] for token
                     in s['tokens']]
            return tokens, spans
        else:
            return tokens

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

    def switch_language(self, language="en"):
        self._check_language(language)
        self.lang = language

    def _request(self, annotators=None, data=None, *args, **kwargs):
        if sys.version_info.major >= 3:
            data = data.encode('utf-8')

        properties = {'annotators': annotators, 'outputFormat': 'json'}
        params = {'properties': str(properties), 'pipelineLanguage': self.lang}
        if 'pattern' in kwargs:
            params = {"pattern": kwargs['pattern'], 'properties': str(properties), 'pipelineLanguage': self.lang}

        logging.info(params)
        r = requests.post(self.url, params=params, data=data, headers={'Connection': 'close'})
        r_dict = json.loads(r.text)

        return r_dict

    def _check_args(self):
        self._check_language(self.lang)
        if not re.match('\dg', self.memory):
            raise ValueError('memory=' + self.memory + ' not supported. Use 4g, 6g, 8g and etc. ')

    def _check_language(self, lang):
        if lang not in ['en', 'zh', 'ar', 'fr', 'de', 'es']:
            raise ValueError('lang=' + self.lang + ' not supported. Use English(en), Chinese(zh), Arabic(ar), '
                                                   'French(fr), German(de), Spanish(es).')
