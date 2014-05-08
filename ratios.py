__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.0.9"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

import os
from Frontier.IO import bamcheckreader as bcr

_data = {}
for root, subfolders, files in os.walk("/pools/encrypted/sanger/frontier/data/bamcheck_2013dec25"):
    print root + "(" + str(len(files)) + " files)"
    for bam in files:
        bampath = os.path.join(root, bam)
        print bampath
        _data[bam] = bcr.BamcheckReader(bampath, auto_close=False)

        duplicate_mapped_ratio = 100.00 * ((float(_data[bam].summary["reads-duplicated"])) / _data[bam].summary["reads-mapped"])

        max_total_mean_baseline_deviation = max(_data[bam].summary["A-percent-total-mean-baseline-deviation"],
                                                _data[bam].summary["C-percent-total-mean-baseline-deviation"],
                                                _data[bam].summary["T-percent-total-mean-baseline-deviation"],
                                                _data[bam].summary["G-percent-total-mean-baseline-deviation"])

        max_max_baseline_deviation = max(_data[bam].summary["A-percent-max-baseline-deviation"],
                                         _data[bam].summary["C-percent-max-baseline-deviation"],
                                         _data[bam].summary["T-percent-max-baseline-deviation"],
                                         _data[bam].summary["G-percent-max-baseline-deviation"])

        ins_to_del_ratio = _data[bam].indel.total_inserts() / _data[bam].indel.total_deletes()

        out = open("/pools/encrypted/sanger/frontier/data/bamcheck_2013dec25_ratios_out/" + bam, "w")

        new_written = False
        for line in _data[bam]:
            if line.startswith("SN") and new_written is False:
                # Write new data...
                out.write("SN\tduplicate_mapped_ratio:\t%f\n" % duplicate_mapped_ratio)
                out.write("SN\tmax_total_mean_baseline_deviation:\t%f\n" % max_total_mean_baseline_deviation)
                out.write("SN\tmax_max_baseline_deviation:\t%f\n" % max_max_baseline_deviation)
                out.write("SN\tindel-ratio:\t%f\n" % ins_to_del_ratio)
                new_written = True
            out.write(line)

        _data[bam].close()
        _data[bam] = None
        out.close()

