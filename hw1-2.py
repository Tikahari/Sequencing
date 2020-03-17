import sys
import random

def sequencePartitioner(input, x, y, output):
    f = open(input, "r")
    o = open(output, "w")
    line = f.readline()
    seqn = 0
    seq = ""
    while line:
        if(not line.startswith('>')):
            # sequence to print
            seqn = seqn+1
            frag = 0
            # iterate through sequence and chop it into blocks
            i = 0
            while i < len(line):
                frag = frag +1
                if seqn == 1 and i == 0:
                    seq = ">Sequence"+ str(seqn) + '|' + "fragment" +str(frag)+'\n'
                else:
                    seq = "\n>Sequence"+ str(seqn) + '|' + "fragment" +str(frag)+'\n'
                # get random number between x and y
                rn = random.randint(int(x), int(y))
                # if the entire sequence of that length exists add it to the output file
                if i + rn < len(line.strip()):
                    seq += line[i:i+rn].strip()
                    o.write(seq)
                # if not, check if a fragment of size greater than 'x' exists
                elif len(line.strip()) - i >= int(x):
                    seq += line[i:len(line)-1].strip()
                    o.write(seq)
                    # print("ONLY X",len(line), i, len(line)-i, x, seq, len(line[i:len(line)-1]))
                # else, through away fragment
                else:
                    seq += line[i:len(line)-1].strip()
                    print("OUT OF RANGE\nlength of line:",len(line.strip()), "\nindex:",i, "\nrandom number generated:", rn, "\ncharacters left in line:", len(line.strip())-i-1, seq, "\nMaximum possible size:",len(line[i:len(line.strip())-1].strip()),"Minimum required size:", x, "\n")
                # start next fragment at end of read fragment
                i=i+rn
        line = f.readline().strip()
    o.close()
    f.close()

if __name__ == '__main__':
    sequencePartitioner(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
