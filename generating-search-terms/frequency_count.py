# Produces a simple word frequency count across text files.
#
# USAGE:
#	frequency_count.py
#
#	input:
#		No explicit input, however all text files to be counted
#       should exist in a folder ../data/seed-papers/
#
#	output:
#		frequency-count.csv		Comma-delimited file in which first
#                       		column is the term and second column
#                               is the number of occurrences across all
#                               text files.
#

import glob, re
import pandas as pd
from os import path
from itertools import chain
from collections import Counter

# Change these if you want to specify a different directory or filename
script_path = path.dirname(__file__)
seed_dir = path.abspath( path.join(script_path, '..', 'data', 'seed-papers') )
output_dir = seed_dir
output_file = 'frequency-count.csv'
output_path = path.join(output_dir, output_file)

# read all text files and do a little text cleanup
txt_files = glob.glob(seed_dir + '*.txt')

all_text = []
for file in txt_files:
    with open(file) as f:
        text = [word.lower() for line in f for word in line.split()]
        text = [re.sub('[,.]', '', word) for word in text]
        all_text.append( text )

# count overall word frequency across all files
total_word_freq = dict(Counter(chain.from_iterable(all_text)))

# count over how many files a word appears
unique_words = [list(set(text)) for text in all_text]
article_freq = dict(Counter(chain.from_iterable(unique_words)))

# combine results into a single dataframe
d1 = pd.DataFrame(total_word_freq.items(), columns=['WORD' , 'FREQUENCY'])
d2 = pd.DataFrame(article_freq.items(), columns=['WORD' , 'PAPERS'])
all_freq_counts = pd.merge(d1, d2, on='WORD').sort_values(by=['FREQUENCY', 'PAPERS'], ascending=False)

# print dataframe to file
all_freq_counts.to_csv(output_path, index=False)