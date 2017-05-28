# _*_coding:utf-8_*_
import json
import os
import socket
import subprocess
import sys
from urlparse import urlparse

import requests
import time

import signal


class StanfordCoreNLP:
    def __init__(self, path_or_host, port=9000, memory='4g', lang='en', timeout=1500):
        self.path_or_host = path_or_host
        self.port = port
        self.memory = memory
        self.lang = lang
        self.timeout = timeout

        if path_or_host.startswith('http'):
            self.url = path_or_host + ':' + str(port)
            print 'Using an existing server {}'.format(self.url)
        else:
            print 'Initializing native server...'
            cmd = "java"
            java_args = "-Xmx{}".format(self.memory)
            java_class = "edu.stanford.nlp.pipeline.StanfordCoreNLPServer"
            path = '"{}*"'.format(self.path_or_host)

            args = [cmd, java_args, '-cp', path, java_class, '-port', str(self.port)]

            args = ' '.join(args)

            print args

            if sys.platform.startswith('win'):
                self.p = subprocess.Popen(args, shell=True)
            else:
                self.p = subprocess.Popen(args, shell=True, preexec_fn=os.setsid)

            self.url = 'http://localhost:' + str(self.port)

        # Wait until server starts
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = urlparse(self.url).hostname
        while sock.connect_ex((host_name, self.port)):
            print 'waiting until the server is available.'
            time.sleep(1)
        print 'The server is available.'

    def __del__(self):
        if sys.platform.startswith('win'):
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.p.pid)])
        else:
            os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)

    def annotate(self, text, properties=None):
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
        return zip(words, tags)

    def ner(self, sentence):
        r_dict = self._request('ner', sentence)
        words = []
        ner_tags = []
        for s in r_dict['sentences']:
            for token in s['tokens']:
                words.append(token['word'])
                ner_tags.append(token['ner'])
        return zip(words, ner_tags)

    def parse(self, sentence):
        r_dict = self._request('pos,parse', sentence)
        return [s['parse'] for s in r_dict['sentences']][0]

    def dependency_parse(self, sentence):
        r_dict = self._request('depparse', sentence)
        return [(dep['dep'], dep['governor'], dep['dependent']) for s in r_dict['sentences'] for dep in
                s['basicDependencies']]

    def _request(self, annotators=None, data=None):
        properties = {'annotators': annotators, 'pipelineLanguage': self.lang, 'outputFormat': 'json'}
        r = requests.post(self.url, params={'properties': str(properties)}, data=data,
                          headers={'Connection': 'close'})
        r_dict = json.loads(r.text)

        return r_dict
