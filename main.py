import cwiid
import time
import sys, pygame
import math
pygame.init()

print 'Press 1+2 on your Wiimote now...'
wm = cwiid.Wiimote()

time.sleep(1)

wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_IR

wm.led = 1

size = width, height = 1000, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)

hand = pygame.image.load("hand.png")

lastir0 = (0,0)
lastir1 = (0,0)

a = math.pi

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

while 1:
	#print wm.state

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	screen.fill(black)

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