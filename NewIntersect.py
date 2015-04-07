#!/usr/bin/env python

"""
Creates an intersection vcf file from two vcf files.

usage: %prog [options]
   -p, --input1=p: vcf file
   -q, --input2=q: vcf file
   -f, --priority=f:	file #
   -i, --intersect=i:	Intersect or unique
   -o, --output1=o: Output vcf
"""

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
#    args = "/home/galaxy/Desktop/Galaxy31.vcf","/home/galaxy/Desktop/Galaxy31.vcf","/home/galaxy/Desktop/test.vcf"

    try:
    #get parameters for intersect command
        file1 = options.input1
        file2 = options.input2
#        file1 = args[0]
#        file2 = open(args[1])
        output1 = 'out.txt'
        output2 = 'out2.txt'
        output3 = options.output1
        intermediate = 'intermediate.txt'
        aliquotsize = 2000001

    #get parameters for intersect command
        if options.priority == "first_file":
#                    opts = '-wa'
            opts = ''
            file3 = file1 #options.input1
            file4 = output1 #options.input2
        else:
#                    opts = '-wb'
            opts = ''
            file3 = output1 #options.input2
            file4 = file1 #options.input1

# count lines
        f2 = open(file2)
        flenght = len(f2.readlines())
        f2.close()
 #       f2.seek(0)

# divide file up into increments of up to aliquotsize (2,000,000)
        counter = 0
        count = 1 + (flenght/aliquotsize)
        print file2 + " has length: " + str(flenght) + " and will be divided into " + str(count) + " subsets."

        while (counter < count):
            counter = counter + 1
            llimit = aliquotsize*(counter-1)
            ulimit = aliquotsize*(counter)
            # print 'Saving lines between ', llimit, " and ", ulimit, "."

            f = open(output1,'wb')
            for i, line in enumerate(open(file2)):
                if i <= ulimit and i >= llimit:
                    f.write(line)
                elif i > ulimit:
                    break
            f.close()

            if options.intersect == 'keep_intersect':
                cmd = 'intersectBed %s -a %s -b %s > %s' % ( opts, file3, file4, output2 )
            else:
#                    opts = ''
                cmd = 'intersectBed %s -v -a %s -b %s > %s' % ( opts, file3, file4, output2 )

# do intersectBed
#            print cmd
            proc = os.system(cmd)

# hand over result of current intersection
            cmd = 'cp -f %s %s' % (output2, intermediate)
            proc = os.system(cmd)
            file3 = intermediate

# save output & clean up temp files
        cmd = 'cp -f %s %s' % (output2, output3)
        proc = os.system(cmd)
        cmd = 'rm %s' % (intermediate)
        proc = os.system(cmd)
        cmd = 'rm %s' % (output1)
        proc = os.system(cmd)
        cmd = 'rm %s' % (output2)
        proc = os.system(cmd)

    finally:
        print "SNP lists intersected!"
    # check that there are results in the output file
#    print os.path.getsize( options.output1 )
#    if os.path.getsize( options.output1 ) > 0:
    sys.stdout.write( 'Intersected VCF A with VCF B' )
#    else:
#      stop_err( 'The output file is empty. Your input file may have had no matches, or there may be an error with your input file or settings.' )

if __name__ == "__main__" : __main__()

