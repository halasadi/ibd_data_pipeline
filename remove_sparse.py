#!/usr/local/bin/python
'''

'''
import argparse as arg

class Region:

	def __init__(self, chromo, pos1, pos2):
		self.chromo = chromo
		self.pos1 = pos1
		self.pos2 = pos2

	def __repr__(self):
		return '(' + str(self.pos1) + ',' + str(self.pos2) + ',' + str(self.chromo) + ')'

def within(sparse, test ):
	return ((test.pos1 <= sparse.pos2) and (sparse.pos1 <= test.pos2) and (test.chromo == sparse.chromo)) 

'''
	Sparse Region File is determined by sparse_regions.py
'''
def create_density_list(sparsefile, thresh):
	sparse_region_list = []
	for line in open(sparsefile, 'r'):
		(chromo, pos1, pos2, nsnps) = line.split()
		if (int(nsnps) < thresh):
			s = Region(int(chromo), int(pos1), int(pos2))
			sparse_region_list.append(s)
	return sparse_region_list


def readRefinedIBD(refinedIBDfile, sparseRegionList, lodthres):
    with open(refinedIBDfile, 'r') as f:
        for line in f:
            [id1, i1, id2, i2, chromo, bp1, bp2, lod] = line.split()
            # now create a list of sparse regions
            # filter by lod score
            # filter by sparsity

            seg = Region(int(chromo), int(bp1), int(bp2))
            not_sparse_roh = True
            for s in sparseRegionList:
                if within(s, seg):
                        not_sparse_roh = False
                        break
		
            if not_sparse_roh and float(lod) > lodthres:
                print line.rstrip()




if __name__ == '__main__':
	parser = arg.ArgumentParser()
	parser.add_argument("-s", "--sparse", required=True, help="Sparse Regions File/Binned Bim file")
	parser.add_argument("-i", "--ibdfile", required=True, help="refinedIBD file")
	parser.add_argument("-lodt", "--lodthres", type=int, default=3, help="The threshold at which you believe a segment is truly IBD")
        parser.add_argument("-st", "--sparsethres", type=int, default=1, help="Number of SNPs per cM below which we consider too sparse.")
	args = parser.parse_args()

	sparse_regions = create_density_list(args.sparse, args.sparsethres)
        readRefinedIBD(args.ibdfile, sparse_regions, args.lodthres)

