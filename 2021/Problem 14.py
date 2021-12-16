from collections import defaultdict

polymer_template = "CNBPHFBOPCSPKOFNHVKV"
xpolymer_template = "NNCB"

polymer_start = "C"
polymer_end = "V"
polymer_pairs = defaultdict(lambda: 0)

for i in range(0, len(polymer_template)- 1):
    polymer_pairs[polymer_template[i:i+2]] += 1

pair_insertion_rules_raw = """CS -> S
FB -> F
VK -> V
HO -> F
SO -> K
FK -> B
VS -> C
PS -> H
HH -> P
KH -> V
PV -> V
CB -> N
BB -> N
HB -> B
HV -> O
NC -> H
NF -> B
HP -> B
HK -> S
SF -> O
ON -> K
VN -> V
SB -> H
SK -> H
VH -> N
KN -> C
CC -> N
BF -> H
SN -> N
KP -> B
FO -> N
KO -> V
BP -> O
OK -> F
HC -> B
NH -> O
SP -> O
OO -> S
VC -> O
PC -> F
VB -> O
FF -> S
BS -> F
KS -> F
OV -> P
NB -> O
CF -> F
SS -> V
KV -> K
FP -> F
KC -> C
PF -> C
OS -> C
PN -> B
OP -> C
FN -> F
OF -> C
NP -> C
CK -> N
BN -> K
BO -> K
OH -> S
BH -> O
SH -> N
CH -> K
PO -> V
CN -> N
BV -> F
FV -> B
VP -> V
FS -> O
NV -> P
PH -> C
HN -> P
VV -> C
NK -> K
CO -> N
NS -> P
VO -> P
CP -> V
OC -> S
PK -> V
NN -> F
SC -> P
BK -> F
BC -> P
FH -> B
OB -> O
FC -> N
PB -> N
VF -> N
PP -> S
HS -> O
HF -> N
KK -> C
KB -> N
SV -> N
KF -> K
CV -> N
NO -> P"""
xpair_insertion_rules_raw = """CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

pair_insertion_rules = dict()
for line in pair_insertion_rules_raw.splitlines():
    pair, insertion = line.split(" -> ")
    pair_insertion_rules[pair] = (pair[0] + insertion, insertion + pair[1])
    #print(pair_insertion_rules[pair][0])

def apply_rules(old_polymer_pairs):
    new_polymer_pairs = defaultdict(lambda: 0)
    for pair, count in old_polymer_pairs.items():
        print(pair_insertion_rules[pair])
        new_polymer_pairs[pair_insertion_rules[pair][0]] += count
        new_polymer_pairs[pair_insertion_rules[pair][1]] += count
    return new_polymer_pairs

for i in range(0, 40):
    polymer_pairs = apply_rules(polymer_pairs)
    
print(polymer_pairs)

doubled_element_count = defaultdict(lambda: 0)
doubled_element_count[polymer_start] += 1
doubled_element_count[polymer_end] += 1
for pair, count in polymer_pairs.items():
    doubled_element_count[pair[0]] += count
    doubled_element_count[pair[1]] += count
# 5810-1470/2 = 2170
#1493794663720
#6338684186286
elements_counts = sorted(doubled_element_count.items(), key = lambda pair: pair[1])

print(elements_counts)
print((elements_counts[-1][1] - elements_counts[0][1]) / 2)