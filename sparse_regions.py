#!/usr/local/bin/python

import argparse as arg
#import gzip

'''
	Given a gzipped map/bim file, get the number of SNPs for each window.
	This can later be processed by other programs to remove sections of ROH or IBD
	found to be in regions of low SNP density.
'''

def print_density(map_file, incr):
        #f = gzip.open(map_file, 'r')
        f = open(map_file, 'r')
        next(f)
        window_start = 0
        nSnps_in_window = 0
        nowchrom = 1
        for line in f:
                # No alleles
                (chrom, snp, cm, bp, a1, a2) = line.split()
                if (nowchrom < int(chrom)):
                        # reset for new chromosome
                        window_start = 0
                        nSnps_in_window = 0
                        nowchrom = int(chrom) 
                        
                # here, cm is read as 0 from the bim file. 
                elif (float(bp) < window_start+incr):
                        nSnps_in_window += 1
                else:
                        outstring = '\t'.join([chrom, str(int(window_start)), str(int(window_start+incr)), str(nSnps_in_window)]) 
                        print(outstring)
			# demarcates the window
                        window_start += incr
                        nSnps_in_window = 0

if __name__ == '__main__':
    parser = arg.ArgumentParser()
    parser.add_argument("-b", "--bim", required=True, help="bim/map file")
    parser.add_argument("-i", "--incr", default=1e6, type=float, help="Increment in bp by which to consider non-overlapping windows")
    args = parser.parse_args()
    print_density(args.bim, args.incr)

