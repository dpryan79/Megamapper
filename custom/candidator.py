#!/usr/bin/env python
# megamapper intersector
# by Nikolaus Obholzer, Jan 2012

import sys, re, tempfile, subprocess
import os, shutil
from galaxy import eggs

def stop_err(msg):
    sys.stderr.write(msg)
    sys.exit()

def main():

    # Handle input params
    in_fname1 = sys.argv[1]
    chr = sys.argv[2]
    start = sys.argv[3]
    end = sys.argv[4]
    out_file1 = sys.argv[5]
    rscript_path = '/export/local_tools/MegaMapper/custom/candidator.R'

    try:
    #prepare command line 

        cmd  = 'Rscript --vanilla %s %s %s %s %s %s' %(rscript_path, in_fname1, chr, start, end, out_file1 )
        os.system(cmd)

    finally:

    # check that there are results in the output file
        if os.path.getsize( out_file1 ) >= 0:
            sys.stdout.write( 'Candidate list compiled.' )
        else:
            stop_err( 'The output file is empty. Your input file may not have had SNPs, or there may be an error with your input file or settings.' )
    
if __name__ == "__main__":
    main()
