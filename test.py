from math import comb
from sympy.utilities.iterables import multiset_permutations

# sum = 0
# k = 22
# for i in range(0, k):
#     print(comb(k, i))
#     sum += comb(k, i)

# print(sum)

# def recursive_comb(bits):
#      """Creates all possible combinations of 0 & 1
#      for a given length
#      """
#      test = []

#      def calc_bits(bits, n=0):
#          if n.bit_length() <= bits:
#              comb_str = '{:0{}b}'.format(n, bits)
#              comb_list = [int(elem) for elem in comb_str]
#              test.append(comb_list) 
#              calc_bits(bits, n + 1)

#      calc_bits(bits)

#      return test

# all_comb = recursive_comb(10)

# print(all_comb)



length = 22

it = pow(2, length)
count = 0
prev_percent = 0
for n in range(0, length + 1):
    lst = [1] * n + [0] * (length - n)
    for perm in multiset_permutations(lst):
        count += 1
        if count/it * 100 > prev_percent:
            print(str(prev_percent) + "%")
            prev_percent += 5
