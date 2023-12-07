from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import random
from game.items import Item
from game.combat import Monster
from game.combat import Combat

class SpectralShark(Monster):
    def __init__(self, name):
        attacks = {
            "bite": ["bites fiercely", random.randrange(50, 76), (15, 25)],
            "tail_whip": ["whips its tail", random.randrange(40, 61), (10, 20)]
        }
        super().__init__(name, random.randrange(20, 31), attacks, 100)
class GhostlyWolf(Monster):
    def __init__(self, name):
        attacks = {
            "howl": ["howls eerily", random.randrange(30, 51), (5, 15)],
            "claw_strike": ["strikes with its claws", random.randrange(45, 66), (10, 20)]
        }
        super().__init__(name, random.randrange(15, 26), attacks, 90)   
class ShadowSerpent(Monster):
    def __init__(self):
        name = "Shadow Serpent"
        attacks = {
            "venomous_bite": ["bites with venomous fangs", random.randrange(60, 81), (20, 30)],
            "constrict": ["wraps its body around its prey", random.randrange(50, 71), (15, 25)]
        }
        health = random.randrange(25, 36)
        speed = 80  # Speed can determine attack order in combat
        super().__init__(name, health, attacks, speed)
class MysticalCrystal(Item):
    def __init__(self):
        super().__init__("Mystical Crystal", "A shimmering crystal radiating mystical energy.")
        self.power = 50
        self.uses = 3  # Limiting the number of uses

    def use(self, player):
        if self.uses <= 0:
            announce("The Mystical Crystal has lost its power.")
            return

        self.uses -= 1
        announce("You use the Mystical Crystal. It glows brightly, enveloping you in its energy!")

        # Randomly choose an effect
        effect = random.choice(['restore_health', 'magic_boost', 'temporary_buff', 'reveal_secrets', 'cure_status'])
        self.apply_effect(effect, player)

    def apply_effect(self, effect, player):
        if effect == 'restore_health':
            player.restore_health(self.power)
            announce(f"Health restored by {self.power} points.")
        elif effect == 'magic_boost':
            # Implement magic power boost logic
            pass
        elif effect == 'temporary_buff':
            # Implement temporary buffs logic
            pass
        elif effect == 'reveal_secrets':
            # Implement reveal secrets logic
            pass
        elif effect == 'cure_status':
            # Implement cure status logic
            pass

class AmuletOfTheSkyWhisperer(Item):
    def __init__(self):
        super().__init__("Amulet of the Sky Whisperer", "A celestial crystal amulet that shimmers like the sky.")
        self.effects = {"weather_prediction": True, "enhanced_reflexes": True, "mood_influence": True}

    def predict_weather(self, current_location):
        if self.effects["weather_prediction"]:
            # Logic to predict weather based on the player's location
            predicted_weather = self.get_weather_prediction(current_location)
            announce(f"The amulet shows signs of {predicted_weather}.")
        else:
            announce("The weather prediction power of the amulet is inactive.")

    def enhance_reflexes(self, player):
        if self.effects["enhanced_reflexes"]:
            # Temporarily boost player's reflexes
            player.increase_evasion()
            announce("Your reflexes feel sharper, more attuned to your surroundings.")
        else:
            announce("The reflex enhancement power of the amulet is inactive.")

    def influence_mood(self, npc):
        if self.effects["mood_influence"]:
            # Logic to influence the mood of an NPC
            self.apply_mood_influence(npc)
            announce(f"The mood of {npc.name} seems to shift subtly.")
        else:
            announce("The mood influence power of the amulet is inactive.")
class CelestialCannon(Item):
    def __init__(self):
        super().__init__("Celestial Cannon", "A legendary gun echoing with cosmic power.")
        self.special_ability = "cosmic_overcharge"
        self.cooldown = 0

    def use(self, target):
        if self.cooldown == 0:
            if target.is_valid():
                damage = self.calculate_damage()
                target.apply_damage(damage)
                self.apply_status_effect(target)
                announce(f"The Celestial Cannon hits {target.name} for {damage} damage, causing a cosmic disruption!")
                self.cooldown = 3
            else:
                announce("There is no valid target.")
        else:
            announce("The Celestial Cannon is recharging its cosmic energy.")

    def cosmic_overcharge(self):
        if self.cooldown == 0:
            affected_targets = self.get_targets_in_radius()
            for target in affected_targets:
                damage = self.calculate_overcharge_damage()
                target.apply_damage(damage)
            announce("The Celestial Cannon unleashes a cosmic overcharge, devastating all enemies in its path!")
            self.cooldown = 10
        else:
            announce("The Celestial Cannon's overcharge is still recharging.")

class EnchantedCompass(Item):
    def __init__(self):
        super().__init__("Enchanted Compass", "A compass that always points to something interesting.")
class MoonLitKey (location.Location):
    def __init__ (self,x,y,w):
        super().__init__(x,y,w)
        self.name = "Moonlit Key"
        self.symbol = 'MK'
        self.visitable = True
        self.starting_location = lunar_beach(self)
        self.location = {}
        self.starting_location = ['Lunar Beach']
        self.location = ['Shadowed Forest']
        self.location = ['Twilight Harbor']
        self.location = ['Glimmering Caverns']
        self.location = ['Silvercliff Summit']

    def enter (self,ship):
        announce ('You have arrived on Moonlit Key')
    
    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
    def trigger_combat_event(self, event_type):
        if event_type == "SpectralSharks":
            monsters = [SpectralShark("Spectral Shark " + str(i)) for i in range(2)]
        elif event_type == "GhostlyWolf":
            monsters = [GhostlyWolf("Ghostly Wolf")]
        
class lunar_beach(location.SubLocation):
    def __init__ (self,MK):
        super().__init__(MK)
        self.name = 'Lunar Beach'
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events = ["spectral_shark_encounter", "find_item"]
        
    def explore(self,Monster):
        event = random.choice(self.events)
        if event == "spectral_shark_encounter":
            self.Monster("SpectralSharks")
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce ('You return to your ship.')
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Shadowed Forest"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Twilight Harbor"]
        
class ShadowedForest (location.SubLocation):
    def __init__ (self,MK):
        super().__init__(MK)
        self.name = "Shadowed Forest"
        self.verbs = {'north': self.move, 'south': self.move, 'east': self.move, 'west': self.move}
        self.event_chance = 50
        
    def enter (self,verb):
        description = "You walk into a forest but you realize the more further in you get the darker it gets. Eventually it's pitch black"
        announce (description)
    def trip_event(self):
        announce("As you make your way through the forest, you trip over a hidden root.")
    def process_verb (self, verb,cmd_list,nouns):
        if random.randint(1, 100) <= self.event_chance:
            self.trip_event()
        self.move(verb)
        if verb == 'north':
            config.the_player.next_loc = self.main_location.locations['Silvercliff Summit']
        elif verb == 'west':
            config.the_player.next_loc = self.main_location.locations["Glimmering Caverns"]
        elif verb == 'south' or verb == 'east':
            config.the_player.next_loc = self.main_location.locations['Twilight Harbor']

    def explore(self):
        if random.randint(1, 100) <= 30:
            self.parent.trigger_combat_event("GhostlyWolf")
        if random.randint(1, 100) <= 20:
            config.the_player.inventory.add(EnchantedCompass())
            announce("You found an Enchanted Compass!")
class TwilightHarbor(location.SubLocation):
    def __init__(self, parent_location, combat, player):
        super().__init__(parent_location)
        self.name = "Twilight Harbor"
        self.verbs = {'explore': self.explore}
        self.combat_manager = combat
        self.player = player
        self.enemy_chance = 50  

    def explore(self,verb,cmd_list,nouns):
        announce("You arrive at the mysterious Twilight Harbor.")
        if random.randint(1, 100) <= self.enemy_chance:
            self.trigger_combat_event("ShadowSerpent")
        else:
            self.check_for_special_item_or_riddle()
        self.move(verb)
        if verb == 'north':
            config.the_player.next_loc = self.main_location.locations['Silvercliff Summit']
        elif verb == 'west':
            config.the_player.next_loc = self.main_location.locations["Glimmering Caverns"]
        elif verb == 'south' or verb == 'east':
            config.the_player.next_loc = self.main_location.locations['Lunar Beach']

    def trigger_combat_event(self, enemy_type):
        enemies = self.combat_manager.create_enemies(enemy_type)
        combat = Combat(self.player, enemies)
        combat.start_combat()

    def check_for_special_item_or_riddle(self):
        if random.randint(1, 2) == 1:
            self.find_special_item()
        else:
            self.solve_riddle()

    def find_special_item(self):
        special_item = self.get_random_special_item()
        announce(f"You found a {special_item.name}!")
        config.the_player.inventory.add(special_item)

    def get_random_special_item(self):
        return MysticalCrystal()
        pass

    def solve_riddle(self):
        announce("A voice in the caverns asks: 'I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?'")
        player_answer = input("Your answer: ")
        if player_answer.lower() == self.riddle_answer:
            announce("Correct! You find a mystical crystal.")
            config.the_player.inventory.add(MysticalCrystal())
        else:
            announce("Incorrect. The caverns remain silent.")

class GlimmeringCaverns(location.SubLocation):
    def __init__(self, MK):
        super().__init__(MK)
        self.name = "Glimmering Caverns"
        self.verbs = {'explore': self.explore}
        self.riddle_answer = "echo"  
    def present_riddle(self):
        chosen_riddle = random.choice(["echo", "cloud"])
        if chosen_riddle == "echo":
            riddle_text = "I speak without a mouth and hear without ears..."
            self.riddle_answer = "echo"
        elif chosen_riddle == "cloud":
            riddle_text = "I fly without wings, I cry without eyes..."
            self.riddle_answer = "cloud"

        announce(riddle_text)

    def reward_player(self):
        
        if self.riddle_answer == "echo":
           
            announce("A hidden compartment opens, revealing a Mystical Crystal!")
            config.the_player.inventory.add(MysticalCrystal())
        elif self.riddle_answer == "cloud":
           
            announce("A hidden panel slides away, unveiling the Amulet of the Sky Whisperer!")
            config.the_player.inventory.add(AmuletOfTheSkyWhisperer())
    def explore(self,verb):
            announce("You have reached the Glimmering Caverns")
        self.move(verb)
        if verb == 'north':
                config.the_player.next_loc = self.main_location.locations['Silvercliff Summit']
        elif verb == 'south' or verb == 'east' or verb == 'west':
            config.the_player.next_loc = self.main_location.locations['Lunar Beach']
   
class SilvercliffSummit(location.SubLocation):
    def __init__(self, MK):
        super().__init__(MK)
        self.name = "Silvercliff Summit"
        self.verbs = {'explore': self.explore, 'return': self.return_to_ship}
        self.final_battle = "AncientDragon"

    def explore(self):
        announce("You have reached the Silvercliff Summit, the final challenge awaits.")
        if random.randint(1, 100) <= 70:
            self.parent.trigger_combat_event(self.final_battle)
            if self.parent.combat_result == "victory":
                self.find_final_weapon()

    def find_final_weapon(self):
        announce("As the Ancient Dragon falls, a hidden chamber reveals itself, illuminated by a celestial light.")
        announce("Inside, you find the Celestial Cannon, a weapon of legend said to be able to change the course of destiny itself.")
        config.the_player.inventory.add(CelestialCannon())

      
        self.conclude_story_or_begin_new_chapter()

    def conclude_story_or_begin_new_chapter(self):
       announce("With the Celestial Cannon in your possession, new paths unfold before you...")
    
    def return_to_ship(self):
        announce("You decide to return to your ship to continue your adventure.")
        config.the_player.next_loc = config.the_player.ship
        config.the_player.visiting = False
    



    
                
    
