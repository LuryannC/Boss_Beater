import random

import pyasge

from game.gameobjects.Entities.BehaviourTrees.BaseTreeNodes import Leaf, ReturnType, Selector
from game.gamefunctions.pathfinding import enemy_resolve


# Check distance between the enemy and player
class PlayerInRange(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        tiles = [[1, 0], [-1, 0], [0, 1], [0, -1], [-1, -1], [1, -1], [1, 1], [-1, 1]]
        player_pos = data.current_map.map.tile(data.player.position)
        enemy_pos = data.current_map.map.tile(actor.position)
        for tile in tiles:
            new_pos = (enemy_pos[0] + tile[0], enemy_pos[1] + tile[1])
            if new_pos == player_pos:
                actor.next_to_player = True
                return ReturnType.SUCCESS
        actor.next_to_player = False
        return ReturnType.FAILURE


class Moving(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        if len(actor.destination) != 0:
            return ReturnType.FAILURE
        return ReturnType.SUCCESS


# Move the enemy towards the player
class Move(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        added_position = [[1, 0], [-1, 0], [0, 1], [0, -1], [-1, -1], [1, -1], [1, 1], [-1, 1]]
        player_pos = data.current_map.map.tile(data.player.position)
        rand_index = random.choice(tuple(added_position))
        new_pos = (player_pos[0] + rand_index[0], player_pos[1] + rand_index[1])
        if not actor.next_to_player:
            actor.move_entity(enemy_resolve(data.current_map.map.world(new_pos), data.current_map.map, actor))
            return ReturnType.SUCCESS
        return ReturnType.FAILURE


# Attack player only if it's closer
class Attack(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        should_attack = 0  # random.randint(0, 1)
        player_pos = data.current_map.map.tile(data.player.position)
        if actor.next_to_player and actor.your_turn and actor.action_points > 0:
            actor.attack(player_pos, data.current_map.entities)
            print("enemy ac: " + str(actor.action_points))
            print("enemy mv: " + str(actor.movement_points))
            print("enemy attacked")
            return ReturnType.SUCCESS
        return ReturnType.FAILURE


# Avoid player
class Defend(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        actor.defending = True
        pass
