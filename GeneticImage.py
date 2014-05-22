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

for i in range(pop):
    r=int(rMax*random.random())
    x, y=int(width*random.random()), int(height*random.random())
    theColor=(int(255*random.random()), int(255*random.random()), int(255*random.random()))
    pygame.draw.circle(screen, theColor, (x,y), r)

pygame.display.flip()

while True:
    a=1
    