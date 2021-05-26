from typing import List, Tuple, Dict
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class GridSquare:
    def __init__(self, coords, grid_square_value,
                 neighbor_north=None,
                 neighbor_east=None,
                 neighbor_south=None,
                 neighbor_west=None):
        self.val = grid_square_value
        self.coords = coords
        self.is_land = grid_square_value == '1'
        self.island = None

        self.neighbors = {
            Direction.NORTH: neighbor_north,
            Direction.EAST: neighbor_east,
            Direction.SOUTH: neighbor_south,
            Direction.WEST: neighbor_west}

    def is_marked(self):
        return self.is_land and self.island is not None

    def __repr__(self):
        if self.is_land:
            return 'WATER'
        else:
            return f'LAND at {self.coords}'

    def unmarked_neighbors(self):
        return {d: neigh for d, neigh in self.neighbors.items() if neigh is None or not neigh.is_marked()}


WATER = GridSquare((-1, -1), '0')


def translate(c1, c2):
    return c1[0] + c2[0], c1[1] + c2[1]


def translate_by_direction(coord, direction: Direction):
    if direction == Direction.NORTH:
        return translate(coord, (0, 1))
    elif direction == Direction.EAST:
        return translate(coord, (1, 0))
    elif direction == Direction.SOUTH:
        return translate(coord, (0, -1))
    elif direction == Direction.WEST:
        return translate(coord, (-1, 0))
    else:
        raise ValueError(f'{direction} is not valid for translation')


def build_square(grid, x, y):
    if grid[x][y] == '1':
        coords = (x, y)
        gs = GridSquare(coords, grid[x][y])
        if coords[0] == 0:
            gs.neighbor_west = WATER
        if coords[0] >= len(grid):
            gs.neighbor_east = WATER
        if coords[1] == 0:
            gs.neighbor_nort = WATER
        if coords[1] >= len(grid[coords[0]]):
            gs.neighbor_sout = WATER

        return gs

    else:
        return WATER


# noinspection PyPep8Naming,PyMethodMayBeStatic
class Solution:
    def __init__(self):
        self.islands: List[List[GridSquare]] = []

    def add_to_island(self, island: List[GridSquare], gs: GridSquare):
        island_index = f'island {self.islands.index(island)}'
        if gs in island:
            print(f'{gs.coords} is already in {island_index}')
            return;
        else:
            print(f'adding {gs.coords} to {island_index}')
            island.append(gs)
            gs.island = island

    def numIslands(self, grid: List[List[str]]) -> int:
        grid_map: Dict[Tuple[int, int], GridSquare] = {}

        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid_map[(x, y)] = build_square(grid, x, y)

        for coords, gs in grid_map.items():
            if gs.is_land:
                # mark square
                if not gs.is_marked():
                    print(f'new island for {gs.coords}')
                    new_island = []
                    self.islands.append(new_island)
                    self.add_to_island(new_island, gs)

                self.mark_neighbors(grid_map, gs)

        count = len(self.islands)

        print(f'islands[{count}]')
        for i in self.islands:
            print(f'Island {i}:')

        return count

    def mark_neighbors(self, grid_map, gs):
        for d in gs.neighbors:
            if gs.neighbors[d] is None:
                d_coords = translate_by_direction(gs.coords, d)
                gs.neighbors[d] = grid_map[d_coords] if d_coords in grid_map else WATER
                print(f'{gs.coords}.neighbor[{d.name}] = {gs.neighbors[d]}')

            if gs.neighbors[d] is not WATER:
                self.add_to_island(gs.island, gs.neighbors[d])

            unmarked_island = (gs2 for gs2 in gs.island if gs2.island is not gs.island)

            for gs2 in unmarked_island:
                self.mark_neighbors(grid_map, gs2)
