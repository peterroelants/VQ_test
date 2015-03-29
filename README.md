# VQ Programming Assignment Test

This repository holds the solution to a programming assignment where to goal is to create a program that is able to detect and return concepts in a given sentence.

## Find Concepts

[`concept_store.py`](https://raw.githubusercontent.com/peterroelants/VQ_test/master/concept_store.py) defines the functionality to match concepts in a given string. The use of this concept store is illustrated in [this IPython notebook](http://nbviewer.ipython.org/github/peterroelants/VQ_test/blob/master/VocallQ_tests.ipynb) where first a concept store is created with the `ConceptStore` constructor, and afterwards concepts are matched in sentences with the `find_matches` method of the concept store.

### Hash map

The current solution uses a case insensitive hash map (subclass of the Python dictionary) to store the concepts. Each concept is stored as a tree of hash maps so that concepts containing multiple words can be matched as well as concepts containing only one word. The hash map structure is `{key:result_dict}` where `result_dict` is a dictionary with either a next word as key to store multi word concepts, or `_end` as key, which means that the words leading up to `_end` formed a concept. For example to match the concept 'Indian' the main store will match 'Indian' as a key and return the `result_dict` which contains `_end` as a key to indicate that 'Indian' is matched as a concept (`{'Indian':{'_end':_}}`). And for example to match the concept 'West Indian' the main store will match 'West' as a key and return the `result_dict` which contains 'Indian' as a key, which will contain `_end` as a key to indicate that 'West Indian' is matched as a concept (`{'West':{'Indian':{'_end':_}}}`).

The lookup of a key in a hash map can be done in constant time, so for a sentence of length n words the runtime is at most O(n * m) with m the number of words of the longest concept. So the matching speed is not affected by the size of the dictionary.

To divide the concept string and the sentence strings into tokens the Python `split()` command is used. This assumes that no punctuation is used. For more advance tokenization the Python [NLTK library](http://www.nltk.org/api/nltk.tokenize.html) can be used.

We assumed that no spelling errors are made in the input sentences. If spelling errors can be made we can first correct the spelling of the input sentences, or store the possible word edits resulting from errors in the dictionary.

### Alternative solutions

As an alternative to the hash map that contains complete words as keys a [trie structure](http://en.wikipedia.org/wiki/Trie) can be used to store the concepts. This data structure will be more efficient to store a large set of concepts.

A second alternative is to use [Named-entity recognition (NER)](http://en.wikipedia.org/wiki/Named-entity_recognition) to classify concepts in the given sentences. This would require a dataset with annotated sentences to train the NER classifier.


## Web service

A web service is provided to match the given concepts to strings. The web service makes use of the [Flask](http://flask.pocoo.org/) module and is coded in [`main.py`](https://raw.githubusercontent.com/peterroelants/VQ_test/master/main.py). The concepts matched by this web service are the concepts from the assignment.

This web service makes use of [`concept_store.py`](https://raw.githubusercontent.com/peterroelants/VQ_test/master/concept_store.py) and stores the concept store in cache. Access to this web service is provided at [http://178.62.253.130/vq](http://178.62.253.130/vq). Requests have to be sent via a POST request with the string as a plain text content type. The web request will return a json file with the matched concepts as a list in this json object: `{result:[list_of_matches]}`.

For example the following request:

    curl -X POST -H "Content-Type: text/plain" -d 'I would like some thai food' http://178.62.253.130/vq

returns `{"result": ["Thai"]}`