from designer import *
from dataclasses import dataclass

@dataclass
class Player:
    obj: DesignerObject
    is_moving: bool
    xspeed: int
    yspeed: float
    jump_delay:int

@dataclass
class World:
    player: Player
    timer:int
    gravity: int

pressed_keys = []
FIRST_JUMP =True

def create_world() -> World:
    return World(create_player(), 0, 1)

def advance_the_timer(world: World):
    world.timer += 1

def create_player() -> Player:
    return Player(emoji("man"), False, 3, 0.0,180)

def physics(world: World):
    world.player.yspeed += world.gravity

def key_pressed(world: World, key: str):
    global FIRST_JUMP
    pressed_keys.append(key)
    if 'left' in pressed_keys and 'right' in pressed_keys:
        world.player.xspeed = 0
    elif 'left' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'right' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = 10
    elif key == 'space':
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
    elif time-world.player.jump_delay >38:
        print(time-world.player.jump_delay,"JUMPED")
        world.player.yspeed = -20
        world.player.jump_delay = time


def player_movement(world: World):
    if world.player.is_moving:
        world.player.obj.x += world.player.xspeed

    world.player.obj.y += world.player.yspeed

    if world.player.obj.y > 200:
        world.player.obj.y = 200
        world.player.yspeed = 0

when('updating', physics)
when('updating', player_movement)
when('typing', key_pressed)
when('done typing', key_released)
when('updating', advance_the_timer)
when('starting', create_world)
start()