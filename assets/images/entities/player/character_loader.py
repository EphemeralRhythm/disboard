from PIL import Image
import os

palette = Image.open("./palette.png")

colors = {}

num_colors = 16

color_names = ["blue", "red", "green", "orange", "yellow", "purple"]

for i in range(num_colors):
    color = palette.getpixel((8 * i, 0))

    colors[color] = [color]

    for j in range(1, 6):
        colors[color].append(palette.getpixel((8 * i, 8 * j)))

print(colors)


def replace_colors(image, index):
    cols, rows = image.size

    for r in range(rows):
        for c in range(cols):
            if (color := image.getpixel((r, c))) in colors:
                image.putpixel((r, c), colors[color][index])

    return image


for item in os.listdir():
    if os.path.isfile(item):
        continue

    for gen in ["male", "female"]:
        path = os.path.join(item, gen + ".png")

        os.makedirs(os.path.join(item, gen), exist_ok=True)

        for index in range(5):
            image = Image.open(path)
            new_image = replace_colors(image, index)

            os.makedirs(os.path.join(item, gen, color_names[index]), exist_ok=True)

            idle = new_image.crop((32 * 0, 32 * 0, 32 * 1, 32 * 1))
            left = new_image.crop((32 * 0, 32 * 1, 32 * 1, 32 * 2))
            down = new_image.crop((32 * 1, 32 * 1, 32 * 2, 32 * 2))
            up = new_image.crop((32 * 2, 32 * 1, 32 * 3, 32 * 2))
            attack = new_image.crop((32 * 0, 32 * 2, 32 * 1, 32 * 3))

            idle.save(os.path.join(item, gen, color_names[index], "idle.png"))
            left.save(os.path.join(item, gen, color_names[index], "left.png"))
            down.save(os.path.join(item, gen, color_names[index], "down.png"))
            up.save(os.path.join(item, gen, color_names[index], "up.png"))
            attack.save(os.path.join(item, gen, color_names[index], "attack.png"))
