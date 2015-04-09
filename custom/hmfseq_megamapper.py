#!/usr/bin/env python
# megamapper executer
# by Nikolaus Obholzer, Jan 2012

import sys, re, tempfile, subprocess
import os, shutil
from galaxy import eggs


def stop_err(msg):
    sys.stderr.write(msg)
    sys.exit()

def main():

    # Handle input params
    in_fname = sys.argv[1]
    out_file1 = sys.argv[2]
    out_file2 = sys.argv[3]
    out_file3 = sys.argv[4]
    Mname = sys.argv[5]
    chr = sys.argv[6]
    rscript_path = '/export/local_tools/MegaMapper/custom/HMFseq_Rscript'

    try:
    #prepare command line 
        cmd  = 'Rscript --vanilla %s %s %s %s %s %s %s' %(rscript_path, in_fname, out_file1, out_file2, out_file3, Mname, chr )
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
