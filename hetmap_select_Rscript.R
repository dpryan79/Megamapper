#############################################
# Homozygosity Mapper v1.0
# by Nikolaus Obholzer, 2011
# License: GPL
############################################# R --min-vsize=10M --max-vsize=8G --min-nsize=10M --max-nsize=8G
############################################# 
##########################################################################################################################################
##########################################################################################################################################
#
#
# Calculates hom vs het SNP densities from total SNPs with 4 columns for ALL SNPs on ALL chromosomes: "Chr","Pos","AlleleFreq", and "Coverage".
# The format of the input file is tab-delimited text as downloaded from Galaxy. Any column labels/ headers will be ignored.
#
#
##########################################################################################################################################
##########################################################################################################################################
#
# Modified by Sarah Diehl to just plot an overview of the het SNP densities of two different datasets.
#
#
#setwd("~/processing/guerri/HMFseq_mod")
#args = c("/data/processing/diehl/guerri/HMFseq_mod/Coverage_Extractor_on_HI020.tsv",
#         "het",
#         "/data/processing/diehl/guerri/HMFseq_mod/Coverage_Extractor_on_WT_Tu.tsv",
#         "hom",
#         "/data/processing/diehl/guerri/HMFseq_mod/out_overview.png",
#         "HI020 vs. WT Tu")
options(bitmapType='cairo')
args <- commandArgs(TRUE)

cat("MegaMapper initialized.\n")
##############################################
##############################################
# Define general variables
# SNP data file path 

snpfilepath_wt <- args[3]
snpfilepath = args[1]
select_wt = args[4]
select_mut = args[2]

# Read in SNPs from txt file  
snps0 <- read.table(file = snpfilepath, header = FALSE, comment.char ="#", sep="\t") # read in SNP file
colnames(snps0) <- c("Chr","Pos","AlleleFreq","Coverage")	#annotate table

if (select_mut == "het"){
  snps0 = subset(snps0, snps0$AlleleFreq < 0.9)
} else if (select_mut == "hom") {
  snps0 = subset(snps0, snps0$AlleleFreq > 0.9)
} else {}

snps_wt <- read.table(file = snpfilepath_wt, header = FALSE, comment.char ="#", sep="\t") # read in SNP file
colnames(snps_wt) <- c("Chr","Pos","AlleleFreq","Coverage")  #annotate table

if (select_wt == "het"){
  snps_wt = subset(snps_wt, snps_wt$AlleleFreq < 0.9)
} else if (select_wt == "hom") {
  snps_wt = subset(snps_wt, snps_wt$AlleleFreq > 0.9)
} else {}

counter = nrow(snps0) #determine number of entries(rows) in table
counter_wt = nrow(snps_wt)

Mname <- "YOUR_SAMPLE_NAME_HERE"
Mname <- args[6] #"test" # name of mutant to be analyzed

#print(paste(counter," unique SNPs.")) # for debugging
#################################################################################################################
# Zv9.60 genome parameters: Chromosome lenghts
#
mutChrom <- c(1:25)	# prepare vector for comparing homozygosity between chromosomes
mutChrom2 <- c(1:25)	# prepare vector for comparing max hom/het ratio between chromosomes
chrLengths <- c(1:25)	# a bit tedious but Notepad otherwise creates linebreaks that cause errors in R when text is cut/pasted
chrLengths[1:10] = c(60348388,60300536,63268876,62094675,75682077,59938731,77276063,56184765,58232459,46591166)
chrLengths[11:20] = c(46661319,50697278,54093808,53733891,47442429,58780683,53984731,49877488,50254551,55952140)
chrLengths[21:25] = c(44544065,42261000,46386876,43947580,38499472) # chromosome 1-25 lengths of Zv9

#################################################################################################################
#################################################################################################################
#1## Part1: Plot SNPs by zygosity for each chromosome and pick mutant chromosome (highest degree of homozygosity)
Nbreaks2 <- 300 # number of bins for all following histograms
png(args[5], width = 600, height = 800, bg = "white") # prepare output file

par(oma=c(4,0.5,2,0.5), mar=c(2.5,2.5,0.5,2), mfrow = c(5,5)) # prepare graph panels
#########################
#scale the y-axis limit based on the max counts in the histograms of chromosome 1 *1.1
z <- subset(snps0, snps0$Chr == 1) 	# take  SNPs of single chromosome as subset of all
z_wt <- subset(snps_wt, snps_wt$Chr == 1)
# prepare sequence of bins for current chromosome to ensure equal binning for all plots
p0 <- hist (z$Pos, breaks = Nbreaks2, plot = FALSE)  
# prepare sequence of bins for current chromosome
bins = p0$breaks
# generate and store het WT SNP density histogram data
p2 <- hist (z_wt$Pos, breaks = bins, plot = FALSE)
# generate and store het mutant SNP density histogram data
p1 <- hist (z$Pos, breaks = bins, plot = FALSE)

#Yscale <- max(max(p1$counts)/counter,max(p2$counts)/counter_wt)
#Yscale <- signif(Yscale*1.5, digits=2)
Yscale <- max(max(p1$counts),max(p2$counts))
#########################

# begin for loop to process all chromosomes
for (x in 1:25)	
{
y <- toString(x)	 		# prepare current chromosome name as string
z <- subset(snps0, snps0$Chr == y)   # take  SNPs of single chromosome as subset of all
z_wt <- subset(snps_wt, snps_wt$Chr == y)
# prepare sequence of bins for current chromosome to ensure equal binning for all plots
p0 <- hist (z$Pos, breaks = Nbreaks2, plot = FALSE)  
# prepare sequence of bins for current chromosome
bins = p0$breaks
# generate and store WT het SNP density histogram data
p2 <- hist (z_wt$Pos, breaks = bins, plot = FALSE)
# generate and store mutant het SNP density histogram data
p1 <- hist (z$Pos, breaks = bins, plot = FALSE)

# Normalize by total number of SNPs
p1$density = p1$counts#/counter
p2$density = p2$counts#/counter_wt

#plot y axis label only for first plot in a row
	if (x %in% c(1,6,11,16,21)) 
	{ 
	# plot homozygous SNP histogram for current chromosome WITH y-axis label
	plot( p2, main = "", col = "limegreen", xlab = paste("Chr", y," Position", sep=""), ylab ="SNP frequency", 
ylim = c(0, Yscale), border = "limegreen", cex.axis=0.75, mgp=c(1.3,0.3,0), freq=FALSE) 
	} else {
	# plot homozygous SNP histogram for current chromosome WITHOUT y-axis label
        plot(p2, main = "", col = "limegreen", xlab = paste("Chr", y," Position", sep=""), ylab ="", 
ylim = c(0, Yscale), border = "limegreen", cex.axis=0.75, mgp=c(1.3,0.3,0), freq=FALSE) 
	}

# plot  heterozygous SNP histogram for current chromosome
plot( p1, main = "", col = rgb(0,0,0), border = rgb(0,0,0), freq=FALSE, add=T) 

} # end for loop, all chromosomes processed

#########################################################
# annotate figure
#
title(paste(Mname, " SNP Density and Homo-/Heterozygosity Map", sep=""), cex=4, outer = TRUE) 	# plot title and text
if (select_mut == "het"){
  mtext(paste("- mutant heterozygous SNP frequency"), side=1, line=0.5, adj=0, cex=0.75, col="black", outer=TRUE)
} else if (select_mut == "hom") {
  mtext(paste("- mutant homozygous SNP frequency"), side=1, line=0.5, adj=0, cex=0.75, col="black", outer=TRUE)
} else {
  mtext(paste("- mutant SNP frequency"), side=1, line=0.5, adj=0, cex=0.75, col="black", outer=TRUE)
}
if (select_wt == "het") {
  mtext(paste("- WT heterozygous SNP frequency"), side=1, line=1.5, adj=0, cex=0.75, col="limegreen", outer=TRUE)
} else if (select_wt == "hom") {
  mtext(paste("- WT homozygous SNP frequency"), side=1, line=1.5, adj=0, cex=0.75, col="limegreen", outer=TRUE)
} else {
  mtext(paste("- WT SNP frequency"), side=1, line=1.5, adj=0, cex=0.75, col="limegreen", outer=TRUE)
}

dev.off() # turn off graphics engine, save plot file to disk
print (paste(counter, "SNPs were analyzed."))


print ("Megamapping complete.")

##############################################
#############################################
quit(save = "no")


