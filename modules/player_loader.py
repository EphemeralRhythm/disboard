import os
import importlib

SKILLS_PATH = "game.skills.classes"


def update_skills(player):
    class_folder_path = f"{SKILLS_PATH}.{player.player_class}"
    folder_path = os.path.join(SKILLS_PATH.replace(".", "/"), player.player_class)

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = file_name[:-3]

            module_path = f"{class_folder_path}.{module_name}"
            module = importlib.import_module(module_path)

            class_name = "".join(word.capitalize() for word in module_name.split("_"))

            skill_class = getattr(module, class_name)

            player.skills.append(skill_class(player))
