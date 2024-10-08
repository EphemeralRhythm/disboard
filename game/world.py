from collections import deque
from game.command import Command

from game.entities.mobs.slime.slime import Slime
import utils.database as db

from game.cell import Cell

from game.entities.player.player import Player
from models.interface.discord_event import DiscordEvent

import importlib


class World:
    def __init__(self):
        self.grid = [[1]]

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.maps = [
            [Cell(self, 1, 0, 0) for c in range(self.cols)] for r in range(self.rows)
        ]

        self.dead_pool = Cell(self, 1, -1, -1)

        self.init_maps()

        self.players = {}

        self.commands_queue = deque()
        self.discord_events = []

    def init_maps(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.maps[r][c] = Cell(self, self.grid[r][c], r, c)

    def update(self):
        self.handle_commands()
        for r in range(self.rows):
            for c in range(self.cols):
                self.maps[r][c].update()

        for player in self.players.values():
            player.update()

    def add_player(self, post):
        player_class_name = post["class"]
        module = importlib.import_module(
            f"game.entities.player.classes.{player_class_name}"
        )

        player_class = getattr(module, player_class_name.title())
        player = player_class(self, post)

        r = player.grid_r
        c = player.grid_c
        self.players[post["_id"]] = player

        self.maps[r][c].add_player(player)

    def init_players(self):
        for player in db.players_collection.find():
            self.add_player(player)

    def init_entities(self):
        slime = Slime(24 * 16, 32 * 16, 0, 0, self)
        if slime.cell:
            slime.cell.spawn_entity(slime)

    def has_player(self, id):
        return db.players_collection.find_one({"_id": id}) is not None

    def create_player(self, id: str, gender, cl, color) -> bool:
        if self.has_player(id):
            return False

        post = {}
        post["_id"] = id

        # x and y are placeholders
        # change after adding spawn location(s)
        post["x"] = 50
        post["y"] = 50
        post["grid_r"] = 0
        post["grid_c"] = 0

        # also placeholders
        post["hp"] = 100
        post["gender"] = gender
        post["class"] = cl
        post["color"] = color

        post["level"] = 1

        self.add_player(post)
        db.players_collection.insert_one(post)
        return True

    def get_players(self) -> dict:
        return self.players

    def get_player(self, id) -> Player | None:
        if id not in self.players:
            return None

        return self.players[id]

    def add_event(self, event: DiscordEvent):
        self.discord_events.append(event)

    def get_events(self):
        events = list(self.discord_events)
        self.discord_events = []

        return events

    def add_command(self, command: Command):
        self.commands_queue.append(command)

    def handle_commands(self):
        while self.commands_queue:
            command = self.commands_queue.popleft()
            self.handle_command(command)

    def handle_command(self, command: Command):
        author_id = command.author.id
        player = self.get_player(author_id)
        assert player

        if command.name == "move":
            x = command.x
            y = command.y

            player.change_to_move_state(x, y)

        elif command.name == "attack":
            t = command.target
            assert t

            if t.name == "player":
                target = self.get_player(t.id)
            else:
                target = player.cell.entities.get(t.id)

            if not target:
                # command failed
                return

            player.change_to_attack_state(target)

        elif command.name == "cast":
            skill = command.skill
            assert skill, "Failed to load skill, world (cast) update"

            index = player.skills.index(skill)
            ps = player.skills[index]
            ps.x = skill.x
            ps.y = skill.y

            t = skill.target

            if t:
                if t.name == "player":
                    target = self.get_player(t.id)
                else:
                    target = player.cell.entities.get(t.id)

                ps.target = target

            print("casting", skill)
            player.cast(ps)

        elif command.name == "set_channel":
            player.channel_id = command.x
            db.players_collection.update_one(
                {"_id": player.id}, {"$set": {"channel_id": command.x}}
            )

    def get_targetable_entities(self, player: Player, x=0, y=0):
        return player.cell.get_targetable_entities(player, x, y)
