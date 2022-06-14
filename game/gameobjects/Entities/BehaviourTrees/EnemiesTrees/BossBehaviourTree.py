from game.gameobjects.Entities.BehaviourTrees.BaseTreeNodes import Leaf, ReturnType
from game.gameobjects.Entities.Enemies.boss_animation_state import AnimationState


def check_tiles(actor, data, tiles) -> bool:
    player_pos = data.current_map.map.tile(data.player.position)
    enemy_pos = data.current_map.map.tile(actor.position)
    for tile in tiles:
        new_pos = (enemy_pos[0] + tile[0], enemy_pos[1] + tile[1])
        if new_pos != player_pos:
            actor.next_to_player = False
        else:
            actor.next_to_player = True
            return True
    return False


class PlayerInRangeSwing(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        if actor.anim_state == AnimationState.IDLE:
            tiles = [[-1, -1], [0, -1], [1, -1],
                     [-1, 0], [1, 0],
                     [-1, 1], [0, 1], [1, 1]]
            if check_tiles(actor, data, tiles):
                return ReturnType.SUCCESS
            else:
                return ReturnType.FAILURE
        else:
            return ReturnType.FAILURE


class PlayerInRangeAOE(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        if actor.anim_state == AnimationState.IDLE:
            tiles = [[-2, -2], [-1, -2], [0, -2], [1, -2], [2, -2],
                     [-2, -1], [2, -1],
                     [-2, 0], [2, 0],
                     [-2, 1], [2, 1],
                     [-2, 2], [-1, 2], [0, 2], [1, 2], [2, 2]]
            if check_tiles(actor, data, tiles):
                return ReturnType.SUCCESS
            else:
                return ReturnType.FAILURE
        else:
            return ReturnType.FAILURE


class PlayerInRangeShoot(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        if actor.anim_state == AnimationState.IDLE:
            tiles_right = [[1, 0], [2, 0], [3, 0], [4, 0]]
            tiles_left = [[-1, 0], [-2, 0], [-3, 0], [-4, 0]]
            tiles_top = [[0, -1], [0, -2], [0, -3], [0, -4]]
            tiles_bot = [[0, 1], [0, 2], [0, 3], [0, 4]]

            if check_tiles(actor, data, tiles_right):
                actor.projectile_direction = "right"
                return ReturnType.SUCCESS
            elif check_tiles(actor, data, tiles_left):
                actor.projectile_direction = "left"
                return ReturnType.SUCCESS
            elif check_tiles(actor, data, tiles_top):
                actor.projectile_direction = "top"
                return ReturnType.SUCCESS
            elif check_tiles(actor, data, tiles_bot):
                actor.projectile_direction = "bot"
                return ReturnType.SUCCESS
            else:
                return ReturnType.FAILURE
        else:
            return ReturnType.FAILURE


class IsBossEnraged(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        if actor.is_enraged:
            return ReturnType.SUCCESS
        else:
            return ReturnType.FAILURE


# Swing attack, AOE around boss
class AttackSwing(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        player_pos = data.current_map.map.tile(data.player.position)
        if actor.next_to_player and actor.your_turn and actor.action_points > 0:
            actor.attack(player_pos, data.current_map.entities)
            # actor.action_points -= 1
            actor.anim_state = AnimationState.ATTACK1
            actor.frame = actor.frame_attack_1
            print("=== SWING ATTACK ===")
            print("BOSS ACTION POINTS: " + str(actor.action_points))
            print("")
            # print("enemy mv: " + str(actor.movement_points))
            # print("enemy attacked")
            return ReturnType.SUCCESS
        return ReturnType.FAILURE


# Ranged AOE attack around player
class AttackAOE(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        player_pos = data.current_map.map.tile(data.player.position)
        if actor.next_to_player and actor.your_turn and actor.action_points > 0:
            actor.attack(player_pos, data.current_map.entities)
            # actor.action_points -= 1
            actor.anim_state = AnimationState.ATTACK2
            actor.frame = actor.frame_attack_2
            print("=== AOE ATTACK ===")
            print("BOSS ACTION POINTS: " + str(actor.action_points))
            print("")
            # print("enemy mv: " + str(actor.movement_points))
            # print("enemy attacked")
            return ReturnType.SUCCESS
        return ReturnType.FAILURE


class AttackShoot(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        player_pos = data.current_map.map.tile(data.player.position)
        if actor.next_to_player and actor.your_turn and actor.action_points > 0:
            actor.attack(player_pos, data.current_map.entities)
            # actor.action_points -= 1
            actor.anim_state = AnimationState.ATTACK2
            actor.frame = actor.frame_attack_2
            print("=== SHOOT ATTACK ===")
            print("BOSS ACTION POINTS: " + str(actor.action_points))
            print("")
            # print("enemy mv: " + str(actor.movement_points))
            # print("enemy attacked")
            return ReturnType.SUCCESS
        return ReturnType.FAILURE


# Deal increased damage on next attack
class Enrage(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        if actor.anim_state == AnimationState.IDLE:
            if actor.your_turn and actor.action_points > 0 and actor.is_enraged is False:
                actor.action_points -= 1
                actor.anim_state = AnimationState.ATTACK2
                actor.frame = actor.frame_attack_2
                actor.is_enraged = True
                print("=== ENRAGE ===")
                print("BOSS ACTION POINTS: " + str(actor.action_points))
                print("")
                return ReturnType.SUCCESS
            return ReturnType.FAILURE
        else:
            return ReturnType.FAILURE


class AttackEnraged(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        player_pos = data.current_map.map.tile(data.player.position)
        if actor.next_to_player and actor.your_turn and actor.action_points > 0:
            actor.attack(player_pos, data.current_map.entities)
            # actor.action_points -= 1
            actor.anim_state = AnimationState.ATTACK1
            actor.frame = actor.frame_attack_enraged
            print("=== ENRAGED SWING ATTACK ===")
            print("BOSS ACTION POINTS: " + str(actor.action_points))
            print("")
            # print("enemy mv: " + str(actor.movement_points))
            # print("enemy attacked")
            return ReturnType.SUCCESS
        return ReturnType.FAILURE


class IsBossNotMoving(Leaf):
    def __init__(self):
        super().__init__()

    def tick(self, actor, data):
        if len(actor.destination) == 0 and actor.anim_state == AnimationState.IDLE:
            return ReturnType.SUCCESS
        else:
            return ReturnType.FAILURE
