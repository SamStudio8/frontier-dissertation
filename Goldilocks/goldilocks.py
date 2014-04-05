import numpy as np
from math import floor, ceil

class Goldilocks(object):

    def __init__(self):
        self.files = {}         # Files to read variants from (path and group)

        self.chr_max_len = {}   # Map chromosomes to the largest variant position
                                # seen across all files

        self.groups = {}        # For each group stores a dict with chromosome
                                # numbers as keys with lists of variant positions
                                # as values

        self.group_buckets = {} # For each group holds keys of region sizes with
                                # values a list of region_i of that size

        self.group_counts = {}  # Holds a list of each region size seen for each
                                # group for calculating quantiles etc.

        self.regions = {}       # Stores information on each region checked

        self.candidates = []    # Lists regions that meet the criteria for final
                                # enrichment and processing

        self.LENGTH = 1000000
        self.STRIDE = 500000 # NOTE STRIDE must be non-zero, 1 is a bad idea (TM)
        self.MED_WINDOW = 12.5 # Middle 25%
        self.GRAPHING = False


    def load_variant_files(self, paths="paths.g"):
        path_list = open(paths)
        files = {}
        current_group = None
        for line in path_list:
            if line.startswith("#"):
                current_group = line[1:].strip()
                self.groups[current_group] = {}
                self.group_buckets[current_group] = {}
                self.group_counts[current_group] = []
                continue
            if current_group is not None:
                fields = line.split("\t")
                self.files[fields[0]] = {
                    "path": fields[1].strip(),
                    "group": current_group
                }
        path_list.close()

    def load_variants_from_file(self, path, group):

        f = open(path)
        for line in f:
            fields = line.strip().split("\t")

            chrno, pos = fields[0].split(":")
            chrno = int(chrno) # NOTE Explodes for allosomes
            pos = int(pos) + 1 # NOTE Positions are 1-indexed

            # Check group exists
            if group not in self.groups:
                raise Exception()
            if chrno not in self.groups[group]:
                self.groups[group][chrno] = []

                if chrno not in self.chr_max_len:
                    self.chr_max_len[chrno] = 1

            # NOTE No duplicate checking to prevent list lookups
            self.groups[group][chrno].append(pos)

            # Check whether this is the highest variant position seen on this chr
            if pos > self.chr_max_len[chrno]:
                self.chr_max_len[chrno] = pos

        f.close()

    def load_chromosome(self, size, locations):
        chro = np.zeros(size+1, np.int8)

        # Populate the chromosome array with 1 for each position a variant exists
        for variant_loc in locations:
            chro[variant_loc] = 1

        return chro

    def search_regions(self):
        regions = {}
        region_i = 0
        for chrno, size in sorted(self.chr_max_len.items()):
            if chrno == 6:
                # Avoid human leukocyte antigen loci
                continue

            chros = {}
            for group in self.groups:
                chros[group] = self.load_chromosome(size, self.groups[group][chrno])

            print "[SRCH] Chr:%d" % (chrno)
            for i, region_s in enumerate(range(1, size+1-self.LENGTH, self.STRIDE)):
                region_e = region_s + self.LENGTH - 1
                regions[region_i] = {
                    "group_counts": {},
                    "chr": chrno,
                    "pos_start": region_s,
                    "pos_end": region_e
                }

                for group in self.groups:
                    num_variants = np.sum(chros[group][region_s:region_e+1])
                    regions[region_i]["group_counts"][group] = num_variants

                    # Record this region (if it contained variants in this group)
                    if num_variants > 0:
                        if num_variants not in self.group_buckets[group]:
                            # Add this particular number of variants as a bucket
                            self.group_buckets[group][num_variants] = []

                        # Add the region id to the bucket
                        self.group_buckets[group][num_variants].append(region_i)

                        # Append the number of variants counted in this region
                        # for this group to a list used to calculate the median
                        self.group_counts[group].append(num_variants)

                    if self.GRAPHING:
                        # NOTE Use i not region_i so regions in the plot start
                        # at 0 for each chromosome rather than cascading
                        print "%s\t%d\t%d\t%d" % (group, chrno, i, num_variants)

                region_i += 1
        return regions

    # TODO Hard coded GWAS group
    def initial_filter(self, group="gwas"):
        candidates = []

        # Select middle 25% of GWAS group
        q_low  = np.percentile(np.asarray(self.group_counts[group]), 50 - self.MED_WINDOW)
        q_high = np.percentile(np.asarray(self.group_counts[group]), 50 + self.MED_WINDOW)

        # For each "number of variants" bucket, mapping the number of variants
        # seen in a region, to all regions that contained that number of variants
        for bucket in self.group_buckets[group]:
            if bucket > floor(q_low) and bucket < ceil(q_high):
                candidates += self.group_buckets[group][bucket]
        return candidates

    # TODO Hard coded iCHIP group
    def enrich(self, filter_group="gwas", enrich_group="ichip"):

        print "WND\tGWAS\tiCHIP\tCHR\tPOSITIONS"
        q_median = np.percentile(np.asarray(self.group_counts[filter_group]), 50)
        for region in sorted(self.regions, key=lambda x: abs(self.regions[x]["group_counts"][filter_group] - q_median)):
            if region in self.candidates:
                if self.regions[region]["group_counts"][enrich_group] > self.regions[region]["group_counts"][filter_group]:
                    print "%d\t%d\t%d\t%s\t%10d - %10d" % (region,
                                                    self.regions[region]["group_counts"][filter_group],
                                                    self.regions[region]["group_counts"][enrich_group],
                                                    self.regions[region]["chr"],
                                                    self.regions[region]["pos_start"],
                                                    self.regions[region]["pos_end"],
                    )

    def execute(self):
        self.load_variant_files()
        for i, f in enumerate(self.files):
            print "[READ] %s [%d of %d]" % (self.files[f]["path"], i+1, len(self.files))
            self.load_variants_from_file(self.files[f]["path"], self.files[f]["group"])

        self.regions = self.search_regions()
        self.candidates = self.initial_filter()
        self.candidates = self.enrich()

if __name__ == "__main__":
    Goldilocks().execute()
