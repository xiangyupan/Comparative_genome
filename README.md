## Comparative_genome_pipeline
=================================
* all tools are download from http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/ </br>
* 自己组装的基因组做注释也是做过Repeatmaske的，所以这步可以省略<br>
```RepeatMasker -engine wublast -species sheep -s -no_is -cutoff 255 -frag 20000 ../reference/sheep.v4.chr.fa```</br>
* NCBI下载的基因组是soft mask的，可以通过程序将小写字母mask成N<br>
```python3.5 lower2N.py -s species.fa -o species.hard.mask.fa```<br>
* 基因组先过滤掉scaffold长度小于500的<br>
```faFilter -minSize=500 Oryx_gazella.v1.hard.mask.fa Oryx_gazella.v1.hard.mask.500.fa```<br>
* 再将N的比例大于90的序列过滤<br>
```faFilterN Oryx_gazella.v1.hard.mask.500.fa Oryx_gazella.v1.hard.mask.500.removeN.fa 90```<br>
* 先对要进行比对的每个基因组生成sizes文件<br>
```faSize cattle_v5.0.fa.hard.mask.fa -detailed >cattle.sizes```<br>
* 将基因组按照名字切开，例如牛，对应生成chr1,chr2………scaffold每个fasta<br>
```faSplit byName cattle_v5.0.fa.hard.mask.fa ./```<br>
* 将每个基因组的所有序列对应生成.nib文件,目录分别命名为target/ query/<br>
```for i in *.fa;do faToNib $i `echo $i | sed -e s/.fa/.nib/`; done```<br>
* Pairwise alignment Lastz<br>
* 批量提交需注意，当target 3万对query 3万，会产生不止30000x30000个文件；所以可以写shell提交并删除比对不上的，使目录下没有过多文件。<br>
```Shell
#!/bin/sh
for i in ../goat3/goat3Nib/*.nib;do mkdir `basename $i .nib`; done
for i in ../goat3/goat3Nib/*.nib
do
for j in ../sheep4/sheep4Nib/*.nib
do
OutNam=./`basename $i .nib`/`basename $i .nib`-`basename $j .nib`.lav
lastz $i $j H=2000 Y=3400 L=6000 K=2200 > $OutNam
RowNum=`wc -l $OutNam|awk '{print $1}'`
if [ $RowNum -le 15 ]; then
rm $OutNam
fi
done
done
```
```for i in ./target/*.nib;do for j in ./query/*.nib;do lastz $i $j H=2000 Y=3400 L=6000 K=2200 >`basename $i .nib`-`basename $j .nib`.lav;done;done```<br>
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
```chainNet all.pre.chain -minSpace=1 target.sizes query.sizes stdout /dev/null | netSyntenic stdin targetspecies_queryspecies.net```<br>
* Maffing <br>
```netToAxt targetspecies_queryspecies.net all.pre.chain target/ query/ stdout | axtSort stdin targetspecies_queryspecies.axt```<br>
```axtToMaf targetspecies_queryspecies.axt target.sizes query.sizes targetspecies_queryspecies.maf -tPrefix=targetspecies. -qPrefix=queryspecies.```<br>
```mafSplit -byTarget dummy.bed maf/ targetspecies_queryspecies.maf```<br>
* MultiZ <br>
```nohup multiz human.chimp.galago.maf human.mouse.rat.maf 1 out1 out2 > hg_chimp_mouse.maf```<br>
```mafAddIRows hg_chimp_mouse.maf human.2bit hg_chimp_mouse.addI.maf```
* PhyloFit<br>
```phyloFit -i MAF maf/the_longest_chromsome.maf ruminant.tree```<br>
* PhastCons <br>
```for i in maf/*.maf;do x=`basename $i .maf`; phastCons $i --target-coverage 0.25 --expected-length 12 --rho 0.4 --msa-format MAF phyloFit.mod --most-conserved mostCons/$x.bed > wig/$x.wig;done```<br>
* 小服务器</br>
```/home/JiangLab/bin/phast-1.4/bin/phastCons --target-coverage 0.25 --expected-length 20 Ruminant.pronghorn.maf --most-conserved mostcons.bed phyloFit.mod >conser.wig```</br>
_______________________________________________________________________________________________________________
This pipeline is based on the website *http://genomewiki.ucsc.edu/index.php/Whole_genome_alignment_howto*		
