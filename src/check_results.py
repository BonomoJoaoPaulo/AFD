import filecmp
import os

CUR_PATH = os.path.dirname(__file__)
OUTPUTS_PATH = os.path.join(CUR_PATH, "../outputs")

for file1 in os.listdir(OUTPUTS_PATH):
    if file1[0] == "e":
        continue
    for file2 in os.listdir(OUTPUTS_PATH):
        if file2[-5] == file1[-5] and file1 != file2:
            f1 = os.path.join(OUTPUTS_PATH, file1)
            f2 = os.path.join(OUTPUTS_PATH, file2)
            result = filecmp.cmp(f1, f2)
            print(f"{file1} == {file2}? {result}")
