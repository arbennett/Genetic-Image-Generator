'''
A quick image generator using genetic algorithms
to mimic input files

Created on May 13, 2014

@author: Andrew Bennett
'''

# Imports
import pygame
import time
import sys
import random
import math
import numpy
import argparse

# Program operation stuff
parser = argparse.ArgumentParser()
parser.add_argument("-L", "--loadImage", help="The name of the imagefile to load (including file extension)", 
                    default="default.jpg")
parser.add_argument("-P", "--population", help="The population of each generation.",
                    type=int, default=50)
parser.add_argument("-G", "--generations", help="The number of generations to evolve.",
                    type=float, default=1e3)
parser.add_argument("-E", "--elements", help="The number of elements per individual in the population.",
                    type=float, default=1e3)
args=parser.parse_args()

# Start up pygame & display window
pygame.init()
image = pygame.image.load(args.loadImage)
size = width, height = image.get_size()

screen = pygame.display.set_mode(size)
screen.blit(image, (0,0))

# Variables
pop = args.population
Ngen = args.generations
Nelements = args.elements
rMax = 50 # Maximum circle radius

# Function definitions
def generateImages():
    for i in range(Nelements):
        r=int(rMax*random.random())
        x, y=int(width*random.random()), int(height*random.random())
        val=random.randint(0,255)
        theColor=(val, val, val)
        pygame.draw.circle(screen, theColor, (x,y), r)
        
    return [r,x,y,val]
        
# Thanks stackoverflow - see if we can do a better job
#  I'm beginning to think pygame is a waste of time except for the saving of images
#  Maybe use PIL instead - I hear good things about that.        
def grayscale(self, img):
    arr = pygame.surfarray.array3d(img)
    #luminosity filter
    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)

def calculateScore(mimic, actual):
    score=0
    for i in range(width):
        for j in range(height):
            realVal=image.Surface.get_at((i,j))
            approxVal=mimic.Surface.get_at((i,j))
            score+=abs(realVal-approxVal)
    return score
    

# Execute the algorithm
#  - generate n samples
#  - choose the best sample from a generation
#  - use it as a seed to make the next generation
image=grayscale(image)
for gen in range(Ngen):
    samples=[]
    lowScore=Infinity
    # TODO: need a good way to keep track of parameter list - ie don't store the images  
    #       themselves, just references with the seeds
    for each in range(pop):
        screen.fill((255,255,255))
        testImage=generateImages()
        samples.append(testImage)
        score=calculateScore(testImage, image)
        if score < lowScore: # This is a terrible method of keeping the low score
            lowScore=score   # fix this so that we can maybe keep the top N from the pop 
            ind=each         # and use some sort of weighted average to seed the next gen
    # save the final image(s) from each generation 

while True:
    a=1
    