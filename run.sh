snakemake --snakefile runibdpipeline \
          --cluster-config cluster.json \
          -c "qsub -l h_vmem={cluster.mem} -o {cluster.out} -e {cluster.err} -cwd -V" \
          -j 30 \
          -p \
          $*


          #--config ibdcalls=/mnt/gluster/home/halasadi/projects/recent_migration/data/HOA/ibdcalls \
          #--config plinkfile=mnt/gluster/home/halasadi/projects/recent_migration/data/HOA/plink/broken_up_by_chr/HOA_ASIA_AMERICA \
	  	  #--config prefix=HOA_ASIA_AMERICA \
