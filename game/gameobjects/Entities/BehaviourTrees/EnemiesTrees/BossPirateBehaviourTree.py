from game.gameobjects.Entities.BehaviourTrees.BaseTreeNodes import BehaviourTree, Selector, Sequence
from game.gameobjects.Entities.BehaviourTrees.EnemiesTrees.EnemiesBehaviourTree import Move
from game.gameobjects.Entities.BehaviourTrees.EnemiesTrees.BossBehaviourTree import PlayerInRangeSwing, \
    AttackSwing, PlayerInRangeShoot, AttackShoot, IsBossNotMoving


# Build tree
class BossPirateBehaviourTree(BehaviourTree):
    def __init__(self):
        super().__init__()
        self.build_tree()

    def build_tree(self):
        self.root.set_child(Selector())

        self.root.children[0].add_child(Sequence())
        self.root.children[0].children[0].add_child(PlayerInRangeSwing())
        self.root.children[0].children[0].add_child(AttackSwing())

        self.root.children[0].add_child(Sequence())
        self.root.children[0].children[1].add_child(PlayerInRangeShoot())
        self.root.children[0].children[1].add_child(AttackShoot())

        self.root.children[0].add_child(Sequence())
        self.root.children[0].children[2].add_child(IsBossNotMoving())
        self.root.children[0].children[2].add_child(Move())

        self.root.ready()
