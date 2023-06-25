import pygame
vec = pygame.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

WIDTH = 1024
HEIGHT = 960
FPS = 60
TITLE = "Project Final"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'survivor-idle_rifle_0.png'
PLAYER_HIT_RECT = pygame.Rect(0, 0, 55, 55)
BARREL_OFFSET = vec(30, 10)

BULLET_IMG = 'bullet.png'
WEAPONS = {}

WEAPONS['rifle'] = {'bullet_speed': 400,
                      'bullet_lifetime': 700,
                      'rate': 400,
                      'kickback': 150,
                      'spread': 1,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 1}

MONSTERS_IMG = 'monsters_7.png'

BOSSES_IMG = 'bosses_5.png'

              

MONSTERS_SPEEDS = [150, 100, 75, 125]
MONSTERS_HIT_RECT = pygame.Rect(0, 0, 16, 16)
MONSTERS_HEALTH = 100
MONSTERS_DAMAGE = 10
MONSTERS_KNOCKBACK = 20
BOSSES_SPEEDS = [150, 100, 75, 125]
BOSSES_HIT_RECT = pygame.Rect(0, 0, 32, 32)
BOSSES_HEALTH = 200
BOSSES_DAMAGE = 20
BOSSES_KNOCKBACK = 40
AVOID_RADIUS = 50
DETECT_RADIUS = 400

MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'splat green.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_soft.png"

WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MONSTERS_LAYER = 2
BOSSES_LAYER = 2
EFFECTS_LAYER = 4
               
BOB_RANGE = 10
BOB_SPEED = 0.3

BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = ['shotgun.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav'}
