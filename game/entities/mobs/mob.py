from game.entities.entity import Entity
from game.states.mobStates.mobIdleState import MobIdleState
from game.states.mobStates.mobAttackState import MobAttackState
from game.states.stateManager import StateManager
from game.utils import distance


class Mob(Entity):
    def __init__(self, name, world):
        super().__init__(name, world)

        self.idleState = MobIdleState(self)
        self.stateManager = StateManager(self, self.idleState)

        self.damage_table = {}

    def get_targets(self):
        return self.cell.players

    def update_enemies(self):
        self.enemies_within_radius.clear()
        players = self.cell.players

        for player in players:
            dist = distance(self, player) // 16

            print("player: ", player, dist)
            if dist <= self.aggro_radius:
                self.enemies_within_radius.append((player, dist))

    def update_aggro(self):
        self.update_enemies()
        target = None
        if isinstance(self.stateManager.currentState, MobAttackState):
            target = self.stateManager.currentState.target

        enemies = self.enemies_within_radius
        aggro_table = self.aggro_table
        mp = {}

        for enemy, dist in enemies:
            if enemy not in aggro_table:
                aggro_table[enemy] = 0

            distance_factor = 30

            if dist <= 2:
                distance_factor = 100
            elif dist <= 6:
                distance_factor = 80
            elif dist <= 12:
                distance_factor = 70

            distance_factor /= 100

            level_difference = self.LEVEL - enemy.LEVEL
            aggro_bonus = 100

            # 20 % of this is distance
            aggro_bonus += int(distance_factor * 20)

            # bonus for level difference
            aggro_bonus += int(level_difference)

            if enemy == target:
                aggro_bonus += 20

            damage = self.damage_table.get(enemy.id, enemy.get_attack_damage() / 10)

            aggro_increase = aggro_bonus * damage / 100

            mp[enemy] = aggro_table[enemy] + aggro_increase

        self.aggro_table = mp
        self.damage_table.clear()

        print(f"{self}, aggro: ", aggro_table)

        if len(self.aggro_table) == 0:
            return

        mx = 0
        new_target = None

        for e in aggro_table:
            if aggro_table[e] > mx:
                mx = aggro_table[e]
                new_target = e

        print("mx: ", mx, new_target)

        if new_target and mx > 1.2 * self.aggro_table.get(target, 0):
            self.stateManager.changeState(MobAttackState(self, new_target))

    def take_damage(self, damage: int, entity=None):
        super().take_damage(damage, entity)

        if entity:
            self.damage_table[entity.id] = damage
