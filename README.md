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
* MultiZ <br>
```nohup multiz human.chimp.galago.maf human.mouse.rat.maf 1 > hg_chimp_mouse.maf```<br>
  ### program description
multiz.v11.2:  -- aligning two files of alignment blocks where top rows are always the reference, reference in both files cannot have duplicats<br>
args: [R=?] [M=?] file1 file2 v? [out1 out2] [nohead] [all]<br>
	  R(30) radius in dynamic programming.<br>
	  M(1) minimum output width.<br>
	  out1 out2(null) null: stdout; out1 out2: file names for collecting unused input.<br>
	  nohead(null) null: output maf header; nohead: not to output maf header.<br>
	  all(null) null: not to output single-row blocks; all: output all blocks.<br>
maf-file1 and maf-file2 are two maf files to be aligned, each topped by a same reference sequence.<br>
The alignment of reference sequence with other components might be just for purpose of determing approximate alignment between two files, thus the alignment might be fixed or not, this is specified by v value, which can be only 0 or 1.<br>
0 - neither alignment of reference in each file is fixed.<br>
1 - the alignment of reference in the first file is fixed.<br>

[R=?] species radius values in dynamic programming, by default 30<br>
[M=?] species minimum output width, by default 1, which means output all blocks.<br>

[out1] collects unused blocks from maf-file1<br>
[out2] collects unused blocks from maf-file2<br>
[nohead] specifies not to have maf header for output<br>
