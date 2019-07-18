Homework 05
===========

1. To generate all the candidate passwords, I first generated all combos of x 
   length using the permutations function. This was a recursive function which
   built all possible passwords from a potential alphabet. This function utilizes
   the yield command and generator elements. From there, I iterated through
   the elements in a generator object in the smash function. For each 
   combination, I added the prefix to the combination. 

   From there, the combination was run through a filter list comprehension 
   which matches each string after being run through the sha1sum function 
   to lines in the hashes string. Only the lines in the hashes files are 
   returned from the smash function.

   I used an if statement to tell if the user wishes to run on multiple cores.
   If they do, I create a partial function to run. The partial function of
   smash has less parameters and uses an altered prefix input. It takes in
   Length - 1 and uses a generator to make prefixes for all of the first letters.
   In turn, this would effectively allow the CPU to make all combos of 
   Length -1 and add the new prefixes to the front.

   To verify that the code was working, I periodically checked with the 
   doctests. This allowed me to build the program function by function.
   After making the main program work on a single core, I was able to 
   include the multiprocessing aspects of the challenge.


2.  
| Processes                           | Elapsed Time  |
|-------------------------------------|---------------|
| 1                                   | 3m2.803s      |
| 2                                   | 2m12.283s     |
| 4                                   | 1m7.495s      |
| 8                                   | 0m37.745s     |

    The number of processes utilized reduces the time required to crack passwords
    in all cases. In most cases, doubling the number of cores cuts the run time
    in about half.

    **NOTE I was running the program when many people were running with multiple
    cores. Thus, the run times are a little higher than expected.

3. A longer password is more effective. As x grows in 36^(x+1) it makes a larger
   difference than (36+1)^x. 36^6 = 2176782336 while 37^6 = 2565726409
   and 36^7 is 78364164096. Changing the exponenet makes a significantly larger
   difference



