import pyasge
import queue
import heapq
from typing import Dict, List, Tuple, TypeVar, Optional
from game.gameobjects.gamemap import GameMap
from game.gameobjects.Entities.entity import Entity

T = TypeVar('T')

Location = TypeVar('Location')


# algorithm from here - https://www.redblobgames.com/pathfinding/a-star/
class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


def get_neighbours(game_map, current_node: Location, map_width, map_height, combat) -> List[Location]:
    neighbours = []
    if combat:
        tiles_to_check = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    else:
        tiles_to_check = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    # , (-1, -1), (-1, 1), (1, -1), (1, 1)
    for new_position in tiles_to_check:
        node_position = (current_node[0] + new_position[0], current_node[1] + new_position[1])

        if node_position[0] > map_width - 1 or node_position[0] < 0 or node_position[1] > map_height - 1 or \
                node_position[1] < 0:
            continue

        if game_map.costs[node_position[1]][node_position[0]] > 8:
            continue

        neighbours.append(node_position)

    return neighbours


def heuristic(a: Location, b: Location) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_2(game_map, start: Location, goal: Location, combat):
    map_width = game_map.width
    map_height = game_map.height
    frontier = PriorityQueue()  # Create priority queue
    frontier.put(start, 0)  # Put in starting node with the highest priority
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()  # Current is now highest priority element from queue

        if current == goal:
            break

        for node in get_neighbours(game_map, current, map_width, map_height, combat):
            new_cost = cost_so_far[current] + game_map.costs[node[1]][node[0]]
            if node not in cost_so_far or new_cost < cost_so_far[node]:
                cost_so_far[node] = new_cost
                priority = new_cost + heuristic(node, goal)
                frontier.put(node, priority)
                came_from[node] = current

    return came_from


def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:  # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def resolve(xy: pyasge.Point2D, game_map: GameMap, entity: Entity):
    """
    Resolves the path needed to get to the destination point.

    Making use of the cost map, a suitable search algorithm should
    be used to create a series of tiles that the ship may pass
    through. These tiles should then be returned as a series of
    positions in world space.

    :param xy: The destination for the ship
    :param data: The game data, needed for access to the game map
    :return: list[pyasge.Point2D]
    """
    """
    box[0] is x
    box[1] is y
    box[2] is width
    box[3] is height
    """

    for box in game_map.out_of_bounds:
        if box[0] < xy.x < box[0] + box[2] and box[1] < xy.y < box[1] + box[3]:
            return []

    # convert point to tile location
    tile_loc = game_map.tile(xy)  # END
    tile_cost = game_map.costs[tile_loc[1]][tile_loc[0]]  # Tile cost of end point

    tiles_to_visit = []  # Path
    total_move_cost = 0

    start = game_map.tile(entity.position)
    end = tile_loc
    if start == end:
        return tiles_to_visit

    if tile_cost > 8:
        return tiles_to_visit

    if tile_cost < entity.movement_points:
        test = a_star_2(game_map, start, end, True)

        coordinates_list = reconstruct_path(test, start, end)

        for coordinates in coordinates_list:
            total_move_cost += game_map.costs[coordinates[1]][coordinates[0]]
            tiles_to_visit.append(game_map.world(coordinates))

        total_move_cost -= game_map.costs[start[1]][start[0]]

        if total_move_cost > entity.movement_points:
            print("too much")
            tiles_to_visit = []
            return tiles_to_visit

    entity.action_points -= 1
    entity.movement_points -= total_move_cost
    entity.tile = end

    # return a list of tile positions to follow
    path = []
    for tile in tiles_to_visit:
        path.append(tile)
    return path


def enemy_resolve(xy: pyasge.Point2D, game_map: GameMap, entity: Entity):
    # Used for enemies because they can try to move further away from their current movement points
    for box in game_map.out_of_bounds:
        if box[0] < xy.x < box[0] + box[2] and box[1] < xy.y < box[1] + box[3]:
            return []

    # convert point to tile location
    tile_loc = game_map.tile(xy)  # END
    tile_cost = game_map.costs[tile_loc[1]][tile_loc[0]]  # Tile cost of end point

    tiles_to_visit = []  # Path
    total_move_cost = 0
    new_move_cost = 0

    start = game_map.tile(entity.position)
    end = tile_loc

    if tile_cost > 8:
        return tiles_to_visit

    if tile_cost < entity.movement_points:
        test = a_star_2(game_map, start, end, True)

        coordinates_list = reconstruct_path(test, start, end)

        for coordinates in coordinates_list:
            total_move_cost += game_map.costs[coordinates[1]][coordinates[0]]
            tiles_to_visit.append(game_map.world(coordinates))

        total_move_cost -= game_map.costs[start[1]][start[0]]
        new_move_cost -= game_map.costs[start[1]][start[0]]

        if total_move_cost > entity.movement_points:
            for coordinate in range(len(tiles_to_visit)):
                temp = game_map.tile(tiles_to_visit[coordinate])
                new_move_cost += game_map.costs[temp[1]][temp[0]]
                if new_move_cost == entity.movement_points:
                    del tiles_to_visit[coordinate:]
                    break
                elif new_move_cost > entity.movement_points:
                    del tiles_to_visit[coordinate - 1:]
                    break
            entity.movement_points -= new_move_cost
        else:
            entity.movement_points -= total_move_cost

    entity.action_points -= 1

    print(entity.movement_points)
    entity.tile = end

    # return a list of tile positions to follow
    path = []
    for tile in tiles_to_visit:
        path.append(tile)
    return path


def can_reach(xy: pyasge.Point2D, game_map: GameMap, entity: Entity) -> bool:

    for box in game_map.out_of_bounds:
        if box[0] < xy.x < box[0] + box[2] and box[1] < xy.y < box[1] + box[3]:
            return False

    # convert point to tile location
    tile_loc = game_map.tile(xy)  # END
    tile_cost = game_map.costs[tile_loc[1]][tile_loc[0]]  # Tile cost of end point

    tiles_to_visit = []  # Path
    total_move_cost = 0

    start = game_map.tile(entity.position)
    end = tile_loc

    if tile_cost > 8:
        return False

    if tile_cost < entity.movement_points:
        test = a_star_2(game_map, start, end, True)

        coordinates_list = reconstruct_path(test, start, end)

        coordinates_list.remove(game_map.tile(entity.position))

        for coordinates in coordinates_list:
            total_move_cost += game_map.costs[coordinates[1]][coordinates[0]]
            tiles_to_visit.append(game_map.world(coordinates))

        if total_move_cost <= entity.movement_points:
            return True
    return False


def world_move(xy: pyasge.Point2D, game_map: GameMap, entity: Entity):

    for box in game_map.out_of_bounds:
        if box[0] < xy.x < box[0] + box[2] and box[1] < xy.y < box[1] + box[3]:
            return []

    # convert point to tile location
    tile_loc = game_map.tile(xy)  # END
    tile_cost = game_map.costs[tile_loc[1]][tile_loc[0]]  # Tile cost of end point

    tiles_to_visit = []  # Path

    start = game_map.tile(entity.position)
    end = tile_loc
    if start == end:
        return tiles_to_visit

    if tile_cost > 8:
        return tiles_to_visit

    if tile_cost < entity.movement_points:
        test = a_star_2(game_map, start, end, False)

        coordinates_list = reconstruct_path(test, start, end)
        if len(entity.destination):
            coordinates_list.remove(game_map.tile(entity.position))

        for coordinates in coordinates_list:
            tiles_to_visit.append(game_map.world(coordinates))

    entity.tile = end

    # return a list of tile positions to follow
    path = []
    for tile in tiles_to_visit:
        path.append(tile)
    return path


def walk_there(xy: pyasge.Point2D, game_map: GameMap):
    # Move without pathfinding
    tile_loc = game_map.tile(xy)
    tile_cost = game_map.costs[tile_loc[1]][tile_loc[0]]

    if tile_cost > 1:
        return []

    tiles_to_visit = [game_map.world(tile_loc)]

    return tiles_to_visit


def can_world_move(xy: pyasge.Point2D, game_map: GameMap) -> bool:

    tile_loc = game_map.tile(xy)
    tile_cost = game_map.costs[tile_loc[1]][tile_loc[0]]

    for box in game_map.out_of_bounds:
        if box[0] < xy.x < box[0] + box[2] and box[1] < xy.y < box[1] + box[3]:
            return False

    if tile_cost > 8:
        return False

    return True


def attack_range(xy: pyasge.Point2D, game_map: GameMap, entity: Entity) -> bool:

    player_pos = game_map.tile(entity.position)
    mouse_pos = game_map.tile(xy)
    mouse_cost = game_map.costs[mouse_pos[1]][mouse_pos[0]]

    if mouse_cost > 8:
        return False

    weapon_range = entity.active_weapon.range

    if player_pos[0] + weapon_range >= mouse_pos[0] >= player_pos[0] - weapon_range and \
            player_pos[1] + weapon_range >= mouse_pos[1] >= player_pos[1] - weapon_range:
        return True

    return False

