#############################################
# Bulk Segregant Mapper v1.0
# by Nikolaus Obholzer, 2012
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
#setwd("~/processing/guerri/BSAseq_mod")
#args = c("/data/processing/diehl/guerri/BSAseq_mod/Coverage_Extractor_JZ061.csv",
#         "/data/processing/diehl/guerri/BSAseq_mod/Coverage_Extractor_on_WT_Tu.csv",
#         "/data/processing/diehl/guerri/BSAseq_mod/Coverage_Extractor_on_WT_Wik_11.csv",
#         "/data/processing/diehl/guerri/BSAseq_mod/out_overview.png",
#         "JM087",
#         "9",
#         "mean")
options(bitmapType='cairo')
args <- commandArgs(TRUE)
cat("MegaMapper initialized.\n")
##############################################
##############################################
# Define general variables
# SNP data file path 
#
Mname <- args[5] # name of mutant to be analyzed
snpfilepath1 <- args[1]
snpfilepath2 <- args[2]
snpfilepath3 <- args[3]

min_AF = 0.2
max_AF = 1

# Read in SNPs from txt file	
#
cutoff = as.integer(toString(args[6]))
percentile = toString(args[7])

cat("Lower SNP coverage cutoff is: ", cutoff , "\n")
cat("Minimal Allele Frequqency is: ", min_AF , "\n")

if (percentile == "mean")
{
  cat("Calculate AF using: ", percentile, "\n")
} else
{
  cat("Calculate AF using: ", percentile , "th percentile\n")
  percentile = as.integer(toString(percentile))/100
}

# read in mutagenesis strain SNP file
snps0 <- read.table(file = snpfilepath1, header = FALSE, comment.char ="#", sep="\t") 
snps0 = snps0[snps0[,4] >= cutoff,] #4,] # filter out low coverage SNPs
snps0 = snps0[snps0[,3] >= min_AF,] #4,] # filter out low coverage SNPs

# read in mapping strain SNP file
snps1 <- read.table(file = snpfilepath2, header = FALSE, comment.char ="#", sep="\t") 
snps1 = snps1[snps1[,4] >= cutoff,] #4,] # filter out low coverage SNPs
snps1 = snps1[snps1[,3] >= min_AF,] #4,] # filter out low coverage SNPs

# read in 2nd mapping strain SNP file
snps2 <- read.table(file = snpfilepath3, header = FALSE, comment.char ="#", sep="\t") 
snps2 = snps2[snps2[,4] >= cutoff,] #4,] # filter out low coverage SNPs
snps2 = snps2[snps2[,3] >= min_AF,] #4,] # filter out low coverage SNPs

colnames(snps0) <- c("Chr","Pos","AlleleFreq","Coverage")	#annotate table
colnames(snps1) <- c("Chr","Pos","AlleleFreq","Coverage")	#annotate table
colnames(snps2) <- c("Chr","Pos","AlleleFreq","Coverage")  #annotate table
counter1 = nrow(snps0) #determine number of entries(rows) in table
counter2 = nrow(snps1) #determine number of entries(rows) in table
counter3 = nrow(snps2) #determine number of entries(rows) in table

# choose only such SNPs for mapping which have coverage in both libraries
#if (counter1 > counter2)
#{
	for (iii in 1:25)
	{
	snps0x = snps1[snps1$Chr == iii,]
	snps1 = snps1[!snps1$Chr == iii,]
	snps0y = snps0[snps0$Chr == iii,]
	snps1 = rbind(snps1, snps0x[snps0x$Pos %in% snps0y$Pos, ])
	snps0x = 0
	snps0y = 0
  gc()
	}
  for (iii in 1:25)
  {
  snps0x = snps2[snps2$Chr == iii,]
  snps2 = snps2[!snps2$Chr == iii,]
  snps0y = snps0[snps0$Chr == iii,]
  snps2 = rbind(snps2, snps0x[snps0x$Pos %in% snps0y$Pos, ])
  snps0x = 0
  snps0y = 0
  gc()
#	snps0 = rbind(snps0, snps0x[snps0x$Pos %in% snps1[snps1$Pos == iii,2]  ,])
	}
#}
# if (counter2 > counter1)
# {
# 	for (iii in 1:25)
# 	{
# 	snps0x = snps1[snps1$Chr == iii,]
# 	snps1 = snps1[!snps1$Chr == iii,]
# 	snps0y = snps0[snps0$Chr == iii,]
# 	snps1 = rbind(snps1, snps0x[snps0x$Pos %in% snps0y$Pos, ])
# 	snps0x = 0
# 	snps0y = 0
# 	}
# }

# print(paste(counter1,"mutant and ",counter2," mutagenesis strain SNPs")) # for debugging
#################################################################################################################
#################################################################################################################
#1## Part1: Plot SNPs by zygosity for each chromosome and pick mutant chromosome (highest degree of homozygosity)
#
Nbreaks2 <- 100 # number of bins for all following histograms
#
# Zv9.60 genome parameters: Chromosome lenghts
#
mutChrom <- c(1:25)	# prepare vector for comparing homozygosity between chromosomes
chrLengths <- c(1:25)	# a bit tedious but Notepad otherwise creates linebreaks that cause errors in R when text is cut/pasted
chrLengths[1:10] = c(60348388,60300536,63268876,62094675,75682077,59938731,77276063,56184765,58232459,46591166)
chrLengths[11:20] = c(46661319,50697278,54093808,53733891,47442429,58780683,53984731,49877488,50254551,55952140)
chrLengths[21:25] = c(44544065,42261000,46386876,43947580,38499472) # chromosome 1-25 lengths of Zv9
#
#
#########################
png(args[4], width = 600, height = 800, bg = "white") # prepare output file
par(oma=c(4,0.5,2,0.5), mar=c(2.5,2.5,0.5,2), mfrow = c(5,5)) # prepare graph panels
#scale the y-axis limit based on the max counts in the histograms of chromosome 1 *1.1
z <- subset(snps0, snps0$Chr == 1) 	# take  SNPs of single chromosome as subset of all
zz <- subset(snps1, snps1$Chr == 1) 	# take  SNPs of single chromosome as subset of all

# prepare sequence of bins for current chromosome to ensure equal binning for all plots
p0 <- hist (c(z$Pos,zz$Pos), breaks = Nbreaks2, plot = FALSE)  
# prepare sequence of bins for current chromosome
bins = p0$breaks
# generate and store het SNP density histogram data
p1 <- hist (z$Pos, breaks = bins, plot = FALSE) 
# generate and store hom SNP density histogram data
p2 <- hist (zz$Pos, breaks = bins, plot = FALSE) 
#
Yscale <- 1.05
#########################
#
# begin for loop to process all chromosomes
for (x in 1:25)	
{
y <- toString(x) 		# prepare current chromosome name as string
# mutagenesis strain
z1 <- subset(snps0, snps0$Chr == y )   # take  SNPs of single chromosome as subset of all
z1 = z1[z1$AlleleFreq >= min_AF,]

# mapping strain
z2 <- subset(snps1, snps1$Chr == y ) 
z2 = z2[z2$AlleleFreq >= min_AF,]

# 2nd mapping strain
z3 <- subset(snps2, snps2$Chr == y ) 
z3 = z3[z3$AlleleFreq >= min_AF,]
#
# prepare sequence of bins for current chromosome to ensure equal binning for all plots
p0 <- hist (c(z1$Pos,z2$Pos), breaks = Nbreaks2, plot = FALSE)  
# prepare sequence of bins for current chromosome
bins = p0$breaks
# generate and store mutagenesis strain hom SNP density of mutagenesis dataset (1) histogram data
p1 <- hist (subset(z1$Pos, z1$AlleleFreq>0.85), breaks = bins, plot = FALSE) 
# generate and store mapping strain hom SNP density of mapping dataset (2) histogram data
p2 <- hist (subset(z2$Pos, z2$AlleleFreq>0.85), breaks = bins, plot = FALSE) 
p3 <- hist (subset(z3$Pos, z3$AlleleFreq>0.85), breaks = bins, plot = FALSE) 
#
for (i in 1:length(p1$counts))	# set all 0 values to 1 to avoid dividing by 0
{
	if (p1$counts[i]==0) { p1$counts[i] = 1}
	else {}
}
for (i in 1:length(p2$counts))	# set all 0 values to 1 to avoid dividing by 0
{
	if (p2$counts[i]==0) { p2$counts[i] = 0.5} #1
	else {}
}
for (i in 1:length(p3$counts))  # set all 0 values to 1 to avoid dividing by 0
{
  if (p3$counts[i]==0) { p3$counts[i] = 0.5} #1
  else {}
}
#plot y axis label only for first plot in a row
if (x %in% c(1,6,11,16,21)) 
{ 
	# plot mapping SNP histogram for current chromosome WITH y-axis label
	plot( hist(0, breaks = bins, plot = FALSE), main = "", col = rgb(1,1,1), xlab = paste("Chr", y," Position", sep=""), ylab ="AF Mut. Haplotype", 
ylim = c(0, Yscale), border = "white", cex.axis=0.75, mgp=c(1.3,0.3,0)) 
} else 
# plot mapping SNP histogram for current chromosome WITHOUT y-axis label
	{
  plot(hist(0, breaks = bins, plot = FALSE), main = "", col = rgb(1,1,1), xlab = paste("Chr", y," Position", sep=""), ylab ="", 
ylim = c(0, Yscale), border = "white", cex.axis=0.75, mgp=c(1.3,0.3,0)) 
}

# plot  mutagenesis SNP histogram for current chromosome

#SNP density
p4 <- p1	# generate and store difference in SNP density histogram data
p4$counts = (p1$counts-p2$counts)/2500 

p5 <- p1  # generate and store difference in SNP density histogram data
p5$counts = (p1$counts-p3$counts)/2500


# plot differential SNP histogram for current chromosome
plot(p4, main = "", col = "grey", border = "grey", add=T) # grey			
plot(p5, main = "", col = "lightblue", border = "lightblue", add=T) # grey


######################################################################
# plot average allele frequency 01
# initialize variables
AFMeans <- c(1: (length(p4$mids)))
# percentile = 0.05 # for debugging

# calculate average coverage ber bin
for (i in 1:(length(p4$mids)))
{
  Tmp_mean <- cbind(z1$Pos,z1$AlleleFreq)
  Tmp_mean <- Tmp_mean[Tmp_mean[,1]>(bins[i+1]-bins[2]) & Tmp_mean[,1]<bins[i+1],]

# dance around because R converts a matrix to an integer when there is only one entry!
	if (is.nan(mean(Tmp_mean)))  #correct SNP coverage dropouts
	{	
	  AFMeans[i] = AFMeans[i-1]	
	}
	else 
	{
	  if (is.matrix(Tmp_mean)) # if there are several SNPs, calculate AF
	  {
		  if (toString(percentile) == "mean") 
		  {
        AFMeans[i] = mean(Tmp_mean[,2])
		  }
  		else
  		{
    		Tmp_mean[,2] = sort(Tmp_mean[,2])
    		AFMeans[i] = quantile(Tmp_mean[,2],percentile)
  		}
	  }
	  else # if there is only 1 SNP, use it for AF
	  {
	    AFMeans[i] = Tmp_mean[2]	
	  }
	}
}

lines(p4$mids, (AFMeans*Yscale), col=rgb(1.000,0.679,0.450),lwd=1) # pastel orange

# fit a smoothing line to the histogram and plot it

lo <- loess((AFMeans*Yscale) ~ p4$mids, span =0.4)	
Fit <- fitted(lo)
lines(p4$mids,Fit, col=rgb(0.850,0.150,0.196), lwd=2) #red
#
######################################################################

#############################################################################
mutChrom[x] <- (mean(AFMeans))  # fractional homozygosity of whole chromosome

#
# Add boxplot showing average cumulative Allele Frequency for current chromosome
# bar thickness is relative to chromosome length (makes them look the same for all chromosomes)
BP_width <-  (chrLengths[x]/15)		
# bar is positioned at the same distance from histogram for each chromosome
BP_offset <- (chrLengths[x]/BP_width)+1.4
# plot the plot
barplot(matrix(c(mutChrom[x]*Yscale,(1-mutChrom[x])*Yscale)), space=BP_offset, width = BP_width, axes=FALSE, col=c("red","black"), cex.axis=0.75, mgp=c(0.5,0.2,0), add=T)
#

#plot boxplot y axis label only for last plot in a row
if (x %in% c(5,10,15,20,25)) 
{ 
# add new y-axis and labels for the new plot
	axis(4, at=c(0,(Yscale/2),Yscale), labels=c("map","het","mut"), las=2, pos=(BP_offset*BP_width*1.05), tick=FALSE, cex.axis=0.5, mgp=c(0.2,0.2,0.2)) 
	mtext("Chr haplotype",4, line=1.5, adj=0.5, cex=0.5, col="black")
	} else {}


} # end for loop, all chromosomes processed
#
#########################################################
# annotate figure

title(paste(Mname, " Homozygous Haplotype Map", sep=""), cex=4, outer = TRUE) 	# plot title and text
mtext(paste("LOESS fit of mutag. strain allele freq."), side=1, line=0.5, adj=0, cex=0.75, col=rgb(0.850,0.150,0.196), outer=TRUE)  
mtext(paste("mutag. strain allele frequency"), side=1, line=0.5, adj=0.33, cex=0.75, col=rgb(1.000,0.679,0.450), outer=TRUE)  
mtext(paste("mutag. strain SNP density excess"), side=1, line=0.5, adj=0.66, cex=0.75, col="grey", outer=TRUE)  
mtext(paste("2nd mutag. strain SNP density excess"), side=1, line=0.5, adj=1.0, cex=0.75, col="lightblue", outer=TRUE)  

trash = dev.off() # turn off graphics engine, save plot file to disk

cat("A total of ", (counter1+counter2+counter3) , " SNPs were analyzed.","\n")

##############################################################################################################

print ("Megamapping complete.")

##############################################
#############################################
quit(save = "no")

