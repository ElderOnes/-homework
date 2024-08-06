import string

class WordsFinder:
    def __init__(self, *file_names):
        self.file_names = file_names

    def get_all_words(self):
        all_words = {}
        punctuation = string.punctuation.replace("-", "")
        for file_name in self.file_names:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    text = file.read().lower()
                    for p in punctuation:
                        text = text.replace(p, '')
                    text = text.replace(" - ", " ")
                    words = text.split()
                    all_words[file_name] = words
            except FileNotFoundError:
                all_words[file_name] = []
        return all_words

    def find(self, word):
        all_words = self.get_all_words()
        word = word.lower()
        result = {}
        for name, words in all_words.items():
            if word in words:
                result[name] = words.index(word)
            else:
                result[name] = None
        return result

    def count(self, word):
        all_words = self.get_all_words()
        word = word.lower()
        result = {}
        for name, words in all_words.items():
            result[name] = words.count(word)
        return result

finder1 = WordsFinder('Walt Whitman - O Captain! My Captain!.txt')
print(finder1.get_all_words())
print(finder1.find('captain'))
print(finder1.count('captain'))