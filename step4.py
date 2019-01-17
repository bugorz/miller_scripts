from itertools import islice

# Output file
output_file = open("output.fastq", "w")

with open('Undetermined_S0_R1_001_H10k.fastq', 'r') as f1, open('Undetermined_S0_R2_001_H10k.fastq', 'r') as f2, open('Undetermined_S0_R3_001_H10k.fastq', 'r') as f3:
    while True:
        array = []
        f1_unit = islice(f1, 4)
        f2_unit = islice(f2, 4)
        f3_unit = islice(f3, 4)

        if not f1_unit:
            break

        new_header = ""
        f1_header = f1_unit.next()
        f1_header_string = str(f1_header).rstrip()
        f1_header_string = f1_header_string[:-1]

        new_header += f1_header_string
        f2_unit.next()
        f2_sequence = f2_unit.next()
        new_header += str(f2_sequence).rstrip()
        f2_unit.next()
        f2_unit.next()

        new_header += "+"

        f3_unit.next()
        f3_sequence = f3_unit.next()
        new_header += str(f3_sequence).rstrip()
        f3_unit.next()
        f3_unit.next()

        array.append(new_header)
        array.append(str(f1_unit.next()).rstrip())
        array.append(str(f1_unit.next()).rstrip())
        array.append(f1_unit.next())

        new_unit = '\n'.join(array)
        output_file.write(new_unit)

output_file.close()
f1.close()
f2.close()
f3.close()