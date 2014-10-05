#!/usr/bin/python
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
import numpy as np
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
                    type=float, default=100)
parser.add_argument("-E", "--elements", help="The number of elements per individual in the population.",
                    type=float, default=100)
args=parser.parse_args()


#-------------------------------------------------------------------------
# Variable declarations
#-------------------------------------------------------------------------
im = Image.open(args.loadImage).convert('LA')
outfile = "greyscale.jpg"
size = width, height = im.size
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
def imageToArray(image):
    return np.asarray(image.getdata(),dtype=np.float64).reshape((image.size[1],image.size[0],2))

# Convert an array to a greyscale image
def arrayToImage(arr):
    return Image.fromarray(np.asarray(arr,dtype=np.uint8),mode='LA')

# Generates a random test
def generateRandomTest():
    testElements=[]
    testImg = Image.new('L',(width,height),"white")
    draw = ImageDraw.Draw(testImg)
    for i in range(Nelements):
        r=int(rMax*random.random())
        x, y=random.randint(0,width), random.randint(0,height)
        theColor=random.randint(0,255)
        alpha = random.randint(0,255)
        testElements.append([r,x,y,theColor,alpha])  
        draw.ellipse((x-r,y-r,x+r,y+r), fill=theColor)
        testImg.putalpha(alpha)
    return testElements, testImg

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

# Adds up the difference between the actual and approximate
def calculateScore(mimic, actual):
    score=0
    for i in range(width):
        for j in range(height):
            score+=abs(actual[i,j]-mimic[i,j])
    return score

# Tests 
inArr = imageToArray(im)
testElements, testIm = generateRandomTest()
testArr = imageToArray(testIm)
print calculateScore(inArr, testArr)
print calculateScore(inArr, inArr)
 
    
######### SAVE ME FOR LATER #########    
    
'''
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
'''        


    