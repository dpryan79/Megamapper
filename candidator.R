# args <- c("/home/ian/Downloads/snpeff.tabular", "/home/ian/Downloads/int.tabular", "/home/ian/Downloads/testout.tabular")
args <- commandArgs(TRUE)

snpfilepath <- args[1]
#snpfilepath <- "/home/ian/galaxy-dist/tools/MegaMapper/test1.tabular"
intfilepath <- args[2]
#intfilepath <- "/home/ian/galaxy-dist/tools/MegaMapper/test2.tabular"

snps <- read.table(file = snpfilepath, header = FALSE, sep = "\t",flush=TRUE) # read in SNP file
critint <- read.table(file = intfilepath, header = FALSE, sep = "\t") # read in critical interval boundaries
# PRIMARY PEAK
snps = snps[snps$V1==critint[1,2],] # filter SNP table for candidate chromosome
snps1 = snps[snps$V2>critint[1,3]&snps$V2<critint[1,4],] # filter SNP table for critical interval
snps1 = snps1[snps1$V12=="protein_coding",]
snps1 = snps1[!snps1$V16=="SYNONYMOUS_CODING",]
snps1 = snps1[!snps1$V16=="SYNONYMOUS_STOP",]
snps1 = snps1[!snps1$V16=="",]
snps1 = snps1[grep("INTRAGENIC",snps1$V16, invert=TRUE),]
snps1a = snps1[!snps1$V16=="NON_SYNONYMOUS_CODING",] # high impact SNPs
snps1b = snps1[snps1$V16=="NON_SYNONYMOUS_CODING",] # moderate impact SNPs
# EXPANDED PRIMARY PEAK
snps2 = snps[snps$V2>critint[2,3]&snps$V2<critint[2,4],] # filter SNP table for critical interval
snps2 = snps2[snps2$V12=="protein_coding",]
snps2 = snps2[!snps2$V16=="SYNONYMOUS_CODING",]
snps2 = snps2[!snps2$V16=="SYNONYMOUS_STOP",]
snps2 = snps2[!snps2$V16=="",]
snps2 = snps2[grep("INTRAGENIC",snps2$V16, invert=TRUE),]
snps2a = snps2[!snps2$V16=="NON_SYNONYMOUS_CODING",] # high impact SNPs
snps2b = snps2[snps2$V16=="NON_SYNONYMOUS_CODING",] # moderate impact SNPs
# SECONDARY PEAK
#snps3 = snps[snps$V2>critint[3,3]&snps$V2<critint[3,4],] # filter SNP table for critical interval
#snps3 = snps3[snps3$V12=="protein_coding",]
#snps3 = snps3[!snps3$V16=="SYNONYMOUS_CODING",]
#snps3 = snps3[!snps3$V16=="SYNONYMOUS_STOP",]
#snps3 = snps3[!snps3$V16=="",]
#snps3 = snps3[grep("INTRAGENIC",snps3$V16, invert=TRUE),]
#snps3a = snps3[!snps3$V16=="NON_SYNONYMOUS_CODING",] # high impact SNPs
#snps3b = snps3[snps3$V16=="NON_SYNONYMOUS_CODING",] # moderate impact SNPs
# EXPANDED SECONDARY PEAK
#snps4 = snps[snps$V2>critint[4,3]&snps$V2<critint[4,4],] # filter SNP table for candidate chromosome
#snps4 = snps4[snps4$V12=="protein_coding",]
#snps4 = snps4[!snps4$V16=="SYNONYMOUS_CODING",]
#snps4 = snps4[!snps4$V16=="SYNONYMOUS_STOP",]
#snps4 = snps4[!snps4$V16=="",]
#snps4 = snps4[grep("INTRAGENIC",snps4$V16, invert=TRUE),]
#snps4a = snps4[!snps4$V16=="NON_SYNONYMOUS_CODING",] # high impact SNPs
#snps4b = snps4[snps4$V16=="NON_SYNONYMOUS_CODING",] # moderate impact SNPs
# COMPROMISE PEAK
snps5 = snps[snps$V2>critint[3,3]&snps$V2<critint[3,4],] # filter SNP table for candidate chromosome
snps5 = snps5[snps5$V12=="protein_coding",]
snps5 = snps5[!snps5$V16=="SYNONYMOUS_CODING",]
snps5 = snps5[!snps5$V16=="SYNONYMOUS_STOP",]
snps5 = snps5[!snps5$V16=="",]
snps5 = snps5[grep("INTRAGENIC",snps5$V16, invert=TRUE),]
snps5a = snps5[!snps5$V16=="NON_SYNONYMOUS_CODING",] # high impact SNPs
snps5b = snps5[snps5$V16=="NON_SYNONYMOUS_CODING",] # moderate impact SNPs



write.table(("POTENTIAL HIGH IMPACT SNP LIST"), file = args[3], append = FALSE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(("MAPPING PEAK INTERVAL"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(cbind("Chrom","Position","Ref","Change","Type","Hom","Qual","Cov","Warng","Gene_ID","Gene_name","Bio_type","Trancript_ID","Exon_ID","Exon_Rank","Effect","old_AA/new_AA","Old_codon/New_codon","Codon_Num(CDS)","Codon_Degeneracy","CDS_size","Codons_around","AAs_around","Custom_interval_ID"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(("COMPROMISE MAPPING INTERVAL (PEAK +/- 3 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(snps5a, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(("PRIMARY PEAK MAPPING INTERVAL (PEAK +/- 3 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(snps1a, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(("SECONDARY PEAK MAPPING INTERVAL (PEAK +/- 3 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(snps2a, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
#write.table(("EXPANDED MAPPING INTERVAL (PEAK +/- 2 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table(("ALTERNATE MAPPING PEAK INTERVAL (PEAK +/- 0.5 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table(snps3a, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table(("EXPANDED MAPPING INTERVAL (PEAK +/- 2 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table(snps4a, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(("POTENTIAL MODERATE IMPACT SNP LIST"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
#write.table(("MAPPING PEAK INTERVAL (PEAK +/- 0.5 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table(snps2b, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table((""), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table(("EXPANDED MAPPING INTERVAL (PEAK +/- 2 mb)"), file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
#write.table(snps4b, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE)
write.table(snps5b, file = args[3], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)

print ("Intersecting complete.")

quit(save = "no")

##############################################
#############################################
#critint
#1	2	3	4
#1	13	26750000	27750000
#2	13	25250000	29250000
#3	13	41250000	42250000
#4	13	39750000	43750000

# Chromo	Position	Reference	Change	Change_type	Homozygous	Quality	Coverage	Warnings	Gene_ID	Gene_name	Bio_type	Trancript_ID	Exon_ID	#Exon_Rank	Effect	old_AA/new_AA	Old_codon/New_codon	Codon_Num(CDS)	Codon_Degeneracy	CDS_size	Codons_around	AAs_around	Custom_interval_ID
#Zv9_NA988	1034	T	C	SNP	Hom	222	10		ENSDARG00000090065	CABZ01109599.1	protein_coding	ENSDART00000121903	exon_Zv9_NA988_874_1080	2	#SYNONYMOUS_CODING	A/A	gcA/gcG	55	3	546			
#Zv9_NA18	1198	T	C	SNP	Hom	222	13		ENSDARG00000088905	pde8a	protein_coding	ENSDART00000127815	exon_Zv9_NA18_1178_1226	3	#SYNONYMOUS_CODING	S/S	tcT/tcC	88	3	978			

