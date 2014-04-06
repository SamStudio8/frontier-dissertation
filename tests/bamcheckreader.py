from Frontier.IO import bamcheckreader as bcr
import unittest

DATA_PATH = "tests/data/example.bamcheck.txt"
DUP_DATA_PATH = "tests/data/example.bamcheck.dups.txt"
BAD_DUP_DATA_PATH = "tests/data/example.bamcheck.baddups.txt"

class TestBamcheckReader(unittest.TestCase):

    def test_tidy_key(self):
        # Test stripping of end colon, spaces and dots
        self.assertEqual("hoot", bcr.tidy_key("hoot:"))
        self.assertEqual("ho-ot", bcr.tidy_key("ho_ot:"))
        self.assertEqual("hoot-hoot", bcr.tidy_key("hoot hoot:"))
        self.assertEqual("hoot-hoot", bcr.tidy_key("hoot.hoot:"))
        self.assertEqual("hoot-hoot-hoot", bcr.tidy_key("hoot hoot.hoot:"))
        self.assertEqual("hoot-hoot-hoot-hoot", bcr.tidy_key("hoot_hoot hoot.hoot:"))

    def test_size_summary(self):
        # Summary dict should be the same size as number of SN lines
        example_lines = open(DATA_PATH).readlines()
        bamcheck = bcr.BamcheckReader(DATA_PATH)

        SN_count = 0
        for line in example_lines:
            if line.startswith("SN"):
                SN_count += 1
        self.assertEqual(SN_count, len(bamcheck.summary))

    def test_duplicate(self):
        example_lines = open(DUP_DATA_PATH).readlines()
        dup_bamcheck = bcr.BamcheckReader(DUP_DATA_PATH)

        SN_count = 0
        keys = []
        for line in example_lines:
            if line.startswith("SN"):
                key = bcr.tidy_key(line.split("\t")[1])
                if key not in keys:
                    keys.append(key)
                    SN_count += 1
        self.assertEqual(SN_count, len(dup_bamcheck.summary))

    def test_invalid_duplicate(self):
        self.assertRaises(Exception, bcr.BamcheckReader, BAD_DUP_DATA_PATH)

    def test_summary_equality(self):
        example_lines = open(DATA_PATH).readlines()
        bamcheck = bcr.BamcheckReader(DATA_PATH)

        # Trivial test?
        for line in example_lines:
            line = line.strip()
            if line.startswith("SN"):
                fields = line.split("\t")
                key = bcr.tidy_key(fields[1])
                value = fields[2]
                self.assertEquals(bamcheck.summary[key], float(value))

        # Some hard-coded tests to ensure coverage
        HARDCODE_TEST_VALUES = {
                "sequences": 41400090.0,
                "reads-mapped": 41291484.0,
                "total-length": 3105006750.0,
                "average-quality": 36.0,
                "fwd-percent-insertions-above-baseline": 1.43135383851191,
                "error-rate": 0.002946675,
                "A-percent-mean-above-baseline": 0.0991164444444441,
                "C-percent-max-baseline-deviation": 0.825733333333332,
                "G-percent-max-baseline-deviation": 0.554400000000001,
                "T-percent-total-mean-baseline-deviation": 0.1736
        }
        for key, value in HARDCODE_TEST_VALUES.items():
            self.assertEquals(bamcheck.summary[key], value)

if __name__ == '__main__':
    unittest.main()
