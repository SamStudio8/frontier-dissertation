library("reshape")
library("plyr")
library("pheatmap")
library("ggplot2")

table = read.table("/pools/encrypted/sanger/frontier/data/crohns-uc-table-a.2013dec25.manual_qc_update.txt", header=T, sep="\t", fill=T, comment.char = "")

levels(table$auto.qc.status) <- c(-1, 1, 0)

ll <- colsplit(table$lanelet, "[_|#]", c("nrun", "nlane", "nlanelet"))

table <- cbind(table, ll)

#ddply(table, c("run", "lane"), function(x) count=nrow(x))

# Index lanes in each run
indx <- unique(table[c("nrun", "nlane", "study")])
indx <- data.frame(indx, lanerun=1:nrow(indx))
table <- merge(table, indx)

# Index lanelets in each lane
laneruns <- c(sort(table$lanerun))
table$laneletrun <- unlist(sapply(rle(laneruns)$lengths, seq))

lanetab <- cast(table, laneletrun ~ lanerun, value='auto.qc.status')
lanetab <- melt(lanetab)
lanetab <- subset(lanetab, laneletrun < 11)

p <- ggplot(lanetab, aes(lanerun, laneletrun))
p <- p + geom_tile(aes(fill=factor(value)))
p <- p + scale_fill_manual(name="Auto QC",
                          labels=c("Pass", "Warn", "Fail"),
                          values=c("#cccccc", "#f0ad4e", "#d9534f"))
p <- p + theme(axis.ticks = element_blank(), axis.text.y = element_blank())
p <- p + xlab("Run-Lane #") + ylab("Lanelet")
