import os
from glob import glob as xmlFiles

file_name = "trainval.txt"
save_folder = "../annotations"
ann_folder = save_folder + '/xmls'
out = ""

for tree in [ann_folder]:
    print(xmlFiles(tree + '/*.xml'))
    for file in xmlFiles(tree + '/*.xml'):
        base = os.path.basename(file)
        out += str(os.path.splitext(base)[0]) + "\n"

text_file = open(os.path.join(save_folder, file_name), "w")
text_file.write(out)
text_file.close()
