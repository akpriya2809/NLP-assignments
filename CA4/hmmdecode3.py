from _collections import defaultdict
import sys

emit = defaultdict(int)
transition = defaultdict(int)
context = defaultdict(int)
states = set()
start = defaultdict(int)
wordToTag = defaultdict(int)

f = open('hmmmodel.txt', 'r')
totalstart = 0
for line in f:
    if line.startswith("T"):
        data = line.rstrip("\n").split(" ")
        transition[data[1].strip() + " " + data[2].strip()] = float(data[4].strip())
        if data[1].strip().startswith("<q>"):
            start[str(data[2].strip())] += int(data[3].strip())
            totalstart += int(data[3].strip())

    elif line.startswith("E"):
        data = line.rstrip("\n").split(" ")
        emit[data[1].strip() + " " + data[2].strip()] = float(data[3].strip())

    elif line.startswith("C"):
        data = line.rstrip("\n").split(" ")
        context[data[1].strip()] = int(data[2].strip())
        states.add(data[1].strip())

    elif line.startswith("W"):
        data = line.rstrip("\n").split(" ")
        word = data[1].strip()
        if word not in wordToTag:
            wordToTag[word] = set()
        tags = data[2].strip().rstrip(",").strip()
        tags = tags.split(",")
        for tag in tags:
            wordToTag[word].add(tag.strip())

for st in states:
    start[st] = float(start[st]) / totalstart

fopen = open(sys.argv[1], 'r')


def viterbi(temp, states, start, transition, emit, context, wordToTag):
    vdictList = [defaultdict(int)]
    backpointer = [defaultdict(int)]
    if temp[0] in wordToTag:
        some_states = wordToTag[temp[0]]
        for i in some_states:
            if i in states and start[i] > 0 and (i + " " + temp[0].strip()) in emit:
                vdictList[0][i] = start[i] * emit[i + " " + temp[0].strip()]
    else:
        for i in states:
            if i in states and start[i] > 0:
                vdictList[0][i] = start[i]

    if "<q>" in states:
        states.remove("<q>")

    for t in range(1, len(temp)):
        vdictList.append(defaultdict(int))
        backpointer.append(defaultdict(int))
        some_states = states

        if temp[t] in wordToTag:

            some_states = wordToTag[temp[t]]

            for ss in some_states:
                maxval = -1
                for y0 in states:
                    if ((y0 in vdictList[t - 1]) and vdictList[t - 1][y0] > 0 and ((ss + " " + temp[t].strip()) in emit)):
                        probvalv = vdictList[t - 1][y0] * transition[y0 + " " + ss] * emit[ss + " " + temp[t].strip()]

                        if maxval <= probvalv:
                            maxval = probvalv
                            backpointer[t][ss] = y0
                vdictList[t][ss] = maxval
        else:

            for ss in states:
                maxval = -1
                for y0 in states:
                    if ((y0 in vdictList[t - 1]) and vdictList[t - 1][y0] > 0):
                        probvalv = vdictList[t - 1][y0] * transition[y0 + " " + ss]
                        if maxval <= probvalv:
                            maxval = probvalv
                            backpointer[t][ss] = y0
                vdictList[t][ss] = maxval

    listOfTags = []

    tag = ""
    maxvalue = -1
    some_states = states
    if temp[len(temp) - 1] in wordToTag:
        some_states = wordToTag[temp[len(temp) - 1]]

    for i in some_states:
        if maxvalue <= vdictList[len(temp) - 1][i]:
            maxvalue = vdictList[len(temp) - 1][i]
            tag = i

    listOfTags.append(temp[len(temp) - 1] + "/" + tag)

    for t in range(len(temp) - 2, -1, -1):
        if tag not in backpointer[t + 1]:
            for i in states:
                if i in backpointer[t + 1]:
                    tag = backpointer[t + 1][i]
                    break;
        else:
            tag = backpointer[t + 1][tag]
        listOfTags.append(temp[t] + "/" + tag)

    return listOfTags


fout = open('hmmoutput.txt', 'w')
for line in fopen:
    temp = line.rstrip("\n").split(" ")
    taggedList = viterbi(temp, states, start, transition, emit, context, wordToTag)
    for i in range(len(taggedList) - 1, -1, -1):
        fout.write(str(taggedList[i]) + " ")
    fout.write("\n")




