import re

def read_common_words(filename):
    '''
    Reads the commmon words file into a set.
    
    If the file name is None returns an emtpy set. If the file cannot be 
    opened returnes an empty set:
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


def read_corpus(filename, common_words, test_words):
    '''
    Reads the corpus from the given file.
    
    Loads the data into a dictionary that holds the targets and the words that
     they occur with in a sentence.
    '''
    
    associations = {}
    word_counts = {}
    
    # regular expression to strip punctuations
    punctuations = "|".join(re.escape(x) for x in ('{', '}', '(', ')', '[', ']', ',', ' ', '\t',':', ';',"'", '"'))
    repl1 = re.compile(punctuations)

    # regular expression to remove --
    repl2 = re.compile("--")
    
    # regular expression to split the text into sentences.
    sent_splitter = re.compile("\.|\?\!")
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
                
                # having split up the sentence in words, let's go through the words and
                # find the associations.
                
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
    Pretty prints the contents of our data structures
    '''
    print(len(word_counts), "words in words list")
    print("word_count_dict\nword_word_dict")
    
    words = sorted(word_counts.keys(), key=lambda x: -word_counts[x])
    
    for word in words:
        count = word_counts[word]
        print(word, count)
        related = associations[word]
        related_words = sorted(related.keys())
        for related_word in related_words:
            print("    ", related_word, related[related_word])
            
def read_test_data(filename):
    '''
    Reads the test data into a set
    '''
    
    data = set()
    
    try:
        with open(filename) as fp:
            for line in fp:
                data.add(line.strip().lower())
    except FileNotFoundError:
        print("Error the test data could not be read")

    return data 


def main(corpus_file_name, test_sets_file, commonwords_file_name = None):
    '''
    Program entry point
    '''
    
    stop_words = read_common_words(commonwords_file_name)
    test_data = read_test_data(test_sets_file)
    word_counts, associations =  read_corpus(corpus_file_name, stop_words, test_data)
    
    print_status(word_counts, associations)
    
if __name__ == '__main__':
    main('punctuation.txt', 'sample0_set.txt', 'common.txt')
    