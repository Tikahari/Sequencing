# Sequence Simulator
###### Contributors: Zahin Ibnat, Tikahari Khanal, Hannah Mathew
#### Necessary Installs
* python>=3.7.6
* openjdk version "11.0.6" 2020-01-14

## Sequence Generator<br/>
#### Compile
    javac hw1-1.java 
#### Usage
    java SequenceGenerator <sequence length> <relative proportion A> <relative proportion C> <relative proportion G> <relative proportion T> <number of sequences> <mutation probability> <path to outputfile>
#### Overview
This program first generates a sequence of a set length with relative proportions of the nucleotides A/C/G/T. Then the sequence is mutated according to a mutation probability a set number of times. 
<br/>
<br/>


## Sequence Partitioner<br/>
#### Usage
    python hw1-2 <path to inputfile> <lower limit of fragment length> <upper limit of fragment length> <path to outputfile>
#### Overview
This program partitions each sequence within an input fasta file into fragments with length between an upper and lower bound. <br/>
<br/>
## Sequence Assembler<br/>
#### Usage
    python hw1-3 <path to inputfile> <match score> <mismatch score> <indel score> <path to outputfile>
#### Overview
This program aligns each a set of fragments in a fasta file using a greedy algorithm:<br/>
- fragment f<sub>i</sub> is aligned with fragment f<sub>j</sub> where i &ne; j using dovetail alignment
- if the alignment score is less than 0, j is incremented
- if the alignment score is greater than 0 the fragments are removed and the combined fragment is inserted into the beginning of the list and i and j are set to the two first items in the list
<br/>
The above algorithm is repeated until the list contains a single fragment or the highest alignment score between fragments is 0.
