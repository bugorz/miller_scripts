from itertools import islice
import os
import re

my_dict = {}

input_file = 'ck_E7loBk_H3K27ac_rep1_S14_R1_001.fastq'
input_basename = os.path.splitext(input_file)[0]

with open(input_file, 'r') as f1:
    while True:
        array = []
        f1_unit = islice(f1, 4)

        if not f1_unit:
            break

        new_header = ""
        try:
            f1_header = str(f1_unit.next())
        except StopIteration:
            break

        new_header = f1_header.split(" ")[0]

        #print(new_header + " " + input_basename)
        my_dict[new_header] = input_basename

        f1_unit.next()
        f1_unit.next()
        f1_unit.next()

f1.close()

step4_file = "output.fastq"
output_file = open(input_basename + ".split.fastq", "w")
not_found_file = open("not_found.fastq", "w")

with open(step4_file, 'r') as step4:
    while True:
        array = []
        step4_unit = islice(step4, 4)

        if not step4_unit:
            break

        try:
            step4_header = str(step4_unit.next())
        except StopIteration:
            break

        step4_split = step4_header.split(' ')

        if (my_dict.has_key(str(step4_split[0]))):
            print("found")
            step4_header_part2 = re.split("\\+|:", step4_split[1])
            new_header = str(step4_split[0]) + "_" + str(step4_header_part2[3]) + " " + str(step4_split[1])
            output_file.write(new_header)
            output_file.write(step4_unit.next())
            output_file.write(step4_unit.next())
            output_file.write(step4_unit.next())
        else:
            print("not found")
            not_found_file.write(step4_header)
            not_found_file.write(step4_unit.next())
            not_found_file.write(step4_unit.next())
            not_found_file.write(step4_unit.next())

step4.close()
output_file.close()
not_found_file.close()
