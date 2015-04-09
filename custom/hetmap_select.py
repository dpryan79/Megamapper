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
    select_mut = sys.argv[2]
    in_fname_wt = sys.argv[3]
    select_wt = sys.argv[4]
    out_file1 = sys.argv[5]
    Mname = sys.argv[6]
    rscript_path = '/export/local_tools/MegaMapper/custom/hetmap_select_Rscript.R'

    try:
    #prepare command line 
        cmd  = 'Rscript --vanilla %s %s %s %s %s %s "%s"' %(rscript_path, in_fname, select_mut, in_fname_wt, select_wt, out_file1, Mname )
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
