from Frontier import frontier as f
import unittest

CLASSES = {
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

class TestFrontierUtils(unittest.TestCase):

    def test_classify_label(self):
        for class_name in CLASSES:
            for name in CLASSES[class_name]["names"]:
                self.assertEquals(class_name, f.classify_label(CLASSES, name))

    def test_classify_unknown_label(self):
        self.assertRaises(Exception, f.classify_label, CLASSES, "hoot")

    def test_encode_class(self):
        for class_name in CLASSES:
            self.assertEquals(CLASSES[class_name]["code"], f.encode_class(CLASSES, class_name))

    def test_encode_unknown_class(self):
        self.assertRaises(Exception, f.encode_class, CLASSES, "hoot")

    def test_encode_class_no_code(self):
        NO_CODE_CLASSES = {
            "pass": {
                "class": ["pass"],
                "names": ["pass", "passed"],
            },
        }
        self.assertRaises(Exception, f.encode_class, NO_CODE_CLASSES, "pass")

    def test_decode_class(self):
        for class_name in CLASSES:
            self.assertEqual(class_name, f.decode_class(CLASSES, CLASSES[class_name]["code"]))

    def test_decode_unknown_class(self):
        self.assertRaises(Exception, f.decode_class, CLASSES, 5)

    #TODO
    def test_decode_recoded_class(self):
        pass

    def test_count_class(self):
        CLASSES_COPY = CLASSES.copy()
        COUNT_LIST = [ "pass", "pass", "fail", "fail", "pass", "warn", "warn", "pass", "fail", "warn" ]
        EXPECT_COUNT = { "pass": 4, "fail": 3, "warn": 3 }
        for class_name in COUNT_LIST:
            f.count_class(CLASSES_COPY, class_name)
        for class_name in CLASSES_COPY:
            self.assertEquals(EXPECT_COUNT[class_name], CLASSES_COPY[class_name]["count"])

    def test_count_unknown_class(self):
        self.assertRaises(Exception, f.count_class, CLASSES, "hoot")


TEST_PARAMETERS = [
    "hoothoot"
]

class TestFrontier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialising the Statplexer in this way seems both terrible and trivial,
        # but the individual readers are seperately tested so it seems unnecessary
        # to test the data and targets are correctly read in.
        cls.plex = f.Statplexer(None, None, CLASSES, None, None)
        for i in range(0, 11):
            sample_name = "Frontier%d" % i
            cls.plex._data[sample_name] = {}
            for tp in TEST_PARAMETERS:
                cls.plex._data[sample_name][tp] = 1
            cls.plex._targets[sample_name] = 1

    def test_list_regressors(self):
        parameters = self.plex.list_regressors()
        self.assertEquals(len(TEST_PARAMETERS), len(parameters))

        for p in parameters:
            self.assertIn(p, TEST_PARAMETERS)

    def test_find_regressors(self):
        pass

    def test_exclude_regressors(self):
        pass

    def test_get_regressors(self):
        pass

    def test_get_data_by_target(self):
        pass

    def test_get_targets(self):
        pass

    def test_count_targets_by_class(self):
        pass



if __name__ == '__main__':
    unittest.main()
