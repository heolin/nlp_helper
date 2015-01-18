#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import argparse

from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


MISSED = 'missed'

def normalize(input_text):
    result = input_text
    result = result[0].lower() + result[1:]
    result = re.sub('[.,?!]', '', result)
    return result


def lemmatize(word):
    args = ["morfologik-tools-1.9.0-standalone.jar", "plstem"]
    process = Popen(['java', '-jar']+list(args), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout = process.communicate(word)[0]
    process.stdin.close()
    result = stdout.split('\n')
    return result[4:-2]


def parse_data(lemma_data):
    lemma_data = lemma_data.split('\t')
    lemma_data[2] = [r.split(':') for r in lemma_data[2].split('+')]
    pos = []
    for r in lemma_data[2]:
        number = ""
        if len(r) > 1:
            if r[1] in ["pl", "sg"]:
                number = r[1]
        pos.append((r[0], number))
    pos = list(set(pos))

    return [lemma_data[0], lemma_data[1], pos]


def filter_data(lemma_data):
    if len(lemma_data) == 0:
        return []
    result = [lemma_data[0]]
    for lemma in lemma_data:
        if result[-1][0] != lemma[0]:
            result.append(lemma)
        else:
            result[-1][2].extend(lemma[2])
    for lemma in result:
        if lemma[1] == "-":
            lemma[1] = lemma[0]
            lemma[2] = ['subst', MISSED]
        lemma[2] = tuple(set([r for r in lemma[2]]))
    return result


def process_sentence(sentence):
    norm_text = normalize(sentence)
    lemma_data = lemmatize(norm_text)
    lemma_data = [parse_data(lemma) for lemma in lemma_data]
    sentence_data = filter_data(lemma_data)
    return tuple([(sentence, "", "")] + sentence_data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to file with input data.", required=True)
    parser.add_argument("-o", "--output", help="Path to output file, where to save parsed data.", required=True)

    args = parser.parse_args(sys.argv[1:])

    input_text = open(args.input).read().split('\n')[:-1]
    output_file = open(args.output, 'w')

    for sentence in input_text:
        sentence_data = process_sentence(sentence)
        for data in sentence_data:
            pos = ["{},{}".format(p[0], p[1]) for p in data[2]]
            output_file.write("{}\t{}\t{}\n".format(data[0], data[1], ";".join(pos)))
        output_file.write('\n')
    output_file.close()

if __name__ == "__main__":
    main()
