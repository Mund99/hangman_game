import nltk
import os

class WordGenerator:
    def __init__(self):
        # Download necessary NLTK resources
        nltk.download('brown')
        nltk.download('words')
        nltk.download('wordnet')

    def generate_word_list(self):
        # Get words from different corpora
        brown_words = set(nltk.corpus.brown.words())
        words_words = set(nltk.corpus.words.words())
        wordnet_words = set(nltk.corpus.wordnet.words())

        # Combine word lists
        word_list = list(brown_words | words_words | wordnet_words)

        # Filter words based on criteria
        filtered_word_list = self.filter_words(word_list)
        return filtered_word_list

    @staticmethod
    def filter_words(words):
        # Filter out words containing digits
        filtered_words = [word for word in words if not any(char.isdigit() for char in word)]
        # Filter out words with length less than 4
        filtered_words = [word for word in filtered_words if len(word) > 3]
        # Filter out words with hyphens, underscores, and apostrophes
        filtered_words = [word for word in filtered_words if '-' not in word and '_' not in word and "'" not in word]
        return filtered_words

    def download_wordbank(self, file_path='wordbank.txt'):
        try:
            word_list = self.generate_word_list()

            # Save the word list to a file
            with open(file_path, 'w') as file:
                for word in word_list:
                    file.write(word + '\n')

            print(f"Wordbank saved to {file_path}")
        except OSError as e:
            print(f"Error: {e}")

                

word_generator = WordGenerator()
script_directory = os.path.dirname(os.path.abspath(__file__))
full_file_path = os.path.join(script_directory, 'assets/wordbank.txt')

word_generator.download_wordbank(full_file_path)