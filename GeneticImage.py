'''
An image generator using genetic algorithms
to mimic input files

Created on May 13, 2014

@author: Andrew Bennett
'''
#########################################################################################################
# TODO: 
#   Fix the size of the converted arrays so that it's all 
#    in one dimension and the right size.
#########################################################################################################


#-------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------
from PIL import Image, ImageDraw
import numpy
import time
import sys
import random
import math
import numpy
import argparse
import copy

#-------------------------------------------------------------------------
# Command line options
#-------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-L", "--loadImage", help="The name of the imagefile to load (including file extension)", 
                    default="testImage.jpg")
parser.add_argument("-P", "--population", help="The population of each generation.",
                    type=int, default=50)
parser.add_argument("-G", "--generations", help="The number of generations to evolve.",
                    type=float, default=1e3)
parser.add_argument("-E", "--elements", help="The number of elements per individual in the population.",
                    type=float, default=1e3)
args=parser.parse_args()


#-------------------------------------------------------------------------
# Variable declarations
#-------------------------------------------------------------------------
image =Image.open(args.loadImage)
size = width, height = image.size
pop = args.population
Ngen = args.generations
Nelements = int(args.elements)
Nreproduce = height/10
rMax = height/10 # Maximum circle radius
diffMax=height/10

#-------------------------------------------------------------------------
# Function definitions
#-------------------------------------------------------------------------

# Convert the image to an array 
# Supposedly this is the fastest way
def imageToArray(image):
    imArr = numpy.fromstring(image.tostring(), dtype=numpy.uint8)
    numpy.reshape(imArr,(height,width))
    return 0 

# Generates a random test
def generateRandomTest():
    testElements=[]
    testImg = Image.new('RGB',(width,height),"white")
    draw = ImageDraw.Draw(testImg)
    for i in range(Nelements):
        r=int(rMax*random.random())
        x, y=random.randint(0,width), random.randint(0,height)
        val=random.randint(0,255)
        theColor=(val, val, val)
        testElements.append([r,x,y,val])  
        draw.ellipse((x-r,y-r,x+r,y+r), fill=theColor)
    return testElements, list(testImg.getData())

# Input specs: [ [ r, x, y, val ], ..., [ r, x, y, val ] ]
def generateSeededTest(input):
    testElements=[]
    testImg = Image.new('RGB',(width,height),"white")
    draw = ImageDraw.Draw(testImg)
    for i in range(Nelements):
        r=int(input[i,0]+random.random()-0.5)
        x, y=input[i,1]+random.randint(), input[i,2]+random.randint()
        val=input[i,3]+random.randint(-5,5)
        theColor=(val, val, val)
        testElements.append([x,y,r,val])   
        draw.ellipse((x-r,y-r,x+r,y+r), fill=theColor)
    return testElements, list(testImg.getData())
        
# Convert the image to grayscale for now - handling color shouldn't be too bad
# Also returns in array form     
def grayscale(img): 
    arr = imageToArray(img)
    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    return numpy.array([[[avg] for avg in col] for col in avgs])

# Adds up the difference betwen the actual and approximate
def calculateScore(mimic, actual):
    score=0
    for i in range(width):
        for j in range(height):
            score+=abs(image[i,j]-mimic[i,j])
    return score
    

#-------------------------------------------------------------------------
# Execute the algorithm
#-------------------------------------------------------------------------
imageArr=grayscale(image)
# Generate the seed population
samples=[]
scores=[Infinity]*Nreproduce
lowScore=255*height*width

for each in range(pop):
    # Start with completely random set
    params, testArr=generateRandomTest()
    score=calculateScore(testArr, imageArr)    
    # If we found a new low score append the list of parameters
    # Then keep the score list sorted (should probably make sure
    # the list stays sorted in a more efficient way)
    if score < scores[-1]:
        scores[-1]=score
        samples=sorted(samples)
        samples.append(params)

# Now continue for as many generations as we need to
for gen in range(Ngen):
    seeds=copy.deepcopy(samples)
    samples=[]
    scores=[Infinity]*Nreproduce
    
    #Generate the sample population and keep the top matches
    for each in range(pop):
        params, testArr=generateSeededTest(seeds[random.randint(0,Nreproduce)])
        score=calculateScore(testArr, imageArr)
        # If we found a new low score
        if score < scores[-1]:
            scores[-1]=score
            samples=sorted(samples)
            samples.append(params)
    # save the final image(s) from each generation
    for each in samples:
        saveImg = Image.fromarray(each)
        saveImg.save("genetic"+each+"_"+gen, "JPEG")
        


    