#face directions
face = {'NORTH': 0, 'EAST': 1, 'SOUTH': 2, 'WEST': 3,
		0: 'NORTH', 1: 'EAST', 2: 'SOUTH', 3: 'WEST'}

import fileinput

######################################################################################

class Robot:

	def __init__(self, x, y, f):
		#initialise robot at position x, y and facing f
		self.x = x
		self.y = y
		self.f = f
	
	#turn the robot left or right
	def turn(self, d):
		#increasing face direction by 1 turns right, decreasing turns left.
		#Mod 4 is used in case of wraparound.
		#eg. north-1 = -1, -1%3 = 3 = west
		if ( d == 'LEFT' ):
			self.f = (self.f-1)%4
		else:
			self.f = (self.f+1)%4
	
	#move forward
	def move(self, others):
		#generate new position
		newX = self.x
		newY = self.y
		#also checks boundaries and ignores unsafe commands
		if ( self.f == face['NORTH'] and self.y != 4 ):
			newY += 1
		elif ( self.f == face['SOUTH'] and self.y != 0 ):
			newY -= 1
		elif ( self.f == face['EAST'] and self.x != 4 ):
			newX += 1
		elif ( self.f == face['WEST'] and self.x != 0 ):
			newX -= 1
		
		#check other robot positions
		if ( (newX, newY) not in others ):
			self.x = newX
			self.y = newY
		
######################################################################################

#array of robots
robots = []
#which robot receives commands
active = -1

#parse input
for line in fileinput.input():

	#place new robot
	if ( line[:5] == 'PLACE' ):
	
		#get arguments
		args = line[6:].split(',')
		#there should be 3 arguments
		if ( len(args) != 3 ):
			print('Error in PLACE: expected 3 arguments. Received ' + str(len(args)) + ' arguments')
			continue
		
		#error check x, y
		try:
			x = int(args[0])
		except:
			print('Error in PLACE: expected an integer for x. Received ' + args[0])
			continue
		
		if ( x<0 or x>4 ):
			print('Error in PLACE: x must be between 0 and 4')
			continue
			
		try:
			y = int(args[1])
		except:
			print('Error in PLACE: expected an integer for y. Received ' + args[1])
			continue
		
		if ( y<0 or y>4 ):
			print('Error in PLACE: y must be between 0 and 4')
			continue
		
		#error check direction
		f = args[2].upper().strip()
		
		#f should be a cardinal direction
		if ( f not in list(face.keys())[:4] ):
			print('Error in PLACE: expected a cardinal direction as 3rd argument. Received ' + args[2].strip())
			continue
		
		#check if a robot already exists at [x,y]
		flag = False
		for r in robots:
			if ( (r.x, r.y) == (x,y) ):
				flag = True
				break
		
		if flag:
			print('Error in PLACE: A robot already exists at ' + args[0] + ', ' + args[1])
			continue
		
		#error checking is done. Place robot
		robots.append(Robot(x, y, face[f]))
		
		#update active robot if this is the first
		if ( len(robots) == 1 ):
			active = 0
			
	##########################################################
	
	#move robot
	elif ( line.strip() == 'MOVE' ):
		if ( active == -1 ):
			print('Error in MOVE: no active robots')
		else:	
			robots[active].move([(r.x, r.y) for r in robots])
	
	##########################################################
	
	#turning
	elif ( line.strip() == 'LEFT' ):
		if ( active == -1 ):
			print('Error in LEFT: no active robots')
		else:	
			robots[active].turn('LEFT')
			
	elif ( line.strip() == 'RIGHT' ):
		if ( active == -1 ):
			print('Error in RIGHT: no active robots')
		else:	
			robots[active].turn('RIGHT')		
			
	##########################################################
	
	#report
	elif ( line.strip() == 'REPORT' ):
		if ( active == -1 ):
			print('Error in REPORT: no active robots')
		else:
			print('Robot ' + str(active+1) + ': ' + 
				str(robots[active].x) + ', ' + 
				str(robots[active].y) + ', ' + 
				face[robots[active].f])
	
	##########################################################
	
	#change robot
	elif ( line[:5] == 'ROBOT' ):
	
		#error checking
		args = line.split(' ')
		
		#number of arguments should be 1. The 2 includes the ROBOT command itself
		if ( len(args) != 2 ):
			print('Error in ROBOT: Expected 1 argument. Received ' + str(len(args)-1))
			continue
		
		index = int(args[1])
			
		#argument should be >=1
		if ( index<1 ):
			print('Error in ROBOT: invalid robot number. Received ' + args[1])
			continue
			
		#robot index should not exceed number of robots	
		if ( index>len(robots) ):
			print('Error in ROBOT: index exceeds the number of robots. There are ' + 
			str(len(robots)) + ' robot(s), received ' + args[1].strip())
			continue
		
		#error checking passed
		active = index-1
	
	#bad input
	else: 
		#allow comments
		if ( line[0] == '#' ):
			continue
		else:
			print('Error: invalid command. Expected PLACE, LEFT, RIGHT, REPORT or ROBOT. Received ' + line.strip())
	
	
	
	
	
	
	
	
	
	
	