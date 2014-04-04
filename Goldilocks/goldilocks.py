import numpy as np
from math import floor, ceil

files = {
    "cd-gwas": {
        "path": "../../vcf/cd-seq.vcf.gz.q",
        "group": 0
    },
    "uc-gwas": {
        "path": "../../vcf/uc-seq.vcf.gz.q",
        "group": 0
    },
    "cd-ichip": {
        "path": "../../vcf/cd.ichip.vcf.gz.q",
        "group": 1
    },
    "uc-ichip": {
        "path": "../../vcf/uc.ichip.vcf.gz.q",
        "group": 1
    },
}

LENGTH = 1000000
STRIDE = 500000 # NOTE STRIDE must be non-zero, 1 is a bad idea
MED_WINDOW = 12.5 # Middle 25%
GRAPHING = False

chr_max_len = {}
snps_by_chrom_gwas = {}
snps_by_chrom_ichip = {}
for i, f in enumerate(files):
    print "[READ] %s [%d of %d]" % (files[f]["path"], i+1, len(files))
    fh = open(files[f]["path"])
    for line in fh:
        fields = line.strip().split("\t")

        chrno, pos = fields[0].split(":")
        chrno = int(chrno) # NOTE Explodes for allosomes
        pos = int(pos) + 1 # NOTE Positions are 1-indexed

        if files[f]["group"] == 0:
            if chrno not in snps_by_chrom_gwas:
                snps_by_chrom_gwas[chrno] = []
            snps_by_chrom_gwas[chrno].append(pos) # NOTE No duplicate checking
        elif files[f]["group"] == 1:
            if chrno not in snps_by_chrom_ichip:
                snps_by_chrom_ichip[chrno] = []
            snps_by_chrom_ichip[chrno].append(pos) # NOTE No duplicate checking

        if chrno not in chr_max_len:
            chr_max_len[chrno] = 1

        if pos > chr_max_len[chrno]:
            chr_max_len[chrno] = pos
    fh.close()

regions = {}

gwas_region_variant_counts = []
gwas_region_variant_buckets = {}

region_i = 0
for chrno, size in sorted(chr_max_len.items()):
    if chrno == 6:
        # Avoid human leukocyte antigen loci
        continue

    chro_gwas = np.zeros(size+1, np.int8)
    chro_ichip = np.zeros(size+1, np.int8)

    # Populate the chromosome array with 1 for each position a variant exists
    for variant_loc in snps_by_chrom_gwas[chrno]:
        chro_gwas[variant_loc] = 1
    for variant_loc in snps_by_chrom_ichip[chrno]:
        chro_ichip[variant_loc] = 1

    print "[SRCH] Chr:%d" % (chrno)
    for i, region_s in enumerate(range(1, size+1-LENGTH, STRIDE)):
        region_e = region_s + LENGTH - 1
        regions[region_i] = {
            "ichip_count": 0,
            "gwas_count": 0,
            "chr": chrno,
            "pos_start": region_s,
            "pos_end": region_e
        }
        gwas_num_region_variants = np.sum(chro_gwas[region_s:region_e+1])
        regions[region_i]["gwas_count"] = gwas_num_region_variants

        ichip_num_region_variants = np.sum(chro_ichip[region_s:region_e+1])
        regions[region_i]["ichip_count"] = ichip_num_region_variants

        # Record this region (if it contained variants)
        if gwas_num_region_variants > 0:
            if gwas_num_region_variants not in gwas_region_variant_buckets:
                gwas_region_variant_buckets[gwas_num_region_variants] = []
            gwas_region_variant_buckets[gwas_num_region_variants].append(region_i)
            gwas_region_variant_counts.append(gwas_num_region_variants)

        if GRAPHING:
            if gwas_num_region_variants > 0:
                print "0\t%d\t%d\t%d" % (chrno, i, gwas_num_region_variants)
            if ichip_num_region_variants > 0:
                print "1\t%d\t%d\t%d" % (chrno, i, ichip_num_region_variants)
        region_i += 1

# Select middle 25%
q_low  = np.percentile(np.asarray(gwas_region_variant_counts), 50 - MED_WINDOW)
q_median = np.percentile(np.asarray(gwas_region_variant_counts), 50)
q_high = np.percentile(np.asarray(gwas_region_variant_counts), 50 + MED_WINDOW)

candidates = []
for bucket in gwas_region_variant_buckets:
    if bucket > floor(q_low) and bucket < ceil(q_high):
        candidates += gwas_region_variant_buckets[bucket]

print "WND\tGWAS\tiCHIP\tCHR\tPOSITIONS"
for region in sorted(regions, key=lambda x: abs(regions[x]["gwas_count"] - q_median)):
    if region in candidates:
        if regions[region]["ichip_count"] > regions[region]["gwas_count"]:
            print "%d\t%d\t%d\t%s\t%10d - %10d" % (region,
                                            regions[region]["gwas_count"],
                                            regions[region]["ichip_count"],
                                            regions[region]["chr"],
                                            regions[region]["pos_start"],
                                            regions[region]["pos_end"],
            )
