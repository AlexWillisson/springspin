#! /usr/bin/env python

import pygame, sys, time, math

WIDTH = 640
HEIGHT = 480
CENTER = (WIDTH / 2, HEIGHT / 2)
MAXVEL = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SIZE = [WIDTH, HEIGHT]

class vect:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    def __str__ (self):
        return "x: " + str (self.x) + ", y: " + str (self.y)

class unit:
    def __init__ (self, x, y, mass, color, player=False, vx=0, vy=0):
        self.pos = [x, y]
        self.mass = mass
        self.color = color
        self.player = player
        self.vel = vect (vx, vy)
        self.force = vect (0, 0)

class link:
    def __init__ (self, node0, node1, k):
        self.node0 = node0
        self.node1 = node1
        self.k = k

def process_input ():
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit ()
            sys.exit ()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit ()
                sys.exit ()
            elif event.key == pygame.K_r:
                player.pos[0] = CENTER[0]
                player.pos[1] = CENTER[1]
                player.vel.x = 0
                player.vel.y = 0

                obj.pos[0] = CENTER[0] - 100
                obj.pos[1] = CENTER[1] - 200
                obj.vel.x = 0
                obj.vel.y = 0
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos ()
            player.force.x = 2000 * float (pos[0] - CENTER[0])
            player.force.y = 2000 * float (pos[1] - CENTER[1])
            pygame.mouse.set_pos (CENTER)

def draw ():
    screen.fill (BLACK)

    for u in units:
        pygame.draw.circle (screen, u.color, (int (u.pos[0]),
                                            int (u.pos[1])), 20, 0)
    if pygame.mouse.get_pressed ()[0]:
        pygame.draw.line (screen, RED, units[0].pos, units[1].pos)

    for s in links:
        pygame.draw.line (screen, RED, s.node0.pos, s.node1.pos)


    pygame.display.flip ()

def rect_to_pol (x, y):
    y = HEIGHT - y

    r = math.hypot (x, y)
    t = math.atan2 (y, x)

    return (r, t)

def pol_to_rect (r, t):
    x = r * math.cos (t)
    y = HEIGHT - r * math.sin (t)

    return (x, y)

def springs ():
    # for s in springs:
    #     dx = float (s.node0.pos[0] - s.node1.pos[0])
    #     dy = float (s.node0.pos[1] - s.node1.pos[1])
        
    #     s.node0.force[0] -= dx * s.k
    #     s.node0.force[1] -= dy * s.k

    #     s.node1.force[0] += dx * s.k
    #     s.node1.force[1] += dy * s.k

    if pygame.mouse.get_pressed ()[0]:
        dx = float (units[0].pos[0] - units[1].pos[0])
        dy = float (units[0].pos[1] - units[1].pos[1])

        r, t = rect_to_pol (dx, dy)
        r -= 30
        dx, dy = pol_to_rect (r, t)
        

        units[0].force.x -= 100 * dx - units[0].vel.x
        units[0].force.y -= 100 * dy - units[0].vel.y

        units[1].force.x += 100 * dx - units[1].vel.x
        units[1].force.y += 100 * dy - units[1].vel.y

def movement ():
    global last_time

    now = time.time ()
    dt = now - last_time
    last_time = now

    for u in units:
        u.vel.x += u.force.x / u.mass
        u.vel.y += u.force.y / u.mass

        u.pos[0] += dt * u.vel.x
        u.pos[1] += dt * u.vel.y

def reset_forces ():
    for u in units:
        u.force.x = 0
        u.force.y = 0

pygame.init ()

screen = pygame.display.set_mode (SIZE)

pygame.display.set_caption ("Spring Spin")

clock = pygame.time.Clock ()

units = []
links = []

player = unit (CENTER[0], CENTER[1], 5000, GREEN, True)
units.append (player)

obj = unit (CENTER[0] - 100, CENTER[1] - 200, 500, BLUE, False, 0, 500)
units.append (obj)

pygame.mouse.set_pos (CENTER)
pygame.mouse.set_visible (False)

last_time = time.time ()

while True:
    process_input ()
    springs ()
    movement ()
    draw ()

    reset_forces ()

    clock.tick (60)

pygame.quit ()
