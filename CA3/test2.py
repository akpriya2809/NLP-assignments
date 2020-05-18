# use this file to learn perceptron classifier
# Expected: generate vanillamodel.txt and averagemodel.txt
import glob
import os
import string
from random import shuffle


def words_cleaning(lines):
    tokens = []
    shuffle(lines)
    for line in lines:
        line = line.rstrip()
        tokens = tokens + line.split()
    # To Lower Case
    tokens = [token.lower() for token in tokens]
    # Remove all punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped_punctuation = [t.translate(table) for t in tokens]
    return stripped_punctuation


def feature_extraction(documents):
    features = {}
    for each_document in documents:
        class1, class2, fold, filename = each_document.split('/')[-4:]
        # if fold == "fold1":
        #     # Don't do anything
        #     continue
        # else:
        input_file_read = open(each_document, "r")
        file_lines = input_file_read.readlines()
        cleaned_words = words_cleaning(file_lines)

        for each_word in sorted(cleaned_words):
            if each_word in features:
                continue
            else:
                features[each_word] = 0
    return features


def extract_words_counts(document):
    input_file_read = open(document, "r")
    lines = input_file_read.readlines()
    cleaned_words = words_cleaning(lines)
    distribution = {}
    for each_word in sorted(cleaned_words):
        if each_word in distribution:
            distribution[each_word] += 1
        else:
            distribution[each_word] = 1
    return distribution


def calculate_activation(words, weights):
    activation = 0
    for word in sorted(words):
        if word in weights:
            activation += words[word] * weights[word]
    return activation


def vanilla_train(documents, features):
    vanilla_positive_negative_weights = features.copy()
    vanilla_truth_deceptive_weights = features.copy()
    vanilla_model = open("vanillamodel.txt", "w")
    vpnbias = 0
    vtdbias = 0
    max_iterations = 30
    shuffle(documents)
    for each_document in documents:
        class1, class2, fold, filename = each_document.split('/')[-4:]
        labela = 0
        labelb = 0
        if "positive" in class1:
            labela = 1
        else:
            labela = -1

        if "truth" in class2:
            labelb = 1
        else:
            labelb = -1

        word_count_distribution = extract_words_counts(each_document)

        for i in range(max_iterations):
            pnactivation = calculate_activation(word_count_distribution, vanilla_positive_negative_weights)
            if (pnactivation + vpnbias) * labela <= 0:
                for word in sorted(word_count_distribution):
                    if word in vanilla_positive_negative_weights:
                        vanilla_positive_negative_weights[word] += (labela * word_count_distribution[word])
                vpnbias += labela

            tdactivation = calculate_activation(word_count_distribution, vanilla_truth_deceptive_weights)
            if (tdactivation + vtdbias) * labelb <= 0:
                for word in sorted(word_count_distribution):
                    if word in vanilla_truth_deceptive_weights:
                        vanilla_truth_deceptive_weights[word] += (labelb * word_count_distribution[word])
                vtdbias += labelb

    vanilla_model.write("VPNBias   " + str(vpnbias) + "\n")
    for each_word in sorted(vanilla_positive_negative_weights):
        if vanilla_positive_negative_weights[each_word] != 0:
            vanilla_model.write(str(each_word) + "  " + str(vanilla_positive_negative_weights[each_word]) + "\n")

    vanilla_model.write("*****\n")
    vanilla_model.write("VTDBias   " + str(vtdbias) + "\n")
    for each_word in sorted(vanilla_truth_deceptive_weights):
        if vanilla_truth_deceptive_weights[each_word] != 0:
            vanilla_model.write(str(each_word) + "  " + str(vanilla_truth_deceptive_weights[each_word]) + "\n")


def average_train(documents, features):
    average_positive_negative_weights = features.copy()
    average_truth_deceptive_weights = features.copy()
    u_positive_negative_cached_weights = features.copy()
    u_truth_deceptive_cached_weights = features.copy()
    average_model = open("averagemodel.txt", "w")
    apnbias = 0
    atdbias = 0
    cpn = 1
    ctd = 1
    atdbeta = 0
    apnbeta = 0
    max_iterations = 30
    shuffle(documents)
    for each_document in documents:
        class1, class2, fold, filename = each_document.split('/')[-4:]
        pn = 0
        td = 0
        if "positive" in class1:
            pn = 1
        else:
            pn = -1
        if "truth" in class2:
            td = 1
        else:
            td = -1

        word_count_distribution = extract_words_counts(each_document)

        for i in range(max_iterations):

            pnactivation = calculate_activation(word_count_distribution, average_positive_negative_weights)
            if (pnactivation + apnbias) * pn <= 0:
                for word in sorted(word_count_distribution):
                    if word in average_truth_deceptive_weights:
                        average_positive_negative_weights[word] += (pn * word_count_distribution[word])
                for word in sorted(word_count_distribution):
                    if word in u_positive_negative_cached_weights:
                        u_positive_negative_cached_weights[word] += (pn * cpn * word_count_distribution[word])
                apnbias += pn
                apnbeta += float(pn*cpn)
            cpn += 1

            tdactivation = calculate_activation(word_count_distribution, average_truth_deceptive_weights)
            if (tdactivation + atdbias) * td <= 0:
                for word in sorted(word_count_distribution):
                    if word in average_truth_deceptive_weights:
                        average_truth_deceptive_weights[word] += (td * word_count_distribution[word])
                for word in sorted(word_count_distribution):
                    if word in u_truth_deceptive_cached_weights:
                        u_truth_deceptive_cached_weights[word] += (td * ctd * word_count_distribution[word])
                atdbias += td
                atdbeta += float(td*ctd)
            ctd += 1

    apnbias -= (float(1/cpn) * apnbeta)
    average_model.write("APNBias   " + str(apnbias) + "\n")
    for each_word in sorted(average_positive_negative_weights):
        average_positive_negative_weights[each_word] = average_positive_negative_weights[each_word] - \
                                                       (float(1 / cpn) * u_positive_negative_cached_weights[each_word])
        if average_positive_negative_weights[each_word] != 0:
            average_model.write(str(each_word) + "  " + str(average_positive_negative_weights[each_word]) + "\n")

    average_model.write("*****\n")
    atdbias -= (float(1/ctd) * atdbeta)
    average_model.write("ATDBias   " + str(atdbias) + "\n")
    for each_word in sorted(average_truth_deceptive_weights):
        average_truth_deceptive_weights[each_word] = average_truth_deceptive_weights[each_word] - \
                                                     (float(1/ctd) * u_truth_deceptive_cached_weights[each_word])
        if average_truth_deceptive_weights[each_word] != 0:
            average_model.write(str(each_word) + "  " + str(average_truth_deceptive_weights[each_word]) + "\n")


all_files = glob.glob(os.path.join('op_spam_training_data', '*/*/*/*.txt'))
extracted_features = feature_extraction(all_files)
vanilla_train(all_files, extracted_features)
average_train(all_files, extracted_features)

