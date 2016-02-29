from collections import Counter
import cPickle as pickle
import random
import itertools
import string
from nltk.tokenize import word_tokenize
 
def words(entry):
    """
    Basic callback, converts an entry to ascii and splits on spaces
    """
    return [entry.split()]
 

def letters(entry):
    """
    Splits an entry on letters, removing punctuation.

    Useful for making random words.
    """

    return [letter for letter in list(entry.lower().decode('ascii', 'ignore')) if letter not in string.punctuation]
 

def ply_markov(entry, ply, current_dict, split_callback):
    """
    Updates the current markov dictionary based on the given entry
    """

    words = split_callback(entry)

    for i in xrange(0, len(words)-ply):
        current_tuple = tuple([words[j] for j in xrange(i, i+ply)])
        if current_dict.get(current_tuple, False):
            current_dict[current_tuple].update([words[i+ply]])
        else:
            current_dict[current_tuple] = Counter([words[i+ply]])
    return current_dict
 

def train(source, ply, split_callback=words, master_dict=None):
    """
    Creates the master markov chain reference dictionary

    ply sets the length of look-behind for markov chain generation.
    1-ply means only based on the current word, 2-ply means based on the current and previous word, etc...

    The split_callback is an optional argument that allows you to define how the program turns a line of text
    into a list of words. The default just casts to ascii and splits on spaces.
    """

    master_dict = master_dict or {i: {} for i in xrange(1,ply+1)}
    for line in source:
        for key, value in master_dict.iteritems():
            master_dict[key] = ply_markov(line, key, value, split_callback)
    return master_dict
 

def get_check_tuple(current_output, ply):
    """
    Gets a tuple of all tokens to consider in generating the next element
    """

    last_n_list = [current_output[-i] for i in xrange(1,ply+1)]
    last_n_list.reverse()
    return tuple(last_n_list)
 

def append_next_word(master_dict, current_output, ply):
    """
    Statisticall adds the next word to the output
    """

    ply = min(len(current_output), ply)
    ply_list = []
    for i in xrange(1, ply+1):
        check = master_dict[i].get(get_check_tuple(current_output, i),{})
        #ply_list.extend([[key]*value*i for key, value in check.iteritems()])
        ply_list.extend([[key]*value*i for key, value in check.iteritems()])

    master_list = list(itertools.chain(*ply_list))
    current_output.append(random.choice(master_list))

def generate_from(master_dict, words, output_length, ply, join_char=" "):
    """
    Given a master dictionary, returns a generated Markov Chain of tokens 
    """

    output = words
    for i in xrange(output_length):
        try:
            append_next_word(master_dict, output, ply)
        except IndexError:
            # If the markov chain gets a token that has always been the end of an entry it will end here
            break
    return join_char.join(output)

def generate(master_dict, output_length, ply, join_char=" "):
    """
    Given a master dictionary, returns a generated Markov Chain of tokens 
    """

    output = []
    output.append(random.choice(master_dict[1].keys())[0])
    for i in xrange(output_length):
        try:
            append_next_word(master_dict, output, ply)
        except IndexError:
            # If the markov chain gets a token that has always been the end of an entry it will end here
            break
    return join_char.join(output)
