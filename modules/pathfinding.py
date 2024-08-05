import math
from queue import PriorityQueue

def heuristic(s: tuple, e: tuple):
    return max(abs(s[0] - e[0]), abs(s[1] - e[1]))


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def astar(start_coords: tuple, end_coords: tuple, world_map):
    """
        Provide the coordinates as (x, y) tuples
    """
    start = (start_coords[1] // 16, start_coords[0] // 16)
    end = (end_coords[1] // 16, end_coords[0] // 16)

    pq = PriorityQueue()
    open_set = set()

    pq.put((0, start))
    open_set.add(start)

    g_score = {}
    came_from = {}

    g_score[start] = 0

    dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while not pq.empty():
        current = pq.get()[1]
        r, c = current
        height = world_map[r][c]
        open_set.remove(current)

        if current == end:
            return reconstruct_path(came_from, end)

        for d in dir:
            nr = r + d[0]
            nc = c + d[1]

            if nr < 0 or nr >= len(world_map):
                continue
            if nc < 0 or nc >= len(world_map[0]):
                continue

            new_height = world_map[nr][nc]

            if abs(height - new_height) > 1:
                continue

            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score.get((nr, nc), float("inf")):
                came_from[(nr, nc)] = current
                g_score[(nr, nc)] = temp_g_score
                f_score = temp_g_score + heuristic(
                    (nr, nc), end
                )

                if (nr, nc) not in open_set:
                    pq.put((f_score, (nr, nc)))
                    open_set.add((nr, nc))
    return None
