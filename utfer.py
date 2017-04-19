import tsv
import sys
import copy
import os
import operator
import re

def main():
    print "starting"
    args = list(sys.argv)
    tweet_filename = args[1]
    infile = tsv.TsvReader(open(tweet_filename))
    count = 0
    file1c = 0
    file2c = 0
    outfile1 = open(tweet_filename[:-4]+"aReal.txt",'w')
    outfile2 = open(tweet_filename[:-4]+"bReal.txt",'w')
    for line in infile:
        print count
        #print line
        try:
            for word in line[0]:
                word.decode(encoding='UTF-8',errors='strict')
            if file1c <= file2c:
                outfile1.write(line[0] + "\tpositive\n")
                file1c += 1
            else:
                outfile2.write(line[0] + "\tpositive\n")
                file2c += 1
        except:
            count += 1
            continue
if __name__  == "__main__":
    main()
