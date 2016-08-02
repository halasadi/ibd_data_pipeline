# e.g. Rscript interpolate.R 1 b36 ../../arjun/bin/chr1/WTCCC2_POBI_illumina_calls_POBI_allchr_illumina_1.merged.nosparse.ibd WTCCC2_POBI_illumina_calls_POBI_allchr_illumina_1.merged.nosparse.cm.ibd

options(echo=TRUE); # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE);
chr <- as.integer(args[1]);
build <- args[2]
ibdfile <- args[3];
outfile <- args[4]

if (build == "b36"){
    mapdir <- "/mnt/gluster/home/halasadi/projects/recent_migration/data/POBI/hapmap_rates/genetic_map_";
    map <- read.table(paste0(mapdir, "chr", chr, "_b36.txt"), as.is=TRUE, header= T, stringsAsFactors = FALSE);
    position = map$position
    genetic_map_cm = map$Genetic_Map.cM.
    
} else{
    mapdir="/mnt/gluster/home/halasadi/data/1000-genomes-genetic-maps/interpolated_from_hapmap"
    map <- read.table(paste0(mapdir, "/chr", chr, ".interpolated_genetic_map"), as.is=TRUE, header= F, stringsAsFactors = FALSE);
    position = map$V2
    genetic_map_cm = map$V3
}

ibd <- data.frame(read.table(ibdfile, header = F, stringsAsFactors = F));
colnames(ibd) <- c("id1", "hap1", "id2", "hap2", "chr", "start", "end", "lod");


start <- approx(position, genetic_map_cm, xout = ibd$start,
                yleft = min(genetic_map_cm), yright = max(genetic_map_cm))
end <- approx(position, genetic_map_cm, xout = ibd$end,
                yleft = min(genetic_map_cm), yright = max(genetic_map_cm))

write.table(data.frame(id1=ibd$id1, hap1 = ibd$hap1, id2=ibd$id2, hap2 = ibd$hap2, chr = ibd$chr,
                       start=start$y, end=end$y, lod = ibd$lod, stringsAsFactors = F), file = outfile, quote=FALSE, row.names=F);



### OLD CODE ###
## reading in bim file, its not necessary but makes interpolation faster than
## working with 1000 genomes
#bimfile <- data.frame(read.table(paste0("/mnt/gluster/home/halasadi/projects/recent_migration/data/POBI/broken_up_by_chr/WTCCC2_POBI_illumina_calls_POBI_allchr_illumina_chr", chr, ".bim"), header = F, stringsAsFactors=F));
#colnames(bimfile) <- c("chr", "rsid", "cM", "pos", "ref", "alt");
#myMatches <- match(bimfile$pos, hapmap$position);
#mymap=hapmap$Genetic_Map.cM.[myMatches];

## interpolation

# transform to log
#epsilon=1e-8
#mymap[mymap == 0 & !is.na(mymap)] <- epsilon;
#logd <- na.omit(data.frame(pos=bimfile$pos, logmap=log(mymap)));
#fit.lo <- loess(logmap ~ pos, data = logd, na.action = na.exclude, span = 0.25, degree = 1, control=loess.control(surface="direct"));

#log_start <- predict(fit.lo, ibd$start);
#log_end <- predict(fit.lo, ibd$end);


# transform back to original scale
#start <- round(exp(log_start),3);
#end <- round(exp(log_end),3);




