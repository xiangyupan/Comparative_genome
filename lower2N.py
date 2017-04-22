lower2N.py by Gao Shan
usage: python3.5 lower2N.py -s species.fa -o species.hard.mask.fa

import sys
import getopt
import os
def usage():
    print('''Useage: python script.py [option] [parameter]
    -s/input_file           input the fasta file
    -o/--output              the output results file
    -h/--help                show possible options''')
#######################default
opts, args = getopt.getopt(sys.argv[1:], "hs:t:o:",["help","sequence_file=","temp=","output="])
for op, value in opts:
    if op == "-s" or op=="--sequence_file":
        sequence_file = value
    elif op == "-o" or op =="--output":
        output = value
    elif op == "-t" or op =="--temp":
        temp = value
    elif op == "-h" or op == "--help":
        usage()
        sys.exit(1)
f1=open(sequence_file)
f2=open(output,'w')
for line in f1.readlines():
        if '>' in line:
                f3.write(line)
        else:
                for letter in line:
                        if letter.islower() is True:
                                f3.write('N')
                        else:
                                f3.write(letter)
f1.close()
f2.close()
