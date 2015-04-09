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
#    seqPath = check_seq_file( options.dbkey, options.indexDir )
    try:
    #get parameters for intersect command
                if options.priority == "first_file":
#                    opts = '-wa'
                    opts = ''
                    file1 = options.input1
                    file2 = options.input2
                else:
#                    opts = '-wb'
                    opts = ''
                    file1 = options.input2
                    file2 = options.input1

                if options.intersect == 'keep_intersect':
                    cmd = 'intersectBed %s -a %s -b %s > %s'
#                    print cmd
                else:
#                    opts = ''
                    cmd = 'intersectBed %s -v -a %s -b %s > %s'
#                    print cmd

#	intersectBed -wa -a /home/ian/Downloads/TUB.vcf -b /home/ian/Downloads/TUG.vcf > /home/ian/Downloads/result.vcf
#	intersectBed -v -a /home/ian/Downloads/TUB.vcf -b /home/ian/Downloads/TUG.vcf > /home/ian/Downloads/result2.vcf
# 	-wa	Write the original entry in A for each overlap.
#	-wb	Write the original entry in B for each overlap.
#		- Useful for knowing _what_ A overlaps. Restricted by -f and -r.
#	-u	Write the original A entry _once_ if _any_ overlaps found in B.
#		- In other words, just report the fact >=1 hit was found.
#	-v	Only report those entries in A that have _no overlaps_ with B.
#		- Similar to "grep -v" (an homage).
#
#report overlap of A in B.
#intersectBed -a /home/ian/test1.vcf -b /home/ian/13.vcf > out2.vcf
#
#report overlap of A in B (if B<<A : more memory efficient).
#intersectBed -wb -a /home/ian/13.vcf -b /home/ian/test1.vcf > out2.vcf
#
#report UNIQUE of A (A - B)
#intersectBed -v -a /home/ian/13.vcf -b /home/ian/test1.vcf > out2.vcf
#                cmd = cmd % ( opts, options.input1, options.input2, options.output1 )

                cmd = cmd % ( opts, file1, file2, options.output1 )
#                print cmd # use for debugging

#perform subtract command
#		tmp = tempfile.NamedTemporaryFile( dir=tmpDir ).name
#		tmp_stderr = open( tmp, 'wb' )
#                proc = subprocess.Popen( args=cmd, shell=True, cwd=tmpDir, stderr=tmp_stderr.fileno() )
                proc = os.system(cmd)
#                proc = subprocess.Popen( args=cmd, shell=True ).wait
#		returncode = proc.wait()
#		tmp_stderr.close() #did it succeed?
#		tmp_stderr = open( tmp, 'rb' ) # get stderr, allowing for case where it's very large
#		stderr = ''
#		buffsize = 1048576
#		while True:
 #                   try:
  #                          stderr += tmp_stderr.read( buffsize )
   #                         if not stderr or len( stderr ) % buffsize != 0:
    #                            break
     #               except OverflowError:
      #                      pass
       #             tmp_stderr.close()
        #            if returncode != 0:
	#		raise Exception, stderr
         #           except Exception, e:
          #          stop_err( 'Error running tool\n' + str( e ) )
    finally:
    #clean up temp files
        print cmd
    # check that there are results in the output file
    print os.path.getsize( options.output1 )
#    if os.path.getsize( options.output1 ) > 0:
    sys.stdout.write( 'Intersected VCF A with VCF B' )
#    else:
#      stop_err( 'The output file is empty. Your input file may have had no matches, or there may be an error with your input file or settings.' )

if __name__ == "__main__" : __main__()
