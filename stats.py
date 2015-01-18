#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import collections

def frequency(input_list):
    return collections.Counter(input_list).most_common()

class TextData(object):
    def __init__(self):
        self.words = []
        self.lemmas = []
        self.poses = []
        self.number = []

        self.sentences = []
        self.simple_sentences = []
        self.complex_sentences = []

    def get_words_freq(self):
        return frequency(self.words)

    def get_lemmas_freq(self):
        return frequency(self.lemmas)

    def get_poses_freq(self):
        return frequency(self.poses)

    def get_number_freq(self):
        return frequency(self.number)

    def get_sentences_freq(self):
        return frequency(self.sentences)

    def get_simple_sentences_freq(self):
        return frequency(self.simple_sentences)

    def get_complex_sentences_freq(self):
        return frequency(self.complex_sentences)


def get_data(data):
    text_data = TextData()

    for sentence in data:
        verbs = 0
        for word in sentence[1:]:
            text_data.words.append(word[0])
            text_data.lemmas.append(word[1])
            pos_data = word[2].split(';')[0].split(',')
            pos = pos_data[0]
            text_data.poses.append(pos)
            if pos == "verb":
                verbs += 1
            number = pos_data[1]
            if number:
                text_data.number.append(number)

        text_data.sentences.append(sentence[0][0])

        if verbs > 1:
            text_data.complex_sentences.append(sentence[0][0])
        else:
            text_data.simple_sentences.append(sentence[0][0])

    return text_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to file with input data with parsed data.", required=True)
    parser.add_argument("-o", "--output", help="Path to output file with stats of parsed data.", required=True)
    parser.add_argument("-w", "--words", help="Path to output file with words frequency list.")
    parser.add_argument("-l", "--lemmas", help="Path to output file with lemmas frequency list.")
    parser.add_argument("-s", "--sentences", help="Path to output file with sentences frequency list.")
    parser.add_argument("-ss", "--simple", help="Path to output file with simple sentences frequency list.")
    parser.add_argument("-cs", "--complex", help="Path to output file with complex sentences frequency list.")

    args = parser.parse_args(sys.argv[1:])

    input_text = open(args.input).read().split('\n\n')[:-1]
    sentences_data = [tuple(tuple(r.split('\t')) for r in sen.split('\n')) for sen in input_text]

    data = get_data(sentences_data)

    with open(args.output, 'w') as stats_file:
        stats_file.write("Words:\t{}\n".format(len(data.words)))
        stats_file.write("\n")
        stats_file.write("Uniq words:\t{}\n".format(len(data.get_words_freq())))
        stats_file.write("Uniq lemmas:\t{}\n".format(len(data.get_lemmas_freq())))
        stats_file.write("\n\n")
        stats_file.write("Sentences:\t{}\n".format(len(data.sentences)))
        stats_file.write("Simple sentences:\t{}\n".format(len(data.simple_sentences)))
        stats_file.write("Complex sentences:\t{}\n".format(len(data.complex_sentences)))
        stats_file.write("\n")
        stats_file.write("Uniq sentences:\t{}\n".format(len(data.get_sentences_freq())))
        stats_file.write("Uniq simple sentences:\t{}\n".format(len(data.get_simple_sentences_freq())))
        stats_file.write("Uniq complex sentences:\t{}\n".format(len(data.get_complex_sentences_freq())))
        stats_file.write("\n\n")
        stats_file.write("POS Tags:\n")

        for pos in data.get_poses_freq():
            stats_file.write("\t{}\t{}\n".format(pos[0], pos[1]))

        stats_file.write("\n")
        stats_file.write("Numbers:\n")
        for number in data.get_number_freq():
            stats_file.write("\t{}\t{}\n".format(number[0], number[1]))


    if args.words:
        with open(args.words, 'w') as output_file:
            output_file.write("\n".join(["{}\t{}".format(word[0], word[1]) for word in data.get_words_freq()]))

    if args.lemmas:
        with open(args.lemmas, 'w') as output_file:
            output_file.write("\n".join(["{}\t{}".format(word[0], word[1]) for word in data.get_lemmas_freq()]))

    if args.sentences:
        with open(args.sentences, 'w') as output_file:
            output_file.write("\n".join(["{}\t{}".format(word[0], word[1]) for word in data.get_sentences_freq()]))

    if args.simple:
        with open(args.simple, 'w') as output_file:
            output_file.write("\n".join(["{}\t{}".format(word[0], word[1]) for word in data.get_simple_sentences_freq()]))

    if args.complex:
        with open(args.complex, 'w') as output_file:
            output_file.write("\n".join(["{}\t{}".format(word[0], word[1]) for word in data.get_complex_sentences_freq()]))


if __name__ == "__main__":
    main()
