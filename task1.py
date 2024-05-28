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
        a = random.randint(1, 69997)
        b = random.randint(1, 69997)
        hash_func = lambda x, a=a, b=b, m=m: (a * x + b) % m
        hash_functions_list.append(hash_func)
    return hash_functions_list

hash_functions_list = generate_hash_functions(50)
def myhashs(object):
    result = []
    for f in hash_functions_list:
        result.append(f(object))
    return result

existing_users = set()
fpr = 0

with open(output_filename, 'w') as text_file:
    text_file.write('Time,FPR\n')
    for ask in range(num_asks):
        stream_users = bx.ask(input_file_path, stream_size)

        for obj in stream_users:
            object_int = int(binascii.hexlify(obj.encode('utf8')),16)
            indices = myhashs(object_int)

            for idx in indices:
                if n_bit_array[idx] == 0:
                    n_bit_array[idx] = 1
                elif object_int not in existing_users:
                    fpr += 1
            existing_users.add(object_int)

        total_positive_predictions = sum(n_bit_array)
        false_positives = fpr

        fpr = false_positives / total_positive_predictions

        text_file.write(str(ask) + ',' + str(fpr) + '\n')

end = time.time()
print("Duration: ", end-start)





