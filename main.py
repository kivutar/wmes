import cwiid
import time
import sys, pygame
import math
import json
import subprocess
pygame.init()

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

clock = pygame.time.Clock()

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
	wm.close()
	pygame.quit()
	sys.exit()

def launch():
	if games[gy][gx].has_key('rom'):
		wm.close()
		pygame.quit()
		subprocess.call([RETROPIE+"RetroArch-Rpi/retroarch",
			"-c", RETROPIE+"RetroArch-Rpi/retroarch.cfg",
			"-L", RETROPIE+"emulatorcores/"+games[gy][gx]['core']+"/libretro.so",
			RETROPIE+"roms/"+games[gy][gx]['rom']])
		sys.exit()

while 1:
	clock.tick(30)

	print wm.state
	wmbuttons = wm.state['buttons']

	WM_2 = False #1
	WM_1 = False #2
	WM_B = False #4
	WM_A = False #8
	WM_MINUS = False #16
	WM_HOME = False #128
	WM_LEFT = False #256
	WM_RIGHT = False #512
	WM_DOWN = False #1024
	WM_UP = False #2048
	WM_PLUS = False #4096

	if wmbuttons >= 4096:
		wmbuttons = wmbuttons - 4096
		WM_PLUS = True
	if wmbuttons >= 2048:
		wmbuttons = wmbuttons - 2048
		WM_UP = True
	if wmbuttons >= 1024:
		wmbuttons = wmbuttons - 1024
		WM_DOWN = True
	if wmbuttons >= 512:
		wmbuttons = wmbuttons - 512
		WM_RIGHT = True
	if wmbuttons >= 256:
		wmbuttons = wmbuttons - 256
		WM_LEFT = True
	if wmbuttons >= 128:
		wmbuttons = wmbuttons - 128
		WM_HOME = True
	if wmbuttons >= 16:
		wmbuttons = wmbuttons - 16
		WM_MINUS = True
	if wmbuttons >= 8:
		wmbuttons = wmbuttons - 8
		WM_A = True
	if wmbuttons >= 4:
		wmbuttons = wmbuttons - 4
		WM_B = True
	if wmbuttons >= 2:
		wmbuttons = wmbuttons - 2
		WM_1 = True
	if wmbuttons >= 1:
		wmbuttons = wmbuttons - 1
		WM_2 = True

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			terminate()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				launch()
			elif event.key == pygame.K_ESCAPE:
				terminate()

	if WM_A:
		launch()

	screen.fill(black)

	for y in range(0,3):
		for x in range(0,4):
			if games[y][x].has_key('thumb'):
				thumb = pygame.image.load("thumbs/"+games[y][x]['thumb'])
				screen.blit(thumb, (x*144+32, y*128+32))

	screen.blit(gui, (0, 0))

	for y in range(0,3):
		for x in range(0,4):
			if cursor[0] > x*144+32 and cursor[0] < (x+1)*144+32 and cursor[1] > y*128+32 and cursor[1] < (y+1)*128+32:
				chan = pygame.image.load("gui/hover.png")
				gx = x
				gy = y
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

	#pygame.draw.circle(screen, (255,0,0), cursor, 5, 0)

	pygame.display.flip()
