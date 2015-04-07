#!/usr/bin/env python

"""
Creates a filtered vcf file from a vcf file.

usage: %prog [options]
   -p, --input1=p: bam file
   -o, --output1=o: Output vcf
   -q, --qv_cutoff=q: Quality cutoff
   -i, --mindepth=i: minimum read depth
   -a, --maxdepth=a: maximum read depth
   -X, --cmdline=$cmdline: X: additional command line options (not yet used)
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

    #link to working directory (can't move because need to leave original)
    os.symlink( options.input1, tmpf0vcf_name )

    blah = "'N'"

    cmd = 'cat %s | java -Xmx4G -jar /home/galaxy/galaxy-dist/tools/snpEff/SnpSift.jar filter "( DP > %s ) & ( DP < %s ) & ( QUAL >= %s ) ! (REF = %s) ! (ALT = %s)" > %s' %(tmpf0vcf_name, options.mindepth, options.maxdepth, options.qv_cutoff, blah, blah, options.output1)

#    cmd = 'cat %s |java -Xmx6G -jar /home/ian/galaxy-dist/tools/snpEff/SnpSift.jar filter "( DP > 2 ) & ( DP < 32 ) & ( QUAL >= 10 ) & ( DP4[0] > 0 ) & ( DP4[1] > 0 ) & ( DP4[2] > 0 ) & ( DP4[3] > 0 ) ! (REF = %s) ! (ALT = %s)" > %s' %(tmpf0vcf_name,blah,blah,options.output2) # cleaned het SNPs read direction corrected

    print cmd # use for debugging

    tmp = tempfile.NamedTemporaryFile( dir=tmpDir ).name
    tmp_stderr = open( tmp, 'wb' )
    proc = subprocess.Popen( args=cmd, shell=True, cwd=tmpDir, stderr=tmp_stderr.fileno() )
    returncode = proc.wait()
    tmp_stderr.close()
    #did it succeed?


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
