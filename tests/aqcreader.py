from Frontier.IO import AQCReader as aqcr
from Frontier.frontier import classify_label, encode_class

import unittest

# NOTE Actual AQC files contain currently unpublished quality control information,
#      test files contain dummy example data and a truncated variable list.
DATA_PATH = "tests/data/example.aqc.txt"
DATA_UNIQ_PATH = "tests/data/example.aqc.uniq.txt"

TEST_DATA = {
    "9999_9#1": {
        "sample": "AQCTest000000",
        "study": "AQCTest",
        "npg": "pass",
        "aqc": "passed",
    },
    "9999_9#2": {
        "sample": "AQCTest000001",
        "study": "AQCTest",
        "npg": "pass",
        "aqc": "pass",
    },
    "9999_9#3": {
        "sample": "AQCTest000002",
        "study": "AQCTest",
        "npg": "fail",
        "aqc": "failed",
    },
    "9999_9#4": {
        "sample": "AQCTest000003",
        "study": "AQCTest",
        "npg": "warn",
        "aqc": "warning",
    },
    "9999_9#5": {
        "sample": "AQCTest000004",
        "study": "AQCTest",
        "npg": "warn",
        "aqc": "warn",
    },
    "9999_9#6": {
        "sample": "AQCTest000005",
        "study": "AQCTest",
        "npg": "pass",
        "aqc": "passed",
    },
    "9999_9#7": {
        "sample": "AQCTest000006",
        "study": "AQCTest",
        "npg": "fail",
        "aqc": "fail",
    },
    "9999_9#8": {
        "sample": "AQCTest000007",
        "study": "AQCTest",
        "npg": "pass",
        "aqc": "passed",
    },
    "9999_9#9": {
        "sample": "AQCTest000008",
        "study": "AQCTest",
        "npg": "warn",
        "aqc": "warning",
    },
}

TEST_UNIQ_DATA = {
    "9998_9#1": {
        "sample": "AQCTest100000",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "pass",
    },
    "9998_9#2": {
        "sample": "AQCTest100001",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "pass",
    },
    "9998_9#3": {
        "sample": "AQCTest100002",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "pass",
    },
    "9998_9#4": {
        "sample": "AQCTest100003",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "warn",
    },
    "9998_9#5": {
        "sample": "AQCTest100004",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "pass",
    },
    "9998_9#6": {
        "sample": "AQCTest100005",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "fail",
    },
    "9998_9#7": {
        "sample": "AQCTest100006",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "pass",
    },
    "9998_9#8": {
        "sample": "AQCTest100007",
        "study": "AQCTest",
        "npg": "npq",
        "aqc": "pass",
    },
}

EXAMPLE_CLASSES = {
    "pass": {
        "class": ["pass"],
        "names": ["pass", "passed"],
        "code": 1,
    },
    "fail": {
        "class": ["fail"],
        "names": ["fail", "failed"],
        "code": -1,
    },
    "warn": {
        "class": ["warn"],
        "names": ["warn", "warning"],
        "code": 0,
    },
}

class TestAQCReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Write test data to files for input
        tdh = open(DATA_PATH, "w")
        tdh.write("lanelet\tsample\tstudy\tnpg\taqc\t...\n")
        for tdname, td in TEST_DATA.items():
            tdh.write("%s\t%s\t%s\t%s\t%s\t...\n" % (tdname, td["sample"], td["study"], td["npg"], td["aqc"]))
        tdh.close()
        tdh = open(DATA_UNIQ_PATH, "w")
        tdh.write("lanelet\tsample\tstudy\tnpg\taqc\t...\n")
        for tdname, td in TEST_UNIQ_DATA.items():
            tdh.write("%s\t%s\t%s\t%s\t%s\t...\n" % (tdname, td["sample"], td["study"], td["npg"], td["aqc"]))
        tdh.close()

    def test_size_targets(self):
        # Should be a target for each line of input (minus header)
        example_lines = open(DATA_PATH).readlines()
        targets = aqcr.AQCReader(DATA_PATH).get_targets()
        self.assertEqual(len(example_lines) - 1, len(targets))

    # Somewhat arbitrary...
    def test_line_content(self):
        aqc = aqcr.AQCReader(DATA_PATH, auto_close=False)
        targets = aqc.get_targets()

        for t in targets:
            self.assertEquals(TEST_DATA[t]["aqc"], targets[t])
        aqc.close()

    # Probably somewhat arbitrary also...
    def test_particular_line_content(self):
        aqc = aqcr.AQCReader(DATA_UNIQ_PATH)
        targets = aqc.get_targets()

        self.assertEquals(TEST_UNIQ_DATA["9998_9#4"]["aqc"], targets["9998_9#4"])
        self.assertEquals(TEST_UNIQ_DATA["9998_9#6"]["aqc"], targets["9998_9#6"])

    # Quick test for integration with Frontier label utils
    def test_coded_line_content(self):
        aqc = aqcr.AQCReader(DATA_PATH, EXAMPLE_CLASSES)
        targets = aqc.get_targets()

        for t in targets:
            expected_class = classify_label(EXAMPLE_CLASSES, TEST_DATA[t]["aqc"])
            expected_code = encode_class(EXAMPLE_CLASSES, expected_class)
            self.assertEquals(expected_code, targets[t])
        aqc.close()

if __name__ == '__main__':
    unittest.main()
