import pyasge

from game.gameobjects.Entities.enemy import Enemy


class BasicEnemy(Enemy):

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.sprite.loadTexture("data/sprites/fishTile_081.png")
        self.sprite.x = 700
        self.sprite.y = 600
        self.width = 64
        self.height = 64
        self.sprite.flip_flags = pyasge.Sprite.FlipFlags.FLIP_X

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> None:
        pass
