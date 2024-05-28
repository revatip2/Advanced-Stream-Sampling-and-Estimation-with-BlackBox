from blackbox import BlackBox
import binascii
import sys
import math
import time
import random

def res_sampling():
    start = time.time()
    random.seed(553)
    bx = BlackBox()
    input_file_path = sys.argv[1]
    stream_size = int(sys.argv[2])
    num_asks = int(sys.argv[3])
    output_filename = sys.argv[4]

    with open(output_filename, 'w') as text_file:
        text_file.write('seqnum,0_id,20_id,40_id,60_id,80_id\n')
        sample = []
        user_index = 0
        users_processed = 0
        for ask in range(num_asks):
            # sample = []
            # user_index = 0
            # users_processed = 0
            all_elements = bx.ask(input_file_path, stream_size)
            # print(len(all_elements))
            for user in all_elements:
                users_processed += 1
                # print(users_processed)
                user_index += 1
                if len(sample) < 100:
                    sample.append(user)

                else:
                    random_fp = random.random()
                    if random_fp < len(sample)/user_index:
                        index_rep = random.randint(0,99)
                        sample[index_rep] = user
                # print(len(sample))

                if users_processed % 100 == 0:
                    # print(users_processed)
                    text_file.write(str(users_processed) + ',' + sample[0] + ',' + sample[20] + ',' + sample[40] + ',' + sample[60] + ',' + sample[80]+'\n')

    end = time.time()
    print("Duration: ", end - start)

if __name__ == '__main__':
    res_sampling()






