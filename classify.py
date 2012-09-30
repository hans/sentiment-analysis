import math
import pickle
import re
import sys

def label_prob(label, tokens, label_probs, label_token_probs, blind=False):
    prob = 0 if blind else math.log(label_probs[label])
    token_probs = label_token_probs[label]

    prob = sum(map(math.log, filter(None, map(token_probs.get, tokens))))

    return prob

def all_label_probs(tokens, label_probs, label_token_probs):
    return {label: label_prob(label, tokens, label_probs, label_token_probs)
            for label in label_probs.keys()}

def classify(tokens, label_probs, label_token_probs):
    probs = all_label_probs(tokens, label_probs, label_token_probs)
    return max(probs, key=probs.get)

def tokenize(text):
    text = re.sub('[^\w\s]', '', text)
    tokens = text.split()
    return tokens

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    label_probs, label_token_probs = pickle.load(f)
    f.close()

    tokens = tokenize(sys.argv[2])
    print classify(tokens, label_probs, label_token_probs)
