import os 
import sys

def rename(infile):
    infile = open(infile, "r")
    for line in infile:
        (id1, hap1, id2, hap2, chr, start, end, lod) = line.split()
        if id1 == "id1":
            # oops this is the header
            continue
        id1 = id1 + "_" + hap1
        id2 = id2 + "_" + hap2
        
        lin = "\t".join((id1, hap1, id2, hap2, chr, start, end, lod))
        print(lin.strip())
        

def main(argv):
    infile = argv[1]
    rename(infile)


if __name__ == "__main__":
   main(sys.argv)
