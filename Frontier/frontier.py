__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.0.1"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

import numpy as np
import os
import sys

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

    def __init__(self, data_dir, target_path, classes, DATA_READER_CLASS, TARGET_READER_CLASS):
        self.data_dir = data_dir
        self.target_path = target_path

        self._data = {}
        self._targets = {}

        self._classes = classes
        for cl in self._classes:
            self._classes[cl]["count"] = 0

        if data_dir and target_path:
            self.load_data(data_dir, target_path, DATA_READER_CLASS, TARGET_READER_CLASS)

    def load_data(self, data_dir, target_path, DATA_READER_CLASS, TARGET_READER_CLASS):
        #TODO Better handling for missing targets
        #TODO Better handling to ensure all observations have all variables

        # targets written to local variable rather than self._targets class
        # variable to ensure only targets for observations actually seen in
        # the input data are added to the data structure
        targets = TARGET_READER_CLASS(target_path, self._classes, auto_close=True).get_targets()

        for root, subfolders, files in os.walk(self.data_dir):
            print root + "(" + str(len(files)) + " files)"
            for f in files:
                fpath = os.path.join(root, f)

                _id = f.split(".")[0]
                if _id in targets:
                    self._targets[_id] = targets[_id]
                    self._data[f] = DATA_READER_CLASS(fpath, self._classes, auto_close=True).get_data()

                    class_label = decode_class(self._classes, targets[_id])
                    count_class(self._classes, class_label)
                else:
                    print "[WARN] INPUT missing TARGET"

        #TODO Warn when no files are input

        # Test parameter variances and output warning if zero
        self._test_variance()

    def _test_variance(self):
        regressors = self.list_regressors()
        variances = np.zeros(len(regressors))
        means = np.zeros(len(regressors))

        for i, observation in enumerate(sorted(self._data)):
            for j, regressor in enumerate(sorted(regressors)):
                obs_val = self._data[observation][regressor]
                if means[j] == 0.0:
                    means[j] = obs_val

                last_mean = means[j]
                last_variance = variances[j]

                means[j] = (last_mean + (obs_val - last_mean)/(i+1))
                variances[j] = last_variance + (obs_val - last_mean)*(obs_val - means[j])

        # TODO Sample or population (n-1 vs n, where n is i+1)?
        #      Although technically moot as we only care about 0 and the
        #      absolute difference would be relatively trivial for larger n
        variances /= i+1
        for i, variance in enumerate(variances):
            if variance == 0.0:
                print("[WARN] %s parameter has NIL variance (with mean %.2f)"
                        % (regressors[i], means[i]))

    def __len__(self):
        return len(self._data)

    def list_regressors(self):
        #TODO Need better method of getting all parameters than
        #     breaking out of counting the first observation...
        regressors = []
        for observation in sorted(self._data):
            for r in self._data[observation]:
                if r not in regressors:
                    regressors.append(r)
            break
        return sorted(regressors)

    def find_regressors(self, queries):
        regressors = []
        for observation in sorted(self._data):
            for r in self._data[observation]:
                for query in queries:
                    if query in r:
                        if r not in regressors:
                            regressors.append(r)
                            continue
            break
        return sorted(regressors)

    def exclude_regressors(self, queries, exact=False):
        regressors = self.list_regressors()
        to_remove = []
        for query in queries:
            for i, r in enumerate(regressors):
                if exact:
                    if query.lower() == r.lower():
                        to_remove.append(r)
                else:
                    if query.lower() in r.lower():
                        to_remove.append(r)

        for key in to_remove:
            regressors.remove(key)
        return sorted(regressors)

    def get_data_by_regressors(self, names):
        np_array = np.empty([len(self),len(names)])
        for i, observation in enumerate(sorted(self._data)):
            observation_n = np.zeros(len(names))
            for j, regressor in enumerate(names):
                observation_n[j] = self._data[observation][regressor]
            np_array[i] = observation_n
        return np_array

    def get_data_by_target(self, names, targets):

        total = 0
        for _id in self._targets:
            target = self._targets[_id]
            if targets:
                if target in targets:
                    total += 1
            else:
                total += 1

        data_np_array = np.empty([total,len(names)])
        targ_np_array = np.empty([total])

        counter = 0
        levels = []
        for observation in sorted(self._data):
            _id = observation.split(".")[0]
            target = self._targets[_id]
            if targets:
                if target not in targets:
                    continue

            observation_n = np.zeros(len(names))
            for j, regressor in enumerate(names):
                observation_n[j] = self._data[observation][regressor]
            data_np_array[counter] = observation_n
            targ_np_array[counter] = self._targets[_id]
            if self._targets[_id] not in levels:
                levels.append(self._targets[_id])
            counter += 1

        return data_np_array, targ_np_array, sorted(levels)

    def get_targets(self):
        np_array = np.empty([len(self)])
        for i, observation in enumerate(sorted(self._data)):
            _id = observation.split(".")[0]
            np_array[i] = self._targets[_id]
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

        o = open(log_filename, 'a')
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
