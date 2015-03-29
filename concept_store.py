# Define the structure to perform lookups and provided initalisation and methods
# to use this structure.


######################################################################
# Util functions
######################################################################    
def tokenize(s):
    """
    Function to split a given string into tokens.
    """
    return s.split()


######################################################################
# Case Insensitive String Dictionary helper class
######################################################################
class CaseInsensitiveStringDict(dict):
    """
    This is a dictonary subclass that allows to retrieve strings ignoring their case.
    
    String are saved in lowercase format, each key is converted to lowercase format
    before performing the action requiring the key.
    
    Note: This class works only for this application. It is not necessarily true
    that this class can be used for other applications that need a similar dictionary.
    """
    def __contains__(self, key):
        """
        Overwrite checking if the dictionary contains a key with the key transformed to lower case.
        """
        return super(CaseInsensitiveStringDict, self).__contains__(key.lower())

    def __getitem__(self, key):
        """
        Overwrite getting of items so that the key is tranformed into lower case.
        """
        return super(CaseInsensitiveStringDict, self).__getitem__(key.lower())
    
    def __setitem__(self, key, value):
        """
        Overwrite setting of items so that the key is tranformed into lower case.
        """
        super(CaseInsensitiveStringDict, self).__setitem__(key.lower(), value)
    
    def setdefault(self, key, default):
        """
        Overwrite the set default method so that the key is tranformed into lower case.
        """
        return super(CaseInsensitiveStringDict, self).setdefault(key.lower(), default)


######################################################################
# Class to define the concept store
######################################################################
class ConceptStore(object):
    """
    Store of concepts.

    Stores concepts as case insensitive strings in an underlying dictionary.
    """
    def __init__(self, concepts):
        """
        Build a store from the given list of concepts.
        
        The store is represented by a dictionary structure that is case insensitive.
        A concept can consist of multiple words that define a concept.
        A concept is stored in the dictionary so that each word in the concept iteratively
        returns a new dictionary, where the last dictionary should have an _end with the 
        full concept as value.
        """
        # Define an end key to denote the end of a lookup
        self._end = '_end'
        # Define the main dictionary to store the concepts
        self.store_dict = CaseInsensitiveStringDict()
        # Store each concept in the list of concepts
        for concept in concepts:
            # current_dict is the current dictionary when iteration of words in one concept
            current_dict = self.store_dict
            # Iterate over all the words (tokens) in the concept
            for token in tokenize(concept):
                # Add the current word in the current concept to the current dictionary
                # by adding a new dictionary if the words doesn't exist already.
                # Update the current dictionary with the new one that is returned when
                # indexing with token.
                current_dict = current_dict.setdefault(token, default=CaseInsensitiveStringDict())
            # Add the end key to denote that the concept ends at the current dictionary.
            current_dict[self._end] = concept

    def find_matches(self, sentence):
        """
        Find all concepts in the sentences that match with concepts in this store.
        Return a list if matches. This list is empty if no matches are found.
        """
        # Split the sentence in words (tokens)
        tokens = tokenize(sentence)
        # Define a list to hold the matches
        matches = []
        # Go over all the words in the sentence
        for i in xrange(len(tokens)):
            current_store = self.store_dict
            # Go over all the words starting from the current word
            for j in xrange(i, len(tokens)):
                word = tokens[j]
                if word in current_store:
                    # If the word is in the current dictionary, update this current dictionary,
                    # and check if there is an _end symbol
                    current_store = current_store[word]
                    if self._end in current_store:
                        # If there is an _end symbol, add the current match to the list of matches.
                        matches.append(current_store[self._end])
                else:
                    # Break and start again with the next word if the word is not 
                    # in the current dictionary
                    break
        return matches