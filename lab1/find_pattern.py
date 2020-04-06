import time

def naive_string_matching(text, pattern):
    result=[]
    for s in range(0, len(text) - len(pattern) + 1):
        if(pattern == text[s:s+len(pattern)]):
            result.append(s)
    return result
def sigma(x, pattern):
    return max([k for k in range(0, len(pattern)+1) if x.endswith(pattern[0:k])])

def transition_table(pattern):
    result = []
    for q in range(0, len(pattern) + 1):
        result.append({})
        for a in set(pattern):
            result[q][a] = sigma(pattern[0:q]+a, pattern)
    return result

def fa_string_matching(text, delta):
    q = 0
    result=[]
    for s in range(0, len(text)):
        q = delta[q].get(text[s], 0)
        if(q == len(delta) - 1):
            result.append(s+1-q)
    return result
def kmp_string_matching(text, pattern, pi):
    result=[]

    q = 0
    for i in range(0, len(text)):
        while(q > 0 and pattern[q] != text[i]):
            q = pi[q-1]
        if(pattern[q] == text[i]):
            q = q + 1
        if(q == len(pattern)):
            result.append(i+1-q)
            q = pi[q-1]
    return result

def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while(k > 0 and pattern[k] != pattern[q]):
            k = pi[k-1]
        if(pattern[k] == pattern[q]):
            k = k + 1
        pi.append(k)
    return pi




def test(text, pattern):
#NAIVE
    start_time = time.time()
    res1 = naive_string_matching(text, pattern);
    print("Naive algorithm: %s seconds" % (time.time() - start_time))
#FA
    start_time = time.time()
    delta = transition_table(pattern)
    print("Finite machine algorithm initialization: %s seconds" % (time.time() - start_time))
    start_time = time.time()
    res2 = fa_string_matching(text, delta)
    print("Finite machine algorithm execution: %s seconds" % (time.time() - start_time))
    if not res1 == res2:
        raise Exception("RESULTS ARE DIFFERENT!")
#KMP
    start_time = time.time()
    pi = prefix_function(pattern)
    print("KMP algorithm initialization: %s seconds" % (time.time() - start_time))
    start_time = time.time()
    res3 = kmp_string_matching(text, pattern, pi)
    print("KMP algorithm execution: %s seconds" % (time.time() - start_time))
    if not res2 == res3:
        raise Exception("RESULTS ARE DIFFERENT!")





def test_big_files(filename, pattern):

#NAIVE
    f = open(filename, "rt", encoding='UTF8')
    res1=[]
    start_time = time.time()
    for line in f:
        res1.extend(naive_string_matching(line, pattern))
    print("Naive algorithm: %s seconds" % (time.time() - start_time))
    f.close()
#FA
    f = open(filename, "rt", encoding='UTF8')
    res2 = []
    start_time = time.time()
    delta = transition_table(pattern)
    print("Finite machine algorithm initialization: %s seconds" % (time.time() - start_time))
    start_time = time.time()
    for line in f:
        res2.extend(fa_string_matching(line, delta))
    print("Finite machine algorithm execution: %s seconds" % (time.time() - start_time))
    if not res1 == res2:
        f.close()
        raise Exception("RESULTS ARE DIFFERENT!")
    f.close()
#KMP
    start_time = time.time()
    pi = prefix_function(pattern)
    print("KMP algorithm initialization: %s seconds" % (time.time() - start_time))
    f = open(filename, "rt", encoding='UTF8')
    res3 = []
    start_time = time.time()
    for line in f:
        res3.extend(kmp_string_matching(line, pattern, pi))
    print("KMP algorithm execution: %s seconds" % (time.time() - start_time))
    if not res2 == res3:
        f.close()
        raise Exception("RESULTS ARE DIFFERENT!")
    f.close()










file = open("ustawa.txt", "rt", encoding='UTF8')
text = file.read()
file.close()
print("\n\n3. Occurences of \"art\" in law act:\n")
print("Naive algorithm results:")
print(naive_string_matching(text, "art"))
delta = transition_table("art")
print("\nFinite machine algorithm results:")
print(fa_string_matching(text, delta))
print("\nKMP algorithm results:")
pi = prefix_function("art")
print(kmp_string_matching(text, "art", pi))

print("\n\n4.Comparing time of finding \"art\" in law act:\n")
test(text, "art")

print("\n5.Comparing time of finding \"kruszwil\" in polish wikipedia:\n")
test_big_files("wikipedia-tail-kruszwil.txt", "kruszwil")

print("\n6.Worst case scenario for naive algorithm")

f=open("ustawa.txt", "rt", encoding='UTF8')
pattern = "cccccccccc"
for i in range(10):
    pattern += pattern
test(f.read(), pattern)
f.close()

print("\n7.Worst case scenario for initializing finite machine algorithm\n")

pattern = "qwertyuiop[]asdfghjkl;'zxcvbnm,./"
for i in range(5):
    pattern += pattern

start_time = time.time()
pi = transition_table(pattern)
print("Finite machine algorithm initialization: %s seconds" % (time.time() - start_time))
start_time = time.time()
pi = prefix_function(pattern)
print("KMP algorithm initialization: %s seconds" % (time.time() - start_time))