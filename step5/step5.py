#!/usr/bin/env python

from itertools import islice
import os, fnmatch, re

dictionary = {}

# File handler cache
file_object_cache = {}

# list files begin with 'ck_' and end with 'fastq' extension
# Then, for every 4 lines add
# the first part of the header as key, filename(w/o '.fastq' extension) as value to dictionary.
listOfFiles = os.listdir('.')
pattern = "ck_*.fastq"
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
            print (entry)
            filename_without_extension = os.path.splitext(entry)[0]

            # Add to file_handler cache
            output_file_name = filename_without_extension + ".split"
            # Note that we are using 'w+', write append. Using 'w' will overwrite the previous result.
            file_object_cache[filename_without_extension] = open(output_file_name, "w+")

            with open(entry, 'r') as f1:
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

                    # print(new_header + " " + filename_without_extension)
                    dictionary[new_header] = filename_without_extension

                    f1_unit.next()
                    f1_unit.next()
                    f1_unit.next()

                f1.close()


# Please change this to the file name you want
step4_file = "output.fastq"

# For fastq that can't find a home
not_found_file = open("not_found.fastq", "w")

with open(step4_file, 'r') as step4:
    while True:
        array = []
        step4_unit = islice(step4, 4)

        try:
            step4_header = str(step4_unit.next())
        except StopIteration:
            break

        step4_split = step4_header.split(' ')

        if (dictionary.has_key(str(step4_split[0]))):
            print("found")
            step4_header_part2 = re.split("\\+|:", step4_split[1])
            new_header = str(step4_split[0]) + "_" + str(step4_header_part2[3]) + " " + str(step4_split[1])

            output_file = file_object_cache.get(dictionary.get(str(step4_split[0])))
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

# Close all file handlers in the cache
for file_object in file_object_cache.values():
    file_object.close()

# Close Step 4 output
step4.close()
# Close Homeless output
not_found_file.close()
