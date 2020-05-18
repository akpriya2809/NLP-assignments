import glob
import os
import string
import sys
from random import shuffle

stopwords = set(["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above",

                 "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added",
                 "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against",
                 "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already",
                 "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce",
                 "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways",
                 "anywhere",
                 "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar",
                 "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking",
                 "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az",
                 "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes",
                 "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind",
                 "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill",
                 "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu",
                 "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't",
                 "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit",
                 "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning",
                 "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding",
                 "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct",
                 "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely",
                 "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different",
                 "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down",
                 "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea",
                 "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el",
                 "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep",
                 "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every",
                 "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f",
                 "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire",
                 "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former",
                 "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full",
                 "further",
                 "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives",
                 "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy",
                 "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't",
                 "have",
                 "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here",
                 "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's",
                 "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how",
                 "howbeit",
                 "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8",
                 "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll",
                 "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc",
                 "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar",
                 "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn",
                 "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j",
                 "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know",
                 "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly",
                 "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked",
                 "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los",
                 "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe",
                 "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill",
                 "million",
                 "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms",
                 "mt", "mu",
                 "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay",
                 "nc", "nd",
                 "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither",
                 "never",
                 "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody",
                 "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel",
                 "now",
                 "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od",
                 "of", "off",
                 "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one",
                 "ones", "only",
                 "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought",
                 "our", "ours",
                 "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2",
                 "p3", "page",
                 "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe",
                 "per",
                 "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly",
                 "possible",
                 "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously",
                 "primarily",
                 "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que",
                 "quickly",
                 "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably",
                 "recent",
                 "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research",
                 "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj",
                 "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said",
                 "same", "saw", "say",
                 "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem",
                 "seemed",
                 "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven",
                 "several",
                 "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should",
                 "shouldn",
                 "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant",
                 "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly",
                 "sm",
                 "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes",
                 "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying",
                 "sq", "sr",
                 "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such",
                 "sufficiently", "suggest",
                 "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc",
                 "td", "te",
                 "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats",
                 "that's",
                 "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter",
                 "thereby",
                 "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto",
                 "thereupon",
                 "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv",
                 "thin",
                 "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand",
                 "three",
                 "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to",
                 "together",
                 "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try",
                 "trying", "ts",
                 "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk",
                 "um", "un",
                 "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups",
                 "ur", "us",
                 "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va",
                 "value", "various", "vd",
                 "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w",
                 "wa", "want",
                 "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll",
                 "well-b", "went",
                 "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats",
                 "what's", "when",
                 "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres",
                 "where's",
                 "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever",
                 "whole",
                 "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will",
                 "willing",
                 "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would",
                 "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn",
                 "xo",
                 "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your",
                 "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi",
                 "zz"])


def removeSuffix(arr):
    newList = []
    for word in arr:
        for suf in ["ly", "ing", "ed", "s"]:
            if word.endswith(suf):
                word = word[:-len(suf)]
        newList.append(word)
    return newList


def processData(data):
    translator = str.maketrans('', '', string.punctuation)
    out = data.translate(translator)
    out = ''.join([i for i in out if not i.isdigit()])
    wordList = out.split()
    wordList = [word.lower().strip() for word in wordList]
    wordList = [word for word in wordList if word not in stopwords]
    wordList = removeSuffix(wordList)
    return wordList;


def extractFeatures(all_files):
    uniqueWords = set()
    for file in all_files:
        f = open(file, 'r')
        data = f.read()
        wordlist = processData(data)
        for word in wordlist:
            uniqueWords.add(word)
    return uniqueWords


def populateWordCountDict(data):
    wordcount = {}
    wordlist = processData(data)
    for word in wordlist:
        if word in wordcount:
            wordcount[word] += 1
        else:
            wordcount[word] = 1
    return wordcount


def calculateActivation(wordCountDict, weightsData):
    activationRes = 0
    for word in wordCountDict:
        if word in weightsData:
            activationRes += wordCountDict[word] * weightsData[word]
    return activationRes


def vanillaModelTraining(featuresList, all_files):
    vanillaPosNegWeights = dict()
    vanillaTruDecWeights = dict()
    for feature in featuresList:
        vanillaPosNegWeights[feature] = 0
        vanillaTruDecWeights[feature] = 0
    vanillaPNBias = 0
    vanillaTDBias = 0
    shuffle(all_files)
    for file in all_files:
        type1, type2, fold, fname = file.split('/')[-4:]
        f = open(file, 'r')
        data = f.read()
        label_a = 0
        label_b = 0
        if 'positive' in type1:
            label_a = 1
        else:
            label_a = -1
        if 'truthful' in type2:
            label_b = 1
        else:
            label_b = -1

        wordCountDict = populateWordCountDict(data)

        for i in range(max_iterations):
            posNegAct = calculateActivation(wordCountDict, vanillaPosNegWeights) + vanillaPNBias
            if (posNegAct * label_a) <= 0:
                for word in sorted(wordCountDict):
                    if word in vanillaPosNegWeights:
                        vanillaPosNegWeights[word] = vanillaPosNegWeights[word] + (label_a * wordCountDict[word])
                vanillaPNBias += label_a

            truDecAct = calculateActivation(wordCountDict, vanillaTruDecWeights) + vanillaTDBias

            if (truDecAct * label_b) <= 0:
                for word in sorted(wordCountDict):
                    if word in vanillaTruDecWeights:
                        vanillaTruDecWeights[word] = vanillaTruDecWeights[word] + (label_b * wordCountDict[word])
                vanillaTDBias += label_b

    # write to weight and bias to vanillamodel.txt
    mf = open('vanillamodel.txt', 'w')
    mf.write("Positive Negative Bias:" + str(vanillaPNBias) + "\n")
    mf.write("Truthful Deceptive Bias:" + str(vanillaTDBias) + "\n")
    mf.write("WORD, P/N WEIGHT, T/D WEIGHT\n")
    for key in featuresList:
        mf.write(str(key) + ":" + str(vanillaPosNegWeights[key])+","+str(vanillaTruDecWeights[key])+"\n")


def averageModelTraining(featuresList, all_files):
    avgPosNegWeights = dict()
    avgTruDecWeights = dict()
    avgPNCacheWeights = dict()
    avgTDCahceWeights = dict()
    for feature in featuresList:
        avgPosNegWeights[feature] = 0
        avgTruDecWeights[feature] = 0
        avgPNCacheWeights[feature] = 0
        avgTDCahceWeights[feature] = 0

    avgPNBias = 0
    avgTDBias = 0
    avgPNBetaBias = 0
    avgTDBetaBias = 0
    countPN = 1
    countTD = 1
    shuffle(all_files)
    for file in all_files:
        type1, type2, fold, fname = file.split('/')[-4:]
        f = open(file, 'r')
        data = f.read()
        label_a = 0
        label_b = 0
        if 'positive' in type1:
            label_a = 1
        else:
            label_a = -1
        if 'truthful' in type2:
            label_b = 1
        else:
            label_b = -1

        wordCountDict = populateWordCountDict(data)

        for i in range(max_iterations):
            pnActivation = calculateActivation(wordCountDict, avgPosNegWeights)+avgPNBias
            if (pnActivation * label_a) <= 0:
                for word in sorted(wordCountDict):
                    if word in avgPosNegWeights:
                        avgPosNegWeights[word] += (label_a * wordCountDict[word])
                    if word in avgPNCacheWeights:
                        avgPNCacheWeights[word] += (label_a * countPN * wordCountDict[word])
                avgPNBias += label_a
                avgPNBetaBias += float(label_a * countPN)
            countPN += 1

            tdaActivation = calculateActivation(wordCountDict, avgTruDecWeights)+avgTDBias
            if(tdaActivation * label_b) <= 0:
                for word in sorted(wordCountDict):
                    if word in avgTruDecWeights:
                        avgTruDecWeights[word] += (label_b * wordCountDict[word])
                    if word in avgTDCahceWeights:
                        avgTDCahceWeights[word] += (label_b * countTD * wordCountDict[word])
                avgTDBias += label_b
                avgTDBetaBias += float(label_b * countTD)
            countTD += 1

    # print("avgPNBias", avgPNBias)
    # print("avgTDBias", avgTDBias)
    # print("avgPNBetaBias", avgPNBetaBias)
    # print("avgTDBetaBias", avgTDBetaBias)
    # print("countPN", countPN)
    # print("countTD", countTD)
    avgPNBias -= (float(1 / countPN) * avgPNBetaBias)
    avgTDBias -= (float(1/countTD) * avgTDBetaBias)
    mf = open('averagemodel.txt', 'w')
    mf.write("avgPNBias:" + str(avgPNBias)+ "\n")
    mf.write("avgTDBias: " + str(avgTDBias) + "\n")

    for word in avgPosNegWeights:
        avgPosNegWeights[word]  -= (float(1 / countPN) * avgPNCacheWeights[word])
    for word in avgTruDecWeights:
        avgTruDecWeights[word] -= (float(1/countTD) * avgTDCahceWeights[word])
    mf.write("WORD, P/N WEIGHTS, T/D WEIGHTS \n")
    for word in featuresList:
        mf.write(word + ":" + str(avgPosNegWeights[word]) + "," + str(avgTruDecWeights[word])+"\n")



max_iterations = 30
all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
featuresList = extractFeatures(all_files)
vanillaModelTraining(featuresList, all_files)
averageModelTraining(featuresList, all_files)

