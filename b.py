from blackbox import BlackBox
import binascii
import sys
import math
import time
import random

bx = BlackBox()

input_file_path = sys.argv[1]
stream_size = int(sys.argv[2])
num_asks = int(sys.argv[3])
output_filename = sys.argv[4]

start = time.time()

n_bit_array = [0] * 69997

def generate_hash_functions(num_functions):
    hash_functions_list = []
    m = 69997
    for i in range(num_functions):
        a = random.randint(1, 9997)
        b = random.randint(1, 9997)
        hash_func = lambda x, a=a, b=b, m=m: (a * x + b) % m
        hash_functions_list.append(hash_func)
    return hash_functions_list

hash_functions_list = generate_hash_functions(60)
size_of_groups = 2
def myhashs(object):
    result = []
    for f in hash_functions_list:
        result.append(f(object))
    return result

with open(output_filename, 'w') as text_file:
    text_file.write('Time,Ground Truth,Estimation\n')
    summ = 0
    for ask in range(num_asks):
        bit_string = []
        max_R = {}
        stream_users = bx.ask(input_file_path, stream_size)

        for obj in stream_users:
            object_int = int(binascii.hexlify(obj.encode('utf8')), 16)
            indices = myhashs(object_int)

            for i, idx in enumerate(indices, 1):
                # print(i, idx, '\n')
                bit_string = bin(idx)[2:]
                # print(bit_string, '\n')
                trail_zeros = len(bit_string) - len(bit_string.rstrip('0'))
                # print(trail_zeros, '\n')
                max_R[f'h{i}'] = max(max_R.get(f'h{i}', 0), trail_zeros)
                # print('a: ',max_R)

        for key in max_R:
            max_R[key] = 2**float(max_R[key])

        values = list(max_R.values())
        group_averages = []

        for i in range(0, len(values), size_of_groups):
            group = values[i:i + size_of_groups]
            average = sum(group) / len(group)
            group_averages.append(average)

        sorted_averages = sorted(group_averages)

        length = len(sorted_averages)
        if length % 2 == 0:
            median_of_averages = (sorted_averages[length // 2 - 1] + sorted_averages[length // 2]) / 2
        else:
            median_of_averages = sorted_averages[length // 2]

        text_file.write(str(ask) + ',' + str(len(stream_users)) + ',' + str(int(median_of_averages)) + '\n')

        summ += int(median_of_averages)
        sum_ask = int(num_asks * len(stream_users))
    print(summ/sum_ask)

end = time.time()
print("Duration: ", end - start)








