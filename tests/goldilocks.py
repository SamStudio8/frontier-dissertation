from Goldilocks.goldilocks import Goldilocks
import numpy as np
import unittest

DATA_PATH_FILE = "tests/data/goldilocks/paths.g"

LENGTH = 10
STRIDE = 5

NUM_TEST_CHRO = 2

LARGEST_POS = {
        1: 50,
        2: 100,
}

# TODO Could randomly generate these files with random positions and
#      alleles below the LARGEST_POS for each chromosome
TEST_DATA = {
    "group0_1": {
        1: [
            [1, 'G', 'A'],
            [LARGEST_POS[1], 'G', 'A'],
        ],
        2: [
        ],
    },
    "group0_2": {
        1: [
            [10, 'G', 'A'],
            [25, 'G', 'A'],
        ],
        2: [
            [5, 'G', 'A'],
        ],
    },
    "group1_1": {
        1: [
            [10, 'G', 'A'],
        ],
        2: [
            [7, 'G', 'A'],
            [LARGEST_POS[2], 'G', 'A'],
        ],
    },
}


class TestGoldilocks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Init Goldilocks
        g = Goldilocks(DATA_PATH_FILE, LENGTH, STRIDE)

        # Write test data to files for input
        groups = {}
        dups = {}
        for td in TEST_DATA:
            tdh = open("tests/data/goldilocks/"+td+".q", "w")
            grp = "test" + td[5]
            for chro in TEST_DATA[td]:
                if grp not in groups:
                    groups[grp] = {}
                    dups[grp] = {}
                if chro not in groups[grp]:
                    groups[grp][chro] = []
                    dups[grp][chro] = 0

                for entry in TEST_DATA[td][chro]:
                    pos = int(entry[0])
                    if pos in groups[grp][chro]:
                        dups[grp][chro] += 1
                    groups[grp][chro].append(pos)

                    tdh.write("%d:%d\t%c\t%c\n" % (chro, pos, entry[1], entry[2]))
            tdh.close()

        # Load variants
        for i, f in enumerate(g.files):
            g.load_variants_from_file(g.files[f]["path"], g.files[f]["group"])
        g.regions = g.search_regions()

        cls.g = g
        cls.groups = groups
        cls.dups = dups

    def test_files_loaded(self):
        paths_file = open(DATA_PATH_FILE)
        num_files = 0
        num_groups = 0
        for line in paths_file:
            if line.startswith("#"):
                num_groups += 1
            elif len(line.strip()) > 0:
                num_files += 1
        paths_file.close()

        self.assertEquals(num_files, len(self.g.files))
        self.assertEquals(num_groups, len(self.g.groups))

    def test_files_grouped(self):
        for fname, fobj in self.g.files.items():
            # Expected group is group number prefixed by "test" (for testing)
            expected_group = "test" + fname[5]
            self.assertEquals(expected_group, fobj["group"])

    def test_largest_variant_position(self):
        for i in range(1, NUM_TEST_CHRO+1):
            self.assertEquals(LARGEST_POS[i], self.g.chr_max_len[i])

    def test_number_seen_variants(self):
        # Check whether the total number of seen variants across all files in a
        # group (including duplicates) have been seen
        for grp in self.g.groups:
            for i in range(1, NUM_TEST_CHRO+1):
                self.assertEquals(len(self.groups[grp][i]), len(self.g.groups[grp][i]))

    def test_size_loaded_chro(self):
        # Technically don't need to iterate the groups here as the size is
        # constant for all (to allow cross-comparison of region_i)
        for grp in self.g.groups:
            for i in range(1, NUM_TEST_CHRO+1):
                # Length should be LARGEST_POS + 1 to account for the unused 0 index
                self.assertEquals(LARGEST_POS[i]+1,
                        len(self.g.load_chromosome(self.g.chr_max_len[i], self.g.groups[grp][i])))

    def test_number_loaded_variants(self):
        # Check that all variants in a group are loaded in to the chromosome
        # numpy array (excluding duplicates)
        for grp in self.g.groups:
            for i in range(1, NUM_TEST_CHRO+1):
                self.assertEquals(len(self.groups[grp][i]) - self.dups[grp][i],
                        sum(self.g.load_chromosome(self.g.chr_max_len[i], self.g.groups[grp][i])))

    def test_location_loaded_variants(self):
        # Check that all variants in a group are loaded in to the chromosome
        # numpy array are actually in the correct position
        for grp in self.g.groups:
            for i in range(1, NUM_TEST_CHRO+1):
                for pos in self.groups[grp][i]:
                    self.assertEquals(1,
                            self.g.load_chromosome(self.g.chr_max_len[i], self.g.groups[grp][i])[pos])

    def test_region_lengths(self):
        # Ensure ALL meet LENGTH
        for region_i, region_data in self.g.regions.items():
            self.assertEquals(LENGTH, len(range(region_data["pos_start"], region_data["pos_end"])) + 1)

    def test_region_stride(self):
        # Ensure regions begin at right STRIDE
        for region_i, region_data in self.g.regions.items():
            expected_start = 1 + (region_data["ichr"] * STRIDE)
            self.assertEquals(expected_start, region_data["pos_start"])

            # -1 as the region includes the start element
            expected_end = (expected_start - 1) + LENGTH
            self.assertEquals(expected_end, region_data["pos_end"])



################################################################################
# NOTE Following tests are hard coded to avoid having to write a test suite    #
#      for the tests themselves, this does need some work but will do for now  #
################################################################################
# CHR 1                                                            Expected
#               6   10    16       25                                Size
#       1 |*========*==============*========================*| 50
#          |        |                                                 2
#               |        |                                            1
#                    |        |                                       0
#                         |        |                                  1
#                              |        |                             1
#                                   |        |                        0
#                                        |        |                   0
#                                             |        |              0
#                                                  |        |         1
#                                                       |        |    x
#
################################################################################

    def test_number_group_regions(self):
        chr_counts = {}
        for region_i, region_data in self.g.regions.items():
            if region_data["chr"] not in chr_counts:
                chr_counts[region_data["chr"]] = 0
            chr_counts[region_data["chr"]] += 1

        # (ChroLength + 1) - (RegionLength - 1)
        #             +1 accounts for ignoring 0th element
        #                                   -1 allows including of last region
        self.assertEquals(len(range(1, (self.g.chr_max_len[1]+1) - (LENGTH-1), STRIDE)), chr_counts[1])

    # TODO Hard coded for now as otherwise we'll end up needing to test the tests...
    def test_content_group_regions(self):
        GROUP0_CHR1_EXPECTED_CONTENT = {
                1: 2,
                6: 1,
                11: 0,
                16: 1,
                21: 1,
                26: 0,
                31: 0,
                36: 0,
                41: 1
        }
        for region_i, region_data in self.g.regions.items():
            if region_data["chr"] == 1:
                self.assertEquals(GROUP0_CHR1_EXPECTED_CONTENT[region_data["pos_start"]],
                        region_data["group_counts"]["test0"])


    #TODO
    def test_content_group_bucket(self):
        pass

    #TODO
    def test_content_group_counter(self):
        pass

    #TODO
    def test_initial_filter(self):
        pass

    #TODO
    def test_enrichment(self):
        pass


if __name__ == '__main__':
    unittest.main()
