#File: Project2
# A program to find synonyms by association

import re
import math

def read_common_words(filename):
    '''
    Reads the commmon words file into a set.
    
    If the file name is None returns an emtpy set. If the file cannot be 
    opened returns an empty set:
    '''
    words = set()
    if filename != None:
        try: 
            with open(filename) as fp:
                for line in fp:
                    words.add(line.strip().lower())
        except FileNotFoundError:
            print("Warning: Couldn't read common words file")
       
    return words


def read_corpus(filename, common_words):
    '''
    Reads the corpus from the given file.
    
    Loads the data into a dictionary that holds the targets and the words that
    occur within a sentence.
    '''
    
    associations = {}
    word_counts = {}
    
    # regular expression to strip punctuations
    punctuations = "|".join(re.escape(x) for x in ('{', '}', '(', ')', '[', ']', ',','\t',':', ';',"'", '"'))
    repl1 = re.compile(punctuations)

    # regular expression to remove --
    repl2 = re.compile("--")
    
    # regular expression to split the text into sentences.
    sent_splitter = re.compile("\.|\?|\!")
    # regular expression to split a sentence into words.
    word_splitter = re.compile("\\s{1,}")
    
    try:
        
        with open(filename) as fp:
            data = fp.read()
            sentences = sent_splitter.split(data.lower())
            # now iterate through the sentence.
            for sentence in sentences:
                sentence = repl2.sub(" ", repl1.sub(" ", sentence))
                words = set([word for word in word_splitter.split(sentence) if word not in common_words])
                # having split up the sentence in words, goes through the words and
                # finds the associations.
                
                for word in words:

                    word_count = word_counts.get(word)
                    if not word_count:
                        word_counts[word] = 1
                    else:
                        word_counts[word] += 1
                        
                    for other_word in words:
                        if word != other_word:
                            count = associations.get(word)
                            if count == None:
                                associations[word] = {other_word: 1}
                            else:
                                ocount = count.get(other_word)
                                if ocount == None:
                                    count[other_word] = 1
                                else:
                                    count[other_word] += 1
                                    
                
                            
        return word_counts, associations
    
    except FileNotFoundError:
        print("Error could not read the corpus")
    
def print_status(word_counts, associations):
    '''
    Prints the contents of the data structures
    '''
    print(len(word_counts), "words in words list")
    print("word_count_dict\nword_word_dict")
    
    words = sorted(word_counts.keys(), key=lambda x: -word_counts[x])
    
    for word in words:
        count = word_counts[word]
        print(word, count)
        related = associations.get(word)
        if related:
            related_words = sorted(related.keys())
            for related_word in related_words:
                print("    ", related_word, related[related_word])

                
def read_test_data(filename):
    '''
    Reads the test data into a set
    '''
    group = []
    data = []
    
    try:
        with open(filename) as fp:
            for line in fp:
                line = line.strip().lower()
                if line :
                    group.append(line)
                else:
                    data.append(group)
                    group = []
                
        data.append(group)
    except FileNotFoundError:
        print("Error the test data could not be read")

    return data 

def print_relationships(word1, word2, targets, test):
    '''
    Print information about common words to help debug
    '''
    intersect = targets.keys() & test.keys()
    common = [(x, targets[x],  test[x]) for x in intersect]
    
    print('query_word', word1, 'test_word', word2, 'common_words', common)
    
def cosine_metric(test_data, associations):
    '''
    Calculate the cosine metric between the target and the tests
    '''
    target = associations[test_data[0]]
    results = []
    for test_word in test_data[1:]:
        dot = 0
        p2 = 0
        q2 = 0
        cross = 0
        test = associations.get(test_word)
        if test:
            # uncomment the following line to get the verbose report of the word
            # relationships.
            # print_relationships(test_data[0], test_word, target, test)
            common_keys = target.keys() & test.keys()
            for key in common_keys:
                dot += test[key] * target[key]
                
            for key in target.keys():
                p2 += target[key] ** 2
            
            for key in test.keys():
                q2 += test[key] ** 2
                
            cross = p2 * q2
            score =  dot / math.sqrt(cross)
        else:
            score = 0
            
        results.append([score, test_word])
        
    return results


def main(corpus_file_name, test_sets_file, commonwords_file_name = None):
    '''
    Program entry point
    '''
    
    stop_words = read_common_words(commonwords_file_name)
    test_data_sets = read_test_data(test_sets_file)
    word_counts, associations =  read_corpus(corpus_file_name, stop_words)
    
    for test_data in test_data_sets:
        # uncomment the following line to get the verbose output
        # print_status(word_counts, associations)
        result = cosine_metric(test_data, associations)
        result.sort(reverse=True)
        
        print(test_data[0])
        for r in result:
            print("\t{0}\t{1:.3f}".format(r[1], r[0]))
            
        print('Synonym for', test_data[0], 'is', result[0][1])
    
    
if __name__ == '__main__':
    main('lifeOnMississippi.txt', 'sample0_set.txt', 'common.txt')
    #main('sample_txt.txt', 'sample0_set.txt', 'common.txt')
    