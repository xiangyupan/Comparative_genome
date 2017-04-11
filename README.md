Multiple genomes alignment
===========================
## Comparative_genome_pipeline

* Repeatmasker<br>
```RepeatMasker -engine wublast -species sheep -s -no_is -cutoff 255 -frag 20000 ../reference/sheep.v4.chr.fa```<br>
* faSplit<br>
```faSplit sequence ASM.fa.hard.mask.fa 30 chr```<br>
* Pairwise alignment Lastz<br>
```for i in {02..29};do mjsub -e lastz.e -o lastz.o -n 2 -M 104857600 -J lastz${i} lastz_32 ../cattle_v5.0.fa.hard.mask.fa[multiple] chr${i}.fa  --gfextend --chain --gapped --identity=90 --rdotplot=cattle_goat_chr${i}.rdotplot --format=maf- --output=cattle_goat_chr${i}.maf;done```<br>
* Download UCSC pairwise alignment<br>
```hg19.canFam3.all.chain.gz;hg19.equCab2.all.chain.gz;hg19.mm10.all.chain.gz;hg19.susScr2.all.chain.gz;hg19.turTru1.all.chain.gz```<br>

