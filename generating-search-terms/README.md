# Generating Search Terms
A simple Python script that produces a frequency count of words used across a set of text files.

This is useful for generating search queries by helping to get a sense of the most commonly used terms across a representative sample of manuscripts on a topic.

## Getting Started
The script is intended to work on a directory containing only text files. For example, each text file may include the title and abstract of a manuscript. Text files can be named whatever you like. Note that the relative paths below assume you are in the top-level directory for this repository.

All text files to be counted should exist in a folder `./data/seed-papers/`.

To use, type:
```bash
python ./generating-search-terms/frequency_count.py
```

This will produce a file called `./data/seed-papers/frequency-count.csv` containing three columns including:
   + [WORD] All unique words found across all files, 
   + [FREQUENCY] the total frequency of each word across all text files, and 
   + [PAPERS] the number of text files a given word was found in.
