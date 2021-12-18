import math

class RegularNumber:
    def __init__(self, value):
        self.value = value
        self.number_at_left = None
        self.number_at_right = None
        
    def get_magnitude(self):
        return self.value
    
    def __str__(self):
        return str(self.value)

class Pair:
    def __init__(self, parent, left, right):
        self.parent = parent
        self.left = left
        self.right = right
        left.parent = self
        right.parent = self
        
        # Attach rightmost RN child of left unit to leftmost RN child of right unit.
        rightmost_number_in_left_unit = find_rightmost_child(left)
        leftmost_number_in_right_unit = find_leftmost_child(right)
        rightmost_number_in_left_unit.number_at_right = leftmost_number_in_right_unit
        leftmost_number_in_right_unit.number_at_left = rightmost_number_in_left_unit
    
    def get_magnitude(self):
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()
    
    def __str__(self):
        return "[%s, %s]" % (self.left, self.right)

def find_rightmost_child(node):
    while isinstance(node, Pair):
        node = node.right
    return node

def find_leftmost_child(node):
    while isinstance(node, Pair):
        node = node.left
    return node

def add_snailfish_numbers(n1, n2):
    unreduced_sum = Pair(None, n1, n2)
    while True:
        a = explode_next(unreduced_sum)
        if a != None:
            unreduced_sum = a
            #print("Exploded: %s" % (unreduced_sum))
            continue
        
        if split_next(unreduced_sum):
            #print("Split: %s" % (unreduced_sum))
            continue
        
        break
    return unreduced_sum

#################### EXPLOSIONS
def explode_next(n):
    exploding_pair = find_first_exploding_pair(n, 0)
    if not exploding_pair:
        print("No exploding pair found")
        return None
    
    # Find marker to replace with 0
    parent = exploding_pair.parent
    new_zero = RegularNumber(0)
    new_zero = parent
        
    # Transfer the left value to the left
    if exploding_pair.left.number_at_left:
        exploding_pair.left.number_at_left.value += exploding_pair.left.value
        exploding_pair.left.number_at_left.number_at_right = new_zero
        new_zero.number_at_left = exploding_pair.left.number_at_left
    
    # Transfer the right value to the right
    if exploding_pair.right.number_at_right:
        exploding_pair.right.number_at_right.value += exploding_pair.right.value
        exploding_pair.right.number_at_right.number_at_left = new_zero
        new_zero.number_at_right = exploding_pair.right.number_at_right
    
    # Actually replace marker with 0
    if parent.left == exploding_pair:
        parent.left = new_zero
    elif parent.right == exploding_pair:
        parent.right = new_zero
    
    return n
    
def find_first_exploding_pair(n, current_depth):
    print("Testing %s at depth %s" % (n, current_depth))
    if isinstance(n, RegularNumber):
        return False
    elif current_depth == 3:
        if isinstance(n.left, Pair):
            return n.left
        elif isinstance(n.right, Pair):
            return n.right
        else:
            return False
    else:
            t1 = find_first_exploding_pair(n.left, current_depth + 1)
            if t1:
                return t1
            t2 = find_first_exploding_pair(n.right, current_depth + 1)
            if t2:
                return t2
    return False

#### REDUCTIONS
def split_next(n):
    if isinstance(n, RegularNumber):
        if n.value >= 10:
            # Split
            new_pair = Pair(n.parent,
                            RegularNumber(math.floor(n.value / 2)),
                            RegularNumber(math.ceil(n.value / 2)))
            new_pair.left.number_at_left = n.number_at_left
            if n.number_at_left:
                n.number_at_left.number_at_right = new_pair.left
            new_pair.right.number_at_right = n.number_at_right
            if n.number_at_right:
                n.number_at_right.number_at_left = new_pair.right
                
            if n.parent:
                if n.parent.left == n:
                    n.parent.left = new_pair
                elif n.parent.right == n:
                    n.parent.right = new_pair
            return True
        else:
            return False
    else:
        if split_next(n.left): return True
        elif split_next(n.right): return True
    return False

def make_snailfish_number(arr):
    if isinstance(arr, int): return RegularNumber(arr)
    else:
        return Pair(None, make_snailfish_number(arr[0]), make_snailfish_number(arr[1]))

snailfish_number_raw = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
snailfish_number_raw="""[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]"""
snailfish_number_raw="""[[[5,3],[[8,6],[7,1]]],[8,0]]
[2,[[3,6],[[3,6],1]]]
[9,[[[7,1],3],3]]
[[[3,[3,9]],[3,9]],[[[7,4],4],3]]
[[[[1,8],[9,6]],[[1,1],2]],[[[3,1],4],6]]
[[[[4,0],[2,5]],[9,4]],[[[6,9],[0,1]],1]]
[[1,[[3,7],[5,3]]],[[[9,9],[9,6]],[0,9]]]
[[[2,[9,9]],[3,3]],[[[5,1],1],[9,0]]]
[3,[3,9]]
[[[[1,6],[4,3]],3],[[9,[4,0]],[[2,0],4]]]
[[2,[6,7]],[6,2]]
[[[9,[3,3]],[5,[8,7]]],[9,[[7,7],[0,6]]]]
[[[4,[7,5]],[9,[9,0]]],0]
[7,[[3,8],8]]
[[[7,0],[9,9]],8]
[4,[[[9,4],[8,1]],[2,[3,5]]]]
[[[2,6],[5,[5,5]]],[[[7,0],[2,2]],[9,8]]]
[[0,[0,[1,1]]],9]
[[[2,[7,9]],1],[8,[[8,8],[6,8]]]]
[[8,[[5,3],[4,4]]],[0,[2,[3,7]]]]
[[[2,[1,3]],5],[[9,[9,8]],[[8,4],[9,7]]]]
[[[9,9],[[0,1],[6,2]]],4]
[[[0,3],[[8,0],4]],[[7,5],2]]
[[[0,[1,7]],4],[[7,4],[[0,6],[2,8]]]]
[[[2,[8,3]],1],[[[5,6],9],[[6,8],[3,9]]]]
[[[0,[5,9]],[7,7]],[4,[[2,3],[6,8]]]]
[[2,[9,7]],[5,0]]
[[1,[[8,1],[1,7]]],[3,5]]
[[[[2,7],0],[[8,6],[0,4]]],[[1,[5,5]],[[0,1],[2,8]]]]
[[0,4],[[1,1],[9,[6,2]]]]
[[[6,[6,0]],7],[3,[4,[3,7]]]]
[[[3,[9,6]],0],9]
[6,[[7,[1,6]],[7,8]]]
[[4,[8,[6,6]]],[[[0,1],1],[6,[9,0]]]]
[[[8,4],[2,[6,0]]],[[9,5],[[7,9],0]]]
[[[7,7],[[7,3],9]],[[3,7],6]]
[[7,[9,0]],5]
[[1,5],[2,[[6,4],[5,0]]]]
[0,[[0,6],[[5,1],7]]]
[[3,0],9]
[1,[8,[[9,8],[6,5]]]]
[[[7,8],[0,[8,2]]],[1,[1,[2,4]]]]
[[[2,[5,6]],3],[[4,[9,5]],[9,8]]]
[[[[0,0],[8,7]],[[9,1],2]],[[9,[6,9]],4]]
[8,[[9,6],[[2,4],5]]]
[[[2,[0,4]],[2,[3,7]]],[[[8,1],[9,4]],4]]
[8,2]
[[[3,7],0],7]
[[0,1],[[2,4],[1,5]]]
[[6,[2,2]],[[[3,3],1],[[4,0],6]]]
[2,[[5,8],6]]
[7,[5,[5,5]]]
[[1,[[2,4],0]],[[2,[8,3]],[4,[3,7]]]]
[[[5,1],[[7,6],3]],[[[4,8],[5,9]],8]]
[[[8,[3,5]],[[1,8],[0,3]]],[[0,[1,8]],[6,8]]]
[[[[0,8],8],[[0,5],[7,6]]],[2,1]]
[5,[4,[7,0]]]
[[7,[[6,5],[5,2]]],[4,6]]
[[2,6],[[2,1],[[2,3],[2,3]]]]
[[[0,[4,9]],[3,[8,9]]],[[[9,0],[6,2]],[2,1]]]
[6,[6,[0,[3,1]]]]
[[[9,8],[[4,9],8]],[[[3,2],[9,1]],5]]
[[[[2,6],[0,9]],[2,7]],[1,[9,2]]]
[[[5,[7,9]],[[2,3],2]],[[[9,5],0],[[9,6],[3,3]]]]
[[[[6,3],[2,1]],[[7,6],[6,8]]],[[[0,2],[8,0]],[0,[9,5]]]]
[[[[2,0],0],1],[4,[[3,6],[3,1]]]]
[[[3,1],[5,0]],[[[3,3],[0,2]],[5,8]]]
[[[[1,0],8],[[2,3],[2,1]]],[[4,[5,5]],[[9,8],3]]]
[[[8,[0,5]],[9,9]],[[[7,0],1],[[7,2],7]]]
[[[[3,0],4],7],[[3,9],[4,[9,7]]]]
[[[8,3],0],[6,5]]
[[2,[[3,8],6]],[[[3,2],[1,4]],[[1,6],[9,4]]]]
[[[[6,2],[4,7]],[3,9]],[[1,[6,5]],4]]
[[[[8,3],2],[8,2]],5]
[[[9,[9,0]],[4,7]],[[[5,9],2],6]]
[4,[[6,0],3]]
[[[5,9],[8,3]],0]
[[[[6,1],[4,8]],[9,[1,6]]],1]
[[[8,5],[2,2]],6]
[2,[5,[[5,7],[6,0]]]]
[[[[3,6],[2,3]],6],[[6,[6,5]],[[6,4],[6,9]]]]
[[4,[[1,3],1]],1]
[[2,[7,[4,3]]],0]
[[8,[[1,1],1]],[[4,1],[[9,6],[1,3]]]]
[[8,1],[3,[2,[5,7]]]]
[8,[[[2,4],[8,3]],[[8,7],[2,8]]]]
[[0,[[5,7],8]],[[3,[6,6]],[0,8]]]
[7,[[1,3],[2,4]]]
[[[2,0],[0,1]],[[[8,9],[7,0]],[3,6]]]
[[[1,6],[[6,9],[6,3]]],[2,[1,1]]]
[[1,[7,[8,1]]],[[[0,3],[9,1]],[[1,5],2]]]
[[[[1,3],2],1],[[[0,4],5],[[5,0],[1,1]]]]
[[[2,[0,1]],[5,6]],4]
[[8,3],[[6,4],[[0,9],5]]]
[[[[2,7],4],[7,0]],[[[6,7],2],[3,8]]]
[[[[9,3],9],[[2,9],[9,0]]],[[[7,5],3],[[8,8],8]]]
[[[[0,1],[8,4]],[4,[8,5]]],[2,[1,[0,2]]]]
[[5,[[3,5],[9,2]]],[[[2,2],3],[[4,7],3]]]
[[[7,8],8],2]
[9,[2,1]]"""
snailfish_number_raw = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
snailfish_number_raw = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""

#UNSAFE
snailfish_number = [make_snailfish_number(eval(line)) for line in snailfish_number_raw.splitlines()]

sum = add_snailfish_numbers(snailfish_number[0], snailfish_number[1])
print("The sum is currently: %s" % (sum))
for i in range(2, len(snailfish_number)):
    sum = add_snailfish_numbers(sum, snailfish_number[i])
    print("Added: %s" % (snailfish_number[i]))
    print("The sum is currently: %s" % (sum))

print(sum)
print(sum.get_magnitude())