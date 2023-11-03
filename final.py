from designer import *
from dataclasses import dataclass

@dataclass
class Stage:
    blocks:[DesignerObject]

#@dataclass
#class Clicker:

@dataclass
class Player:
    obj: DesignerObject
    is_moving: bool
    colliding_with_block: bool
    xspeed: int
    yspeed: float
    jump_delay:int
    beam :DesignerObject


@dataclass
class World:
    player: Player
    timer:int
    gravity: int
    stages: [Stage]
    is_clicking: bool

pressed_keys = []
FIRST_JUMP =True

def create_world() -> World:
    return World(create_player(), 0, 1,create_stages(), False)

def advance_the_timer(world: World):
    world.timer += 1

def create_stages():
    return [Stage([rectangle('black', get_width(),80, get_width()/2, get_height()-40),rectangle('black',get_width(),80, get_width()/2, 40)])]

def create_player() -> Player:
    return Player(emoji("🔴"), False, False, 3, 0.0,0, line('black', 0, 0,0,0))

def physics(world: World):
    if colliding(world.player.obj, world.stages[0].blocks[0]):
        if not world.player.colliding_with_block:
            world.player.yspeed = 0
            world.player.colliding_with_block = True
    else:
        world.player.colliding_with_block = False
        world.player.yspeed += world.gravity

def line_creation(world: World):
    if world.is_clicking:
        destroy(world.player.beam)
        world.player.beam = line('blue', world.player.obj.x, world.player.obj.y, get_mouse_x(), get_mouse_y(), 2)

def clicked(world: World):
    world.is_clicking = True

#def unclicked(world: World):
def unclicked(world: World):
    hide(world.player.beam)
    world.is_clicking = False


def key_pressed(world: World, key: str):
    global FIRST_JUMP
    pressed_keys.append(key)
    if 'left' in pressed_keys and 'right' in pressed_keys:
        world.player.xspeed = 0
    if 'left' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = -10
    if 'right' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = 10
    if key == 'space':
        jump(world)
        FIRST_JUMP=False

def key_released(world: World, key: str):
    if key in pressed_keys:
        pressed_keys.remove(key)
    if 'left' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'right' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = 10
    else:
        world.player.is_moving = False
        world.player.xspeed = 0

def jump(world: World):
    time = world.timer
    print(time-world.player.jump_delay)
    if FIRST_JUMP:
        world.player.yspeed = -20
        world.player.jump_delay=time
    elif time-world.player.jump_delay >10 and world.player.colliding_with_block:
        print(time-world.player.jump_delay,"JUMPED")
        world.player.yspeed = -20
        world.player.jump_delay = time


def player_movement(world: World):
    if world.player.is_moving:
        world.player.obj.x += world.player.xspeed

    world.player.obj.y += world.player.yspeed

when('input.mouse.down', clicked)
when('input.mouse.up', unclicked)
when('updating', physics)
when('updating', player_movement)
when('updating', line_creation)
when('typing', key_pressed)
when('done typing', key_released)
when('updating', advance_the_timer)
when('starting', create_world)
start()