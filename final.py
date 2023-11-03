from designer import *
from dataclasses import dataclass

set_window_size(1300,600)
@dataclass
class Box:
    body:[DesignerObject]
    xspeed:int
    yspeed:int
    grow:float
    outline:[DesignerObject]

@dataclass
class Stage:
    blocks:[DesignerObject]
    boxes:[Box]
    flag:DesignerObject

@dataclass
class Beam:
    body: DesignerObject
    length:float
    is_colliding:bool
    endpoint: DesignerObject

@dataclass
class Player:
    obj: DesignerObject
    is_moving: bool
    colliding_with_block: bool
    xspeed: int
    yspeed: float
    jump_delay:int
    beam :Beam


@dataclass
class World:
    player: Player
    timer:int
    gravity: int
    stages: [Stage]
    is_clicking: bool
    level:int

pressed_keys = []
FIRST_JUMP =True

def create_world() -> World:
    return World(create_player(), 0, 1,create_stages(), False,0)

def advance_the_timer(world: World):
    world.timer += 1

def create_stages():
    return [Stage([rectangle('black', get_width(),80, get_width()/2, get_height()-40),
                      rectangle('black',90,200, 800, get_height()-80,0,)],
                      [Box(rectangle('red',80,80, 600, get_height()-160,0,anchor='midbottom'),0,0
                           ,1.0,rectangle('purple',80,80,600,get_height()-160,2)
                           )],emoji('🚩',1100,510))]

def create_player() -> Player:
    return Player(emoji("🔴",20,510,anchor='midbottom'), False, False, 3, 0.0,0, Beam(line('black', 0, 0,0,0), 0.0, False,circle('purple',0,0,0)))

def physics(world: World):
    if colliding(world.player.obj, world.stages[0].blocks[0]):
        if not world.player.colliding_with_block:
            world.player.yspeed = 0
            world.player.colliding_with_block = True
            hide(world.stages[world.level].boxes[0].outline)

    else:
        world.player.colliding_with_block = False
        world.player.yspeed += world.gravity
        hide(world.stages[world.level].boxes[0].outline)

    if world.player.beam.is_colliding and colliding(world.player.beam.body, world.stages[0].boxes[0].body):
         world.stages[world.level].boxes[0].body.x = get_mouse_x()
         world.stages[world.level].boxes[0].body.y = get_mouse_y()+(world.stages[world.level].boxes[0].body.height/2)
         world.stages[world.level].boxes[0].yspeed = 0
         destroy(world.stages[world.level].boxes[0].outline)
         world.stages[world.level].boxes[0].outline=rectangle('purple',world.stages[world.level].boxes[0].body.width,world.stages[world.level].boxes[0].body.height,world.stages[world.level].boxes[0].body.x,world.stages[world.level].boxes[0].body.y,3,anchor='midbottom')

    elif not colliding(world.stages[world.level].boxes[0].body, world.stages[world.level].blocks[0]):
        world.stages[world.level].boxes[0].yspeed += world.gravity
        world.stages[world.level].boxes[0].body.y += world.stages[world.level].boxes[0].yspeed
    else:
        world.stages[world.level].boxes[0].yspeed=0

def push_out(world: World):
    if world.player.obj.y > 521 :
        world.player.obj.y=521
    if world.stages[world.level].boxes[0].body.y > 523:
        world.stages[world.level].boxes[0].body.y=523



def scale(world: World,key:str):
    if colliding(world.player.beam.body, world.stages[world.level].boxes[0].body) and world.is_clicking:
        if key == 'z':
            world.stages[world.level].boxes[0].grow=1.035
        elif key == 'x':
            world.stages[world.level].boxes[0].grow=.965
        world.stages[world.level].boxes[0].body.height=world.stages[world.level].boxes[0].body.height*world.stages[world.level].boxes[0].grow
        world.stages[world.level].boxes[0].body.width = world.stages[world.level].boxes[0].body.width * world.stages[world.level].boxes[0].grow
        world.stages[world.level].boxes[0].outline.height = world.stages[world.level].boxes[0].outline.height * world.stages[world.level].boxes[0].grow
        world.stages[world.level].boxes[0].outline.width = world.stages[world.level].boxes[0].outline.width * world.stages[world.level].boxes[0].grow

def line_creation(world: World):
    if world.is_clicking:
        destroy(world.player.beam.body)
        destroy(world.player.beam.endpoint)
        world.player.beam.body = line('blue', world.player.obj.x, world.player.obj.y-15, get_mouse_x(), get_mouse_y(), 2)
        world.player.beam.endpoint = circle('purple',3,get_mouse_x(),get_mouse_y())
        if colliding(world.player.beam.endpoint, world.stages[world.level].boxes[0].body):
            world.player.beam.is_colliding=True

def clicked(world: World):
    world.is_clicking = True


def unclicked(world: World):
    hide(world.player.beam.body)
    hide(world.stages[world.level].boxes[0].outline)
    hide(world.player.beam.endpoint)
    world.is_clicking = False
    world.player.beam.is_colliding=False

def key_pressed(world: World, key: str):
    global FIRST_JUMP
    pressed_keys.append(key)
    if 'a' in pressed_keys and 'd' in pressed_keys:
        world.player.xspeed = 0
    elif 'a' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'd' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = 10
    if key == 'space':
        jump(world)
        FIRST_JUMP=False
    if key == 'z':
        scale(world,'z')
    if key == 'x':
        scale(world,'x')


def key_released(world: World, key: str):
    if key in pressed_keys:
        pressed_keys.remove(key)
    if 'a' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'd' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = 10
    else:
        world.player.is_moving = False
        world.player.xspeed = 0
        world.stages[world.level].boxes[0].grow = 1

def jump(world: World):
    time = world.timer
    if FIRST_JUMP:
        world.player.yspeed = -16
        world.player.jump_delay=time
    elif time-world.player.jump_delay >10 and world.player.colliding_with_block:
        world.player.yspeed = -16
        world.player.jump_delay = time

def player_movement(world: World):
    if world.player.obj.x>10 and world.player.obj.x<get_width():
         if world.player.is_moving:
              world.player.obj.x += world.player.xspeed
    elif world.player.obj.x<=10:
        world.player.obj.x+=1
    elif world.player.obj.x>=get_width():
        world.player.obj.x-=1

    world.player.obj.y += world.player.yspeed

when('updating',scale)
when('input.mouse.down', clicked)
when('input.mouse.up', unclicked)
when('updating', physics)
when('updating', push_out)
when('updating', player_movement)
when('updating', line_creation)
when('typing', key_pressed)
when('done typing', key_released)
when('updating', advance_the_timer)
when('starting', create_world)
start()