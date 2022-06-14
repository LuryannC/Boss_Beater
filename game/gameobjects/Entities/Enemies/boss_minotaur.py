import pyasge
from game.gamedata import GameData
from game.gameobjects.Entities.enemy import Enemy
from game.gameobjects.Entities.BehaviourTrees.EnemiesTrees.BossMinotaurBehaviourTree import BossMinotaurBehaviourTree
from game.gameobjects.Entities.Enemies.boss_animation_state import AnimationState
from game.gameobjects.Weaponry.basic_sword import BasicSword
from game.gameobjects.Weaponry.boss_minotaur_enraged_weapon import EnragedWeapon


class MinotaurBoss(Enemy):
    def __init__(self):
        super().__init__()

        self.anim_state = AnimationState.IDLE
        self.fps = 0.1
        self.frame = 0
        self.frame_attack_1 = 18
        self.frame_attack_2 = 27

        self.boss_sprite = pyasge.Sprite()
        self.init_boss_sprite()

        self.is_enraged = False
        self.frame_attack_enraged = 33
        self.normal_weapon = BasicSword()
        self.enraged_weapon = EnragedWeapon()

        self.sprite.loadTexture("data/sprites/Blank 64x64.png")
        self.max_health = 25
        self.current_health = self.max_health
        self.armor = self.SUPER_HEAVY
        self.your_turn = False

        self.tree = BossMinotaurBehaviourTree()

        self.init()

    def init_boss_sprite(self):
        self.boss_sprite.loadTexture("data/sprites/Minotaur Boss-Sheet.png")
        self.boss_sprite.z_order = 11
        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 192
        self.boss_sprite.width = 192
        self.boss_sprite.scale = 1

    def init(self):
        self.sprite.alpha = 1.0
        self.sprite.scale = 1
        self.sprite.width = 64
        self.sprite.height = 64
        self.sprite.x = 0
        self.sprite.y = 0

    def update(self, game_time: pyasge.GameTime, data) -> None:
        self.move_boss_sprite()
        self.play_animation(game_time)
        self.check_enraged()

        if self.your_turn:
            self.tree.root.tick(self, data)

        self.update_health_bar()

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        if len(self.destination):
            self.anim_state = AnimationState.WALK
            if abs(self.position.distance(self.destination[0])) < self.speed * 0.02:
                self.position = self.destination.pop(0)
                self.midpoint = pyasge.Point2D(self.position.x + (self.sprite.width / 2),
                                               self.position.y + (self.sprite.height / 2))
                self.rotate()
                return

            self.position += self.direction * self.speed * game_time.fixed_timestep
        else:
            if self.anim_state == AnimationState.WALK:
                self.anim_state = AnimationState.IDLE

    def render(self, renderer: pyasge.Renderer) -> None:
        renderer.render(self.boss_sprite)
        renderer.render(self.sprite)
        renderer.render(self.health_bar)

    def play_animation(self, game_time: pyasge.GameTime):
        self.fps -= game_time.fixed_timestep
        if self.fps < 0:
            self.fps = 0.1
            self.frame += 1

        if self.anim_state == AnimationState.IDLE:
            self.idle_animation()
        elif self.anim_state == AnimationState.WALK:
            self.walk_animation()
        elif self.anim_state == AnimationState.ATTACK1:
            self.swing_animation()
        elif self.anim_state == AnimationState.ATTACK2:
            self.enrage_animation()

        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = self.frame * self.boss_sprite.width

    def idle_animation(self):
        if self.is_enraged:
            if self.frame > 9 or self.frame < 5:
                self.frame = 5
        else:
            if self.frame > 4:
                self.frame = 0

    def walk_animation(self):
        if self.is_enraged:
            if self.frame > 58 or self.frame < 51:
                self.frame = 51
        else:
            if self.frame > 17 or self.frame < 10:
                self.frame = 10

    def swing_animation(self):
        if self.is_enraged:
            if self.frame > 50:
                self.is_enraged = False
                self.anim_state = AnimationState.IDLE
        else:
            if self.frame > 25:
                self.anim_state = AnimationState.IDLE

    def enrage_animation(self):
        if self.frame > 32:
            self.anim_state = AnimationState.IDLE

    def check_enraged(self):
        if self.is_enraged:
            self.active_weapon = self.enraged_weapon
        else:
            self.active_weapon = self.normal_weapon

    def move_boss_sprite(self):
        self.boss_sprite.x = self.sprite.midpoint.x - (self.boss_sprite.width * self.boss_sprite.scale / 2)
        self.boss_sprite.y = self.sprite.y + self.sprite.height - ((self.boss_sprite.height - 64) * self.boss_sprite.scale)
