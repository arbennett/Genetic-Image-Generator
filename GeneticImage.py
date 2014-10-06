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
                    default="testImage.png")
parser.add_argument("-P", "--population", help="The population of each generation.",
                    type=int, default=5000)
parser.add_argument("-G", "--generations", help="The number of generations to evolve.",
                    type=float, default=50000)
parser.add_argument("-E", "--elements", help="The number of elements per individual in the population.",
                    type=float, default=75)
args=parser.parse_args()


#-------------------------------------------------------------------------
# Variable declarations
#-------------------------------------------------------------------------
im = Image.open(args.loadImage).convert('LA')
size = width, height = im.size
pop = args.population
Ngens = args.generations
Nelements = int(args.elements)
rMax = height/3 # Maximum circle radius
dx = width/5    # Maximum change in x for new child
dy = height/5   # Maximum change in y for new child
da = 255/5      # Maximum change in color for new child
dc = 255/5      # Maximum change in alpha for new child
j=1 # Counter

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
    decals=[]
    testImg = Image.new('LA',(width,height),(255,255))
    testImg.save("blank.png")
    for i in range(Nelements):
        decals.append(Image.new('RGBA',(width,height),(0,0,0,0)))
        draw = ImageDraw.Draw(decals[-1])
        r=int(rMax*random.random())
        x, y=random.randint(0,width), random.randint(0,height)
        theColor=random.randint(0,255)
        alpha = random.randint(0,255)
        testElements.append([r,x,y,theColor,alpha])  
        draw.ellipse((x-r,y-r,x+r,y+r), fill=(theColor,theColor,theColor,alpha))
        testImg.paste(decals[-1], (0,0), decals[-1])
    return testElements, testImg

# Input specs: [ [ r, x, y, val, alpha ], ..., [ r, x, y, val, alpha ] ]
def generateSeededTest(input):
    testElements=[]
    decals=[]
    testImg = Image.new('LA',(width,height),"black")
    for i in range(Nelements):
        decals.append(Image.new('RGBA',(width,height),(0,0,0,0)))
        draw = ImageDraw.Draw(decals[-1])
        r=input[i][0]
        x=input[i][1]
        y=input[i][2]
        theColor=input[i][3]
        alpha=input[i][4]
        # Mutate ~20% of the "genes"
        if random.random() > 0.8:
            temp = decals[-1]
            swapIndex = random.randint(0,len(decals)-1)
            decals[-1]=decals[swapIndex]
            decals[swapIndex]=temp
            r+=10*(random.random()-0.5)
            x, y=np.max([0, np.min([width, x+random.randint(-dx/2,dx/2)]) ]), \
                 np.max([0, np.min([height, y+random.randint(-dy/2,dy/2)]) ])
            theColor=np.max( [0, np.min( [255, theColor+random.randint(-dc/2,dc/2)] )] )
            alpha=np.max( [0, np.min([255, alpha+random.randint(-da/2,da/2)] )] )
        testElements.append([r,x,y,theColor,alpha])   
        draw.ellipse((x-r,y-r,x+r,y+r), fill=(theColor,theColor,theColor,alpha))
        testImg.paste(decals[-1], (0,0), decals[-1])
    return testElements, testImg

# Adds up the difference between the actual and approximate
def calculateScore(mimic, actual):
    score=0
    for i in range(width):
        for j in range(height):
            score+=(actual[i,j]-mimic[i,j])**2
    return score


#################################
# Simple parent vs child method #
#################################
inArr = imageToArray(im)

# In the beginning, there was one:
parentElements, parentIm = generateRandomTest()
parentArr = imageToArray(parentIm)

childElements, childIm = generateSeededTest(parentElements)
childArr = imageToArray(childIm)

# Go for it...
for i in range(Ngens):
    # Build a child and calculate all the important stuff.
    childElements, childIm = generateSeededTest(parentElements)
    childArr = imageToArray(childIm)
    parentScore = calculateScore(parentArr,inArr)[0]
    childScore = calculateScore(childArr,inArr)[0]
    print str(i) + "  :  " + str(parentScore/1000000)
    # If the child image is better, make it pass on it's genome
    # Otherwise, the parent gets another go at making a superior child
    if childScore < parentScore:
        parentElements = childElements
        parentIm = childIm
        parentArr = childArr
        j+=1
        parentIm.save("output" + str(j) + ".png")
        

######### SAVE ME FOR LATER #########    
# Notes for a real genetic method:
#  
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

    
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


    