#!/usr/bin/env python

"""
Creates a mpileup file from a bam file and a reference.

usage: %prog [options]
   -p, --input1=p: bam file
   -o, --output1=o: Output pileup
   -R, --ref=R: Reference file type
   -n, --ownFile=n: User-supplied fasta reference file
   -d, --dbkey=d: dbkey of user-supplied file
   -x, --indexDir=x: Index directory
   -b, --bamIndex=b: BAM index file
   -B, --baq=B: use BAQ model or not
   -C, --mapCo=$mapCo: coefficient for downgrading mapping quality
   -M, --mapCap=M: Cap mapping quality
   -d, --readCap=d: Cap read quality
   -q, --mapq=q: min map quality threshold
   -Q, --baseq=Q: min base quality threshold
   -I, --callindels=I: call indels or not
   -i, --indels=i: Only output lines containing indels
   -c, --consensus=c: Call the consensus sequence using MAQ consensus model ("10-column pileup")
   -u, --fformat=$fformat: bcf or vcf format
   -T, --theta=T: Theta parameter (error dependency coefficient)
   -N, --hapNum=N: Number of haplotypes in sample
   -r, --fraction=r: Expected fraction of differences between a pair of haplotypes
   -P, --phredProb=I: Phred probability of an indel in sequencing/prep
   -X, --cmdline=$cmdline: X: additional command line options

"""

import os, shutil, subprocess, sys, tempfile
from galaxy import eggs
import pkg_resources; pkg_resources.require( "bx-python" )
from bx.cookbook import doc_optparse

def stop_err( msg ):
    sys.stderr.write( '%s\n' % msg )
    sys.exit()

def check_seq_file( dbkey, GALAXY_DATA_INDEX_DIR ):
    seqFile = '%s/sam_fa_indices.loc' % GALAXY_DATA_INDEX_DIR
    seqPath = ''
    for line in open( seqFile ):
        line = line.rstrip( '\r\n' )
        if line and not line.startswith( '#' ) and line.startswith( 'index' ):
            fields = line.split( '\t' )
            if len( fields ) < 3:
                continue
            if fields[1] == dbkey:
                seqPath = fields[2].strip()
                break
    return seqPath

def __main__():
    #Parse Command Line
    options, args = doc_optparse.parse( __doc__ )
    seqPath = check_seq_file( options.dbkey, options.indexDir )
    # output version # of tool
    try:
        tmp = tempfile.NamedTemporaryFile().name
        tmp_stdout = open( tmp, 'wb' )
        proc = subprocess.Popen( args='samtools 2>&1', shell=True, stdout=tmp_stdout )
        tmp_stdout.close()
        returncode = proc.wait()
        stdout = None
        for line in open( tmp_stdout.name, 'rb' ):
            if line.lower().find( 'version' ) >= 0:
                stdout = line.strip()
                break
        if stdout:
            sys.stdout.write( 'Samtools %s\n' % stdout )
        else:
            raise Exception
    except:
        sys.stdout.write( 'Could not determine Samtools version\n' )
    #prepare file names 
    tmpDir = tempfile.mkdtemp()
    tmpf0 = tempfile.NamedTemporaryFile( dir=tmpDir )
    tmpf0_name = tmpf0.name
    tmpf0.close()
    tmpf0bam_name = '%s.bam' % tmpf0_name
    tmpf0bambai_name = '%s.bam.bai' % tmpf0_name
    tmpf1 = tempfile.NamedTemporaryFile( dir=tmpDir )
    tmpf1_name = tmpf1.name
    tmpf1.close()
    tmpf1fai_name = '%s.fai' % tmpf1_name
    #link bam and bam index to working directory (can't move because need to leave original)
    os.symlink( options.input1, tmpf0bam_name )
    os.symlink( options.bamIndex, tmpf0bambai_name )

    #get parameters for mpileup command
    if options.baq == 'yes':
        baq = '-B'
    else:
        baq = ''
    if options.callindels == 'yes':
        callindels = ''
    else:
        callindels = '-I'
    if options.indels == 'yes':
        indels = '-i'
    else:
        indels = ''
    if options.fformat == 'pileup':
       fformat = ''
    else:
       fformat = '-u'
        

#    opts = '%s -B -C %s -M %s -d %s -q %s -Q %s %s %s %s %s' % ( baq, options.mapCo, options.mapCap, options.readCap, options.mapq, options.baseq, callindels, indels, fformat, options.cmdline )
 # use for debugging # 
    opts = '-B -C 50 -q 30 -Q 30 -u ' #-r 10:20,000,000-21,000,000'
    print options.cmdline #use for debugging

#    if options.consensus == 'yes':
#        opts  += ' -c'
#   print opts #use for debugging
#    else:
#   print opts #use for debugging

#    if options.chs_cmdline == 'yes':
#        opts  = opts
#   print cmdline #use for debugging
#    else:
#   opts = opts
#   print opts #use for debugging

     

#               opts # += ' -c -T %s -N %s -r %s -I %s' % ( options.theta, options.hapNum, options.fraction, options.phredProb )
#      pileup only subset for troubleshooting:   opts += -r 2:100,000-150,000

    
# samtools mpileup -C50 -d24 -q20 -Q30 -uf /media/DATA1/galaxy/reference_genomes/danrer7/sam_index/danrer7.fa test.bam | /home/ian/samtools-0.1.18/bcftools/bcftools view -bvcg - > var.raw.bcf 
#/home/ian/samtools-0.1.18/bcftools/bcftools view var.raw.bcf | vcfutils.pl varFilter -D50 > var.flt.vcf' 
    
# samtools mpileup -B -C50 -M60 -d24 -q20 -Q30 -I -i -c -T -N -r -uf /media/DATA1/galaxy/reference_genomes/danrer7/sam_index/danrer7.fa test.bam | /home/ian/samtools-0.1.18/bcftools/bcftools view -bvcg - > var.raw.bcf 
#   -C, --mapCo=$mapCo: coefficient for downgrading mapping quality
#   -M, --mapCap=M: Cap mapping quality
#   -d, --readCap=d: Cap read quality
#   -q, --mapq=q: min map quality threshold
#   -Q, --baseq=Q: min base quality threshold
#   -c, --consensus=c: Call the consensus sequence using MAQ consensus model
#   -T, --theta=T: Theta parameter (error dependency coefficient)
#   -N, --hapNum=N: Number of haplotypes in sample
#   -r, --fraction=r: Expected fraction of differences between a pair of haplotypes
#   -P, --phredProb=I: Phred probability of an indel in sequencing/prep
#   Input Options:
#   -6  Assume the quality is in the Illumina 1.3+ encoding. -A Do not skip anomalous read pairs in variant calling.
#   -B  Disable probabilistic realignment for the computation of base alignment quality (BAQ). BAQ is the Phred-scaled probability of a read #   base being misaligned. Applying this option greatly helps to reduce false SNPs caused by misalignments.
#   -b FILE     List of input BAM files, one file per line [null]
#   -C INT  Coefficient for downgrading mapping quality for reads containing excessive mismatches. Given a read with a phred-scaled probability q of being generated from the mapped position, the new mapping quality is about sqrt((INT-q)/INT)*INT. A zero value disables this functionality; if enabled, the recommended value for BWA is 50. [0]
#   -d INT  At a position, read maximally INT reads per input BAM. [250]
#   -E  Extended BAQ computation. This option helps sensitivity especially for MNPs, but may hurt specificity a little bit.
#   -f FILE     The faidx-indexed reference file in the FASTA format. The file can be optionally compressed by razip. [null]
#   -l FILE     BED or position list file containing a list of regions or sites where pileup or BCF should be generated [null]
#   -q INT  Minimum mapping quality for an alignment to be used [0]
#   -Q INT  Minimum base quality for a base to be considered [13]
#   -r STR  Only generate pileup in region STR [all sites]
#   Output Options:
#   -D  Output per-sample read depth
#   -g  Compute genotype likelihoods and output them in the binary call format (BCF).
#   -S  Output per-sample Phred-scaled strand bias P-value
#   -u  Similar to -g except that the output is uncompressed BCF, which is preferred for piping.
#   Options for Genotype Likelihood Computation (for -g or -u):
#   -e INT  Phred-scaled gap extension sequencing error probability. Reducing INT leads to longer indels. [20]
#   -h INT  Coefficient for modeling homopolymer errors. Given an l-long homopolymer run, the sequencing error of an indel of size s is modeled as INT*s/l. [100]
#   -I  Do not perform INDEL calling
#   -L INT  Skip INDEL calling if the average per-sample depth is above INT. [250]
#   -o INT  Phred-scaled gap open sequencing error probability. Reducing INT leads to more indel calls. [40]
#   -P STR  Comma dilimited list of platforms (determined by @RG-PL) from which indel candidates are obtained. It is recommended to collect indel candidates from sequencing technologies that have low indel error rate such as ILLUMINA. [all] 
#where the -D option sets the maximum read depth to call a SNP. SAMtools acquires sample information from the SM tag in the @RG header lines. One alignment file can contain multiple samples; reads from one sample can also be distributed in different alignment files. SAMtools will regroup the reads anyway. In addition, if no @RG lines are present, each alignment file is taken as one sample. 
# Tuning the parameters
#One should consider to apply the following parameters to mpileup in different scenarios:
#    Apply -C50 to reduce the effect of reads with excessive mismatches. This aims to fix overestimated mapping quality and appears to be preferred for BWA-short.
#    Given multiple technologies, apply -P to specify which technologies to use for collecting initial INDEL candidates. It is recommended to find INDEL candidates from technologies with low INDEL error rate, such as Illumina. When this option is in use, the value(s) following the option must appear in the PL tag in the @RG header lines.
#    Apply -D and -S to keep per-sample read depth and strand bias. This is preferred if there are more than one samples at high coverage.
#    Adjust -m and -F to control when to initiate indel realignment (requiring r877+). Samtools only finds INDELs where there are sufficient reads containing the INDEL at the same position. It does this to avoid excessive realignment that is computationally demanding. The default works well for many low-coverage samples but not for, say, 500 exomes. In the latter case, using -m 3 -F 0.0002 (3 supporting reads at minimum 0.02% frequency) is necessary to find singletons.
#    Apply -A to use anomalous read pairs in mpileup, which are not used by default (requring r874+). 


    #prepare basic mpileup command
    if options.fformat == 'vcf':
        cmd = 'samtools mpileup %s -f %s %s | bcftools view -vcg - > %s' #| bcftools view -bvcg - > RAL_samtools.raw.bcf % ( opts, tmpf1_name, tmpf0bam_name, options.output1 ) 
        #print cmd # use for debugging

    else:
        cmd = 'samtools mpileup %s -f %s %s > %s'
    
    try:
        # have to nest try-except in try-finally to handle 2.4
        try:
            #index reference if necessary and prepare mpileup command
            if options.ref == 'indexed':
                if not os.path.exists( "%s.fai" % seqPath ):
                    raise Exception, "No sequences are available for '%s', request them by reporting this error." % options.dbkey
                cmd = cmd % ( opts, seqPath, tmpf0bam_name, options.output1 )
                print cmd # use for debugging
                
            elif options.ref == 'history':
                os.symlink( options.ownFile, tmpf1_name )
                cmdIndex = 'samtools faidx %s' % ( tmpf1_name )
                tmp = tempfile.NamedTemporaryFile( dir=tmpDir ).name
                tmp_stderr = open( tmp, 'wb' )
                proc = subprocess.Popen( args=cmdIndex, shell=True, cwd=tmpDir, stderr=tmp_stderr.fileno() )
                returncode = proc.wait()
                tmp_stderr.close()
                # get stderr, allowing for case where it's very large
                tmp_stderr = open( tmp, 'rb' )
                stderr = ''
                buffsize = 1048576
                try:
                    while True:
                        stderr += tmp_stderr.read( buffsize )
                        if not stderr or len( stderr ) % buffsize != 0:
                            break
                except OverflowError:
                    pass
                tmp_stderr.close()
                #did index succeed?
                if returncode != 0:
                    raise Exception, 'Error creating index file\n' + stderr

                cmd = cmd % ( opts, tmpf1_name, tmpf0bam_name, options.output1 )
                print cmd # use for debugging

            #perform mpileup command
            tmp = tempfile.NamedTemporaryFile( dir=tmpDir ).name
            tmp_stderr = open( tmp, 'wb' )
            proc = subprocess.Popen( args=cmd, shell=True, cwd=tmpDir, stderr=tmp_stderr.fileno() )
            returncode = proc.communicate()
#            returncode = proc.wait()
            tmp_stderr.close()
            #did it succeed?
            # get stderr, allowing for case where it's very large
            tmp_stderr = open( tmp, 'rb' )
            stderr = ''
            buffsize = 1048576
            try:
                while True:
                    stderr += tmp_stderr.read( buffsize )
                    if not stderr or len( stderr ) % buffsize != 0:
                        break
            except OverflowError:
                pass
            tmp_stderr.close()
            if returncode != 0:
                print returncode

#                raise Exception, stderr
        except Exception, e:
            stop_err( 'Error running Samtools mpileup tool\n' + str( e ) )


        tmp_out = tempfile.NamedTemporaryFile( dir=tmpDir)
        tmp_out_name = tmp_out.name
        tmp_out.close()
        try:
            shutil.move( options.output1, tmp_out_name )
        except Exception, e:
            raise Exception, 'Error moving output file before removing headers. ' + str( e )
        fout = file( options.output1, 'w' )

        for line in file( tmp_out.name, 'r' ):
            if ( line.startswith( 'chr' )):
                fout.write( line[3:] )
            else:
                fout.write( line )
        fout.close()

    finally:
        #clean up temp files
        if os.path.exists( tmpDir ):
            shutil.rmtree( tmpDir )
    # check that there are results in the output file
    if os.path.getsize( options.output1 ) > 0:
        sys.stdout.write( 'Converted BAM to pileup' )
    else:
        stop_err( 'The output file is empty. Your input file may have had no matches, or there may be an error with your input file or settings.' )

if __name__ == "__main__" : __main__()
