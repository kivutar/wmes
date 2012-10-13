import cwiid
import time
import sys, pygame
import math
import json
import subprocess
pygame.init()

RETROPIE = '/home/pi/RetroPie/'

dbstring = open('db.json').read()
games = json.loads(dbstring)

print 'Press 1+2 on your Wiimote now...'
wm = cwiid.Wiimote()

time.sleep(1)

wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_IR

wm.led = 1
wm.rumble = 1
time.sleep(0.5)
wm.rumble = 0

size = width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)

hand = pygame.image.load("gui/hand.png")
gui = pygame.image.load("gui/background.png")

lastir0 = (0,0)
lastir1 = (0,0)

a = math.pi

cursor = (0,0)
gx = 0
gy = 0

def rot_center(image, angle):
	"""rotate an image while keeping its center and size"""
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image

def terminate():
	pygame.quit()
	sys.exit()

while 1:
	#print wm.state

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			terminate()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pygame.quit()
				subprocess.call([RETROPIE+"RetroArch-Rpi/retroarch",
					"-c", RETROPIE+"RetroArch-Rpi/retroarch.cfg",
					"-L", RETROPIE+"emulatorcores/"+games[gy][gx]['core']+"/libretro.so",
					RETROPIE+"roms/"+games[gy][gx]['rom']])
				sys.exit()
			elif event.key == pygame.K_ESCAPE:
				terminate()

	screen.fill(black)

	for y in range(0,3):
		for x in range(0,4):
			if games[y][x].has_key('thumb'):
				thumb = pygame.image.load("thumbs/"+games[y][x]['thumb'])
				screen.blit(thumb, (x*144+32, y*128+32))

	screen.blit(gui, (0, 0))

	for x in range(0,4):
		for y in range(0,3):
			if cursor[0] > x*144+32 and cursor[0] < (x+1)*144+32 and cursor[1] > y*128+32 and cursor[1] < (y+1)*128+32:
				chan = pygame.image.load("gui/hover.png")
			elif games[y][x].has_key('thumb'):
				chan = pygame.image.load("gui/default.png")
			else:
				chan = pygame.image.load("gui/blank.png")
			screen.blit(chan, (x*144+32, y*128+32))

	ir = wm.state['ir_src'][0]
	if ir:
		#pygame.draw.circle(screen, (0,255,0), (ir['pos'][0], ir['pos'][1]), ir['size']*3, 0)
		lastir0 = (ir['pos'][0], ir['pos'][1])
	
	ir = wm.state['ir_src'][1]
	if ir:
		#pygame.draw.circle(screen, (0,255,0), (ir['pos'][0], ir['pos'][1]), ir['size']*3, 0)
		lastir1 = (ir['pos'][0], ir['pos'][1])
	
	a = math.atan2(lastir1[0]-lastir0[0], lastir1[1]-lastir0[1])
	
	cursor = (1000-(lastir0[0]+lastir1[0])/2, (lastir0[1]+lastir1[1])/2)
	
	rothand = rot_center(hand, math.degrees(a-math.pi/2))
	screen.blit(rothand, (cursor[0] - 48, cursor[1] - 48))

	pygame.draw.circle(screen, (255,0,0), cursor, 5, 0)

	pygame.display.flip()
