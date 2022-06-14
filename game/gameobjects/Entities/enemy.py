import pyasge

from game.gamedata import GameData
from abc import abstractmethod
from game.gameobjects.Entities.entity import Entity


class Enemy(Entity):

    @abstractmethod
    def __init__(self):
        super().__init__()
        self.max_health = 5
        self.current_health = self.max_health
        self.init()
        self.next_to_player = False
        self.tree = None

        self.health_bar = pyasge.Sprite()

        self.init_health_bar()

    @abstractmethod
    def init(self):
        pass

    def init_health_bar(self):
        self.health_bar.loadTexture("data/sprites/Health Bar-Sheet.png")
        self.health_bar.z_order = 11
        self.health_bar.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.health_bar.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 64
        self.health_bar.width = 64

    def update_health_bar(self):
        health_ratio = round(self.current_health/self.max_health, 1)
        self.health_bar.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = ((health_ratio * 10) - 1) * self.health_bar.width

        self.health_bar.x = self.sprite.x
        self.health_bar.y = self.sprite.y + 68

    @abstractmethod
    def update(self, game_time: pyasge.GameTime, data) -> None:
        pass

