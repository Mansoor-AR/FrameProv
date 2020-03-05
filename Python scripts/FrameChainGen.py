from __future__ import division

import matplotlib.pyplot as plt
import picamera
import picamera.array
import numpy as np
import hashlib
'''
TODO:
Update dev to python3.6 to use sha3
Experiment with Raw Bayer Video capture, will require major engineering-
Currently we work on RGB feed from GPU

'''
np.set_printoptions(threshold=np.nan) #print entire array
initial_seed = "this should be amazingly random"
prev = hashlib.sha256()
prev.update(bytes(initial_seed, 'UTF-8'))
prevdigest = prev.digest()
print(prevdigest)

class MyAnalysis(picamera.array.PiRGBAnalysis):
    def __init__(self, camera):
        super(MyAnalysis, self).__init__(camera)
        self.frame_num = 0

    def analyse(self, a):
        #implement hashing here
##        r = int(np.mean(a[..., 0]))
##        g = int(np.mean(a[..., 1]))
##        b = int(np.mean(a[..., 2]))
##        c = (r << 16) | (g << 8) | b
##        print("Frame number= "+ str(self.frame_num))
##        print('Average color: #%06x' % c)
        global prevdigest
        a.setflags(write=1) #Now prepare to write over the image
        i = 0
        j = 0
        for b in prevdigest:
            if i%3 == 0:
                a[j,50,0] = b
            if i%3 == 1:
                a[j,50,1] = b
            if i%3 == 2:
                a[j,50,2] = b
                j = j + 1
            i = i+1

        a.flags.writeable = False
        #Need >=python3.6 for sha3; use that in production
        #hasher = hashlib.sha3_256()
        #For now, we'll fall back to sha256
        hasher = hashlib.sha256()
        hasher.update(a.data.tobytes()) #hash updated
        prevdigest = hasher.digest()
        #Now save the frame
        np.save("testspace/frame_"+str(self.frame_num),a)
##            plt.imshow(a[:,:,0])
##            plt.show()
        self.frame_num += 1
        print(prevdigest)


with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 24
    time_to_record = 5
    output = MyAnalysis(camera)
    camera.start_recording(output, 'rgb')
    camera.wait_recording(time_to_record)
    camera.stop_recording()
    print('FPS: %.2f' % (output.frame_num / time_to_record))
    print("Total frames= " + str(output.frame_num))
    
