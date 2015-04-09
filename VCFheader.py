#!/usr/bin/env python

from galaxy import eggs
import sys, os

def stop_err(msg):
    sys.stderr.write(msg)
    sys.exit()
    
def main():
    outfile = sys.argv[1]
    infile = sys.argv[2]
    headerfile = '/export/local_tools/MegaMapper/VCF4.1_header.vcf'
    
    try:
        fout = open(sys.argv[1],'w')
    except:
        stop_err("Output file cannot be opened for writing.")
        
    try:
        fin = open(sys.argv[2],'r')
    except:
        stop_err("Input file cannot be opened for reading.")
    
    os.system("cp %s %s" %(infile,outfile))
#    sys.exit()


#    print os.getcwd()

# python -c print os.getcwd()
   
    cmdline = "cat %s %s " %(headerfile, infile)
#    for inp in sys.argv[3:]:
#        cmdline = cmdline + inp + " "
    cmdline = cmdline + ">" + outfile
    try:
        os.system(cmdline)
    except:
        stop_err("Error encountered with cat.")
        
if __name__ == "__main__": main()
