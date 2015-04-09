#!/usr/bin/env python
# bsaseq_megamapper executer
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
    in_fname1 = sys.argv[1]
    in_fname2 = sys.argv[2]
    in_fname3 = sys.argv[3]
    out_file1 = sys.argv[4]
    Mname = sys.argv[5]
    galaxy_root = sys.argv[6]
    #rscript_path = os.path.join( galaxy_root, '../local_tools/MegaMapper/custom/hapmap_Rscript.R' ) 
    rscript_path = "/export/local_tools/MegaMapper/custom/hapmap_Rscript.R"
    cutoff = sys.argv[7] 
    bfilter = sys.argv[8]

#    print in_fname1
    try:
    #prepare command line 
#        print os.getcwd()

        cmd  = 'Rscript --vanilla %s %s %s %s %s %s %s %s' %(rscript_path, in_fname1, in_fname2, in_fname3, out_file1, Mname, cutoff, bfilter)
        print cmd # for debugging 
        os.system(cmd)
#        subprocess.Popen(args=cmd, shell=True).wait

    finally:
        sys.stdout.write( 'Megamapping complete.' )
    # check that there are results in the output file
#        if os.path.getsize( out_file1 ) >= 0:
#            sys.stdout.write( 'Megamapping complete.' )
#        else:
#            stop_err( 'The output file is empty. Your input file may not have had SNPs, or there may be an error with your input file or settings.' )
    
if __name__ == "__main__":
    main()
