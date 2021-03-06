import os
from collections import defaultdict
from string import punctuation

import nltk
import sys
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for file_name in os.listdir(directory):
        with open(os.path.join(directory, file_name), 'r') as f:
            files[file_name] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    return [word for word in nltk.word_tokenize(document.lower())
            if word not in punctuation and
            word not in nltk.corpus.stopwords.words("english")]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = defaultdict(float)
    total_docs = len(documents)

    for document in documents.values():
        words_appeared = set()
        for word in document:
            if word not in words_appeared:
                idfs[word] += 1
                words_appeared.add(word)

    for word in idfs:
        idfs[word] = round(log(total_docs / idfs[word]), 4)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filenames = list(files)
    tfidf = {
        file: sum(idfs[word] * words.count(word) for word in query)
        for file, words in files.items()
    }
    filenames.sort(key=lambda file: tfidf[file], reverse=True)

    return filenames[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    matched_sentences = list(sentences)
    idf_term_density = {
        sentence: (sum(idfs[word] for word in query if word in words),
                   sum(1 for word in words if word in query) / len(sentence))
        for sentence, words in sentences.items()
    }
    matched_sentences.sort(key=lambda sentence: idf_term_density[sentence], reverse=True)

    return matched_sentences[:n]


if __name__ == "__main__":
    main()
