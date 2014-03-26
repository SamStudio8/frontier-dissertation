library(ggplot2)
library(scales)

d = read.table(file="megabase_regions",
               sep="\t",
               comment.char="",
               na.strings="NA",
               header=T
)

type_labeller <- function(variable,value){
    value[value==0] <- "GWAS"
    value[value==1] <- "iCHIP"
    return(value)
}

p <- ggplot(d, aes(x = Region, y = NumVariants, colour=factor(Chromosome)))
p <- p + geom_point()
p <- p + facet_grid(~ Type, labeller=type_labeller)
p <- p + guides(col = guide_legend(title="Chr#"))
p <- p + xlab("Megabase Region") + ylab("Number of Variants")
#p <- p + scale_y_continuous(limits = c(0, 2000), oob=squish)

ggsave(plot=p,
       filename="megabase_plot.pdf",
       width=297,
       height=210,
       unit="mm")
ggsave(plot=p,
       filename="megabase_plot.png",
       width=297,
       height=210,
       unit="mm")
