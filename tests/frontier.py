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
                self.assertEqual(class_name, f.classify_label(CLASSES, name))

    def test_classify_unknown_label(self):
        self.assertRaises(Exception, f.classify_label, CLASSES, "hoot")

    def test_encode_class(self):
        for class_name in CLASSES:
            self.assertEqual(CLASSES[class_name]["code"], f.encode_class(CLASSES, class_name))

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
            self.assertEqual(EXPECT_COUNT[class_name], CLASSES_COPY[class_name]["_count"])

    def test_count_unknown_class(self):
        self.assertRaises(Exception, f.count_class, CLASSES, "hoot")


NUM_OBSERVATIONS = 10
TEST_PARAMETERS = [
    "hoothoot",
    "hoot",
    "owl-ratio",
    "wing-span",
    "wiseness-coefficient",
    "talon-sharpness",
    "talon-length",
    "bath-frequency",
    "cat-likeability",
    "number-of-doctorates",
]

TARGETS = [
    2, 2,
    1, 1,
    0, 0, 0,
    2, 2,
    3,
]

class TestFrontier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialising the Statplexer in this way seems both terrible and trivial,
        # but the individual readers are seperately tested so it seems unnecessary
        # to test the data and targets are correctly read in.
        cls.plex = f.Statplexer(None, None, CLASSES, None, None)
        for i in range(0, NUM_OBSERVATIONS):
            sample_name = "Frontier%d" % i
            cls.plex._data[sample_name] = {}
            for j, tp in enumerate(TEST_PARAMETERS):
                cls.plex._data[sample_name][tp] = i * j
            cls.plex._targets[sample_name] = TARGETS[i]

    def test_list_parameters(self):
        parameters = self.plex.list_parameters()
        self.assertEqual(len(TEST_PARAMETERS), len(parameters))

        for p in parameters:
            self.assertIn(p, TEST_PARAMETERS)

    def test_find_regressor(self):
        search_term = "hoot"
        parameters = self.plex.find_parameters([search_term])
        self.assertEqual(2, len(parameters))

        for p in parameters:
            self.assertIn(search_term, p)

        search_term = "hoothoot"
        parameters = self.plex.find_parameters([search_term])
        self.assertEqual(1, len(parameters))

        for p in parameters:
            self.assertIn(search_term, p)

        search_term = "wing-span"
        parameters = self.plex.find_parameters([search_term])
        self.assertEqual(1, len(parameters))

        for p in parameters:
            self.assertIn(search_term, p)

    def test_find_parameters(self):
        search_terms = ["wing-span", "hoot"]
        parameters = self.plex.find_parameters(search_terms)
        self.assertEqual(3, len(parameters))

        for p in parameters:
            self.assertTrue(search_terms[0] in p or search_terms[1] in p)

    def test_find_regressor_unknown(self):
        parameters = self.plex.find_parameters(["imgur-appearances"])
        self.assertEqual(0, len(parameters))

    def test_find_parameters_unknown(self):
        parameters = self.plex.find_parameters(["confirmed-kills", "height"])
        self.assertEqual(0, len(parameters))

        parameters = self.plex.find_parameters(["confirmed-kills", "height", "hoot"])
        self.assertEqual(2, len(parameters))
        for p in parameters:
            self.assertIn("hoot", p)

    def test_exclude_regressor(self):
        exclude_term = "hoot"
        parameters = self.plex.exclude_parameters([exclude_term])
        self.assertEqual(8, len(parameters))

        for p in parameters:
            self.assertNotIn("hoot", p)

    def test_exclude_regressor_exact(self):
        exclude_term = "hoot"
        parameters = self.plex.exclude_parameters([exclude_term], exact=True)
        self.assertEqual(9, len(parameters))

        exclude_term = "owl-ratio"
        parameters = self.plex.exclude_parameters([exclude_term], exact=True)
        self.assertEqual(9, len(parameters))

        for p in parameters:
            self.assertNotIn("owl-ratio", p)

    def test_exclude_parameters(self):
        exclude_terms = ["wing-span", "hoot"]
        parameters = self.plex.exclude_parameters(exclude_terms)
        self.assertEqual(7, len(parameters))

        for p in parameters:
            self.assertFalse(exclude_terms[0] in p or exclude_terms[1] in p)

        exclude_terms = ["talon", "hoot"]
        parameters = self.plex.exclude_parameters(exclude_terms)
        self.assertEqual(6, len(parameters))

        for p in parameters:
            self.assertFalse(exclude_terms[0] in p or exclude_terms[1] in p)

    def test_exclude_parameters_exact(self):
        exclude_terms = ["wing-span", "hoot"]
        parameters = self.plex.exclude_parameters(exclude_terms, exact=True)
        self.assertEqual(8, len(parameters))

        exclude_terms = ["wiseness-coefficient", "talon-sharpness"]
        parameters = self.plex.exclude_parameters(exclude_terms, exact=True)
        self.assertEqual(8, len(parameters))

        for p in parameters:
            self.assertFalse(exclude_terms[0] in p or exclude_terms[1] in p)

    def test_number_get_targets(self):
        targets = self.plex.get_targets()
        self.assertEqual(len(targets), NUM_OBSERVATIONS)

    def test_content_get_targets(self):
        targets = self.plex.get_targets()

        for i, t in enumerate(targets):
            self.assertEqual(TARGETS[i], t)

    def test_number_get_data_by_parameters(self):
        search_terms = ["hoot", "talon-length"]
        data = self.plex.get_data_by_parameters(search_terms)

        self.assertEqual(NUM_OBSERVATIONS, data.shape[0])
        self.assertEqual(len(search_terms), data.shape[1])

    def test_get_data_by_parameters(self):
        search_terms = ["hoot", "talon-length"]
        data = self.plex.get_data_by_parameters(search_terms)

        self.assertEqual(NUM_OBSERVATIONS, data.shape[0])
        self.assertEqual(len(search_terms), data.shape[1])

        # Data was generated in __init __ as i*j for jth attribute of ith observation
        # Where j is the index of the parameter in the TEST_PARAMETER list
        for i, param_set in enumerate(data):
            for k, value in enumerate(param_set):
                j = TEST_PARAMETERS.index(search_terms[k])
                self.assertEqual(i*j, data[i,k])

    def test_get_data_by_regressor(self):
        search_terms = ["wiseness-coefficient"]
        data = self.plex.get_data_by_parameters(search_terms)

        self.assertEqual(NUM_OBSERVATIONS, data.shape[0])
        self.assertEqual(len(search_terms), data.shape[1])

        # Data was generated in __init __ as i*j for jth attribute of ith observation
        # Where j is the index of the parameter in the TEST_PARAMETER list
        for i, param_set in enumerate(data):
            for k, value in enumerate(param_set):
                j = TEST_PARAMETERS.index(search_terms[k])
                self.assertEqual(i*j, data[i,k])

    def test_get_data_by_unknown_parameters(self):
        search_terms = ["hoothoot", "hoot", "talon-length", "max-altitude"]
        self.assertRaises(KeyError, self.plex.get_data_by_parameters, search_terms)

    def test_get_data_by_unknown_regressor(self):
        search_terms = ["max-distance"]
        self.assertRaises(KeyError, self.plex.get_data_by_parameters, search_terms)

    def test_get_data_by_targets(self):
        search_terms = ["hoot", "hoothoot", "number-of-doctorates"]
        search_targets = [3, 2]
        data, target, levels = self.plex.get_data_by_target(search_terms, search_targets)

        # Data was generated in __init __ as i*j for jth attribute of ith observation
        # Where j is the index of the parameter in the TEST_PARAMETER list
        # Ignore ith row if the corresponding target is not in search_targets
        for i, param_set in enumerate(data):
            if TARGETS[i] not in search_targets:
                continue

            for k, value in enumerate(param_set):
                j = TEST_PARAMETERS.index(search_terms[k])
                self.assertEqual(i*j, data[i,k])

        # One data element must exist for each target
        self.assertEqual(len(data), len(target))

        expected_count = 0
        for t in TARGETS:
            if t in search_targets:
                expected_count += 1
        self.assertEqual(expected_count, len(target))

        # Target should only contain targets in search_targets
        for t in target:
            self.assertIn(t, search_targets)

        # Levels returns one entry for each coded group of targets returned
        self.assertEqual(len(search_targets), len(levels))
        self.assertEqual(sorted(search_targets), levels)

    #TODO Not urgent, only used as part of log output and correct
    #     behaviour observed by manual check
    def test_count_targets_by_class(self):
        pass


if __name__ == '__main__':
    unittest.main()
