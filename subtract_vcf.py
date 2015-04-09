#!/usr/bin/env python

"""
Creates an intersection vcf file from two vcf files.

usage: %prog [options]
   -p, --input1=p: vcf file
   -q, --input2=q: vcf file
   -f, --priority=f:    file #
   -i, --intersect=i:   Intersect or unique
   -o, --output1=o: Output vcf
   -r, --output2=r: Output stats
"""

import os, shutil, subprocess, sys, tempfile
#from galaxy import eggs
import pkg_resources; pkg_resources.require( "bx-python" )
from bx.cookbook import doc_optparse

def subtract(infile, outfile):
    mismatches = {}
    matches = set()
    input_handle = file(infile, "r")
    output_handle = file(outfile, "a")
    for line in input_handle:
        columns = line.split("\t")
        position = "%s_%s" % (columns[0],columns[1])
        
        if (len(columns) == 20 and columns[0] == columns[10] and columns[1] == columns[11] and columns[3] == columns[13]):
            matches.add(position)
            if (position in mismatches):
                del(mismatches[position])
        
            alt1 = set(columns[4].split(","))
            alt2 = set(columns[14].split(","))
            
            newAlt = alt1 - alt2
            
            if (len(newAlt) > 0):
                newRecord = columns[0:10]
                newRecord[4] = ",".join(newAlt)
                output_handle.write("\t".join(newRecord)+"\n")
        else:
            if ((not position in mismatches) and (not position in matches)):
                mismatches[position] = columns[0:10]
        
        
    input_handle.close()
    
    for rec in mismatches.values():
        output_handle.write("\t".join(rec)+"\n")
    
    output_handle.close()


def stop_err( msg ):
    sys.stderr.write( '%s\n' % msg )
    sys.exit()

def __main__():
    #Parse Command Line
    options, args = doc_optparse.parse( __doc__ )
    #get parameters for intersect command
    if options.priority == "second_file":
        file1 = options.input2
        file2 = options.input1
    else:
        file1 = options.input1
        file2 = options.input2
    
    cmd = "wc -l %s | cut -f1 -d ' '" % (file1)
    nrBefore = float(subprocess.check_output(cmd, shell=True))
    
    if options.intersect == 'keep_intersect':
        cmd = 'intersectBed -header -sorted -a %s -b %s > %s' % ( file1, file2, options.output1 )
        subprocess.check_call(cmd, shell=True)
        print cmd
    elif options.intersect == 'keep_unique':
        cmd = 'intersectBed -v -header -sorted -a %s -b %s > %s' % ( file1, file2, options.output1 )
        subprocess.check_call(cmd, shell=True)
        print cmd
    elif options.intersect == 'keep_allele':
        try:
            x,tmp1 = tempfile.mkstemp()
            x,tmp2 = tempfile.mkstemp()
            cmd = 'intersectBed -v -a %s -b %s > %s' % ( file1, file2, tmp1 )
            subprocess.check_call(cmd, shell=True)
            print cmd
            
            cmd = 'intersectBed -wa -wb -a %s -b %s > %s' % ( file1, file2, tmp2 )
            subprocess.check_call(cmd, shell=True)
            print cmd
            
            subtract(tmp2,tmp1)
            
            cmd = 'sortBed -i %s > %s' % ( tmp1, options.output1 )
            subprocess.check_call(cmd, shell=True)
            print cmd
        
        finally:
            os.remove(tmp1)
            os.remove(tmp2)
    
    
    cmd = "wc -l %s | cut -f1 -d ' '" % (options.output1)
    nrAfter = float(subprocess.check_output(cmd, shell=True))
    
    output_handle = file(options.output2, "w")
    output_handle.write("# SNPs before\tSNPs after\tfraction subtracted\tfraction retained\n")
    output_handle.write("%i\t%i\t%.4f\t%.4f\n" % (nrBefore, nrAfter, (nrBefore-nrAfter)/nrBefore, nrAfter/nrBefore))
    output_handle.close()
    
    # check that there are results in the output file
    print os.path.getsize( options.output1 )
    sys.stdout.write( 'Intersected VCF A with VCF B\n' )

if __name__ == "__main__" : __main__()

