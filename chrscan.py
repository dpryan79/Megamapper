#!/usr/bin/env python
# megamapper executer
# by Nikolaus Obholzer, Jan 2012
"""

usage: %prog [options]
   -x, --galaxyDir=x: Galaxy root directory

"""

import sys, re, tempfile, subprocess
import os, shutil
from galaxy import eggs
from rpy import *
import pkg_resources; pkg_resources.require( "bx-python" )
from bx.cookbook import doc_optparse


def stop_err(msg):
    sys.stderr.write(msg)
    sys.exit()

def main():

    # Handle input params
    in_fname = sys.argv[1]
    Mname = sys.argv[2]
    chrom = sys.argv[3]
    out_file1 = sys.argv[4]
    out_file2 = sys.argv[5]
    #Parse Command Line
    options, args = doc_optparse.parse( __doc__ )
    galaxy_root = options.galaxyDir
    rscript_path = os.path.join( galaxy_root, 'tools/MegaMapper/chrscan' ) 

    try:
    #prepare command line 
        cmd  = 'Rscript --vanilla %s %s %s %s %s %s %s' %(rscript_path,in_fname,out_file1,out_file2,Mname,chrom,galaxy_root)
        print cmd # for debugging 
        os.system(cmd)

    finally:
        sys.stdout.write( 'Megamapping complete.' )
    # check that there are results in the output file
#        if os.path.getsize( out_file1 ) >= 0:
#            sys.stdout.write( 'Megamapping complete.' )
#        else:
#            stop_err( 'The output file is empty. Your input file may not have had SNPs, or there may be an error with your input file or settings.' )
    
if __name__ == "__main__":
    main()
