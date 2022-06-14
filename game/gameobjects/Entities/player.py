import math

import pyasge
from enum import Enum

from game.gameobjects.Entities.entity import Entity
from game.gameobjects.Weaponry.god_sword import GodSword
from game.gameobjects.Weaponry.bow import Bow
from game.gameobjects.Entities.player_animation_state import PlayerAnimationState


class PlayerMode(Enum):
    MELEE = 1
    RANGED = 2


class Player(Entity):

    def __init__(self):
        super().__init__()
        self.max_health = 100
        self.current_health = self.max_health
        self.armor = self.HEAVY
        self.your_turn = False
        self.sword = GodSword()
        self.bow = Bow()

        self.movement = False
        self.in_range = False
        self.melee = False
        self.ranged = False
        self.mode = PlayerMode.MELEE
        self.active_weapon = self.sword

        self.anim_state = PlayerAnimationState.IDLE
        self.anim_timer = 0
        self.frame = 0
        self.current_timer = 0

        self.init()

    def init(self) -> None:
        self.sprite.loadTexture("data/sprites/player-gt-Sheet copy.png")
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 64
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_Y] = 64
        self.sprite.x = 600
        self.sprite.y = 600
        # self.sprite.scale = 0.5
        self.width = 64
        self.height = 64
        self.sprite.z_order = 51

        self.weapons.append(self.sword)
        self.weapons.append(self.bow)

    def reset(self) -> None:
        self.current_health = self.max_health
        self.your_turn = True
        self.damage_dealt = 0
        self.damage_taken = 0
        self.enemies_killed = 0

    def combat_reset(self):
        self.your_turn = True
        self.action_points = 2
        self.movement_points = 8
        self.current_health = self.max_health

    def weapon_move(self):
        self.sword.sprite.x = self.sprite.x + 40
        self.sword.sprite.y = self.sprite.y + 8

        self.bow.sprite.x = self.sprite.x
        self.bow.sprite.y = self.sprite.y

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        pass

    def update(self, game_time: pyasge.GameTime, data) -> None:
        self.play_animation(game_time, self.current_timer)

        if self.mode == PlayerMode.MELEE:
            self.active_weapon = self.sword
        elif self.mode == PlayerMode.RANGED:
            self.active_weapon = self.bow
        self.weapon_move()

        if len(self.destination) == 0:
            self.anim_state = PlayerAnimationState.IDLE
        else:
            self.anim_state = PlayerAnimationState.WALK

    def play_animation(self, game_time: pyasge.GameTime, current_timer):
        self.anim_timer -= game_time.fixed_timestep
        if self.anim_timer < 0:
            self.anim_timer = current_timer
            self.frame += 1

        if self.anim_state == PlayerAnimationState.IDLE:
            self.current_timer = 0.2
            self.idle_animation()
        elif self.anim_state == PlayerAnimationState.WALK:
            self.current_timer = 0.06
            self.walk_animation()
        elif self.anim_state == PlayerAnimationState.ATTACK:
            self.attack_animation()
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = self.frame * self.sprite.width

    def idle_animation(self):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = 0
        if self.frame > 6:
            self.frame = 0

    def walk_animation(self):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = 64
        if self.frame > 6:
            self.frame = 0

    def attack_animation(self):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = 128
        if self.frame > 5:
            self.frame = 0
