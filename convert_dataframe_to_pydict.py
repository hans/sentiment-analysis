"""Converts the R data frame format used by the UMass Amherst
Linguistics Sentiment Corpora to a Python tuple and serializes it to a
file in Pickle format. The tuple is of the form

    (label_probabilities, label_token_probabilities)

`label_probabilities` is a dict mapping label ID (integer rating) to
probability. For any key-value pair in this dict `k, v`, v represents
P(k), where k is a label.

`label_token_probabilities` is a dict mapping label ID (integer rating)
to token (string) to probability (float). For any multidimensional pair
`l, t, p`, p represents P(t|l).
"""

from collections import defaultdict
import pickle

f = open('english-amazon-reviewfield-unigrams.frame', 'r')

# Skip the columns line
f.next()

label_counts = {}
label_token_probs = defaultdict(dict)
for line in f:
    _, tok_quoted, label, tok_count, label_total_count = line.split()
    tok = tok_quoted[1:][:-1]

    label_token_probs[int(label)][tok] = ( float(tok_count)
                                           / float(label_total_count) )

    label_counts[int(label)] = int(label_total_count)

total_tokens = float(sum(label_counts.values()))
label_probabilities = {k: v / total_tokens
                       for k, v in label_counts.items()}

to_serialize = (label_probabilities, label_token_probs)

out = open('sentiment_labels.pickle', 'w')
pickle.dump(to_serialize, out)
f.close()
