import java.util.HashMap;
import java.io.File; 
import java.io.FileWriter;



class SequenceGenerator{
    public HashMap<Integer, Node> nucleotides;
    public int seq;
    public String fasta;
    public SequenceGenerator(){
        //hashmap for sequence generation
        this.nucleotides = new HashMap();
        nucleotides.put(1, new Node('A'));
        nucleotides.put(2, new Node('C'));
        nucleotides.put(3, new Node('G'));
        nucleotides.put(4, new Node('T'));
        // System.out.println("constructed");
        //string that will hold initial formatting of fasta file
        this.seq = 1;
        this.fasta = "";
    }
    public char addWeightedNucleotide(double prob, int s, String sequence, boolean no_replace, char to_replace){
        //iterate through A/C/T/G until you reach the letter within the bounds corresponding to that letter
        //this algorithms results in each letter being chosen with the weighted probability given as input
        int j = 0;
        double lower = 0;
        while(j < 4){
            if(prob <= this.nucleotides.get(j+1).getProbability() && prob >= lower && ( no_replace || to_replace != this.nucleotides.get(j+1).getLetter())){
                // System.out.println("Added "+this.nucleotides.get(j+1).getLetter() +"\n\tlower:"+lower+"\n\trandom:"+prob+"\n\tprobabilty"+this.nucleotides.get(j+1).getProbability());
                return this.nucleotides.get(j+1).getLetter();
            }
            else{
                // System.out.println("j is "+j+" lower is "+lower);
                lower = this.nucleotides.get(j+1).getProbability();
                j++;
            }
        }
        //if we were unable to return a character that means we need to add a weighted nucleotide that is not the same as the replaced nucleotide (run the same function again with different output from random number generator)
        // System.out.println("CALL FUNCTION AGAIN");
        return addWeightedNucleotide((double)s*Math.random(), s, sequence, no_replace, to_replace);
    }
    
    /*
    This function will generate a random number between 0 and 's' ('s' being the sum of arguments 1-5).
    An A/C/T/G will be selected depending on whther the random number falls within the upper and lower bounds that correspond to it in 'addWeightedNucleotide' function.
    The upper and lower bounds of A/C/T/G will be defined by a 'running_weight' variable that will ascribe an upper bound onto the character as it traverses and sums the input arguments.
    */
    public String generate_initial(String args[]){
        // System.out.println("generate" );
        //return string
        this.fasta += "";
        //define upper and lower bounds of A/C/T/G
        double running_weights = 0;
        for(int i = 0; i < 4; i++){
            running_weights += (double)Integer.parseInt(args[i+1]);
            this.nucleotides.get(i+1).changeProbability(running_weights);
        }
        int s = (Integer.parseInt(args[1]) + Integer.parseInt(args[2]) + Integer.parseInt(args[3]) + Integer.parseInt(args[4]));
        // System.out.println("s is "+s);
        for(int i = 0; i < Integer.parseInt(args[0]); i++){
            //create a random number between 0 and 's'
            double random = Math.random() * s;
            // System.out.println("random number is " + random + "\t\t" + i);
            this.fasta += this.addWeightedNucleotide(random, s, this.fasta, true, 'Q');
        }
        // System.out.println("sequence is "+this.fasta);
        return ">Sequence "+ this.seq +"\n"+this.fasta;
    }

    public String generate_post(String args[]){
        //return string (empty since ">Sequence" will have to be initialized within loop)
        String sequence = "";
        //'s' as defined previously
        int s = (Integer.parseInt(args[1]) + Integer.parseInt(args[2]) + Integer.parseInt(args[3]) + Integer.parseInt(args[4]));
        //iterate through sequence
        for(int j = 0; j < Integer.parseInt(args[5])-1; j++){
            //will keep track of sequence to write
            this.seq++;
            sequence += "\n>Sequence "+this.seq+"\n";
            for(int i  = 0; i < this.fasta.length(); i++){
                double random = Math.random();
                if (random <= Double.parseDouble(args[6])){
                    // System.out.println("mutation " + random + "\t"+args[6] + "\tcharacter\t"+this.fasta.charAt(i));
                    //if there is a mutation, randomly select whether or not it will be a replacement or deletion
                    double r2 = Math.random() *2;
                    // System.out.println("\t\tr2 is "+r2);
                    if(r2 >= 1){
                        //replace (else do nothing)
                        // System.out.println("\t\treplace");
                        //add nucleotide (with restriction that the added nucleotide cannot be the same as the nucleotide to replace)
                        sequence += this.addWeightedNucleotide((double)Math.random()*s, s, sequence, false, this.fasta.charAt(i));
                    }
                    else{
                        // System.out.println("\t\tdelete");
                    }
                    // System.out.println("m ~ "+ sequence);
                }
                else{
                    // System.out.println("no mutation");
                    //if there is no mutation, add the character at the corresponding index
                    sequence += this.fasta.charAt(i);
                    // System.out.println("nm ~ "+ sequence);
                }
            }
        }
        return sequence;
    }
    public void write(String outfile, String sequences){
        try {
            File f=  new File(outfile); 
            f.createNewFile();
            FileWriter writer = new FileWriter(outfile);
            writer.write(sequences);
            writer.close();
        } catch (Exception e) {
            //TODO: handle exception
            System.out.println("Error, file not created.");
        }


    }
    public static void main(String args[]){
        SequenceGenerator gen = new SequenceGenerator();
        String seqs = gen.generate_initial(args);
        seqs += gen.generate_post(args);
        gen.write(args[7], seqs);
    }
}

//Node class allows us to store probability and character as one element in the hashmap
class Node{
    public double probability;
    public char letter;
    public Node(){
        this.probability = 0;
        this.letter = '\0';
    }
    public Node(char c){
        this.probability = 0;
        this.letter = c;
    }
    public void changeProbability(double p){
        this.probability = p;
    }
    public char getLetter(){
        return this.letter;
    }
    public double getProbability(){
        return this.probability;
    }
}