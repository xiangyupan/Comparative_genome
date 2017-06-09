produce_lastz_shell.py by Pan Xiangyu
usage: python3.5 produce_lastz_shell.py list
list which is the goat chromosome list

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 16:06:21 2017

@author: Jiang_lab
"""
def usage():
    print('''Useage: python3.5 script.py [sample_list]''')
def load_sample_list(name_file):
    nameList = []
    with open(name_file) as f :
        for sample in f:
            nameList.append(sample.strip())
    return nameList
def produce(nameList):
    name_num  = len(nameList)
    for i in nameList:
        with open(str(i)+'.sh','w') as f:
            f.write('''#!/bin/sh
''')
#            for j in nameList:
            f.write('''
for x in ../Goat_pseudoChr/''')
            f.write(i+'.nib')
            f.write('''
do
for y in ../Blue/BlueNib/*.nib
do
OutNam=./`basename $x .nib`/`basename $x .nib`-`basename $y .nib`.lav
lastz $x $y H=2000 Y=3400 L=6000 K=2200 > $OutNam
RowNum=`wc -l $OutNam|awk '{print $1}'`
if [ $RowNum -le 15 ]; then
rm $OutNam
fi
done
done''')

def main():
    import sys
#    print(1233)
    if len(sys.argv) < 2:
#        print(12333)
        usage()
        sys.exit(1)
    else:
#        print(133)
        nameList = load_sample_list(sys.argv[1])
        produce(nameList)
main()
