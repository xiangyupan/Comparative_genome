Multiple genomes alignment
===========================
## Comparative_genome_pipeline

* Repeatmasker<br>
```RepeatMasker -engine wublast -species sheep -s -no_is -cutoff 255 -frag 20000 ../reference/sheep.v4.chr.fa```<br>
** 下载的基因组是soft mask的，可以通过程序将小写字母mask成N<br>
```python3.5 lower2N.py -s species.fa -o species.hard.mask.fa```<br>
* 先对要进行比对的每个基因组生成sizes文件<br>
```faSize cattle_v5.0.fa.hard.mask.fa -detailed >cattle.sizes```<br>
* 将基因组按照名字切开，例如牛，对应生成chr1,chr2………scaffold每个fasta<br>
* faSplit byName cattle_v5.0.fa.hard.mask.fa ./<br>
* 将每个基因组的所有序列对应生成.nib文件,目录分别命名为target/ query/
```for i in *.fa;do faToNib $i `echo $i | sed -e s/.fa/.nib/`; done```<br>
* Pairwise alignment Lastz<br>
```for i in ./target/*.nib;do for j in ./query/*.nib;do jsub -e lastz.e -o lastz.o -n 1 -J LASTZ lastz $i $j H=2000 Y=3400 L=6000 K=2200 >`basename $i .nib`-`basename $j .nib`.lav;done;done```<br>
* Download outgroup from UCSC pairwise alignment<br>
```hg19.canFam3.all.chain.gz;hg19.equCab2.all.chain.gz;hg19.mm10.all.chain.gz;hg19.susScr2.all.chain.gz;hg19.turTru1.all.chain.gz```<br>
```hg19.canFam3.net.gz;hg19.equCab2.net.gz;hg19.mm10.net.gz;hg19.susScr2.net.gz;hg19.turTru1.net.gz```<br>
```canFam3.chrom.sizes;equCab2.chrom.sizes;hg19.chrom.sizes;mm10.chrom.sizes;susScr2.chrom.sizes;turTru1.chrom.sizes```<br>
```wget -c ftp://hgdownload.soe.ucsc.edu/goldenPath/hg19/vsSusScr2/axtNet/* ``` <br>
	eg: chrUn_gl000231.hg19.turTru1.net.axt.gz<br>
* Chaining <br>
```for i in *.lav;do lavToPsl $i `basename $i .lav`.psl;done```<br>
```cat *.psl > all.psl```<br>
```grep -v '#' all.psl > all_nohead.psl```<br>
```pslSplitOnTarget all_nohead.psl psl/ -lump```<br>
```for i in psl/*.psl;do axtChain $i target/ query/ chain/`basename $i .psl`.chain -linearGap=loose -psl;done```<br>
```chainMergeSort chain/*.chain >all.chain```<br>
```chainPreNet all.chain target.sizes query.sizes all.pre.chain```<br>
* Netting<br>
```chainNet all.pre.chain =minSpace=1 target.sizes query.sizes stdout /dev/null | netSyntenic stdin targetspecies_queryspecies.net```<br>
* Maffing <br>
```netToAxt targetspecies_queryspecies.net all.pre.chain target/ query/ stdout | axtSort stdin targetspecies_queryspecies.axt```<br>
```axtToMaf targetspecies_queryspecies.net target.sizes query.sizes targetspecies_queryspecies.maf -tPrefix=targetspecies. -qPrefix=queryspecies.```<br>
```mafSplit -byTarget dummy.bed maf/ targetspecies_queryspecies.maf```<br>
* MultiZ <br>
```nohup multiz human.chimp.galago.maf human.mouse.rat.maf 1 > hg_chimp_mouse.maf```<br>
* PhyloFit<br>
```phyloFit -i MAF maf/the_longest_chromsome.maf```<br>
* PhastCons <br>
```for i in maf/*.maf;do x=`basename $i .maf`; phastCons --target-coverage 0.25 --expected-length 12 --rho 0.4 --msa-format MAF phyloFit.mod --most-conserved mostCons/$x.bed > wig/$x.wig;done```<br>
