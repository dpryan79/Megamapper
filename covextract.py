#!/usr/bin/env python

import sys
import optparse
import re
from decimal import *
import vcf

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()

def main():
    usage = """%prog [options]
    
options (listed below) default to 'None' if omitted
    """
    parser = optparse.OptionParser(usage=usage)
    
    
    parser.add_option(
        '-f','--file',
        dest='input_txt',
        default = False,
        help='Name of file to be chopped. STDIN is default')
    
    options, args = parser.parse_args()
    invalid_starts = '#'
    
    infile = open ( options.input_txt, 'r')
    
    vcf_reader = vcf.Reader(infile)
    
    samtools = False
    if ('samtoolsVersion' in vcf_reader.metadata):
        samtools = True
    
    fields = ['']*4
    
    for record in vcf_reader:
        fields[0] = str(record.CHROM)
        fields[1] = str(record.POS)
        fields[3] = str(record.INFO['DP'])
        if samtools:
            getcontext().prec = 1
            REF = Decimal(record.INFO['DP4'][0])+Decimal(record.INFO['DP4'][1]) # combine reference reads
            ALT = Decimal(record.INFO['DP4'][2])+Decimal(record.INFO['DP4'][3]) # combine alternate reads
            getcontext().prec = 2 #decimal precion
            fields[2] = str(Decimal(ALT)/(Decimal(REF)+Decimal(ALT)))
        else:
            getcontext().prec = 1
            REF = Decimal(record.INFO['SRF'])+Decimal(record.INFO['SRR']) # combine reference reads
            ALT = Decimal(record.INFO['SAF'][0])+Decimal(record.INFO['SAR'][0]) # combine alternate reads
            getcontext().prec = 2 #decimal precion
            fields[2] = str(Decimal(ALT)/(Decimal(REF)+Decimal(ALT)))
        
        line = '\t'.join(fields)
        print line

if __name__ == "__main__": main()

