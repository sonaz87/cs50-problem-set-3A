import os
import random
import re
import sys

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

# written by me
def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = dict()
    
    random_number = random.random()
    if random_number < (1-damping_factor):
        result = random.choice(list(corpus.keys()))
    
    else: 
        my_list = corpus[page]
        if len(my_list) == 0:
            result = random.choice(list(corpus.keys()))
        else:
            result = random.choice(list(my_list))       
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
        # setting up a dictionary for counting the page hits
    counter_dict = dict()
    for element in corpus:
        counter_dict.update({element:0})
        
        # first page is randomly selected
    page = random.choice(list(corpus.keys()))
    counter_dict[page] += 1
    
        # sampling with transition_model
    
    for i in range(n-1):
        page = transition_model(corpus, page, DAMPING)
        counter_dict[page] += 1
        
        # setting fractional values based on count
        
    for entry in counter_dict:
        counter_dict[entry] = counter_dict[entry]/n
        
    return counter_dict
    
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    
    for element in corpus:
        page_rank.update({element:(1/len(corpus))})
    
    not_close_enough = True
    while not_close_enough:
        for element in page_rank:
            not_close_enough = False
            
            new_value = ((1-damping_factor)/len(corpus)) 
            for element2 in corpus:
                if element in corpus[element2]:
                    to_add = damping_factor * page_rank[element2] / len(corpus[element2])
                    new_value = new_value + to_add
                
                
            if abs(new_value-page_rank[element]) > 0.001:
                not_close_enough = True
            page_rank[element] = new_value

    return page_rank

if __name__ == "__main__":
    main()

# page = '2.html'
# corpus = crawl(sys.argv[1])
# result1 = iterate_pagerank(corpus, DAMPING)
# print(result1)