import numpy as np

files = [
    #"cd.ichip.vcf.gz.q",
    #"uc.ichip.vcf.gz.q",
    "cd-seq.vcf.gz.q",
    "uc-seq.vcf.gz.q"
]

LENGTH = 1000000
STRIDE = 500000

chr_max_len = {}

snps_by_chrom = {}
for i, f in enumerate(files):
    print "[READ] %s [%d of %d]" % (f, i+1, len(files))
    f = open(f)
    for line in f:
        fields = line.strip().split("\t")

        chrno, pos = fields[0].split(":")
        chrno = int(chrno) # NOTE Explodes for allosomes
        pos = int(pos) + 1 # NOTE Positions are 1-indexed

        if chrno not in snps_by_chrom:
            snps_by_chrom[chrno] = []
            chr_max_len[chrno] = 1
        snps_by_chrom[chrno].append(pos) # NOTE No duplicate checking

        if pos > chr_max_len[chrno]:
            chr_max_len[chrno] = pos
    f.close()

regions = {}
region_variant_counts = []
region_variant_buckets = {}

region_i = 0
for chrno, size in sorted(chr_max_len.items()):
    chro = np.zeros(size+1, np.int8)

    # Populate the chromosome array with 1 for each position a variant exists
    for variant_loc in snps_by_chrom[chrno]:
        chro[variant_loc] = 1

    print "[SRCH] Chr:%d" % (chrno)
    for region_s in range(1, len(chro)-LENGTH, STRIDE):
        regions[region_i] = {
            "count": 0,
            "chr": chrno,
            "pos_start": region_s,
            "pos_end": region_s+LENGTH
        }
        num_region_variants = np.sum(chro[region_s:region_s+LENGTH])
        regions[region_i]["count"] = num_region_variants

        # Record this region (if it contained variants)
        if num_region_variants > 0:
            if num_region_variants not in region_variant_buckets:
                region_variant_buckets[num_region_variants] = []
            region_variant_buckets[num_region_variants].append(region_i)
            region_variant_counts.append(num_region_variants)
        region_i += 1

median = np.median(np.asarray(region_variant_counts))

candidates = []

if median in region_variant_buckets:
    candidates = region_variant_buckets[median]

TRY_SIZE = 10
for i in range(1, TRY_SIZE):
    if median + i in region_variant_buckets:
        candidates += region_variant_buckets[median + i]
        flag = 1
    if median - i in region_variant_buckets:
        candidates += region_variant_buckets[median - i]
        flag = 1

    if flag:
        break

print "WND\tMED\tCHR\tPOS (S-E)"
for candidate in candidates:
    print "%d\t%d\t%s\t%10d - %10d" % (candidate,
                                       regions[candidate]["count"],
                                       regions[candidate]["chr"],
                                       regions[candidate]["pos_start"],
                                       regions[candidate]["pos_end"],
    )
