import pyasge
from game.gamedata import GameData
from game.gameobjects.Entities.enemy import Enemy
from game.gameobjects.Entities.BehaviourTrees.EnemiesTrees.BossPirateBehaviourTree import BossPirateBehaviourTree
from game.gameobjects.Entities.Enemies.boss_animation_state import AnimationState
from game.gameobjects.Weaponry.halberd import Halberd


class PirateBoss(Enemy):
    def __init__(self):
        super().__init__()

        self.anim_state = AnimationState.IDLE
        self.fps = 0.1
        self.frame = 0
        self.frame_attack_1 = 0
        self.frame_attack_2 = 38

        self.boss_sprite = pyasge.Sprite()
        self.init_boss_sprite()

        self.projectile_sprite = pyasge.Sprite()
        self.init_projectile_sprite()
        self.projectile_direction = None

        self.sprite.loadTexture("data/sprites/Blank 64x64.png")
        self.max_health = 30
        self.current_health = self.max_health
        self.armor = self.SUPER_HEAVY
        self.your_turn = False
        self.active_weapon = Halberd()

        self.tree = BossPirateBehaviourTree()

        self.init()

    def init_boss_sprite(self):
        self.boss_sprite.loadTexture("data/sprites/Pirate Boss-Sheet.png")
        self.boss_sprite.z_order = 11
        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 180
        self.boss_sprite.width = 180
        self.boss_sprite.scale = 1

    def init_projectile_sprite(self):
        self.projectile_sprite.loadTexture("data/sprites/Shoot Bone-Sheet.png")
        self.projectile_sprite.z_order = 101
        self.projectile_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.projectile_sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 256
        self.projectile_sprite.width = 256
        self.projectile_sprite.scale = 1

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
            renderer.render(self.projectile_sprite)
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
            self.shoot_animation()

        self.boss_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = self.frame * self.boss_sprite.width

    def idle_animation(self):
        if self.frame > 24 or self.frame < 14:
            self.frame = 14

    def walk_animation(self):
        if self.frame > 37 or self.frame < 25:
            self.frame = 25

    def swing_animation(self):
        if self.frame > 13:
            self.anim_state = AnimationState.IDLE

    def shoot_animation(self):
        if self.frame > 43:
            self.anim_state = AnimationState.IDLE

        if self.projectile_direction == "right":
            self.projectile_sprite.rotation = 0
            self.projectile_sprite.x = self.sprite.x + 64
            self.projectile_sprite.y = self.sprite.y

        elif self.projectile_direction == "left":
            self.projectile_sprite.rotation = 3.14
            self.projectile_sprite.x = self.sprite.x - 256
            self.projectile_sprite.y = self.sprite.y

        elif self.projectile_direction == "top":
            self.projectile_sprite.rotation = -1.57
            self.projectile_sprite.x = self.sprite.x - 96
            self.projectile_sprite.y = self.sprite.y - 96

        elif self.projectile_direction == "bot":
            self.projectile_sprite.rotation = 1.57
            self.projectile_sprite.x = self.sprite.x - 96
            self.projectile_sprite.y = self.sprite.y + 160

        self.projectile_sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = (self.frame - 38) * self.projectile_sprite.width

    def move_entity(self, path: list[pyasge.Point2D]) -> None:
        """Updates the ship's destination route"""
        self.destination = path

        for path in self.destination:
            path.x -= self.width * 0.5
            path.y -= self.height * 0.5

    def move_boss_sprite(self):
        self.boss_sprite.x = self.sprite.midpoint.x - (self.boss_sprite.width * self.boss_sprite.scale / 2)
        self.boss_sprite.y = self.sprite.y + self.sprite.height - self.boss_sprite.height * self.boss_sprite.scale
