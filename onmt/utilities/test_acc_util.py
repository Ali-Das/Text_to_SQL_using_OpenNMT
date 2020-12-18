from __future__ import unicode_literals
import nltk
from numpy.core.defchararray import lower


class TestAccUtil:
    """Class is responsible for testing accuracy of predicted queries comparing it with ground truth queries"""

    def __init__(self, model, predicted_file, gr_truth_file):
        self.model = model
        self.predicted_file = predicted_file
        self.gr_truth_file = gr_truth_file
        pass

    def test_acc(self, ):
        pred_file = "/content/drive/My Drive/OpenNMT-py/data/" + self.predicted_file
        correct_pred_file = "/content/drive/My Drive/OpenNMT-py/data/" + self.model + self.predicted_file
        ground_truth__file = "/content/drive/My Drive/OpenNMT-py/data/" + self.gr_truth_file
        filepr = open(pred_file, "r", encoding="utf-8")
        filecpr = open(correct_pred_file, "w", encoding="utf-8")
        filegt = open(ground_truth__file, "r", encoding="utf-8")
        acc = 0
        err = 0
        tot = 0
        pred_contents = filepr.readlines()
        filelen = len(pred_contents)
        gr_contents = filegt.readlines()
        print("length of files: ", filelen)
        tot_similarity = 0
        #no_of_iter = 0
        length = None
        for line1, line2 in zip(pred_contents, gr_contents):
            """no_of_iter += 1
            if no_of_iter > 10:
                break"""
            if line1 == line2:
                filecpr.write(line1)
                #print("line1:", line1, "line2", line2)
                acc += 1
            elif line1 != line2:
                err += 1
            tot += 1
            line1_tokens = nltk.word_tokenize(line1)
            line2_tokens = nltk.word_tokenize(line2)
            str1_words = set(lower(line1_tokens))
            str2_words = set(lower(line2_tokens))
            common = str1_words.intersection(str2_words)
            #print("\n the common words are:", common, str2_words,str2_words)
            if len(str1_words) > len(str2_words):
                length = len(str1_words)
            else:
                length = len(str2_words)
            similarity = len(common) / length
            #print(line1, " and ", line2, " are ", similarity, " similar", "common length:", len(common), "length:", length)
            tot_similarity += similarity

        acc_percentage = acc/tot
        tot_similarity = tot_similarity / tot
        print("\n In ", self.model, ": correct queries:", acc, "wrong queries:", err, "total queries:", tot,
              "accuracy percentage = ", acc_percentage, " similarity percentage = ", tot_similarity)
        filepr.close()
        filegt.close()
        filecpr.close()
