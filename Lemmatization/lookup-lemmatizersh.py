import sys
import re
from operator import itemgetter

### Global variables

# Paths for data are read from command line
train_file = sys.argv[1]
test_file = sys.argv[2]

# Counters for lemmas in the training data: word form -> lemma -> count
lemma_count = {}

# Lookup table learned from the training data: word form -> lemma
lemma_max = {}

# Variables for reporting results
training_stats = ['Wordform types', 'Wordform tokens', 'Unambiguous types', 'Unambiguous tokens', 'Ambiguous types',
                  'Ambiguous tokens', 'Ambiguous most common tokens', 'Identity tokens']
training_counts = dict.fromkeys(training_stats, 0)

test_outcomes = ['Total test items', 'Found in lookup table', 'Lookup match', 'Lookup mismatch',
                 'Not found in lookup table', 'Identity match', 'Identity mismatch']
test_counts = dict.fromkeys(test_outcomes, 0)

accuracies = {}

### Training: read training data and populate lemma counters

train_data = open(train_file, 'r')
tokens = 0
ambi_type = 0
ambi_token = 0
ambi_most_common = 0
unambi_type = 0
unambi_token = 0
identity_token = 0
max_lemma_count = 0


for line in train_data:

    # Tab character identifies lines containing tokens
    if re.search('\t', line):
        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')

        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        tokens+=1
        if form == lemma:
            identity_token += 1
        if form in lemma_count:
            l_list = lemma_count.get(form)
            found_existing_lemma = False
            for lemmas_count in l_list:
                if lemma == lemmas_count[0]:
                    found_existing_lemma = True
                    lemmas_count[1] += 1
            if found_existing_lemma is False:
                    l_list.append([lemma,1])
            lemma_count[form]=l_list
        else:
            lemma_count[form] = [[lemma,1]]


        ######################################################
        ### Insert code for populating the lemma counts    ###
        ######################################################

### Model building and training statistics

for form in lemma_count.keys():
    lemmas_list = lemma_count[form]
    lemma_max[form] = max(lemmas_list,key=itemgetter(1))[0]
    if len(lemmas_list)>1:
        ambi_type += 1
        mc = 0
        for i in lemmas_list:
            ambi_token += i[1]
            if i[1]>mc:
                mc = i[1]
        ambi_most_common += mc
        max_lemma_count += mc
    elif len(lemmas_list)==1:
        unambi_type += 1
        unambi_token += lemmas_list[0][1]
        max_lemma_count += lemmas_list[0][1]

for k,v in training_counts.items():
    if k == 'Wordform types':
        training_counts[k] = len(lemma_count)
    if k == "Wordform tokens":
        training_counts[k] = tokens
    if k == "Unambiguous types":
        training_counts[k] = unambi_type
    if k == "Unambiguous tokens":
        training_counts[k] = unambi_token
    if k =="Ambiguous types":
        training_counts[k] = ambi_type
    if k == "Ambiguous tokens":
        training_counts[k] = ambi_token
    if k == "Ambiguous most common tokens":
        training_counts[k] = ambi_most_common
    if k == "Identity tokens":
        training_counts[k] = identity_token


accuracies['Expected lookup'] = max_lemma_count/tokens

accuracies['Expected identity'] = identity_token/tokens

### Testing: read test data, and compare lemmatizer output to actual lemma

test_data = open(test_file, 'r')
test_items = 0
found_lookup_table = 0
not_found_lookup_table = 0
lookup_match = 0
lookup_mismatch = 0
identity_match = 0
identity_mismatch = 0

for line in test_data:
    # Tab character identifies lines containing tokens
    if re.search('\t', line):
    # Tokens represented as tab-separated fields
        field = line.strip().split('\t')
        form = field[1]
        lemma = field[2]
        test_items += 1
        if form in lemma_max:
            found_lookup_table += 1
            if lemma == lemma_max.get(form):
                lookup_match += 1
            else:
                lookup_mismatch += 1

        else:
            not_found_lookup_table += 1
            if form == lemma:
                identity_match += 1
            else:
                identity_mismatch += 1


for k,v in test_counts.items():
    if k == 'Total test items':
        test_counts[k] = test_items
    if k == "Found in lookup table":
        test_counts[k] = found_lookup_table
    if k == "Lookup match":
        test_counts[k] = lookup_match
    if k == "Lookup mismatch":
        test_counts[k] = lookup_mismatch
    if k =="Not found in lookup table":
        test_counts[k] = not_found_lookup_table
    if k == "Identity match":
        test_counts[k] = identity_match
    if k == "Identity mismatch":
        test_counts[k] = identity_mismatch


accuracies['Lookup'] = lookup_match/found_lookup_table

accuracies['Identity'] = identity_match/not_found_lookup_table

accuracies['Overall'] = (lookup_match + identity_match)/test_items

### Report training statistics and test results

output = open('lookup-output.txt', 'w')

output.write('Training statistics\n')

for stat in training_stats:
    output.write(stat + ': ' + str(training_counts[stat]) + '\n')

for model in ['Expected lookup', 'Expected identity']:
    output.write(model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.write('Test results\n')

for outcome in test_outcomes:
    output.write(outcome + ': ' + str(test_counts[outcome]) + '\n')

for model in ['Lookup', 'Identity', 'Overall']:
    output.write(model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.close