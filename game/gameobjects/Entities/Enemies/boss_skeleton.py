import pyasge

from game.gameobjects.Entities.enemy import Enemy
from game.gameobjects.Entities.BehaviourTrees.EnemiesTrees.BossSkeletonBehaviourTree import BossSkeletonBehaviourTree
from game.gameobjects.Entities.Enemies.boss_animation_state import AnimationState
from game.gameobjects.Weaponry.falcon_punch import FalconPunch


class SkeletonBoss(Enemy):
    def __init__(self):
        super().__init__()

        self.anim_state = AnimationState.IDLE
        self.fps = 0.2
        self.frame = 0
        self.frame_attack_1 = 8
        self.frame_attack_2 = 13

        self.active_weapon = FalconPunch()

        self.boss_sprite = pyasge.Sprite()
        self.init_boss_sprite()

        self.shockwave_sprite = pyasge.Sprite()
        self.init_shockwave_sprite()

        self.sprite.loadTexture("data/sprites/Blank 64x64.png")
        self.max_health = 25
        self.current_health = self.max_health
        self.armor = self.HEAVY
        self.your_turn = False

        self.tree = BossSkeletonBehaviourTree()

        self.init()

    def init_boss_sprite(self):
        self.boss_sprite.loadTexture("data/sprites/Ghost Boss-Sheet.png")
        self.boss_sprite.z_order = 11
        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 96
        self.boss_sprite.width = 96
        self.boss_sprite.scale = 1.5

    def init_shockwave_sprite(self):
        self.shockwave_sprite.loadTexture("data/sprites/Shockwave-Sheet.png")
        self.shockwave_sprite.z_order = 101
        self.shockwave_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.shockwave_sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 320
        self.shockwave_sprite.width = 320
        self.shockwave_sprite.height = 320
        self.shockwave_sprite.scale = 1

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
        if self.anim_state == AnimationState.ATTACK2:
            renderer.render(self.shockwave_sprite)

        renderer.render(self.health_bar)

    def play_animation(self, game_time: pyasge.GameTime):
        self.fps -= game_time.fixed_timestep
        if self.fps < 0:
            self.fps = 0.2
            self.frame += 1

        if self.anim_state == AnimationState.IDLE:
            self.idle_animation()
        elif self.anim_state == AnimationState.WALK:
            self.walk_animation()
        elif self.anim_state == AnimationState.ATTACK1:
            self.swing_animation()
        elif self.anim_state == AnimationState.ATTACK2:
            self.aoe_animation()

        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = self.frame * self.boss_sprite.width

    def idle_animation(self):
        if self.frame > 1:
            self.frame = 0

    def walk_animation(self):
        if self.frame > 7 or self.frame < 2:
            self.frame = 2

    def swing_animation(self):
        if self.frame > 12:
            self.anim_state = AnimationState.IDLE

    def aoe_animation(self):
        if self.frame > 15:
            self.anim_state = AnimationState.IDLE

        self.shockwave_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = (self.frame - 13) * self.shockwave_sprite.width

        self.shockwave_sprite.x = self.sprite.x - 128
        self.shockwave_sprite.y = self.sprite.y - 128

    def move_boss_sprite(self):
        self.boss_sprite.x = self.sprite.midpoint.x - (self.boss_sprite.width * self.boss_sprite.scale / 2)
        self.boss_sprite.y = self.sprite.y + self.sprite.height - self.boss_sprite.height * self.boss_sprite.scale
