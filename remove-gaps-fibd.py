description='''Merge any adjacent blocks that are separated by no more than the distance gap_threshold.
Output is one line per tract per pair of individuals, with positions of start and end of tract.

Warning: this reads the entire file into memory at once.
'''
# highly modified by plr from process-ibd.py by Browning

import sys, gzip
from math import isnan
import re
from optparse import OptionParser
from itertools import chain

parser = OptionParser(description=description)
parser.add_option("-b","--ibdfile",dest="ibdfile",help="name of file to read ibd from (or '-' for stdin)",default="-")
parser.add_option("-o","--outfile",dest="outfile",help="name of file to output merged ibd from (or '-' for stdout)",default="-")
parser.add_option("-g","--gaplen",dest="gaplen",help="merge blocks separated by a block no longer than this long (in MORGANS)", default=0.0)
(options,args) =  parser.parse_args()

# alternatively one can read everything in base pairs (and specific -g in terms of base pairs).

# size of maximum gap to merge
gapthresh = float(options.gaplen)

results = {}
infile = open(options.ibdfile,"r")
outfile = open(options.outfile,"w")
for line in infile:
    # note: what is read is NOT the "length" but it is different (by one position) than the output.  
    # Beagle reports the starting (inclusive) and ending (exclusive) positions.
    (id1, hap1, id2, hap2, chr, start, end,  lod) = line.split()
    if id1 == "id1":
        # oops this is the header
        continue
    start = float(start)
    end = float(end)
    if (id1,id2) in results:
        currentlist = results[(id1,id2)]
        markremove = [False for x in currentlist]
        for j in range(len(currentlist)):
            x = currentlist[j]
            ovlap = x[0]<=end and start<=x[1]
            # is a gap?
            gap = ( x[0] <= end+gapthresh ) and ( start <= x[1] + gapthresh )
            # is shorter than an adjacent segment?
             # gaplen is max( start1-end2, start2-end1 ) since the min is negative
            gap = gap and ( max( x[0]-end, start-x[1] ) < max( end-start, x[1]-x[0] ) )
            if ovlap or gap:
                 # overlap
                markremove[j] = True
                start = min(x[0],start)
                end = max(x[1],end)
        if sum(markremove):
            results[(id1,id2)] = [x for x,r in zip(currentlist,markremove) if not r]
        results[(id1,id2)].append([start,end])
    else:
        results[(id1,id2)] = [[start,end]]


outfile.write("id1 id2 start end\n")
for x in results:
    # id1 = x[0]; id2 = x[1]
    for y in results[x]:
        l = list(chain(map(str,x), map(str,y)))
        outfile.write(" ".join(l) + "\n")

outfile.close()
