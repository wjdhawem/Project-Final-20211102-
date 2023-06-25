import pygame
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        self.player = None
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("20211102정윤철")
        self.clock = pygame.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'img')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pygame.transform.scale(pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha(), (64, 42.3))
        self.monsters_img = pygame.image.load(path.join(img_folder, MONSTERS_IMG)).convert_alpha()
        self.monsters_img = pygame.transform.scale(pygame.image.load(path.join(img_folder, MONSTERS_IMG)).convert_alpha(), (64, 64))
        self.bosses_img = pygame.image.load(path.join(img_folder, BOSSES_IMG)).convert_alpha()
        self.bosses_img = pygame.transform.scale(pygame.image.load(path.join(img_folder, BOSSES_IMG)).convert_alpha(), (96, 96))
        self.bullet_images = {}
        self.bullet_images['lg'] = pygame.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pygame.transform.scale(self.bullet_images['lg'], (10, 10))
        self.splat = pygame.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pygame.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pygame.image.load(path.join(img_folder, img)).convert_alpha())

        self.fog = pygame.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pygame.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        pygame.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pygame.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sound = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.weapon_sound = pygame.mixer.Sound(path.join(snd_folder, snd))
            self.weapon_sound.set_volume(0.3)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pygame.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pygame.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group() 
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'Project_map.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'monster':
                self.monsters = Monsters(self, obj_center.x, obj_center.y)
            if tile_object.name == 'boss':
                self.bosses = Bosses(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                self.wall = Obstacle(self, tile_object.x, tile_object.y,
                                     tile_object.width, tile_object.height)
                
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.effects_sounds['level_start'].play()

    def run(self):
        self.playing = True
        pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):

        self.all_sprites.update()
        self.camera.update(self.player)

        if self.player.health == 0:
            self.playing = False

        hitsm = pygame.sprite.spritecollide(self.player, self.monsters, False, collide_hit_rect)
        for hit in hitsm:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MONSTERS_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hitsm:
            self.player.hit()
            self.player.pos += vec(MONSTERS_KNOCKBACK, 0).rotate(-hitsm[0].rot)

        hitsb = pygame.sprite.spritecollide(self.player, self.bosses, False, collide_hit_rect)
        for hit in hitsb:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MONSTERS_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hitsb:
            self.player.hit()
            self.player.pos += vec(BOSSES_KNOCKBACK, 0).rotate(-hitsb[0].rot)

        hitsm = pygame.sprite.groupcollide(self.monsters, self.bullets, False, True)
        hitsb = pygame.sprite.groupcollide(self.bosses, self.bullets, False, True)
        for m in hitsm:
            for bullet in hitsm[m]:
                m.health -= bullet.damage
            m.vel = vec(0, 0)

        for b in hitsm:
            for bullet in hitsm[b]:
                b.health -= bullet.damage
            b.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            if isinstance(sprite, Monsters):
                sprite.draw_health()
            if isinstance(sprite, Bosses):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
 
        if self.night:
            self.render_fog()
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_n:
                    self.night = not self.night

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("LAST SURVIVOR", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press any key to start", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
