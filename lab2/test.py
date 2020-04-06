from suffix_tree import SuffixTree as SuffixTree
from suffix_tree_naive import SuffixTree as SuffixTreeNaive
from trie import Trie as Trie
import random
from timeit import default_timer as timer

def check_validity(text, structure, skip, test_string=""):

        error = False
        for i in range(0, len(text), skip):
                for j in range(i + 1, len(text), skip):
                        if not structure.find(text[i:j]):
                                print("Test called: " + test_string + " has NOT passed!!!")
                                error = True
                                return False
        if not error:
                print("Test called: " + test_string+" passed")
                return True



def benchmark(text, structures, length=-1):
        if length==-1:
                length=len(text)
        print("LENGTH: "+str(length))
        test_string = natural_text_input[:length]
        for S in structures:
                start = timer()
                t=S(test_string)
                end = timer()
                print(t.name+" construction: " + str(end - start) + " sec.")


#Check validity of algorithms
file = open("1997_714.txt", "r", encoding="utf8")
basic_inputs = ["bbb$","aabbabd", "ababcd", "abcbccd", "anyananym", ]
natural_text_input = file.read()
artificial_text_input = ""
for i in range(0, 200000):
        if random.randint(0, 1)==0:c='a'
        else: c='b'
        artificial_text_input+=c

i = 0
for input in basic_inputs:
        i=i+1
        trie = Trie(input)
        check_validity(input, trie, 1, test_string="Trie- Basic test no. "+str(i))
        simple_suffix_tree = SuffixTreeNaive(input)
        check_validity(input, simple_suffix_tree, 1, test_string="Simple SuffixTree- Basic test no. "+str(i))
        fast_suffix_tree = SuffixTree(input)
        check_validity(input, fast_suffix_tree, 1, test_string="McCreight- Basic test no. "+str(i))

trie = Trie(natural_text_input[:2000])
check_validity(natural_text_input[:2000], trie, 10, test_string="Trie- law act test")
simple_suffix_tree = SuffixTreeNaive(natural_text_input)
check_validity(natural_text_input, simple_suffix_tree, 1000, test_string="Simple SuffixTree- law act text")
fast_suffix_tree = SuffixTree(natural_text_input)
check_validity(natural_text_input, fast_suffix_tree, 1000, test_string="McCreight- law act test" )

trie = Trie(artificial_text_input[:2000])
check_validity(artificial_text_input[:2000], trie, 10, test_string="Trie- artificial test")
simple_suffix_tree = SuffixTreeNaive(artificial_text_input)
check_validity(artificial_text_input, simple_suffix_tree, 1000, test_string="Simple SuffixTree- artificial text")
fast_suffix_tree = SuffixTree(artificial_text_input)
check_validity(artificial_text_input, fast_suffix_tree, 1000, test_string="McCreight- artificial test" )


#Benchmark
structures = [Trie, SuffixTreeNaive, SuffixTree]
print("NATURAL TEXT BENCHMARK:")
benchmark(natural_text_input, structures, 100)
benchmark(natural_text_input, structures, 1000)
benchmark(natural_text_input, structures, 2000)
benchmark(natural_text_input, structures, 3000)
benchmark(natural_text_input, structures[1:], 10000)
benchmark(natural_text_input, structures[1:], 50000)
benchmark(natural_text_input, structures[1:], 100000)
benchmark(natural_text_input, structures[1:], 150000)
benchmark(natural_text_input, structures[1:], 200000)
benchmark(natural_text_input, structures[1:])


print("ARTIFICIAL TEXT BENCHMARK:")
benchmark(artificial_text_input, structures, 100)
benchmark(artificial_text_input, structures, 1000)
benchmark(artificial_text_input, structures, 2000)
benchmark(artificial_text_input, structures, 3000)
benchmark(artificial_text_input, structures[1:], 10000)
benchmark(artificial_text_input, structures[1:], 50000)
benchmark(artificial_text_input, structures[1:], 100000)
benchmark(artificial_text_input, structures[1:], 150000)
benchmark(artificial_text_input, structures[1:])

quit()
