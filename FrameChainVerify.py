import numpy as np
import hashlib
import os
import glob
import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

initial_seed = "this should be amazingly random"
prev = hashlib.sha256()
prev.update(bytes(initial_seed, 'UTF-8'))
prevdigest = prev.digest()
print(prevdigest)
matched = True
#Here we read the frames from a directory and verify that it is a valid framechain
for file in sorted(glob.glob('./testspace/*.npy'), key=numericalSort):
    print("Now processing file: "+file)
    a = np.load(file)
    i=0
    j=0
    #global prevdigest
    for b in prevdigest:
        if i%3 == 0:
            if int(b) != a[j,50,0]:
                print("Disparity found at frame: " + file)
                print("Disparity at byte " + str(i))
                matched = False
                break
        if i%3 == 1:
            if int(b) != a[j,50,1]:
                print("Disparity found at frame: " + file)
                print("Disparity at byte " + str(i))
                matched = False
                break
        if i%3 == 2:
            if int(b) != a[j,50,2]:
                print("Disparity found at frame: " + file)
                print("Disparity at byte " + str(i))
                matched = False
                break
            else:
                j = j+1
        i = i+1

    if not matched:
        break
    a.flags.writeable = False
    hasher = hashlib.sha256()
    hasher.update(a.data.tobytes())
    prevdigest = hasher.digest()
    print(prevdigest)

if matched:
    print("Successfully verified the framechain!")
        
