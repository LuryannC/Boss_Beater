from game.gameobjects.Entities.BehaviourTrees.BaseTreeNodes import BehaviourTree, Selector, Sequence, Leaf
from game.gameobjects.Entities.BehaviourTrees.EnemiesTrees.EnemiesBehaviourTree import PlayerInRange, Attack, Defend, \
    Move, Moving


class ScytheAttack(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        pass


# Build tree
class GhostBehaviourTree(BehaviourTree):
    def __init__(self):
        super().__init__()
        self.build_tree()

    def build_tree(self):
        self.root.set_child(Selector())

        self.root.children[0].add_child(Sequence())
        self.root.children[0].children[0].add_child(PlayerInRange())
        self.root.children[0].children[0].add_child(Attack())

        self.root.children[0].add_child(Sequence())
        self.root.children[0].children[1].add_child(Moving())
        self.root.children[0].children[1].add_child(Move())

        # self.root.children[0].add_child(Defend())

        self.root.ready()