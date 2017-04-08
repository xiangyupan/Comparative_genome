Multiple genomes alignment
===========================
## Comparative_genome_pipeline

* Repeatmasker<br>
```RepeatMasker -engine wublast -species sheep -s -no_is -cutoff 255 -frag 20000 ../reference/sheep.v4.chr.fa```
* Pairwise alignment Lastz<br>
* faSplit<br>
<br>
```for i in {02..29};do mjsub -e lastz.e -o lastz.o -n 2 -J lastz${i} lastz ../cattle_v5.0.fa.hard.mask.fa[multiple] chr${i}.fa  --gfextend --chain --gapped --identity=90 --rdotplot=cattle_goat_chr${i}.rdotplot --format=maf- --output=cattle_goat_chr${i}.maf;done```

