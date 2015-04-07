#!/usr/bin/env python

import sys
import optparse
import re
from decimal import *

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()

def main():
    usage = """%prog [options]
    
options (listed below) default to 'None' if omitted
    """
    parser = optparse.OptionParser(usage=usage)
    
#    parser.add_option(
#        '-a','--ascii',
#        dest='ascii',
#        action='store_true',
#        default = False,
#        help='Use ascii codes to defined ignored beginnings instead of raw characters')
        
#    parser.add_option(
#        '-q','--fastq',
#        dest='fastq',
#        action='store_true',
#        default = False,
#        help='The input data in fastq format. It selected the script skips every even line since they contain sequence ids')

#    parser.add_option(
#        '-i','--ignore',
#        dest='ignore',
#        help='A comma separated list on ignored beginnings (e.g., ">,@"), or its ascii codes (e.g., "60,42") if option -a is enabled')

#    parser.add_option(
#        '-s','--start',
#        dest='start',
#        default = '0',
#        help='Trim from beginning to here (1-based)')

#    parser.add_option(
#        '-e','--end',
#        dest='end',
#        default = '0',
#        help='Trim from here to the ned (1-based)')

    parser.add_option(
        '-f','--file',
        dest='input_txt',
        default = False,
        help='Name of file to be chopped. STDIN is default')
            
#    parser.add_option(
#        '-c','--column',
#        dest='col',
#        default = '8',
#        help='Column to chop. If 0 = chop the whole line')
       

    options, args = parser.parse_args()
    invalid_starts = '#'

    #if options.input_txt:
    infile = open ( options.input_txt, 'r')
    #else:
    #infile = sys.stdin
    	
    #if options.ignore and options.ignore != "None":
#    invalid_starts = '#'
        
    #if options.ascii and options.ignore and options.ignore != "None":
#    for i, item in enumerate( invalid_starts ):
#        invalid_starts[i] = chr( int( item ) )

    col = 8 #int( options.col ) # this is the INFO column of VCF4.1 files
 
    for i, line in enumerate( infile ):
        line = line.rstrip( '\r\n' )
        if line:

            if line[0] not in invalid_starts:
                if col == 0:
                    print line

                else:
                    fields = line.split( '\t' )
                    if col-1 > len( fields ):
                        stop_err('Column %d does not exist. Check input parameters\n' % col)
                        
                    else:
                        fields[col-1] = fields[col - 1].replace(';','\t') # split info field into tab-separated words
                        
                        if fields[col-1].split()[0].startswith('INDEL'): # INDEL INFO field is present
                            if fields[col-1].split()[2].startswith('VDB'): # INDEL AND VDB INFO field are present
                                fields[2] = fields[col-1].split()[3] # copy allele freq to column 3
                                fields[3] = fields[col-1].split()[1] # copy coverage to column 4
                                fields[4] = fields[col-1].split()[5] # copy reads # to col 5
                            else:  # only INDEL INFO field is present
                                fields[2] = fields[col-1].split()[2] # copy allele freq to column 3
                                fields[3] = fields[col-1].split()[1] # copy coverage to column 4
                                fields[4] = fields[col-1].split()[4] # copy reads # to col 5

                        elif fields[col-1].split()[4].startswith('DP4'): # VDB INFO field is present
                            fields[2] = fields[col-1].split()[2] # copy allele freq to column 3
                            fields[3] = fields[col-1].split()[0] # copy coverage to column 4
                            fields[4] = fields[col-1].split()[4] # copy reads # to col 5
                            #print line

                        else:   # VDB INFO field is missing
                            fields[4] = fields[col-1].split()[3] # copy reads # to col 5
                            fields[2] = fields[col-1].split()[1] # copy allele freq to column 3
                            fields[3] = fields[col-1].split()[0] # copy coverage to column 4
                            #print line
                            
                        fields[4] = fields[4].replace('DP4=','') #remove directional depth string
                        fields[4] = fields[4].replace(',','\t')# split directional depth string
                        fields[3] = fields[3].replace('DP=','')# remove coverage string
                        fields[2] = fields[2].replace('AF1=','')# remove allele freq string
                        line = '\t'.join(fields[0:5])
                        #print line
                        fields = line.split( '\t' )
                        getcontext().prec = 1 #decimal precion
                        REF = Decimal(fields[4])+Decimal(fields[5]) # combine reference reads
                        ALT = Decimal(fields[6])+Decimal(fields[7]) # combine alternate reads
                        getcontext().prec = 2 #decimal precion
                        fields[2] = Decimal(ALT)/(Decimal(REF)+Decimal(ALT)) # Alternate Allele Frequency
                        fields[2] = str(fields[2])
                        #line = '\t'.join(fields[0:4])
                        #print line

                    line = '\t'.join(fields[0:4])
                    print line
                    #line = '\t'.join(fields)
            #return i+1
            continue
        

if __name__ == "__main__": main()

