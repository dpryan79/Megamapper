This is a github repository holding our modified version of the positional cloning tool known as "MegaMapper" available our local galaxy instance. The original tool is found [here](https://wiki.med.harvard.edu/SysBio/Megason/MegaMapper) and all references should be made to it and its [accompanying paper](http://dev.biologists.org/content/139/22/4280.long).

#Background
We use this pipeline fairly frequently to aid in positional cloning in zebra fish. However, this pipeline has presented a number of problems regarding its interactions with Galaxy (e.g., it can kill the server). Many of these problems seem to be due simply to how the MegaMapper tools are written (e.g., writing unneeded large temporary files) and not some other cause. Consequently, we're hoping that simply rewriting some of the more problematic tools will improve stability and run time.

#To Do
I need to go through the code a bit and remove some of the inefficiencies. VCF files are sorted by default, so we needn't have bedtools (or whatever) read the whole 10+ gig file into memory and convert it into an R-tree to subtract VCF files. We also need to prevent the various tools from needlessly writing to TMP files. The following files need to be checked:

 - [ ] bsa_megamapper.xml
 - [ ] bsaseq_megamapper.py
 - [ ] BSAseq_Rscript
 - [ ] candidator.py
 - [ ] candidator.R
 - [ ] candidator.xml
 - [ ] chrscan
 - [ ] chrscan.py
 - [ ] chrscan.xml
 - [ ] covextract.py
 - [ ] covextract.xml
 - [ ] hmf_megamapper.xml
 - [ ] hmfseq_megamapper.py
 - [ ] HMFseq_Rscript
 - [ ] mpileup_VCF.py
 - [ ] mpileup_VCF.xml
 - [ ] NewIntersect.py
 - [ ] new_intersect.xml
 - [ ] recombination_weight
 - [ ] subtract_vcf.py
 - [ ] subtract_vcf.xml
 - [ ] VCF4.1_header.vcf
 - [ ] VCFheader.py
 - [ ] VCFheader.xml
 - [ ] custom:
   - [ ] candidator.py
   - [ ] candidator.R
   - [ ] candidator.xml
   - [ ] hapmap_Rscript.R
   - [ ] hapmap_sd.py
   - [ ] hapmap_sd.xml
   - [ ] hetmap_Rscript.R
   - [ ] hetmap_sd.py
   - [ ] hetmap_sd.xml
   - [ ] hetmap_select.py
   - [ ] hetmap_select_Rscript.R
   - [ ] hetmap_select.xml
   - [ ] hmf_megamapper.xml
   - [ ] hmfseq_megamapper.py
   - [ ] HMFseq_Rscript
