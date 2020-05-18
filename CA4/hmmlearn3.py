import sys
from collections import defaultdict

emit = defaultdict(int)
transition = defaultdict(int)
context = defaultdict(int)
wordToTag = defaultdict(int)
states = set()


f = open(sys.argv[1], 'r')

for line in f:
    prev = '<q>'
    context[prev] += 1
    wordTagList = line.strip().split(" ")
    word = ""
    tag = ""
    for wordtag in wordTagList:
        index = -1
        for i in range(len(wordtag), 0, -1):
            if wordtag[i - 1] == '/':
                index = i - 1
        word = wordtag[:index]
        #  print(wordtag[:index])
        tag = wordtag[index + 1:]
        # if wordtag[len(wordtag) - 4] == '/':
        #     # print(wordtag[:len(wordtag) - 4])
        #     # print(wordtag[-3:])
        #     word = wordtag[:len(wordtag) - 4]
        #     tag = wordtag[-3:]
        # if wordtag[len(wordtag) - 2] == '/':
        #     #print(wordtag[:len(wordtag) - 2])
        #     word = wordtag[:len(wordtag) - 2]
        #     tag = wordtag[-1:]
        # if wordtag[len(wordtag) - 3] == '/':
        #     #print(wordtag[:len(wordtag) - 3])
        #     word = wordtag[:len(wordtag) - 3]
        #     tag = wordtag[-2:]
        #word = wordtag[:len(wordtag) - 3]
        #print(word)
        # tag = wordtag[-2:]
        # if tag.startswith("/"):
        #     tag = tag[1:]
        transition[prev + " " + tag] += 1
        context[tag] += 1
        emit[tag + " " + word] += 1
        prev = tag
        states.add(tag)
        if word not in wordToTag:
            wordToTag[word] = set()
        wordToTag[word].add(tag)
    transition[prev+" </q>"] += 1

hm = open('hmmmodel.txt', 'w')
numberOfStates = len(states)

for key in transition:
    prev, tag = key.split(" ")
    prob = str(float(transition[key]+1)/(context[prev]+numberOfStates))

    hm.write("Transition " + key + " " + str(transition[key]) + " " + prob+"\n")

for key in emit:
        tag, word = key.split(" ")
        # print("key",emit[key])
        # print("tag",context[tag])
        # val = float(emit[key]/ context[tag])
        # print("val", val)
        hm.write("Emission " + key + " " + str(float(emit[key])/ context[tag]) + "\n")

for key in context:
        hm.write("Context " + key + " " + str(context[key]) + "\n")

for key in wordToTag:
    tags = ""
    for tag in wordToTag[key]:
        tags += str(tag) + ","
    tags+="\n"
    hm.write("WordToTag "+ key+" "+ tags)

