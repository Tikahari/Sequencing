import sys
import numpy as np

class Node:
    def __init__(self, val=0, parent=-1):
        self.val = val
        self.parent = list()
        self.parent.append(parent)

def max(list):
    # print('list is', list)
    m = -999
    indices = []
    for i in range(len(list)):
        # print('list',list[i], i, list[i] > m, m)
        if list[i] == m:
            # print('append parent',indices)
            indices.append(i)
        if list[i] > m:
            m = list[i]
            indices = [i]
            # print('m is now', m)
            # print('parent is now', indices)
    return m, indices

def computeMatrix(f1, f2, match, p_replace, p_indel):
    # print('f1',f1, len(f1))
    # print('f2',f2, len(f2))
    a = [[Node() for j in range(len(f2)+1)] for i in range(len(f1)+1)]
    b = np.zeros((len(f1)+1, len(f2)+1))
    for i in range(len(f1)+1):
        for j in range(len(f2)+1):
            # check whether relevant nucleotides in f1 and f2 are a match or mismatch
            if i >0 and j > 0:
                if f1[i-1] == f2[j-1]:
                    # print('match', i, j, f1[i-1], f2[j-1])
                    cond = match
                else:
                    # print('replace', i, j, f1[i-1], f2[j-1])
                    cond = p_replace
                    # print(a[i][j-1].val+p_indel, a[i-1][j].val+p_indel, a[i-1][j-1].val+cond)
                val, parent = max((a[i][j-1].val+p_indel, a[i-1][j].val+p_indel, a[i-1][j-1].val+cond))
                # print('element is', val, f1[i-1], f2[j-1], i, j)
                # print('parent is ', parent)
                #if(val >= 0):
                a[i][j] = Node(val, parent)
                b[i][j] = val
                #else:
                    #a[i][j] = Node(0, parent)
                    #b[i][j] = 0
            # else:
    #             print('element is', a[i][j].val, a[i][j].parent, i, j)
    # print('return\n')
    print(b)
    # print(f1)
    # print(f2)
    return a,b

def findDovetail(a, f1, f2):
    v = -99
    ij = []
    for i in range(len(f1)+1):
        for j in range(len(f2)+1):
            # check last row
            if i == len(f1) and a[i][j].val > v:
                v = a[i][j].val
                ij = (i, j)
            # check last column
            if j == len(f2) and a[i][j].val > v:
                v = a[i][j].val
                ij = (i, j)
    return v, ij

def getPath(v, ij, a, f1, f2):
    path = [ij]
    l = len(path)
    while(path[-1][0] > 0 and path[-1][1] > 0):
        # print('path[-1] is', path[-1])
        if(a[path[-1][0]][path[-1][1]].parent[0] is not -999):
            # print('parent', a[path[-1][0]][path[-1][1]].parent[0])
            if(2 in a[path[-1][0]][path[-1][1]].parent[0]):
                # print(2)
                path.append((path[-1][0]-1, path[-1][1]-1))
            elif(0 in a[path[-1][0]][path[-1][1]].parent[0]):
                # print(0)
                path.append((path[-1][0], path[-1][1]-1))
            elif(1 in a[path[-1][0]][path[-1][1]].parent[0]):
                # print(1)
                path.append((path[-1][0]-1, path[-1][1]))
            # break
        elif( a[path[-1][0]][path[-1][1]].parent[0] is -999):
            # print('no parents')
            sys.exit()
        # else:
        #     print('more than one parent')
    return path
            
def convert(path, f1, f2):
    (f2, f1) = sorted((f1, f2))
    print(f1)
    print(f2)
    print('path is', path, path[-1])
    # will keep track of where we are in path
    p = 0
    seq = ""
    #series = False
    i = 0
    j = 0
        # find which string is the end
    if path[0][0]==0:
        end =f2
        beg = f1
        stop=path[0][1]
    elif path[0][1]==0:
        end = f1
        beg = f2
        stop=path[0][0]
    print("new")
    print(beg)
    print(end)
    print("Stop")
    print(stop)
    # essentially finding where the dovetail is, what goes first, then goes to the other string after u reach stop

    for i in range(0, stop): 
        if(i>stop):
            seq+=beg[i]
        # print(beg[i])
    # print("test in here")
    # print(beg[stop])
    # print("end")
    for j in range(0, len(end)):
        seq+=end[j]
        # print(end[j])
    print("Seq is "+ seq) 
    
    while j < (len(f2)) and p < len(path) and path[p][0] < len(f1):
        #print('i', i, len(f1),'j', j, len(f2),'p', p, len(path), path[p][0])
        if j < path[0][1]:
            seq += f2[j]
            #print('before', seq)
            j+= 1
        else:
            seq += f1[path[p][0]]
            #print('during', seq, p, path[p][0],path, f1[path[p][0]])
            j = path[p][1]
            p +=1
    #print('after', path[p-1][0], f1)
    i = path[p-1][0]
    while i < len(f1):
        seq += f1[i]
        #print('after', seq)
        i += 1 
    return seq

def sequenceAssembler(input, match, p_replace, p_indel, output):
    f = open(input, "r")
    # o = open(output, "w+")
    seq = 1
    lines = list()
    line = f.readline().strip()
    count = 1
    # add all sequences to 'lines' list
    while line:
        if count % 2 == 0:
            lines.append(line)
            #print(line)
        count += 1
        line = f.readline().strip()
    # align each member of lines to every other member of lines
    i = 0
    o = open(output, "a+")
    newseq = ""
    while i < len(lines)-1:
        a,b = computeMatrix(lines[i], lines[i+1], match, p_replace,p_indel)
        # find largest alignment score
        v, ij =  findDovetail(a, lines[i], lines[i+1])
        # print('v, ij', v, ij)
        if v > 0:
            path = getPath(v, ij, a, lines[i], lines[i+1])
            newseq = convert(path[::-1], lines[i], lines[i+1])
            # stg = str(seq)
            # lenstr = len(seq)
            # o.write('>Sequence'+str(seq)+'\n'+newseq+'\n')
            # o.close()
            # remove two original sequences from 'lines' and replace with 'newseq'
            # print('length of lines', len(lines))
            lines.pop(i+1)
            lines[i] = lines[0]
            lines[0] = newseq
            i = 0
            # print("length of lines now", len(lines))
            # print(lines)
            seq +=1
        else:
            #print(i, 'alignment score too low', lines[i], lines[i+1], v)
            #print(lines)
            i += 1
    o.write('>Sequence'+str(seq)+'\n'+newseq+'\n')
    o.close()
    print("alignments", lines)
    # m = [][]
    f.close()
    # o.close()


if __name__ == '__main__':
    sequenceAssembler(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5])