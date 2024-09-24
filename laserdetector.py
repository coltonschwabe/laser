import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import math
from scipy.optimize import curve_fit

freqPercentage = [['5', 77.2],['7', 111.8],['9', 148.5],['11', 178.0], ['13', 202.8], ['15', 229.7],['17', 243.5],['19', 259.8],['21', 279.8],['23', 286.7],['25', 297.0]]

def drawcenter(a, b):
    for y in range(np.shape(LaserSpotData)[0]):
        LaserSpotData[y][a-1] = [255, 255, 255]
        LaserSpotData[y][a] = [255, 255, 255]
        LaserSpotData[y][a+1] = [255, 255, 255]

    for x in range(np.shape(LaserSpotData)[1]):
        LaserSpotData[b - 1][x] = [255, 255, 255]
        LaserSpotData[b][x] = [255, 255, 255]
        LaserSpotData[b + 1][x] = [255, 255, 255]

def getPos(data):
    xsum = 0
    ysum = 0
    xnum = 0
    ynum = 0

    # loops through all pixels on image
    for y in range(np.shape(data)[0]):
        for x in range(np.shape(data)[1]):
            if (data[y][x][0] >= 100): # if pixel has a certain amount of red in it
                xsum += x*(data[y][x][0]/100)
                xnum += data[y][x][0]/100
                ysum += y*(data[y][x][0]/100)
                ynum += data[y][x][0]/100

    xavg = round(xsum / xnum) # takes average off x value of all red pixels
    yavg = round(ysum / ynum) # takes average off y value of all red pixels
    return [xavg, yavg]

x=[]
y=[]

#width of images in pixels
imagewidth = np.shape(np.array(Image.open('25percent.jpg')))[1]

for i in range(0, len(freqPercentage)):
    #Import the image as an object and plot it
    LaserSpotImage = Image.open(freqPercentage[i][0] + 'percent.jpg')

    x.append(freqPercentage[i][1]) #adds frequency    

    #LaserSpotImage.show()
    # Create a numpy array form the image object
    LaserSpotData=np.array(LaserSpotImage)

    averages = getPos(LaserSpotData)
    y.append((imagewidth-averages[0])*0.0000048) #adds x position of spot in meters

def func(x, a, b):
    return a*x + b

# y = Ax + B, where x = frequency and y = x-displacement on camera
[A, B], pcovmatrix = curve_fit(func, x, y)
linebestfit = np.poly1d([A, B])

plt.plot(x, y, '.', x, linebestfit(x))
plt.show()

#   x = 8*pi*r*d*f/c
#   c = 8*pi*r*d*(f/x)
#   in our case, (f/x) = 1/slope = 1/A
#   c = 8*pi*r*d/A

r = (100.8-12.8+10.8)/100
d = (112.5+85.6+595)/100

covmatrix = np.cov(x, y)
# [[cov(x, x)=var(x),  cov(x, y)],
#  [cov(x, y),  cov(y, y)=var(y)]]

#uncertainty is sqrt of variance
uncertainty = [math.sqrt(covmatrix[0][0]), math.sqrt(covmatrix[1][1])] #[x, y]

#uncertainty of parameters
paramuncert = [math.sqrt(pcovmatrix[0][0]), math.sqrt(pcovmatrix[1][1])]

print(uncertainty)
print(paramuncert)

#speed of light
c = 8*math.pi*r*d/A
print(c)