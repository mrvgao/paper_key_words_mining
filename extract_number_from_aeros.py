import csv
from tqdm import tqdm
from collections import defaultdict
from nltk import WordNetLemmatizer
import re

file_name = '/Users/Minchiuan/Downloads/keywords_extracted_by_initial_8_keywords.txt'

wnl = WordNetLemmatizer()


def lemmatize_string(string, type='n'):
    words = string.split()
    string = ' '.join(map(lambda w: wnl.lemmatize(w, type), words))
    return string


def get_key_word_value(keyword, string, file_name, alreay_result):
    ngram = 5

    if keyword in string:
        string = lemmatize_string(string, type='n')
        connected_keywords = '_'.join(keyword.split())
        new_string = string.replace(keyword, connected_keywords)
        # new_string = new_string.replace('-', ' ').replace(':', ' ')
        words = re.split('\W', new_string)

        index = -1
        for ii, w in enumerate(words):
            if w.find(connected_keywords) >= 0:
                index = ii
                break

        assert index > -1

        # index = words.index(connected_keywords)
        sub_string = words[index - ngram: index + ngram]

        for w in sub_string:
            if str(w).isnumeric():
                alreay_result[file_name][keyword] = w


result = defaultdict(lambda : {})
keywords = "backscatter coefficient\|extinction coefficient\|optical depth\|lidar ratio\|depolarization ratio\|color ratio\|depolarization spectral ratio\|angstrom exponent".split(r'\|')
print(keywords)
for ii, line in tqdm(enumerate(open(file_name, encoding='utf-8')), total=101617):
    file_name = line.strip().split(':')[0]

    # if ii > 1000: break

    for k in keywords:
        get_key_word_value(k, str(line).lower(), file_name, result)


with open('气溶胶数据.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['file_name'] + keywords)
    writer.writeheader()

    for f in result:
        info = result[f]
        info['file_name'] = f
        writer.writerow(info)

print(result)
