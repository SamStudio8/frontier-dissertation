__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.0.1"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

import argparse
import datetime
import numpy as np
import pydot
import os

from sklearn.cross_validation import cross_val_score, StratifiedKFold
from sklearn.externals.six import StringIO
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from Frontier import frontier
from Frontier.IO.BamcheckReader import BamcheckReader
from Frontier.IO.AQCReader import AQCReader

CLASSES = {
        "pass": {
            "names": ["pass", "passed"],
            "code": 1,
        },
        "fail": {
            "names": ["fail", "failed"],
            "code": -1,
        },
        "warn": {
            "names": ["warn", "warning"],
            "code": 0,
        },
}

PARAMETER_SETS = {
    "AQC": [
        "error-rate",
        "insert-size-average",
        "average-quality",

        "fwd-percent-insertions-above-baseline",
        "fwd-percent-insertions-below-baseline",
        "fwd-percent-deletions-above-baseline",
        "fwd-percent-deletions-below-baseline",
        "rev-percent-insertions-above-baseline",
        "rev-percent-insertions-below-baseline",
        "rev-percent-deletions-above-baseline",
        "rev-percent-deletions-below-baseline",

        "A-percent-max-baseline-deviation",
        "C-percent-max-baseline-deviation",
        "G-percent-max-baseline-deviation",
        "T-percent-max-baseline-deviation",
        "A-percent-total-mean-baseline-deviation",
        "C-percent-total-mean-baseline-deviation",
        "G-percent-total-mean-baseline-deviation",
        "T-percent-total-mean-baseline-deviation",
        "quality-dropoff-rev-high-iqr-max-contiguous-read-cycles",
        "quality-dropoff-fwd-high-iqr-max-contiguous-read-cycles",
        "quality-dropoff-fwd-mean-runmed-decline-max-contiguous-read-cycles",
        "quality-dropoff-rev-mean-runmed-decline-max-contiguous-read-cycles",

        "quality-dropoff-fwd-mean-runmed-decline-high-value",
        "quality-dropoff-rev-mean-runmed-decline-high-value",
        "quality-dropoff-fwd-mean-runmed-decline-low-value",
        "quality-dropoff-rev-mean-runmed-decline-low-value",
    ],
    "AQCN": [
        "error-rate",
        "insert-size-average",
        "average-quality",

        "fwd-percent-insertions-above-baseline",
        "fwd-percent-insertions-below-baseline",
        "fwd-percent-deletions-above-baseline",
        "fwd-percent-deletions-below-baseline",
        "rev-percent-insertions-above-baseline",
        "rev-percent-insertions-below-baseline",
        "rev-percent-deletions-above-baseline",
        "rev-percent-deletions-below-baseline",

        "max-max-baseline-deviation",
        "max-total-mean-baseline-deviation",
        "quality-dropoff-rev-high-iqr-max-contiguous-read-cycles",
        "quality-dropoff-fwd-high-iqr-max-contiguous-read-cycles",
        "quality-dropoff-fwd-mean-runmed-decline-max-contiguous-read-cycles",
        "quality-dropoff-rev-mean-runmed-decline-max-contiguous-read-cycles",

        "quality-dropoff-fwd-mean-runmed-decline-high-value",
        "quality-dropoff-rev-mean-runmed-decline-high-value",
        "quality-dropoff-fwd-mean-runmed-decline-low-value",
        "quality-dropoff-rev-mean-runmed-decline-low-value",
    ],
    "AQCN_MIN": [
        "error-rate",
        "fwd-percent-insertions-above-baseline",
        #"max-total-mean-baseline-deviation",
        #"max-max-baseline-deviation",
    ],
    "ERROR": [
        "error-rate"
    ],
    "NO_ERROR": {
        "exclude": ["error-rate"]
    },
    "BASELINE": {
        "find": ["baseline"],
    },
    "NOBASELINE": {
        "exclude": ["baseline"],
    },
    "MARP": {
        "find": ["mean", "percent", "rate", "average"],
    },
    "NO_MARP": {
        "exclude": ["mean", "percent", "rate", "average"],
    },
}

DATA_SETS = {
    "IGNWARN": {
        "codes": [1, -1],
    },
    "WARNPASS": {
        "codes": [1, -1],
        "recode": {
            "warn": 1
        }
    },
    "WARNFAIL": {
        "codes": [1, -1],
        "recode": {
            "warn": -1
        }
    },
}
class QC:
    def __init__(self, args):
        #TODO Naughtly global-like behaviour going on here...
        self.CLASSES = CLASSES
        self.PARAMETER_SETS = PARAMETER_SETS
        self.DATA_SETS = DATA_SETS

        self.data_dir = args.data_dir
        self.target_path = args.target_path

        self.data_set = args.data_set.upper()
        self.parameter_set = args.param_set.upper()

        self.no_log = args.no_log
        self.folds = args.folds

        # Handle invalid options
        if self.parameter_set not in self.PARAMETER_SETS and self.parameter_set != "ALL":
            raise Exception("%s is not a valid option for parameter_set" % self.parameter_set)
        if self.data_set not in self.DATA_SETS and self.data_set != "ALL":
            raise Exception("%s is not a valid option for data_set" % self.data_set)

        # Process data set
        # Use "ALL" classes unless otherwise told
        self.override_codes = None
        if self.data_set != "ALL":
            #TODO Warn when using ALL as codes and recode will be ignored
            if "codes" in self.DATA_SETS[self.data_set]:
                self.override_codes = self.DATA_SETS[self.data_set]["codes"]

            if "recode" in self.DATA_SETS[self.data_set]:
                for class_label, new_code in self.DATA_SETS[self.data_set]["recode"].items():
                    print("[NOTE] Class %s will be encoded as %d instead of %d" %
                            (class_label, new_code, self.CLASSES[class_label]["code"]))
                    #TODO Check this code is actually used?
                    self.CLASSES[class_label]["code"] = new_code
                    self.CLASSES[class_label]["_recode"] = True

        self.statplexer = frontier.Statplexer(
            self.data_dir,
            self.target_path,
            CLASSES,
            BamcheckReader,
            AQCReader)

        # Process parameter_set
        if self.parameter_set == "ALL":
            self.parameters = self.statplexer.list_parameters()
        elif "find" in self.PARAMETER_SETS[self.parameter_set]:
            self.parameters = self.statplexer.find_parameters(self.PARAMETER_SETS[self.parameter_set]["find"])
        elif "exclude" in self.PARAMETER_SETS[self.parameter_set]:
            self.parameters = self.statplexer.exclude_parameters(self.PARAMETER_SETS[self.parameter_set]["exclude"])
        else:
            #TODO Check this is a list, not a dict with incorrect keys
            self.parameters = self.PARAMETER_SETS[self.parameter_set]

        self.execute()

    def execute(self):
        data, target, levels = self.statplexer.get_data_by_target(self.parameters, self.override_codes)
        w_data, w_target, w_levels = self.statplexer.get_data_by_target(self.parameters, [CLASSES["warn"]["code"]])

        # Sanity
        if len(data) != len(target):
            print "[FAIL] Number of INPUTS does not match number of TARGETS!"
            sys.exit(0)

        # Init
        clf = DecisionTreeClassifier()
        kf = StratifiedKFold(target, n_folds=self.folds)

        importances = []
        scores = np.zeros(self.folds)

        count = 0
        if not self.no_log:
            pdf_path = "pdf/" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + "__" + self.data_set + "_" + self.parameter_set + "_" + "/"
            os.makedirs(pdf_path)

        confusion = np.zeros([len(levels), len(levels)])
        wconfusion = np.zeros([len(CLASSES), len(CLASSES)])
        for train_index, test_index in kf:
            X_train, X_test = data[train_index], data[test_index]
            y_train, y_test = target[train_index], target[test_index]
            clf.fit(X_train, y_train)

            # Score the fit
            score = clf.score(X_test, y_test)
            scores[count] = score
            count += 1

            # Calculate feature importance
            importance = clf.tree_.compute_feature_importances()
            importances.append(importance)

            # Compute confusion matrix
            y_pred = clf.predict(X_test)
            confusion += confusion_matrix(y_test, y_pred)

            # Compute warnings confusion matrix
            y_pred = clf.predict(w_data)
            wconfusion += confusion_matrix(w_target, y_pred)

            # Draw the graph
            if not self.no_log:
                dot_data = StringIO()
                export_graphviz(clf, out_file=dot_data)
                graph = pydot.graph_from_dot_data(dot_data.getvalue())
                pdf_filename = pdf_path + str(count) + ".pdf"
                graph.write_pdf(pdf_filename)

        #cv_scores = cross_val_score(clf, data, target, cv=kf)
        print(confusion/self.folds)
        print(wconfusion/self.folds)

        imps = {}
        for importance_run in importances:
            for i, entry in enumerate(importance_run):
                if self.parameters[i] not in imps:
                    imps[self.parameters[i]] = []
                imps[self.parameters[i]].append(entry)
        imp_means = {}
        for name, score_list in imps.items():
            imp_means[name] = sum(score_list)/len(score_list)
        importance = imp_means

        total_used = len(target)
        if not self.no_log:
            log_filename = "log/" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + "__" + self.data_set + "_" + self.parameter_set + "_" + str(int(scores.mean() * 100)) + ".txt"
            self.statplexer.write_log(log_filename, pdf_path, self.data_set, self.parameter_set, self.parameters, target, scores, self.folds, importance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', metavar='data_dir',
            help=("Path to directory containing bamcheckr outputs"))
    parser.add_argument('target_path', metavar='target_path',
            help=("Path to tabulated QC summary file"))
    parser.add_argument('-d', '--data_set', metavar='data_set', default="all",
            help=("Data set [all]"))
    parser.add_argument('-p', '--param_set', metavar='parameter_set', default="all",
            help=("Parameter set [all]"))
    parser.add_argument('-f', '--folds', metavar='folds', type=int, default=10,
            help=("Number of Cross Validation Folds [10]"))
    parser.add_argument('--no_log', action='store_true',
            help=("Do not output a log file"))
    QC(parser.parse_args())
