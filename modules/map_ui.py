from PIL import Image, ImageDraw
from utils.constants import VIEWPORT_X, VIEWPORT_Y, ZOOMED_VIEWPORT_X, ZOOMED_VIEWPORT_Y


def in_image_bounds(map_object, camera_x, camera_y):
    u_x, u_y = map_object.x, map_object.y

    return not (
        u_x < camera_x - VIEWPORT_X // 2 - map_object.size[0]
        or u_x > camera_x + VIEWPORT_X // 2 + map_object.size[0]
        or u_y < camera_y - VIEWPORT_Y // 2 - map_object.size[1]
        or u_y > camera_y + VIEWPORT_Y // 2 + map_object.size[1]
    )


def draw_map(x: int, y: int, map_cell, zoomed=False, unit=None):
    if zoomed:
        viewport_x = ZOOMED_VIEWPORT_X
        viewport_y = ZOOMED_VIEWPORT_Y
    else:
        viewport_x = VIEWPORT_X
        viewport_y = VIEWPORT_Y

    map_size_x, map_size_y = map_cell.size[0], map_cell.size[1]

    # constraint x and y
    x = max(x, viewport_x // 2)
    x = min(x, map_size_x - viewport_x // 2)

    y = max(y, viewport_y // 2)
    y = min(y, map_size_y - viewport_y // 2)

    map_entities = []

    grid_collections = [
        map_cell.players,
        map_cell.entities.values(),
        map_cell.map_objects,
    ]

    for collection in grid_collections:
        for obj in collection:
            if in_image_bounds(obj, x, y):
                map_entities.append(obj)

    map_entities.sort(key=lambda obj: obj.y)

    map_image = Image.open(map_cell.base_image_path)

    draw = ImageDraw.Draw(map_image)

    if unit:

        player = unit
        node_x = player.x - player.x % 16
        node_y = player.y - player.y % 16
        print(node_x, node_y)

        # draw.rounded_rectangle((node_x, node_y, node_x + 16, node_y + 16), fill="red")

    for entity in map_entities:
        if not entity.is_stealthed() or entity == unit:
            entity.draw(map_image)

    for entity in map_entities:
        pass
        # entity.draw_effects()

    map_image = map_image.crop(
        (
            x - viewport_x // 2,
            y - viewport_y // 2,
            x + viewport_x // 2,
            y + viewport_y // 2,
        )
    )

    if zoomed:
        map_image = map_image.resize((viewport_x * 4, viewport_y * 4), Image.NEAREST)

    return map_image
