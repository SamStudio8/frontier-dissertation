__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.0.1"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

import numpy as np
import os
import sys

from bamcheckreader import BamcheckReader

def classify_label(classes, label):
    for cl in classes:
        for name in classes[cl]["names"]:
            if name.lower() == label.lower():
                return cl
    raise Exception("Unknown Label Class: %s" % label)

def encode_class(classes, class_label):
    if not class_label in classes:
        raise Exception("Unknown Class: %s" % class_label)

    if "code" not in classes[class_label]:
        raise Exception("Class %s has no Code" % class_label)
    return classes[class_label]["code"]

def decode_class(classes, class_code):
    for cl in classes:
        if classes[cl]["code"] == class_code and "recoded" not in classes[cl]:
            return cl
    raise Exception("Unknown Label Code: %s" % class_code)

def count_class(classes, class_label):
    if not class_label in classes:
        raise Exception("Unknown Class: %s" % class_label)

    if "count" not in classes[class_label]:
        classes[class_label]["count"] = 0
    classes[class_label]["count"] += 1

class Statplexer(object):

    def __init__(self, data_dir, target_path, classes):
        self.data_dir = data_dir
        self.target_path = target_path

        self.listing = []
        self._data = {}
        self._targets = {}
        self._len = 0

        self._classes = classes
        for cl in self._classes:
            self._classes[cl]["count"] = 0

        t = open(target_path, 'r')
        t.readline()
        targets = {}
        for line in t:
            line = line.strip()
            fields = line.split("\t")
            lanelet = fields[0]

            auto_qc_class = classify_label(classes, fields[4])
            auto_qc_code = encode_class(classes, auto_qc_class)

            targets[lanelet] = auto_qc_code

        #TODO Better handling for missing targets
        for root, subfolders, files in os.walk(self.data_dir):
            print root + "(" + str(len(files)) + " files)"
            for bam in files:
                bampath = os.path.join(root, bam)

                lanelet = bam.split(".")[0]
                if lanelet in targets:
                    self._targets[lanelet] = targets[lanelet]
                    self._data[bam] = BamcheckReader(bampath)
                    self._len += 1

                    class_label = decode_class(classes, targets[lanelet])
                    count_class(classes, class_label)
                else:
                    print "[WARN] BAM missing TARGET"


    def __len__(self):
        return self._len

    def list_regressors(self):
        regressors = []
        for bam in sorted(self._data):
            for r in self._data[bam].summary:
                if r not in regressors:
                    regressors.append(r)
            break
        return sorted(regressors)

    def find_regressors(self, queries):
        regressors = []
        for bam in sorted(self._data):
            for r in self._data[bam].summary:
                for query in queries:
                    if query in r:
                        if r not in regressors:
                            regressors.append(r)
                            continue
            break
        return sorted(regressors)

    def exclude_regressors(self, queries):
        regressors = []
        for bam in sorted(self._data):
            for r in self._data[bam].summary:
                for query in queries:
                    if query not in r:
                        if r not in regressors:
                            regressors.append(r)
                            break
                    else:
                        break
            break
        return sorted(regressors)

    def get_regressors(self, names):
        np_array = np.empty([len(self),len(names)])
        for i, bam in enumerate(sorted(self._data)):
            bam_n = np.zeros(len(names))
            for j, regressor in enumerate(names):
                bam_n[j] = self._data[bam].summary[regressor]
            np_array[i] = bam_n
        return np_array

    def get_data_by_target(self, names, targets):

        total = 0
        for lanelet in self._targets:
            target = self._targets[lanelet]
            if targets:
                if target in targets:
                    total += 1
            else:
                total += 1

        data_np_array = np.empty([total,len(names)])
        targ_np_array = np.empty([total])

        counter = 0
        levels = []
        for bam in sorted(self._data):
            lanelet = bam.split(".")[0]
            target = self._targets[lanelet]
            if targets:
                if target not in targets:
                    continue

            bam_n = np.zeros(len(names))
            for j, regressor in enumerate(names):
                bam_n[j] = self._data[bam].summary[regressor]
            data_np_array[counter] = bam_n
            targ_np_array[counter] = self._targets[lanelet]
            if self._targets[lanelet] not in levels:
                levels.append(self._targets[lanelet])
            counter += 1

        return data_np_array, targ_np_array, sorted(levels)

    def get_targets(self):
        np_array = np.empty([len(self)])
        for i, bam in enumerate(sorted(self._data)):
            lanelet = bam.split(".")[0]
            np_array[i] = self._targets[lanelet]
        return np_array

    def count_targets_by_class(self, targets=None):
        counts = {}
        for class_label in self._classes:
            counts[class_label] = 0

        if targets is None:
            targets = self._targets.values()

        for target in targets:
            class_label = decode_class(self._classes, target)
            counts[class_label] += 1
        return counts

    def write_log(self, log_filename, pdf_filename, data_set, param_set, regressors, used_targets, scores, folds, importance):

        def write(message):
            sys.stdout.write(message)
            o.write(message)

        o = open(log_filename, 'w')
        write("Frontier\n")
        write("********\n")
        write("Data Dir\t%s\n" % self.data_dir)
        write("AQC File\t%s\n" % self.target_path)
        write("\n")
        write("Class Def\t" + "\t".join([cl for cl in sorted(self._classes)]) + "\n")
        write("Class Read\t" + "\t".join([str(v["count"]) for k,v in sorted(self._classes.items())]) + "\n")
        write("Class Used\t" + "\t".join([str(v) for k,v in sorted(self.count_targets_by_class(used_targets).items())]) + "\n")
        write("\n")
        write("Total Read\t%d\n" % len(self))
        write("Total Used\t%d\n" % len(used_targets))
        write("\n")
        write("Param Set\t%s\n" % param_set)
        write("Param Count\t%d\n" % len(regressors))
        write("Param List:\n")
        for param in regressors:
            write("\t\t%s\n" % param)
        write("\n")
        write("Feature Importances:\n")
        for imp in sorted(importance, key=lambda x: importance[x], reverse=True):
            if importance[imp] > 0.01:
                write("\t\t%0.2f\t%s\n" % (importance[imp], imp))
        write("\n")
        write("CV Score (Fld)\t%0.2f +/- %0.2f (%d)\n" % (scores.mean(), scores.std() * 2, folds))
        write("\n")
        write("Decision PDF\t%s\n" % pdf_filename)
        write("********")
        o.close()
