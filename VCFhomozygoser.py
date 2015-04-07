#!/usr/bin/env python

"""
Creates a filtered vcf file from a vcf file.

usage: %prog [options]
   -p, --input1=p: bam file
   -o, --output1=o: Output vcf
   -X, --cmdline=$cmdline: X: additional command line options (not yet used)
   -l, --mindepth=$mindepth: l: minimal sequencing depth
   -m, --maxdepth=$maxdepth: m: maximal sequencing depth
   -d, --path=${GALAXY_ROOT_DIR}: d: Galaxy root directory
"""
#    -o, --output2=q: Output vcf2


import os, shutil, subprocess, sys, tempfile
from galaxy import eggs
import pkg_resources; pkg_resources.require( "bx-python" )
from bx.cookbook import doc_optparse

def stop_err( msg ):
    sys.stderr.write( '%s\n' % msg )
    sys.exit()

def __main__():
    #Parse Command Line
    options, args = doc_optparse.parse( __doc__ )

    #prepare file names 
    tmpDir = tempfile.mkdtemp()
    tmpf0 = tempfile.NamedTemporaryFile( dir=tmpDir )
    tmpf0_name = tmpf0.name
    tmpf0vcf_name = '%s.vcf' % tmpf0_name
    tmpf0.close()
    sift_dir = options.path + "/tools/snpEff/SnpSift.jar"
    #link to working directory (can't move because need to leave original)
    os.symlink( options.input1, tmpf0vcf_name )

    blah = "'N'"

    cmd = 'cat %s |java -Xmx4G -jar %s filter "( DP > %s ) & ( DP < %s ) & ( QUAL >= 10 ) & ( DP4[0] = 0 ) & ( DP4[1] = 0 ) ! (REF = %s) ! (ALT = %s)" > %s' %(tmpf0vcf_name,sift_dir,options.mindepth,options.maxdepth,blah,blah,options.output1) # cleaned out het SNPs

    print cmd # use for debugging

    tmp = tempfile.NamedTemporaryFile( dir=tmpDir ).name
    tmp_stderr = open( tmp, 'wb' )
    proc = subprocess.Popen( args=cmd, shell=True, cwd=tmpDir, stderr=tmp_stderr.fileno() )
    returncode = proc.wait()
    tmp_stderr.close()
    #did it succeed?

#    finally:
        #clean up temp files
    if os.path.exists( tmpDir ):
        shutil.rmtree( tmpDir )
    # check that there are results in the output file
    if os.path.getsize( options.output1 ) > 0:
        sys.stdout.write( 'Successfully cleaned up VCF' )
    else:
        stop_err( 'The output file is empty. Your input file may have had no matches, or there may be an error with your input file or settings.' )

if __name__ == "__main__" : __main__()
