import sys
import re
import matplotlib.pyplot as plt

word_counts = {} # global variable to store word counts

def lemmatize(word):
    # little hard coded dictionary for irregular forms
    lemmatization_dict = {
        # "slipped": "slip",
        # "running": "run",
        "ran": "run",
        "better": "good",
        "best": "good",
        "children": "child",
        "worse": "bad",
        "worst": "bad",
        "teeth": "tooth",
        "men": "man",
        "women": "woman",
        "feet": "foot",
        "people": "person",
        "mice": "mouse",
        "was": "was",
        "bus": "bus",
        "minutes": "minute",
        "is": "is",
        "paused": "pause",
    }

    stopwords_ends_with_s = {"ours", "yours", "hers", "theirs", "is", "was", "has", "does", "this", "his", "its", "as"}
    
    # check word in dic
    if word in lemmatization_dict:
        return lemmatization_dict[word]
    if word in stopwords_ends_with_s:
        return word
    # check if word ends with 'ing' or 'ed' and has a repeating character 
    if re.search(r'(\w)\1ing$', word):
        return re.sub('(\w)ing$', '', word)
    if re.search(r'(\w)\1ed$', word):
        return re.sub('(\w)ed$', '', word)
    # check if word ends with 'ss'
    if re.search('ss$', word):
        return word
    return re.sub('(ing|ed|es|s|ly|ment)$', '', word)

def stop_words(word):

    stopwords_list = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}

    new_line = []
    if word.lower() not in stopwords_list:
        return word
    return ''

def normalize_text(line, lowercase, stemming, lemmatization, stopwords, remove_punctuation,):
    if lowercase:
        line = line.lower()
        #lemma comes before stemming because we use a dictionary for lemma and then we can stem after...
    if lemmatization:
        new_line = []
        for word in line.split():
            word = lemmatize(word)
            new_line.append(word)
        line = ' '.join(new_line) + '\n'
    elif stemming: 
        # remove common suffixes, $ means match the end of the word.
        new_line = []
        for word in line.split():
            word = re.sub('(ing|ed|es|s|ly|ment)$', '', word)
            new_line.append(word)
        line = ' '.join(new_line) + '\n'
    if stopwords:
        new_line = []
        for word in line.split():
            word = stop_words(word)
            new_line.append(word)
            new_line = [word for word in new_line if word != '']
        line = ' '.join(new_line) + '\n'
    if remove_punctuation:
        # remove these special dashes and underscores
        line = re.sub('[—_]', ' ', line)
         # reg ex means match anything that's not(^) a word character(\w) or whitespace(\s)
        line = re.sub(r'[^\w\s]','', line)
    return line

def process(filename, lowercase, stemming, lemmatization, stopwords, remove_punctuation):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                normalized_line = normalize_text(line, lowercase, stemming, lemmatization, stopwords, remove_punctuation)
                # print(normalized_line, end='')

                for word in normalized_line.split():
                    if word in word_counts:
                        word_counts[word] += 1
                    else:
                        word_counts[word] = 1
    except FileNotFoundError:
        print("File not found")

    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    count(sorted_word_counts, 'word_count.txt')
    plot(sorted_word_counts[:25], "Top 25 Word Count by Rank (Semi-Log Scale)")
    plot(sorted_word_counts[-25:], "Bottom 25 Word Count by Rank (Semi-Log Scale)")

# Write the word counts to a new file
def count(word_counts, output_filename):
    try:
        total_tokens = 0
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for word, count in word_counts:
                output_file.write(f"{word} {count}\n")
                total_tokens += count
        print('----------------------------------------------------------------------------')
        print(f"{output_filename} file written successfully | Total tokens: {total_tokens}")
    except Exception as e:
        print("Error writing file")

def plot(word_counts, title):
    ranks = range(1, len(word_counts) + 1)
    counts = [count for word, count in word_counts]
    words = [word for word, count in word_counts]

    # plot stuff
    plt.figure(figsize=(8, 4))
    plt.bar(ranks, counts, color='purple')

    # use log scale only for y axis
    plt.yscale('log')

    # Labels and titles
    plt.xlabel('Words', fontsize=12)
    plt.ylabel('Count (log scale)', fontsize=12)
    plt.title(title, fontsize=14)

    # display words
    plt.xticks(ticks=ranks, labels=words, rotation=45, fontsize=8)
    plt.tight_layout()
    plt.show()


def main():
    # if len(sys.argv) < 2:
    #     return

    filename = sys.argv[1]
    lowercase = 'lowercase' in sys.argv
    stemming = 'stemming' in sys.argv
    lemmatization = 'lemmatization' in sys.argv
    remove_punctuation = 'remove_punctuation' in sys.argv
    stopwords = 'stopwords' in sys.argv
    process(filename, lowercase, stemming, lemmatization, stopwords, remove_punctuation)

if __name__ == "__main__":
    main()
