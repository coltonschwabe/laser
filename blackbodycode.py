import numpy
from PIL import Image
import os
import math
import matplotlib.pyplot as plt
from scipy.constants import h
from scipy.constants import c
from scipy.constants import k

def BaslerRAW (File_Name):
    Data=numpy.fromfile(File_Name, dtype=numpy.uint8)
    ImageData=Data.reshape((1024,1280))

    red_tile = numpy.array([[0, 0],[0, 1]], dtype=numpy.bool_)
    green_tile_1 = numpy.array([[0, 1],[0, 0]], dtype=numpy.bool_)
    green_tile_2 = numpy.array([[0, 0],[1, 0]], dtype=numpy.bool_)
    blue_tile = numpy.array([[1, 0],[0, 0]], dtype=numpy.bool_)
    red_index_array=numpy.tile(red_tile,(512,640))
    green_index_array_1=numpy.tile(green_tile_1,(512,640))
    green_index_array_2=numpy.tile(green_tile_2,(512,640))
    blue_index_array=numpy.tile(blue_tile,(512,640))
    Red_layer=ImageData[red_index_array].reshape((512,640))
    Green_layer_1=ImageData[green_index_array_1].reshape((512,640))
    Green_layer_2=ImageData[green_index_array_2].reshape((512,640))
    Blue_layer=ImageData[blue_index_array].reshape((512,640))

    Image=numpy.empty([512,640,3], numpy.uint8)
    Image[:,:,0]=Red_layer
    Image[:,:,1]=((Green_layer_1.astype('d')+Green_layer_2.astype('d'))/2).astype('B')
    Image[:,:,2]=Blue_layer
    return Image

# Import image
#FileName="FB450 NE10B.raw"
RedOnData=BaslerRAW("redon.raw")
GreenOnData=BaslerRAW("greeon.raw")
BlueOnData=BaslerRAW("blueon.raw")

RedOffData=BaslerRAW("redoff.raw")
BlueOffData=BaslerRAW("blueoff.raw")
GreenOffData=BaslerRAW("greenoff.raw")

redtotal = numpy.sum(RedOnData[:,:,0])
bluetotal = numpy.sum(BlueOnData[:,:,2])
greentotal = numpy.sum(GreenOnData[:,:,1])

redbacktotal = numpy.sum(RedOffData[:,:,0])
bluebacktotal = numpy.sum(BlueOffData[:,:,2])
greenbacktotal = numpy.sum(GreenOffData[:,:,1])

print("Red Total:" + str(redtotal))
print("Green Total:" + str(greentotal))
print("Blue Total:" + str(bluetotal))

print("RedB Total:" + str(redbacktotal))
print("GreenB Total:" + str(greenbacktotal))
print("BlueB Total:" + str(bluebacktotal))

#exposure times for [red, green, blue]
exposure = [5000, 20000, 70000]

#calculating intensity for each color
redI = (redtotal - redbacktotal)/exposure[0]
greenI = (greentotal - greenbacktotal)/exposure[1]
blueI = (bluetotal - bluebacktotal)/exposure[2]

# gets frequencies
strfreqs = []
with open("FB450-40.txt", "rt") as cont:
    for line in cont:
        strfreqs.append(line)

f = []

#extracts frequencies from txt file
for unit in strfreqs:
    f.append(float(unit[3:12]) * 10**(int(unit[15])-9))

T = 3000
intensity = []

for l in f:
    result = (2*(math.pi)*h*c*c/(l**5))/(math.exp(h*c/(l*k*T)) - 1)

    intensity.append(result)

plt.figure(1)
plt.plot(f,intensity,'-r')
plt.show()

#newim=Image.fromarray(Data)
#newim.show()

# Import transmission data for red pixels of the camera sensor
#TD=numpy.loadtxt('Basler_red.txt')
#w=TD[:,0] #array of wavelengths
#Basler_red=TD[:,1] #array of transmissions
##plt.figure(1)
#plt.plot(w,Basler_red,'-r')
#plt.show()
