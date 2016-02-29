#!/usr/bin/env python3
"""Markov chain module."""

import random
import re
import pickle


class MarkovChain(object):
    """Markov chain class."""

    def __init__(self):
        """Create a new markov chain."""
        self._states = {}
        self._state_counts = {}

    def train(self, state, next):
        """Train the state, next state pair."""
        if state not in self._states:
            self._states[state] = {}

        state_dict = self._states[state]
        state_dict[next] = state_dict.get(next, 0) + 1
        self._state_counts[state] = self._state_counts.get(state, 0) + 1

    def next(self, state):
        """Get the next state from the given one."""
        state_dict = self._states[state]  # throw exception if not there
        choice = random.randint(0, self._state_counts[state])

        sum = 0
        for word, count in state_dict.items():
            if sum + count > choice:
                return word
            sum += count

        return random.choice(list(self._states.keys()))

    def train_words(self, words):
        """Train on the list of words."""
        it = iter(words)
        last = next(it)
        for curr in it:
            self.train(last, curr)
            last = curr

    def generate(self, count, start=None):
        """Generate the given number of words."""
        if start is None:
            start = random.choice(list(self._states))
        elif start not in self._states:
            import sys
            print("error: %sd not in word list" % start, file=sys.stderr)
            return
        return MarkovGenerator(self, start, count)


class MarkovGenerator(object):
    """Iterator that generates text from a Markov Chain."""

    def __init__(self, markov_chain, start_word, count=None):
        """Create a MarkovGenerator with a starting word and count."""
        self._markov = markov_chain
        self._previous = start_word
        self._count = count

    def __iter__(self):
        """This is an iterator!"""
        return self

    def __next__(self):
        """Generate and return a new word."""
        # Stop after we have generated enough.
        if self._count is not None and self._count <= 0:
            raise StopIteration()

        retval = self._markov.next(self._previous)
        self._previous = retval

        if self._count is not None:
            self._count -= 1

        return retval


def words(file):
    """Get words from a file."""
    for line in file.readlines():
        # Defines words as sequences of letters, hyphens, and apostrophes.  We
        # want apostrophes because they could be part of contractions, and
        # hyphens because they're in hyphenated words.
        for word in re.findall(r"[a-zA-Z'-]+", line):
            # However, we do not want apostrophes or hyphens at the beginning
            # or end.
            word = word.strip("'-")
            if word:
                # Convert to lower case so that we are case insensitive.
                yield word.lower()


def main():
    """Take arguments and perform their operations."""
    import argparse
    ap = argparse.ArgumentParser(description="train a Markov chain")
    ap.add_argument('-i', dest='in_markov', type=argparse.FileType('rb'),
                    default=None, help='input Markov chain')
    ap.add_argument('-o', dest='out_markov', type=argparse.FileType('wb'),
                    default=None, help='output Markov chain')
    ap.add_argument('-T', dest='in_text', type=argparse.FileType('r'),
                    default=None, help='train on a file')
    ap.add_argument('-G', dest='out_text', action='store_true',
                    default=False, help='generate to a file')
    ap.add_argument('-w', dest='words', type=int, default=100,
                    help='number of words to generate')
    ap.add_argument('-s', dest='start', type=str, default=None,
                    help='start word for generation')
    args = ap.parse_args()

    if args.in_markov is not None:
        markov = pickle.load(args.in_markov)
        args.in_markov.close()
    else:
        markov = MarkovChain()

    if args.in_text is not None:
        markov.train_words(words(args.in_text))

    if args.out_text:
        if args.start is not None:
            args.start = args.start.lower()

        wordlist = list(markov.generate(args.words, args.start))

        if args.start is not None:
            wordlist.insert(0, args.start)
        print(' '.join(wordlist))

    if args.out_markov is not None:
        pickle.dump(markov, args.out_markov)


if __name__ == '__main__':
    main()
    