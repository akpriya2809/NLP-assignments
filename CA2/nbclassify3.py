import glob
import math
import os
import string
import sys

pathname = "nboutput.txt"
all_List = []
classProb = dict()
vocabSize = dict()
wordProb = dict()

# len(commonDict)
totalUniqueWords = 0

stopwords = set(["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above",

                "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added",
                "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against",
                "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already",
                "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce",
                "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere",
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
                "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further",
                "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives",
                "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy",
                "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have",
                "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here",
                "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's",
                "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit",
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
                "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million",
                "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu",
                "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd",
                "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never",
                "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody",
                "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now",
                "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off",
                "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only",
                "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours",
                "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page",
                "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per",
                "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible",
                "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily",
                "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly",
                "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent",
                "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research",
                "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj",
                "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say",
                "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed",
                "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several",
                "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn",
                "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant",
                "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm",
                "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes",
                "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr",
                "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest",
                "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te",
                "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's",
                "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby",
                "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon",
                "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin",
                "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three",
                "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together",
                "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts",
                "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un",
                "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us",
                "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd",
                "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want",
                "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went",
                "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when",
                "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's",
                "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole",
                "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing",
                "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would",
                "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo",
                "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your",
                "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"])

# stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
#                  "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
#                  'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
#                  'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am',
#                  'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
#                  'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
#                  'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
#                  'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
#                  'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
#                  'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
#                  'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
#                  "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
#                  'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
#                  "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
#                  'shouldn', "shouldn't",
#                  'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

def readModelParameters():
    count = 0
    with open("nbmodel.txt") as f:
        for line in f:
            if count == 0:
                arr = line.split('-')
                global totalUniqueWords
                totalUniqueWords = int(arr[1])
            if ':' in line and count < 6:
                arr = line.split(':')
                classProb[arr[0].strip()] = arr[1].strip()
            elif ':' in line and count < 12:
                arr= line.split(':')
                vocabSize[arr[0].strip()] = int(arr[1].strip())
            else:
                if count >= 14:
                    finallistProb = []
                    arr = line.split(':')
                    listProb = arr[1].split(',')
                    for i in range(len(listProb)):
                        x=listProb[i].strip()
                        finallistProb.append(int(x))
                    wordProb[arr[0].strip()] = finallistProb
            count+=1

def removeSuffix(arr):
    newList = []
    for word in arr:
        for suf in ["ly", "ing", "ed", "s", "ous", "tion"]:
            if word.endswith(suf):
                word = word[:-len(suf)]
        newList.append(word)
    return newList;

def calWordGivenPos(word):
    count = float(wordProb[word][0])+1
    posVocabSize = vocabSize['posVocabSize']
    N = totalUniqueWords+posVocabSize
    res = count/N
    # print("count", count)
    # print("N", N)
    # print("POS",res)
    # res = count / posVocabSize
    return res

def calWordGivenNeg(word):

    count = float(wordProb[word][1])+1
    negVocabSize = vocabSize['negVocabSize']

    N = totalUniqueWords+negVocabSize
    res = count / N
    # res = count/negVocabSize
    return res

def calWordGivenDec(word):
    count = float(wordProb[word][2])+1
    decVocabSize = vocabSize['decVocabSize']
    N = totalUniqueWords+decVocabSize
    #res = count/decVocabSize
    res = count / N
    # print("count", count)
    # print("N", N)
    # print("Dec",res)
    return res

def calWordGivenTru(word):
    count = float(wordProb[word][3])+1
    truVocabSize = vocabSize['truVocabSize']
    # print("totalUniqueWords",totalUniqueWords)
    N = totalUniqueWords+truVocabSize
    res = count / N
    # res = count/truVocabSize
    return res

def readTestData():
    for file in all_files:
        type1, type2, fold, fname = file.split('/')[-4:]
        f = open(file, 'r')
        review = f.read()
        translator = str.maketrans('', '', string.punctuation)
        review = review.translate(translator)
        review = ''.join([i for i in review if not i.isdigit()])
        tokens = review.split()
        tokens = [word.lower() for word in tokens]
        tokens = [word for word in tokens if word not in stopwords]
        tokens = removeSuffix(tokens) # remove words ending with s, ing, ed, and numbers

        positive_prob_list = list()
        negative_prob_list = list()
        deceptive_prob_list = list()
        truthful_prob_list = list()

        for word in tokens:
            if word in wordProb:
                #calculate P(word| positive)
                condPos = calWordGivenPos(word)
                positive_prob_list.append(condPos)

                condNeg = calWordGivenNeg(word)
                negative_prob_list.append(condNeg)

                condDec = calWordGivenDec(word)
                deceptive_prob_list.append(condDec)

                condTru = calWordGivenTru(word)
                truthful_prob_list.append(condTru)

        finalPosProb = 0
        finalNegProb = 0
        finalDecProb = 0
        finalTruProb = 0
        for i in positive_prob_list:
            print("i:",i, "log(i):",math.log(i))
            finalPosProb += math.log(i)
        finalPosProb += math.log(float(classProb['positive']))

        for i in negative_prob_list:
            finalNegProb += math.log(i)
        finalNegProb += math.log(float(classProb['negative']))

        for i in deceptive_prob_list:
            finalDecProb += math.log(i)
        finalDecProb += math.log(float(classProb['deceptive']))
        for i in truthful_prob_list:
            finalTruProb += math.log(i)
        finalTruProb += math.log(float(classProb['truthful']))
        #print("pos",finalPosProb, "neg", finalNegProb)
        label_a = ''
        label_b = ''
        if finalDecProb > finalTruProb:
            label_a += 'deceptive'
        else:
            label_a += 'truthful'
        if finalPosProb > finalNegProb:
            label_b += 'positive'
        else:
            label_b += 'negative'
        fout.write(label_a.strip()+" "+label_b.strip()+" "+str(file))
        fout.write("\n")


readModelParameters()
all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
fout = open('nboutput.txt', 'w')
# print("totalUniqueWords",totalUniqueWords)
readTestData()


