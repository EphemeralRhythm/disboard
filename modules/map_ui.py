from PIL import Image, ImageDraw
from utils.constants import VIEWPORT_X, VIEWPORT_Y


def in_image_bounds(map_object, camera_x, camera_y):
    u_x, u_y = map_object.x, map_object.y

    return not (
        u_x < camera_x - VIEWPORT_X // 2 - map_object.size[0]
        or u_x > camera_x + VIEWPORT_X // 2 + map_object.size[0]
        or u_y < camera_y - VIEWPORT_Y // 2 - map_object.size[1]
        or u_y > camera_y + VIEWPORT_Y // 2 + map_object.size[1]
    )


def draw_map(x: int, y: int, map_cell, unit=None):

    map_size_x, map_size_y = map_cell.size[0], map_cell.size[1]

    # constraint x and y
    x = max(x, VIEWPORT_X // 2)
    x = min(x, map_size_x - VIEWPORT_X // 2)

    y = max(y, VIEWPORT_Y // 2)
    y = min(y, map_size_y - VIEWPORT_Y // 2)

    map_entities = []

    player_mp = map_cell.world.players
    players = [player_mp[p] for p in map_cell.players]

    grid_collections = [players, map_cell.entities, map_cell.map_objects]

    for collection in grid_collections:
        for obj in collection:
            if in_image_bounds(obj, x, y):
                map_entities.append(obj)

    map_entities.sort(key=lambda obj: obj.y)

    map_image = Image.open(map_cell.base_image_path)

    draw = ImageDraw.Draw(map_image)

    if unit:

        player = map_entities[0]
        node_x = player.x - player.x % 16
        node_y = player.y - player.y % 16
        print(node_x, node_y)

        draw.rounded_rectangle((node_x, node_y, node_x + 16, node_y + 16), fill="red")

    for entity in map_entities:
        entity.draw(map_image)

    for entity in map_entities:
        pass
        # entity.draw_effects()

    map_image = map_image.crop(
        (
            x - VIEWPORT_X // 2,
            y - VIEWPORT_Y // 2,
            x + VIEWPORT_X // 2,
            y + VIEWPORT_Y // 2,
        )
    )

    return map_image
