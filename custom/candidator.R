args <- commandArgs(TRUE)

snpfilepath <- args[1]
#intfilepath <- args[2]
chr <- as.integer(args[2])
start <- as.integer(args[3])
end <- as.integer(args[4])

snps <- read.table(file = snpfilepath, header = FALSE, sep = "\t",flush=TRUE) # read in SNP file
#critint <- read.table(file = intfilepath, header = FALSE, sep = "\t") # read in critical interval boundaries
critint <- data.frame("SNP region", chr, start,end)
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


write.table(("POTENTIAL HIGH IMPACT SNP LIST"), file = args[5], append = FALSE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(("MAPPING PEAK INTERVAL"), file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(cbind("Chrom","Position","Ref","Change","Type","Hom","Qual","Cov","Warng","Gene_ID","Gene_name","Bio_type","Trancript_ID","Exon_ID","Exon_Rank","Effect","old_AA/new_AA","Old_codon/New_codon","Codon_Num(CDS)","Codon_Degeneracy","CDS_size","Codons_around","AAs_around","Custom_interval_ID"), file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
#write.table(("PRIMARY PEAK MAPPING INTERVAL (PEAK +/- 3 mb)"), file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
write.table(snps1, file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
#write.table((""), file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
#write.table((""), file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
#write.table(("POTENTIAL MODERATE IMPACT SNP LIST"), file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)
#write.table(snps1b, file = args[5], append = TRUE, quote = FALSE, sep = "\t",col.names = FALSE, row.names = FALSE)

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

