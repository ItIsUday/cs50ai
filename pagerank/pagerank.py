import os
import random
import re
import sys
from math import isclose
from collections import defaultdict

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if not len(corpus[page]):
        return dict.fromkeys(corpus.keys(), 1 / len(corpus))
    transitions = dict.fromkeys(corpus.keys(), (1 - damping_factor) / len(corpus))
    tmp = damping_factor / len(corpus[page])
    for value in corpus[page]:
        transitions[value] += tmp

    return transitions


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    sample = random.choice(list(pages))
    pagerank = dict.fromkeys(pages, 0)

    for _ in range(n):
        transition = transition_model(corpus, sample, damping_factor)
        values = [transition[key] for key in pages]
        sample = random.choices(pages, values)[0]
        pagerank[sample] += 1

    for page in pages:
        pagerank[page] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict.fromkeys(corpus.keys(), 1 / len(corpus))
    parents = defaultdict(set)

    for key, value in corpus.items():
        for page in value:
            parents[page].add(key)
        if not len(value):
            for page in corpus.keys():
                parents[page].add(key)

    while True:
        prior_rank = pagerank.copy()
        for page in corpus.keys():
            tmp = 0
            for parent in parents[page]:
                tmp += pagerank[parent] / len(corpus[parent]) if len(corpus[parent]) else pagerank[parent] / len(corpus)
            pagerank[page] = (1 - damping_factor) / len(corpus) + damping_factor * tmp

        if all(isclose(pagerank[page], prior_rank[page], abs_tol=0.0001) for page in corpus.keys()):
            return pagerank


if __name__ == "__main__":
    main()
