import pyasge

from game.gameobjects.Entities.enemy import Enemy
from game.gameobjects.Entities.BehaviourTrees.EnemiesTrees.GhostBehaviourTree import GhostBehaviourTree
from game.gameobjects.Weaponry.scythe import Scythe


class GhostEnemies(Enemy):

    def __init__(self):
        super().__init__()

        self.max_health = 25
        self.current_health = self.max_health
        self.armor = self.WEAK
        self.your_turn = False
        self.tree = GhostBehaviourTree()
        self.active_weapon = Scythe()

        self.init()

    def init(self):
        self.sprite.loadTexture("data/sprites/GhostPNG.png")
        self.sprite.alpha = 1.0
        self.sprite.width = 64
        self.sprite.height = 64

    def update(self, game_time: pyasge.GameTime, data) -> None:
        if self.your_turn:
            self.tree.root.tick(self, data)

        self.update_health_bar()

    def render(self, renderer: pyasge.Renderer) -> None:
        renderer.render(self.sprite)
        renderer.render(self.health_bar)
