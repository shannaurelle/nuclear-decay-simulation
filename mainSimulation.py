"""Alpha decay simulation for CS and Physics"""
"""
Authors: Shann Aurelle Ripalda
         Natalie Shayne Macababbad
         Michelle Healmer Castro
Description: This is the fourth quarter project for CS 5 and Physics 3.
             On this simulation, one can see how uranium-238 decays into
             thorium-234 by alpha particle emission. 
Date of Submission: May 3, 2019

"""
# libraries for import
import pygame
import random
import math
import os
import sys


#global variables for the simulation
clock = pygame.time.Clock()
global my_particles 
global loopCount
global frameCount
global selected_button
global size
global number_of_particles

file = open('data.txt','r+')
dataline = file.readlines()
data = []
for line in dataline:
    data = line.split(',')
T = (int(data[1]) - 1440)//10
if T < 0:
    T = 0
R = 8.314472
M = 238.0
PI = 3.14628
formula = (8*R*T)/(PI*M)
mean_speed = int(math.sqrt(formula))

# random initialization of simulation particles and buttons
(number_of_particles, initial_speed) = (int(data[0]),mean_speed)
my_particles = []
my_decay_particles = []
my_alpha_particles = []
my_buttons = []
# images for alpha particle
small_alpha_images = ['salpha1.png']
# variable for the images folder
folder = 'sprites'
# size variable for alpha particle
small_size = 5
# size for atom
size = 60
# half-life of uranium-238 in billions of years
half_life = 4.5
# FPS
FPS = 40
# Boolean flag to determine if simulation started
simulationStarted = []
# name of atom to be simulated
atom = "Uranium-238"
decay_name = "Thorium-234"

#initialization of background color in (R,G,B) format
background_color = (240,240,240)

# initialization of width and height in a tuple
(width,height) = (1020,420)

# initialization of simulation box width and height 
(simul_width,simul_height) = (640,360)

#initialization of the vector gravity in terms of (angle, magnitude/length)
gravity = (math.pi, 0.05)

#intialization of constants for slowing down the particles
# drag is for air resistance
drag = 0.999
# elasticity is for energy loss from bouncing on the simulation walls
elasticity = 0.99

#size for the atom radius in pixels
size = 20

# simulation initialization
pygame.init()
iconimg = pygame.image.load(os.path.join('sprites','nuclear.png'))
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(iconimg)
pygame.display.set_caption('Alpha Decay Simulator')
screen.fill(background_color)

#initialization of text variables
text = pygame.font.SysFont("verdana,arial,calibri",20)

# function to end simulation from exit button
def exitSimul():
    pygame.quit()
    sys.exit(0)

#list shuffling function
def listShuffle(mylist):
    num1 = random.randint(0,len(mylist)-1)
    num2 = random.randint(0,len(mylist)-1)
    temp = mylist[num1]
    mylist[num1] = mylist[num2]
    mylist[num2] = temp
    return mylist

# particle collision detection function
def collide(p1, p2):
    
    dx = p1.x - p2.x
    dy = p1.y - p2.y
        
    sq_distance = dx*dx + dy*dy # <- pythagorean theorem from coordinate geometry
    if sq_distance < (p1.size + p2.size)**2:
        tangent = math.atan2(dy, dx)
        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle
        (p1.speed, p2.speed) = (p2.speed, p1.speed)
        p1.speed *= elasticity
        p2.speed *= elasticity
        angle = 0.5 * math.pi + tangent
        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)

# vector is a tuple with definition (angle, length)
# adding vectors function
def addVectors(vector1, vector2):
    x  = math.sin(vector1[0]) * vector1[1] + math.sin(vector2[0]) * vector2[1]
    y  = math.cos(vector1[0]) * vector1[1] + math.cos(vector2[0]) * vector2[1]
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)


#detecting the clicked particle function
def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None
#detecting the clicked particle function
def findButton(buttons, x, y):
    for b in buttons:
        if abs(b.x-x) < (b.width) and abs(b.y-y) < (b.height):
            return b
    return None

#class for Button objects
class Button:
    def __init__(self, coord, width, height, img_src=None, function=None):
        self.x = coord[0] + width
        self.y = coord[1] + height
        self.colour = (0, 0, 255)
        self.width = width
        self.height = height
        self.functions = function
        self.img = pygame.image.load(os.path.join(folder,img_src[0]))
        
    def display(self):
        screen.blit(self.img, (int(self.x),int(self.y)))

    def onClick(self):
        print("Just clicked me!")
        
        # one-way button
        if self.functions is not None: 
            self.functions()
        
        return True

#class for Particle objects
class Particle:
    # particle characteristics function
    def __init__(self, coord, size, img_src=None):
        self.x = coord[0] 
        self.y = coord[1] 
        self.size = size 
        self.speed = 0.01
        self.mass = 1
        self.angle = 0            # values are from (0, 2*math.pi)
        self.img = []
        self.time = 0
        if len(img_src) == 1:
            self.img.append(pygame.image.load(os.path.join(folder,img_src[0])))
        elif len(img_src) > 1:
            for img in img_src:
                self.img.append(pygame.image.load(os.path.join(folder,img)))
        else:
            self.img.append(pygame.image.load(os.path.join(folder,'alpha1.png')))                        
            
    # move function      
    def move(self):
        self.x += (math.sin(self.angle) * self.speed // self.mass)
        self.y -= (math.cos(self.angle) * self.speed // self.mass)
        # this allows gravity to interact with the particles
        # (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.speed *= drag
        
    # wall bounce function
    def bounce(self):
        # if the particle reaches the right wall, bounce it to the left
        if self.x > (simul_width - self.size):
            self.x = 2 * (simul_width - 2* size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity # reduce the particle's speed after wall collision
            
        # if the particle reaches the left wall, bounce it to the right
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity # reduce the particle's speed after wall collision
            
        # if the particle reaches the bottom wall, bounce it upwards
        if self.y > (simul_height - self.size):
            self.y = 2 * (simul_height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity # reduce the particle's speed after wall collision
            
        # if the particle reaches the top wall, bounce it downwards
        elif (self.y < self.size):
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity # reduce the particle's speed after wall collision
        
    # display of particle function        
    def display(self,frame_count,timeCount):
            if len(self.img) == 1: # if there's only one image available
                screen.blit(self.img[0], (int(self.x),int(self.y)))
            else: # else display all image frames of the image array
                screen.blit(self.img[frame_count], (int(self.x),int(self.y)))
        

# initialization of images to be used for atomic particle
alpha_images = ['atom1.png']
# images for decay particle
decay_images = ['decay2.png']
small_images = ['new_alpha.png']

my_buttons = []

#initialization of simulation variables
running = True
frameCount = 0
frameRate = len(alpha_images)
time = 0
loopCount = 0
delayConstant = 3
selected_particle = None
selected_button = None
pressedControl = []
temp = 0
haha = False
timeVar = 0
# mainloop

# random particle initialization function
for n in range(number_of_particles):
    size = 60
    x = random.randint(size, simul_width-2*size)
    y = random.randint(size, simul_height-2*size)
    alpha_images = listShuffle(alpha_images)
    particle = Particle((x, y), size,alpha_images)
    particle.speed = random.random() + initial_speed
    particle.angle = random.uniform(0, math.pi*2)
    my_particles.append(particle)

# initializing the text dimensions
    (textWidth,textHeight) = text.size((str(time)+" ms"))
    # initializing the time elapsed text 
    timeTitleText = text.render("Time elapsed:", True, (0,0,0))
    # initializing the title of half-life
    halfLifeTitleText = text.render("Half-life of",True, (0,0,0))
    # initializing half-life value 
    halfLifeText = text.render(str(half_life)+" billion years",True, (0,0,0))
    atomText = text.render(atom,True, (0,0,0))
    decayText = text.render(decay_name,True, (0,0,0))
    """rendering the GUI buttons"""
    #rendering the exit button
    exitButton = Button( (simul_width+size-40, simul_height-size-50+100), 80, 30, ['exit.png'],exitSimul)
    my_buttons.append(exitButton)
    #rendering the start button
    controlButton = Button( (simul_width+size+80, simul_height-size-50+100), 80, 30, ['start.png','stop.png'])
    my_buttons.append(controlButton)

while running:

    (margin) = 20
    frameCount = frameCount % 4

    clock.tick(FPS) # runs the simulation at FPS in maxiumum 
    print(" "+str(clock.get_fps())+" fps") # checking fps of the simulation

    #display images and text at GUI
    screen.fill(background_color)
    vertices = [(0,0),(0,simul_height+size),(simul_width+size,simul_height+size),(simul_width+size,0)]
    pygame.draw.polygon(screen, (0,0,0), vertices)
    screen.blit(timeTitleText, (simul_width+100-(textWidth//2), 50+(margin//2)-(textHeight//2)))
    screen.blit(halfLifeTitleText, (simul_width+100-(textWidth//2), 100+(margin//2)-(textHeight//2)))
    screen.blit(atomText, (simul_width+100-(textWidth//2), 120+(margin//2)-(textHeight//2)))
    screen.blit(decayText, (simul_width+100-(textWidth//2), 120+120+(margin//2)-(textHeight//2)))
    screen.blit(halfLifeText, (simul_width+100-(textWidth//2), 160+(margin//2)-(textHeight//2)))
    alphaText = text.render("Alpha particle",True,(0,0,0))
    screen.blit(alphaText,  (simul_width+100-(textWidth//2), 180+120+40+(margin//2)-(textHeight//2)))
    if len(alpha_images) >=1:
        atom_image = pygame.image.load(os.path.join(folder,alpha_images[0]))
    else:
        atom_image = pygame.image.load(os.path.join(folder,'alpha1.png'))
    screen.blit(atom_image, (simul_width+205+size-(textWidth//2),100-(textHeight//2)))
    if len(decay_images) >=1:
        decay_image = pygame.image.load(os.path.join(folder,decay_images[0]))
    else:
        decay_image = pygame.image.load(os.path.join(folder,'anti.png'))
    if len(small_images) >=1:
        alpha_image = pygame.image.load(os.path.join(folder,small_images[0]))
    else:
        alpha_image = pygame.image.load(os.path.join(folder,'anti.png'))
        
    screen.blit(decay_image, (simul_width+205+size+10-(textWidth//2),100+120-(textHeight//2)))
    screen.blit(alpha_image, (simul_width+205+size+30-(textWidth//2),180+120+40+(margin//2)-(textHeight//2)))

    (mouseX,mouseY) = pygame.mouse.get_pos() # get mouse position in (X, Y)
    for event in pygame.event.get():
        
        # if the x button is clicked, exit the program
        if event.type == pygame.QUIT:
           running = False
           pygame.quit()
           sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouseX <= simul_width and mouseY <= simul_height:
                selected_particle = findParticle(my_particles, mouseX, mouseY)
            else:
                selected_button = findButton(my_buttons, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
            selected_button = None
    
        if selected_button is not None:
                selected_button.onClick()
                haha = not haha

        if haha and len(pressedControl) == 0:
             pressedControl.append(True)
             controlButton.img = pygame.image.load(os.path.join(folder,'stop.png'))
        elif not haha and len(pressedControl) > 0:
            pressedControl.remove(True)
            controlButton.img = pygame.image.load(os.path.join(folder,'start.png'))

    #display buttons as images
    exitButton.display()
    controlButton.display()
    
    if True in pressedControl:
        
        time += clock.get_time()
        timeVar = time/(1000*delayConstant)
        
        # compute remaining particles using half-life equation
        exp = timeVar/half_life
        particles_to_remove = int(number_of_particles*(1-(0.5)**exp)) 
        print(particles_to_remove," ",number_of_particles) # test console
        
        # if my_particles array isn't empty 
        if len(my_particles) > 0:
            
            # if number of particles to remove increased, remove an atom and create one decay and alpha particle 
            if particles_to_remove > temp:
                
                    # removal of one atom. Variable serves to store the (x,y) coordinates of the decayed atom                                                 
                    temp_particle = my_particles.pop()               
                    size = 60
                    
                    # decay particle creation
                    decay_images = listShuffle(decay_images)
                    particle = Particle((temp_particle.x, temp_particle.y), (size-10),decay_images)
                    particle.speed = random.random() + initial_speed
                    particle.angle = random.uniform(0, math.pi*2)
                    my_decay_particles.append(particle)
                    
                    # alpha particle creation
                    particle = Particle((temp_particle.x, temp_particle.y), small_size,small_images)
                    particle.speed = random.random() + initial_speed
                    particle.mass = 0.05 
                    particle.angle = random.uniform(0, math.pi*2)
                    my_alpha_particles.append(particle)
                    
            # set number of particles as the temporary number for comparison
            temp = particles_to_remove 

    #drawing the time
    timeText = text.render((str(round(timeVar,2))+" billion years"), True, (0,0,0))
    screen.blit(timeText, (simul_width+100-(textWidth//2),70+(margin//2)-(textHeight//2)))
    

    # drawing the particles
    all_particles = my_particles + my_alpha_particles + my_decay_particles
    # move, bounce, and display all atoms
    for i,particle in enumerate(my_particles):
        if True in pressedControl:
            if particle is not selected_particle:
                particle.move()
                particle.bounce()
            for particle2 in all_particles[i+1:]:
                collide(particle, particle2)
        particle.display(frameCount,timeVar)
    # move, bounce, and display all decayed particles
    for i,particle in enumerate(my_decay_particles):
        if True in pressedControl:
            if particle is not selected_particle:
                particle.move()
                particle.bounce()
            for particle2 in all_particles[i+1:]:
                collide(particle, particle2)
        particle.display(frameCount,timeVar)
    # move, bounce, and display all alpha particles
    for i,particle in enumerate(my_alpha_particles):
        if True in pressedControl:
            if particle is not selected_particle:
                particle.move()
                particle.bounce()
            for particle2 in all_particles[i+1:]:
                collide(particle, particle2)
        particle.display(frameCount,timeVar)

    # function to display all elements set up above
    pygame.display.flip()

    #used for determining the frame number for particles
    if (loopCount%frameRate==0):
        frameCount += 1
    loopCount += 1
        
