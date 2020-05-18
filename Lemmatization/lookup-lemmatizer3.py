### This program is a very simple lemmatizer, which learns a
### lemmatization function from an annotated corpus. The function is
### so basic I wouldn't even consider it machine learning: it's
### basically just a big lookup table, which maps every word form
### attested in the training data to the most common lemma associated
### with that form. At test time, the program checks if a form is in
### the lookup table, and if so, it gives the associated lemma; if the
### form is not in the lookup table, it gives the form itself as the
### lemma (identity mapping).

### The program performs training and testing in one run: it reads the
### training data, learns the lookup table and keeps it in memory,
### then reads the test data, runs the testing, and reports the
### results.

### The program takes two command line arguments, which are the paths
### to the training and test files. Both files are assumed to be
### already tokenized, in Universal Dependencies format, that is: each
### token on a separate line, each line consisting of fields separated
### by tab characters, with word form in the second field, and lemma
### in the third field. Tab characters are assumed to occur only in
### lines corresponding to tokens; other lines are ignored.

import sys
import re

### Global variables

# Paths for data are read from command line
train_file = sys.argv[1]
test_file = sys.argv[2]

# Counters for lemmas in the training data: word form -> lemma -> count
lemma_count = {}

# Lookup table learned from the training data: word form -> lemma
lemma_max = {}

# Variables for reporting results
training_stats = ['Wordform types' , 'Wordform tokens' , 'Unambiguous types' , 'Unambiguous tokens' , 'Ambiguous types' , 'Ambiguous tokens' , 'Ambiguous most common tokens' , 'Identity tokens']
training_counts = dict.fromkeys(training_stats , 0)

test_outcomes = ['Total test items' , 'Found in lookup table' , 'Lookup match' , 'Lookup mismatch' , 'Not found in lookup table' , 'Identity match' , 'Identity mismatch']
test_counts = dict.fromkeys(test_outcomes , 0)

accuracies = {}

# Training: read training data and populate lemma counters

train_data = open (train_file , 'r')
tokens=0
unambiType = 0
unambiTok = 0
ambiType = 0
ambiTok = 0
amc = 0 # ambiguous most common
identityTok = 0
maxLemmaCnt = 0

for line in train_data:
    # Tab character identifies lines containing tokens
    if re.search ('\t' , line):
        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')
        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        tokens+=1
        if form == lemma:
            identityTok += 1
        if form in lemma_count:
            list = lemma_count.get(form)
            found = False
            for p in list:
                if lemma == p[0]:
                    p[1]+=1
                    found = True
            if not found:
                list.append([lemma, 1])
            lemma_count[form]=list
        else:
            lemma_count[form]=[[lemma,1]]
        ######################################################
        ### Insert code for populating the lemma counts    ###
        ######################################################

# Model building and training statistics

for form in lemma_count.keys():
    list = lemma_count[form]
    max = 0
    finalLemma = ''
    if len(list)>1:
        ambiType+=1
        mostComm = 0
        for p in list:
            ambiTok+=p[1]
            if p[1] > mostComm:
                mostComm = p[1]
        amc+=mostComm
        maxLemmaCnt+=mostComm
    elif len(list)==1:
        unambiType+=1;
        unambiTok += list[0][1]
        maxLemmaCnt += list[0][1]
    for p in list:
        if p[1]> max:
            max = p[1]
            finalLemma = p[0]
    lemma_max[form]=finalLemma

training_counts['Wordform types'] = len(lemma_count)
training_counts['Wordform tokens'] = tokens
training_counts['Unambiguous types'] = unambiType
training_counts['Unambiguous tokens'] = unambiTok
training_counts['Ambiguous types'] = ambiType
training_counts['Ambiguous tokens'] = ambiTok
training_counts['Ambiguous most common tokens'] = amc
training_counts['Identity tokens'] = identityTok

accuracies['Expected lookup'] = maxLemmaCnt/tokens
### Calculate expected accuracy if we used lookup on all items ###

accuracies['Expected identity'] = identityTok/tokens
# ### Calculate expected accuracy if we used identity mapping on all items ###

### Testing: read test data, and compare lemmatizer output to actual lemma
    
test_data = open (test_file , 'r')

testItems = 0
foundLT = 0
lookupMatch = 0
lookupMismatch = 0
notFoundLT = 0
identityMatch = 0
identityMismatch = 0

for line in test_data:

    # Tab character identifies lines containing tokens
    if re.search ('\t' , line):

        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')

        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        testItems+=1
        if form in lemma_max:
            foundLT+=1
            if lemma==lemma_max.get(form):
                lookupMatch+=1
            else:
                lookupMismatch+=1
        else:
            notFoundLT+=1
            if form == lemma:
                identityMatch+=1
            else:
                identityMismatch+=1

#         ######################################################
#         ### Insert code for populating the test counts     ###
#         ######################################################
test_counts['Total test items']= testItems
test_counts['Found in lookup table']= foundLT
test_counts['Lookup match']= lookupMatch
test_counts['Lookup mismatch']= lookupMismatch
test_counts['Not found in lookup table']= notFoundLT
test_counts['Identity match']= identityMatch
test_counts['Identity mismatch']= identityMismatch
accuracies['Lookup'] = lookupMatch/foundLT
### Calculate accuracy on the items that used the lookup table ###
#

accuracies['Identity'] = identityMatch/notFoundLT
#
accuracies['Overall'] = (lookupMatch+identityMatch)/testItems
### Calculate overall accuracy ###
#
# ### Report training statistics and test results
#

output = open ('lookup-output.txt' , 'w')

output.write ('Training statistics\n')

for stat in training_stats:
    output.write (stat + ': ' + str(training_counts[stat]) + '\n')

for model in ['Expected lookup' , 'Expected identity']:
    output.write (model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.write ('Test results\n')

for outcome in test_outcomes:
    output.write (outcome + ': ' + str(test_counts[outcome]) + '\n')

for model in ['Lookup' , 'Identity' , 'Overall']:
    output.write (model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.close
