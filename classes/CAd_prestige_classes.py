#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 12:32:33 2025
@author: gtauxe
"""

import reactivex.operators as ops

import core
import phb.races, phb.classes
import dmg.prestige_classes
import splat.epic_level_handbook as elh
import utilities as util
sourcebook = 'Complete Adventurer'

#%% Animal lord
class AnimalLord(core.PrestigeClass):
    _name = 'animal lord'
    _hit_die = 10; skill_points = 4; bab_type = 'full'; good_saves = ['Fortitude', 'Reflex']
    _class_skills = ['Climb', 'Escape Artist', 'Handle Animal', 'Heal', 'Hide', 'Intimidate',
        'Jump', 'Knowledge (nature)', 'Listen', 'Move Silently', 'Spot', 'Survival', 'Swim']
    advancement = core.get_class_advancement({
        ('WildEmpathy', 'animal bond', 'detect animals'): [1],
        ('first totem', 'LowLightVision'): [2],
        'wild aspect': list(range(3,10,3)),
        'speak with animals': [4],
        'summon animal': [5],
        'second totem': [6],
        'animal growth': [7],
        'animal telepathy': [8],
        'third totem': [9]
        })

    def __init__(self, character):
        super().__init__(character)
        self._plural = 'wolves' if self.group=='wolf' else self.group + 's'

    def LowLightVision(self):
        self.character.features.add_if_missing(name='low-light vision', source=self)
        base_ = self.character.senses['low-light vision'].active_.pipe(
            ops.map(lambda p: [x for x in p if x.type in ['racial', 'base']]),
            ops.map(lambda p: [x for x in p if x.source != self]),
            ops.map(lambda p: len(p) > 0),
            ops.distinct_until_changed()
            )
        self.character.senses['low-light vision'].add(1, condition=base_, source=self)

    @classmethod
    def prereq(cls, character):
        return all(
            character.alignment=='neutral',
            character.BAB >= 5,
            character.skills['Handle Animal'].ranks >= 4,
            character.skills['Knowledge (nature)'].ranks >= 2,
            character.skills[cls._prereq_skill].ranks >= 4,
            cls._prereq_feat in character.feats.active
            )

class Apelord(AnimalLord):
    _name = 'apelord'; group = 'ape'
    _prereq_skill = 'Climb'; _prereq_feat = 'Toughness'

class Bearlord(AnimalLord):
    _name = 'bearlord'; group = 'bear'
    _prereq_skill = 'Intimidate'; _prereq_feat = 'Endurance'

class Birdlord(AnimalLord):
    _name = 'birdlord'; group = 'bird'
    _prereq_skill = 'Spot'; _prereq_feat = 'Improved Flight'

class Catlord(AnimalLord):
    _name = 'catlord'; group = 'cat'
    _prereq_skill = 'Move Silently'; _prereq_feat = 'Weapon Finesse'

class Horselord(AnimalLord):
    _name = 'horselord'; group = 'horse'
    _prereq_skill = 'Jump'; _prereq_feat = 'Run'

class Sharklord(AnimalLord):
    _name = 'sharklord'; group = 'shark'
    _prereq_skill = 'Swim'; _prereq_feat = 'Improved Swimming'

class Snakelord(AnimalLord):
    _name = 'snakelord'; group = 'snake'
    _prereq_skill = 'Escape Artist'; _prereq_feat = 'Combat Reflexes'

class Wolflord(AnimalLord):
    _name = 'wolflord'; group = 'wolf'
    _prereq_skill = 'Survival'; _prereq_feat = 'Track'

class AnimalBond(core.Feature):
    _name = 'animal bond'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        al = self.character.build.get_instances('AnimalLord')[0]
        group_ = self.character.challenges.register(target=al.group)
        self.character.skills['Handle Animal'].add(4, condition=group_, source=self)
        self.character.checks['wild empathy'].add(4, condition=group_, source=self)

        def add_level(pipes):
            if not pipes: return
            ac = pipes[0]
            ac.level.update(al.level, source=self)

        self.character.features.active_.pipe(
            ops.map(lambda p: [x for x in p if util.is_a(x, 'animal companion')]),
            ops.distinct_until_changed()
            ).subscribe(add_level)

class DetectAnimals(core.Feature):
    _name = 'detect animals'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        al = self.character.build.get_instances('AnimalLord')[0]
        self.character.magic.spell_like_abilities.add(name=f'detect {al._plural}',
            caster_level=al.level, frequency='at will', source=self)

class FirstTotem(core.Feature):
    _name = 'first totem'
    def __init__(self, character):
        super().__init__(character)
        al = self.character.build.get_instances('AnimalLord')[0]
        self.character.skills[al._prereq_skill].add(4, source=self)

class WildAspect(core.Feature):
    _name = 'wild aspect'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SummonAnimal(core.Feature):
    _name = 'summon animal'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SecondTotem(core.Feature):
    _name = 'second totem'
    _feats = {'ape': 'Brachiation', 'bear': 'Improved Grapple', 'bird': 'Flyby Attack',
        'cat': 'Lightning Reflexes', 'horse': 'Trample', 'shark': 'Improved Critical (bite)',
        'snake': 'Improved Initiative', 'wolf': 'Improved Trip'}
    def __init__(self, character):
        super().__init__(character)
        al = self.character.build.get_instances('AnimalLord')[0]
        feat = self._feats[al.group]
        if feat in self.character.build.active:
            al.BonusFeat()
        else:
            self.character.feats.add(name=feat, override=True, source=self)

class AnimalGrowth(core.Feature):
    _name = 'animal growth'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

class AnimalTelepathy(core.Feature):
    _name = 'animal telepathy'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError

class ThirdTotem(core.Feature):
    _name = 'third totem'
    _benefits = {'ape': 'strength', 'bear': 'constitution', 'bird': 'wisdom', 'cat': 'dexterity',
        'horse': 'constitution', 'shark': 'strength', 'snake': 'charisma', 'wolf': 'strength'}
    def __init__(self, character):
        super().__init__(character)
        al = self.character.build.get_instances('AnimalLord')[0]
        self.character.abilities[self._benefits[al.group]].add(2, source=self)

#%% Beastmaster
class Beastmaster(core.PrestigeClass):
    _name = 'beastmaster'
    _hit_die = 10; skill_points = 4; bab_type = 'full'; good_saves = ['Fortitude', 'Reflex']
    _class_skills = ['Climb', 'Handle Animal', 'Heal', 'Hide', 'Jump', 'Knowledge (nature)',
                     'Listen', 'Ride', 'Spot', 'Survival', 'Swim']

    advancement = core.get_class_advancement({
        ('AnimalCompanion', 'WildEmpathy'): [1],
        'Alertness': [2],
        'SpeakWithAnimals': list(range(3,10,3)),
        'ExtraAnimalCompanion': list(range(4,11,3)),
        'scent': [8]
        })

    def AnimalCompanion(self):
        ac = self.character.features.add_if_missing(item='AnimalCompanionFeature', source=self)
        ac.effective_level.add(util.LiveAttribute(self.level, lambda x: x+3), 'base', source=self)

    def Alertness(self):
        self.character.feats.add(name='Alertness', override=True, source=self)

    def LowLightVision(self):
        self.character.features.add_if_missing(name='low-light vision', source=self)
        base_ = self.character.senses['low-light vision'].active_.pipe(
            ops.map(lambda p: [x for x in p if x.type in ['racial', 'base']]),
            ops.map(lambda p: [x for x in p if x.source != self]),
            ops.map(lambda p: len(p) > 0),
            ops.distinct_until_changed()
            )
        self.character.senses['low-light vision'].add(1, condition=base_, source=self)

    @staticmethod
    def prereq(character):
        return (character.skills['Handle Animal'].ranks >= 8 and
                character.skills['Survival'].ranks >= 4 and
                any(x.focus=='Handle Animal'
                    for x in character.feats.get_all(name='Skill Focus', status='active'))
                )

class ExtraAnimalCompanion(core.Feature):
    _name = 'extra animal companion'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Bloodhound
class Bloodhound(core.PrestigeClass):
    _name = 'bloodhound'
    _hit_die = 10; skill_points = 6; bab_type = 'full'; good_saves = ['Fortitude', 'Reflex']
    _class_skills = ['Bluff', 'Climb', 'Diplomacy', 'Disguise', 'Gather Information', 'Heal',
        'Hide', 'Intimidate', 'Jump', 'Listen', 'Move Silently', 'Open Lock', 'Ride', 'Search',
        'Sense Motive', 'Spot', 'Survival', 'Swim', 'Use Rope']
    proficiencies = ['simple', 'martial', 'light']
    advancement = {
        1: ['mark', 'swift tracker'],
        2: ['nonlethal force', 'ready and waiting'],
        3: ["bring 'em back alive", 'tenacious pursuit'],
        4: ['mark', "hunter's dedication", 'move like the wind'],
        5: ['crippling strike', 'track the trackless'],
        6: ['tenacious pursuit', 'see invisibility', 'shielded mind'],
        7: ['mark', 'locate creature'],
        8: ['freedom of movement'],
        9: ['tenacious pursuit', 'scent'],
        10: ['mark', 'find the path']
        }
    @staticmethod
    def prereq(character):
        return (character.BAB >= 4,
                all(character.skills[x].ranks >= 4
                    for x in ['Gather Information', 'Move Silently', 'Survival']),
                all(x in character.feats.active for x in ['Endurance', 'Track'])
                )

class Mark(core.Feature):
    _name = 'mark'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class NonlethalForce(core.Feature):
    _name = 'nonlethal force'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ReadyAndWaiting(core.Feature):
    _name = 'ready and waiting'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class BringEmBackAlive(core.Feature):
    _name = "bring 'em back alive"
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class TenaciousPursuit(core.Feature):
    _name = 'tenacious pursuit'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class HuntersDedication(core.Feature):
    _name = "hunter's dedication"
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError

class MoveLikeTheWind(core.Feature):
    _name = 'move like the wind'
    _tags = ['extraordinary']

class TrackTheTrackless(core.Feature):
    _name = 'track the trackless'
    _tags = ['supernatural']

class SeeInvisibility(core.Feature):
    _name = 'see invisibility'
    _tags = ['supernatural']

class ShieldedMind(core.Feature):
    _name = 'shielded mind'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.benefit = util.Attribute(15)
        self.benefit.add(self.character.build.level_of('bloodhound'), 'base')
        self.character.resistances.spell_resistance['divination'].add(self.benefit, 'base', source=self)

class LocateCreature(core.Feature):
    _name = 'locate creature'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        lvl = self.character.build.level_of('bloodhound')
        self.character.magic.spell_like_abilities.add(name='locate creature', caster_level=lvl,
            frequency=util.Frequency(1,1,'day'), source=self)

class FreedomOfMovement(core.Feature):
    _name = 'freedom of movement'
    _tags = ['supernatural']
    def __init__(self, character):
        raise NotImplementedError

#%% Daggerspell mage and shaper
class _DaggerspellClass(core.PrestigeClass):
    _hit_die = 6; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Balance', 'Climb', 'Concentration', 'Craft', 'Handle Animal', 'Heal', 'Hide',
                     'Jump', 'Listen', 'Move Silently', 'Profession', 'Ride', 'Spellcraft', 'Spot',
                     'Survival', 'Swim', 'Tumble']

    @staticmethod
    def prereq(character):
        return (character.alignment!='evil' and
                character.skills['Concentration'].ranks >= 8 and
                'Two-Weapon Fighting' in character.feats.active and
                any(x.focus=='dagger'
                    for x in character.feats.get_all(name='Weapon Focus', status='active'))
                )

class DaggerspellMage(_DaggerspellClass):
    _name = 'daggerspell mage'
    _class_skills = _DaggerspellClass._class_skills + ['Knowledge (arcana)']
    advancement = core.get_class_advancement({
        'ArcaneCasterLevel': list(range(2,11)),
        'daggercast': [1],
        'invocation of the knife': [2],
        'sneak attack': list(range(3,11,3)),
        'double daggercast': [5],
        'arcane infusion': [7],
        'arcane throw': [8],
        'daggerspell flurry': [10]
        })
    @staticmethod
    def prereq(character):
        return (_DaggerspellClass.prereq(character) and
                any(sc.magic_type=='arcane' and sc.caster_level >= 5
                    for sc in character.features.get_all(name='spellcasting')) and
                'sneak attack' in character.features.active
                )

class DaggerspellShaper(core.PrestigeClass):
    _name = 'daggerspell shaper'
    _class_skills = _DaggerspellClass._class_skills + ['Knowledge (nature)']
    advancement = core.get_class_advancement({
        'DivineCasterLevel': list(range(2,11)),
        'daggercast': [1],
        'wild shape': [1,5,10],
        ('dagger claws', 'WildShapeTiny'): [2],
        'sneak attack': list(range(3,11,3)),
        'WildShapeLarge': [4],
        'fast wild shape': [7],
        'enhanced wild shape': [8],
        'daggerspell flurry': [10]
        })

    def WildShapeTiny(self): self.character.features.get_one(name='wild shape').valid_sizes.append('Tiny')
    def WildShapeLarge(self): self.character.features.get_one(name='wild shape').valid_sizes.append('Large')

    @staticmethod
    def prereq(character):
        return (_DaggerspellClass.prereq(character) and
                'wild shape' in character.features.active and
                any(x in character.features.active for x in ['sneak attack', 'skirmish'])
                )

class Daggercast(core.Feature):
    _name = 'daggercast'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class InvocationOfTheKnife(core.Feature):
    _name = 'invocation of the knife'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class DoubleDaggercast(core.Feature):
    _name = 'double daggercast'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ArcaneInfusion(core.Feature):
    _name = 'arcane infusion'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class ArcaneThrow(core.Feature):
    _name = 'arcane throw'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class DaggerspellFlurry(core.Feature):
    _name = 'daggerspell flurry'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class DaggerClaws(core.Feature):
    _name = 'dagger claws'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class EnhancedWildShape(core.Feature):
    _name = 'enhanced wild shape'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Dread pirate
class DreadPirate(core.PrestigeClass):
    _name = 'dread pirate'
    _hit_die = 8; skill_points = 6; bab_type = 'full'; good_saves = ['Reflex']
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Craft', 'Gather Information',
        'Intimidate', 'Jump', 'Listen', 'Perform', 'Profession', 'Search', 'Sense Motive',
        'Sleight of Hand', 'Spot', 'Swim', 'Tumble', 'Use Rope']
    proficiencies = ['simple', 'rapier', 'light'] # TODO add light martial weapons
    advancement = core.get_class_advancement({
        ('seamanship', 'TwoWeaponFighting'): [1],
        'fearsome reputation': [2,6,10],
        ('acrobatic charge', 'steady stance'): [4],
        'SkillMastery': [8],
        'pirate king': [10]
        })
    honorable_features = core.ClassFeatures({
        'rally the crew': [3,7],
        'luck of the wind': [5],
        'fight to the death': [9]
        })
    dishonorable_features = core.ClassFeatures({
        'sneak attack': [3,7],
        'scourge of the seas': [5],
        'motivate the scum': [9]
        })

    def __init__(self, character):
        super().__init__(character)
        self.reputation = None

    def advance(self):
        super().advance()
        if not self.reputation: return
        extra_features = getattr(self, f'{self.reputation}_features')
        for feature in extra_features.get(self.level.attribute, []):
            self._allocate_feature(feature)

    def set_reputation(self, value):
        value = value.lower()
        if value not in ['honorable', 'dishonorable']:
            util.logger.warning('Reputation value not recognized: %s', value); return

        self.reputation = value
        extra_features = getattr(self, f'{self.reputation}_features')
        for lvl in range(1, self.level+1):
            for feature in extra_features.get(lvl, []):
                self._allocate_feature(feature)

    def SkillMastery(self):
        sm = self.character.features.add(name='skill mastery', source=self)
        sm.add_skills(['Balance', 'Climb', 'Jump', 'Tumble'], source=self)

    @staticmethod
    def prereq(character, special=False):
        '''Special: The character must own a ship worth at least 10,000 gp.'''
        return (character.alignment != 'lawful' and
                character.BAB >= 4 and
                all(character.skills[x].ranks >= 8
                    for x in ['Appraise', 'Profession (sailor)']) and
                all(character.skills[x].ranks >= 4 for x in ['Swim', 'Use Rope']) and
                all(x in character.feats.active for x in ['Quick Draw', 'Weapon Finesse']) and
                special
                )

class Seamanship(core.Feature):
    _name = 'seamanship'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        dp = self.character.build.get_one(name='dread pirate')
        self.character.skills['Profession (sailor)'].add(dp.level, 'insight', source=self)
        raise NotImplementedError
        # allies in sight or hearing gain 1/2 lvl insight bonus to profession (sailor)

class FearsomeReputation(core.Feature):
    _name = 'fearsome reputation'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.dp = self.character.build.get_one(name='dread pirate')
        def check_reputation():
            if self.active and not self.dp.reputation.value:
                util.logger.warning('Dread pirate reputation not set.')
        self.character.add_to_build(-2, 1, check_reputation)

    def set_reputation(self, value):
        self.dp.set_reputation(value)

class PirateKing(core.Feature):
    _name = 'pirate king'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class RallyTheCrew(core.Feature):
    _name = 'rally the crew'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class LuckOfTheWind(core.Feature):
    _name = 'luck of the wind'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ScourgeOfTheSeas(core.Feature):
    _name = 'scourge of the seas'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class FightToTheDeath(core.Feature):
    _name = 'fight to the death'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class MotivateTheScum(core.Feature):
    _name = 'motivate the scum'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Dungeon delver
class DungeonDelver(core.PrestigeClass):
    _name = 'dungeon delver'
    _hit_die = 6
    skill_points = 8
    _class_skills = ['Appraise', 'Balance', 'Climb', 'Craft', 'Disable Device', 'Hide', 'Jump',
        'Knowledge (dungeoneering)', 'Listen', 'Move Silently', 'Open Lock', 'Search', 'Spot',
        'Survival', 'Swim', 'Tumble', 'Use Magic Device', 'Use Rope']
    bab_type = 'three quarters'
    good_saves = ['Fortitude', 'Reflex']
    advancement = {
        1: ['trap sense', 'darkvision', 'deep survival'],
        2: ['reduce', 'stonecunning'],
        3: ['augury', 'SkillMastery'],
        4: ['trap sense', 'Evasion'],
        5: ['blindsense'],
        6: ['augury', 'passwall'],
        7: ['trap sense'],
        8: ['find the path'],
        9: ['augury'],
        10: ['trap sense', 'blindsense', 'phase door']
        }
    def Evasion(self):
        evasion_ = self.character.features.active_.pipe(
            ops.map(lambda p: [x for x in p if x.name=='evasion']),
            ops.map(lambda p: [x for x in p if x.source!=self]),
            ops.map(lambda p: len(p) >= 1), ops.distinct_until_changed())
        not_evasion_ = evasion_.pipe(ops.map(lambda x: not x))
        self.character.features.add(name='evasion', source=not_evasion_)
        self.character.features.add(name='improved evasion', source=evasion_)

    def SkillMastery(self):
        sm = self.add_feature('skill mastery')
        sm.grade.add(3, 'base')
        sm.grade.add(self.character.INT.attribute, 'INT')

    @staticmethod
    def prereq(character, special=False):
        return (all(character.skills[x].ranks >= 10
                    for x in ['Climb', 'Disable Device', 'Open Lock', 'Search']) and
                all(character.skills[x].ranks >= 5
                    for x in ['Craft (stonemasonry)', 'Hide', 'Knowledge (dungeoneering)',
                              'Move Silently']) and
                all(x in character.feats.active for x in ['Alertness', 'Blind-Fight']) and
                'trapfinding' in character.features.active and
                special)

class EpicDungeonDelver(elh.EpicClass, DungeonDelver):
    _name = 'epic dungeon delver'
    # trap sense 10 + 3
    # augury 9 + 3
    # Skill mastery every level
    # blindsense 10 + 5
    # bonus feats 10 + 3

class Darkvision(core.Feature):
    _name = 'darkvision'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        vision = util.NumeralAttribute(0)
        self.character.senses['darkvision'].active_.pipe(
            ops.map(lambda p: [x for x in p if x.source!=self.name]),
            ops.map(lambda p: sum(x.attribute for x in p if x.type in ['base', 'racial'])),
            ops.distinct_until_changed(),
            ops.map(lambda x: 60 if x==0 else 3)
            ).subscribe(vision.value_.on_next, util.log_error)
        self.character.senses['darkvision'].add(vision, 'base', source=self)

class DeepSurvival(core.Feature):
    _name = 'deep survival'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        lvl = self.character.build.level_of('dungeon delver')
        underground_ = self.character.challenges.register(location='underground')
        self.character.skills['Survival'].add(lvl, condition=underground_, source=self)

class Reduce(core.Feature):
    _name = 'reduce'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.character.magic.spell_like_abilites.add(name='reduce person',
            caster_level=self.source.level, frequency=util.Frequency(3,1,'day'), source=self)
        # TODO self only, ignores creature type

class Stonecunning(phb.races.Stonecunning):
    _name = 'stonecunning'
    bonus_type = 'competence'

class Augury(core.Feature):
    _name = 'augury'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.character.magic.spell_like_abilities.add(name='augury',
            caster_level=self.source.level, frequency=util.Frequency(self.grade, 1, 'day'), source=self)
    def escalate(self): self.grade.attribute += 1

class Blindsense(core.Feature):
    _name = 'blindsense'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Passwall(core.Feature):
    _name = 'passwall'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.character.magic.spell_like_abilities.add(name='passwall',
            caster_level=self.source.level, frequency=util.Frequency(1,1,'day'), source=self)

class FindThePath(core.Feature):
    _name = 'find the path'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.character.magic.spell_like_abilities.add(name='find the path',
            caster_level=self.source.level, frequency=util.Frequency(2,1,'day'), source=self)

class PhaseDoor(core.Feature):
    _name = 'phase door'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.character.magic.spell_like_abilities.add(name='phase door', caster_level=18,
            frequency=util.Frequency(1,1,'day'), source=self)

#%% Exemplar
class Exemplar(core.PrestigeClass):
    _name = 'exemplar'
    _hit_die = 6; skill_points = 8; bab_type = 'three quarters'; good_saves = ['Will']
    advancement = core.get_class_advancement({
        'skill artistry': list(range(1,11,3)),
        'SkillMastery': [1],
        'lend talent': [2,8],
        'BonusFeat': list(range(3,11,3)),
        'sustaining presence': [4],
        'persuasive performance': [5],
        'intellectual agility': [8],
        'perfect self': [10]
        })
    feats = ['Acrobatic', 'Agile', 'Alertness', 'Animal Affinity', 'Athletic', 'Blind-Fight',
            'Combat Casting', 'Combat Expertise', 'Deceitful', 'Deft Hands', 'Diligent',
            'Improved Intiative', 'Improved Swimming', 'Investigator', 'Magical Aptitude',
            'Negotiator', 'Nimble Fingers', 'Open Minded', 'Persuasive', 'Self-Sufficient',
            'Skill Focus', 'Stealthy', 'Track', 'Versatile Performer']
    def __init__(self, character):
        super().__init__(character)
        self.class_skills = util.Any()

    def SkillMastery(self):
        sm = self.add_feature('skill mastery')
        sm.grade.add(self.level, 'base')
        sm.grade.add(self.character.INT.attribute, 'INT')

    @staticmethod
    def prereq(character):
        return (character.skills['Diplomacy'].ranks >= 6 and
                any(k!='Diplomacy' and v.ranks >= 13 for k,v in character.skills.items()) and
                'Skill Focus' in character.feats.active)

class SkillArtistry(core.Feature):
    _name = 'skill artistry'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.skills = []

    def apply(self, skill):
        skill = skill.lower()
        if not (skill in self.character.skills and self.character.skills[skill].ranks >= 13):
            util.logger.warning('You must have 13 ranks in a skill to apply skill artistry. %s', skill)
            return
        if skill in self.skills:
            util.logger.warning('You already have artistry in that skill. %s', skill)
            return
        if len(self.skills) >= self.grade:
            util.logger.warning('You have already allocated all of your available skill artistry. %s', skill)
            return
        self.skills.append(skill)
        self.character.skills[skill].add(4, 'competence', source=self)
    def escalate(self): self.grade.attribute += 1

class LendTalent(core.Feature):
    _name = 'lend talent'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError
    def escalate(self): raise NotImplementedError

class SustainingPresence(core.Feature):
    _name = 'sustaining presence'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        bonus = util.LiveAttribute(self.character.CHA, lambda x: x)
        bonus.minimum = 0
        self.character.skills['Concentration'].add(bonus, 'CHA', source=self)
        self.character.saves['Fortitude'].add(bonus, 'CHA', source=self)

class PersuasivePerformance(core.Feature):
    _name = 'persuasive performance'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class IntellectualAgility(core.Feature):
    _name = 'intellectual agility'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        bonus = util.LiveAttribute(self.character.INT, lambda x: x)
        bonus.minimum = 0
        self.character.initiative.add(bonus, 'INT', source=self)
        self.character.saves['Reflex'].add(bonus, 'INT', source=self)

#%% Fochlucan lyrist
class FochlucanLyrist(core.PrestigeClass):
    _name = 'Fochlucan lyrist'
    _hit_die = 6; skill_points = 6; bab_type = 'full'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Appraise', 'Bluff', 'Concentration', 'Craft', 'Decipher Script', 'Diplomacy',
        'Disguise', 'Gather Information', 'Handle Animal', 'Heal', 'Hide', 'Knowledge', 'Listen',
        'Move Silently', 'Perform', 'Profession', 'Ride', 'Sense Motive', 'Sleight of Hand',
        'Speak Language', 'Spellcraft', 'Survival', 'Swim', 'Use Magic Device']
    advancement = core.get_class_advancement({
        ('ArcaneCasterLevel', 'DivineCasterLevel'): list(range(1,11,)),
        ('BardicKnowledge', 'BardicMusic', 'unbound'): [1]
        })

    def BardicKnowledge(self):
        self.add_feature('bardic knowledge')
        self.character.checks['bardic knowledge'].add(self.level, 'base', source=self)

    def BardicMusic(self):
        bm = self.add_feature('bardic music')
        bm.frequency.add(self.level, 'base', source=self)

    @staticmethod
    def prereq(character):
        return (character.alignment == 'neutral' and character.alignment != 'lawful' and
                all(character.skills[x].ranks >= 7
                    for x in ['Decipher Script', 'Diplomacy', 'Gather Information',
                        'Knowledge (nature)', 'Sleight of Hand']) and
                character.skills['Perform (string instruments)'].ranks >= 13 and
                'Druidic' in character.skills.languages and
                any(sc.magic_type=='arcane' and sc.caster_level >= 1
                    for sc in character.features.get_all(name='spellcasting')) and
                any(sc.magic_type=='divine' and sc.caster_level >= 1
                    for sc in character.features.get_all(name='spellcasting')) and
                all(x in character.features.active for x in ['bardic knowledge', 'evasion'])
                )

class Unbound(core.Feature):
    _name = 'unbound'
    def __init__(self, character): raise NotImplementedError

#%% Ghost-faced killer
class GhostFacedKiller(core.PrestigeClass):
    _name = 'ghost-faced killer'
    _hit_die = 8; bab_type = 'full'; good_saves = ['Fortitude']; skill_points = 4
    _class_skills = ['Bluff', 'Climb', 'Concentration', 'Hide', 'Intimidate', 'Jump', 'Listen',
                     'Move Silently', 'Open Lock', 'Search', 'Spot', 'Swim', 'Tumble']
    proficiencies = ['simple', 'martial', 'light']
    advancement = core.get_class_advancement({
        'ghost step': list(range(1,11,3)),
        'sudden strike': list(range(2,11,3)),
        'frightful attack': list(range(3,11,3)),
        'GhostStepEthereal': [6],
        'ghost sight': [7],
        'frightful cleave': [10]
        })

    @staticmethod
    def prereq(character):
        return (character.alignment == 'evil' and
                character.BAB >= 5 and
                all(character.skills[x].ranks >= 6 for x in ['Hide', 'Move Silently']) and
                character.skills['Concentration'].ranks >= 4 and
                character.skills['Intimidate'].ranks >= 8 and
                all(x in character.feats.active for x in ['Improved Initiative', 'Power Attack'])
                )

class FrightfulAttack(core.Feature):
    _name = 'frightful attack'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.frequency = util.Frequency(self.grade,1,'day')
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class FrightfulCleave(core.Feature):
    _name = 'frightful cleave'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Highland stalker
class HighlandStalker(core.PrestigeClass):
    _name = 'highland stalker'
    _hit_die = 8; skill_points = 4; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Balance', 'Climb', 'Craft', 'Hide', 'Jump', 'Knowledge (geography)',
                     'Knowledge (nature)', 'Listen', 'Move Silently', 'Search', 'Spot', 'Survival']
    proficiencies = ['light']
    advancement = core.get_class_advancement({
        'mountain stride': [1],
        'skirmish': list(range(2,11,2)),
        'swift tracker': [3],
        'surefooted': [5],
        'camouflage': [7]
        })
    @staticmethod
    def prereq(character):
        return (character.BAB >= 5 and
                all(character.skills[x].ranks >= 8 for x in ['Listen', 'Spot', 'Survival']),
                'Track' in character.feats.active and
                any(x in character.features.active for x in ['skirmish', 'sneak attack'])
                )

class MountainStride(core.Feature):
    _name = 'mountain stride'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Surefooted(core.Feature):
    _name = 'surefooted'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Maester
class Maester(core.PrestigeClass):
    _name = 'maester'
    _hit_die = 4; skill_points = 4; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Appraise', 'Concentration', 'Craft', 'Disable Device', 'Knowledge (arcana)',
        'Knowledge (architecture and engineering)', 'Spellcraft', 'Use Magic Device']
    advancement = core.get_class_advancement({
        'CasterLevel': list(range(2,6)),
        'BonusFeat': [1,5],
        'quick crafting': [1],
        'identification': [3]
        })
    feats = ['item creation'] #TODO this... what?
    @staticmethod
    def prereq(character):
        return ('gnome' in character.build.active and
                any(k.startswith('Craft') and v.ranks >= 8 for k,v in character.skills.items()) and
                character.skills['Use Magic Device'].ranks >= 4 and
                len(character.feats.get_instances('ItemCreationFeat')) >= 2 and
                any(sc.magic_type=='arcane' and sc.caster_level >= 5
                    for sc in character.features.get_all(name='spellcasting'))
                )

class QuickCrafting(core.Feature):
    _name = 'quick crafting'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Identification(core.Feature):
    _name = 'identification'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

#%% Master of many forms
class MasterOfManyForms(core.PrestigeClass):
    _name = 'master of many forms'
    _hit_die = 8; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Fortitude', 'Reflex']
    _class_skills = ['Climb', 'Concentration', 'Craft', 'Diplomacy', 'Disguise', 'Handle Animal',
                     'Hide', 'Jump', 'Knowledge (nature)', 'Listen', 'Spot', 'Swim', 'Survival']
    features = {
        1: ["shifter's speech", 'improved wild shape', 'WildShapeHumanoid'],
        2: ['WildShapeLarge', 'WildShapeGiant'],
        3: ['fast wild shape', 'WildShapeMonstrousHumanoid'],
        4: ['WildShapeFey', 'WildShapeTiny'],
        5: ['WildShapeVermin'],
        6: ['WildShapeAberration', 'WildShapeHuge'],
        7: ['extraordinary wild shape', 'WildShapePlant'],
        8: ['WildShapeOoze', 'WildShapeDiminutive'],
        9: ['WildShapeElemental'],
        10: ['evershifting form', 'WildShapeDragon', 'WildShapeGargantuan']
        }

    def __init__(self, character):
        super().__init__(character)
        self.wild_shape = self.character.features.get_one(name='Wild shape', status='active')

    def WildShapeHumanoid(self): self.wild_shape.valid_types.append('humanoid')
    def WildShapeLarge(self): self.wild_shape.valid_sizes.append('Large')
    def WildShapeGiant(self): self.wild_shape.valid_types.append('giant')
    def WildShapeMonstrousHumanoid(self): self.wild_shape.valid_types.append('monstrous humanoid')
    def WildShapeFey(self): self.wild_shape.valid_types.append('fey')
    def WildShapeTiny(self): self.wild_shape.valid_sizes.append('Tiny')
    def WildShapeVermin(self): self.wild_shape.valid_types.append('vermin')
    def WildShapeAberration(self): self.wild_shape.valid_types.append('aberration')
    def WildShapeHuge(self): self.wild_shape.valid_sizes.append('Huge')
    def WildShapePlant(self): self.wild_shape.valid_types.append('plant')
    def WildShapeOoze(self): self.wild_shape.valid_types.append('ooze')
    def WildShapeDiminutive(self): self.wild_shape.valid_sizes.append('Diminutive')
    def WildShapeElemental(self): self.wild_shape.valid_types.append('elemental')
    def WildShapeDragon(self): self.wild_shape.valid_types.append('dragon')
    def WildShapeGargantuan(self): self.wild_shape.valid_sizes.append('Gargantuan')

    @staticmethod
    def prereq(character):
        return (all(x in character.feats.active for x in ['Alertness', 'Endurance']) and
                'wild shape' in character.features.active)

class ShiftersSpeech(core.Feature):
    _name = "shifter's speech"
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ImprovedWildShape(core.Feature):
    _name = 'improved wild shape'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.source.wild_shape.frequency.add(self.source.level, 'base', source=self)
    # errata: momf levels stack for the purposes of determining max HD

class ExtraordinaryWildShape(core.Feature):
    _name = 'extraordinary wild shape'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class EvershiftingForm(core.Feature):
    _name = 'evershifting form'
    def __init__(self, character): raise NotImplementedError

#%% Nightsong enforcer and infiltrator
class NightsongEnforcer(core.PrestigeClass):
    _name = 'Nightsong enforcer'
    _hit_die = 8; skill_points = 4; bab_type = 'full'; good_saves = ['Reflex']
    _class_skills = ['Balance', 'Climb', 'Disable Device', 'Disguise', 'Escape Artist', 'Hide',
                     'Intimidate', 'Jump', 'Listen', 'Move Silently', 'Open Lock', 'Profession',
                     'Ride', 'Search', 'Spot', 'Swim', 'Tumble']
    proficiencies = ['light']
    advancement = core.get_class_advancement({
        'sneak attack': list(range(1,11,3)),
        'teamwork': [1,9],
        'agility training': [2],
        'skill teamwork': [3,7],
        'flanking teamwork': [5],
        'opportunist': [6],
        'improved evasion': [8]
        })
    @staticmethod
    def prereq(character, special=False):
        '''Special: you must undergo intensive training and tests with the Nightsong Guild.'''
        return (character.BAB >= 5 and
                all(character.skills[x].ranks >= 10 for x in ['Hide', 'Move Silently']) and
                'Improved Initiative' in character.feats.active and
                'evasion' in character.features.active and
                special)

class NightsongInfiltrator(core.PrestigeClass):
    _name = 'Nightsong infiltrator'
    _hit_die = 6; skill_points = 8; bab_type = 'three quarters'; good_saves = ['Reflex']
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Craft', 'Decipher Script',
        'Diplomacy', 'Disable Device', 'Disguise', 'Escape Artist', 'Forgery', 'Gather Information',
        'Hide', 'Jump', 'Listen', 'Move Silently', 'Open Lock', 'Profession', 'Ride', 'Search',
        'Sleight of Hand', 'Spot', 'Swim', 'Tumble', 'Use Magic Device', 'Use Rope']
    advancement = {
        1: ['teamwork trap sense', 'trapfinding'],
        2: ['teamwork infiltration', 'steady stance'],
        3: ['break away', 'trackless step'],
        4: ['teamwork trap sense', 'teamwork sneak attack', 'detect magic'],
        5: ['grant move action', 'defensive roll'],
        6: ['improved evasion', 'SkillMastery', 'specialized tools'],
        7: ['teamwork trap sense', 'TracklessStepAllies'],
        8: ['teamwork infiltration', 'teamwork sneak attack'],
        9: ['grant move action'],
        10: ['teamwork trap sense', 'HideInPlainSight']
        }
    def TracklessStepAllies(self): raise NotImplementedError

    def SkillMastery(self):
        sm = self.character.features.add(name='skill mastery', source=self)
        sm.add_skills(['Climb', 'Disable Device', 'Open Lock', 'Search'], source=self)

    def HideInPlainSight(self):
        hips = self.character.features.add_if_missing(name='hide in plain sight', source=self)
        hips.set_terrain('natural terrain')

    @staticmethod
    def prereq(character, special=False):
        '''Special: you must undergo intensive training and tests with the Nightsong Guild.'''
        return (character.skills['Climb'].ranks >= 10 and
                all(character.skills[x].ranks >= 5 for x in ['Disable Device', 'Open Lock', 'Search']) and
                'Alertness' in character.feats.active and
                'evasion' in character.features.active and
                special)

class Teamwork(core.Feature):
    _name = 'teamwork'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        ally_ = self.character.challenges.register(target='ally', source=self)
        for skill in ['Listen', 'Spot']:
            self.character.skills[skill].add(20, 'circumstance', condition=ally_, source=self)
    def escalate(self): raise NotImplementedError

class AgilityTraining(core.Feature):
    _name = 'agility training'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SkillTeamwork(core.Feature):
    _name = 'skill teamwork'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class FlankingTeamwork(core.Feature):
    _name = 'flanking teamwork'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class TeamworkTrapSense(phb.classes.TrapSense):
    _name = 'teamwork trap sense'
    def __init__(self, character): raise NotImplementedError

class TeamworkInfiltration(core.Feature):
    _name = 'teamwork infiltration'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.bonus = util.LiveAttribute(self.grade, lambda x: x*2)
        for x in ['Balance', 'Climb', 'Disable Device', 'Hide', 'Move Silently', 'Open Lock',
                  'Search', 'Tumble']:
            self.character.skills[x].add(self.bonus, 'competence', source=self)
            #TODO in target area, for 24 hrs after casing it
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class BreakAway(core.Feature):
    _name = 'break away'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class TeamworkSneakAttack(phb.classes.SneakAttack):
    _name = 'teamwork sneak attack'
    def __init__(self, character): raise NotImplementedError

class GrantMoveAction(core.Feature):
    _name = 'grant move action'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SpecializedTools(core.Feature):
    _name = 'specialized tools'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Ollam
class Ollam(core.PrestigeClass):
    _name = 'ollam'
    _hit_die = 8; skill_points = 6; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Decipher Script', 'Diplomacy', 'Gather Information',
                     'Heal', 'Knowledge', 'Listen', 'Perform', 'Search', 'Sense Motive',
                     'Speak Language', 'Spellcraft']
    proficiencies = ['simple', 'light', 'medium', 'heavy', 'shield', 'tower shield']
    advancement = core.get_class_advancement({
        'lore': [1],
        'CasterLevel': [2,3,4],
        'inspire competence': [3],
        'inspire resilience': [5]
        })

    @staticmethod
    def prereq(character):
        return ('dwarf' in character.build.active and
                character.alignment == 'lawful good' and
                character.skills['Knowledge (history)'].ranks >= 10 and
                any(k.startswith('Knowledge') and k!='Knowledge (history)' and v.ranks >= 10 for k,v in character.skills) and
                character.skills['Perform (oratory)'].ranks >= 5
                )

class Lore(dmg.prestige_classes.Lore):
    _tags = ['extraordinary']
    # TODO new: stacks with bardic knowledge etc

class InspireCompetence(phb.classes.InspireCompetence):
    def __init__(self, character): raise NotImplementedError

class InspireResilience(core.Feature):
    _name = 'inspire resilience'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Shadowbane inquisitor and stalker
class ShadowbaneInquisitor(core.PrestigeClass):
    _name = 'shadowbane inquisitor'
    _hit_die = 10; skill_points = 4; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Climb', 'Concentration', 'Craft', 'Decipher Script', 'Gather Information',
                     'Heal', 'Hide', 'Jump', 'Knowledge (religion)', 'Move Silently', 'Profession',
                     'Search', 'Sense Motive', 'Swim']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield']
    advancement = core.get_class_advancement({
        ('absolute conviction', 'pierce shadows'): [1],
        'sacred stealth': [2,7],
        'smite': [2,6,10],
        'ImprovedSunder': [3],
        'sneak attack': [4,7,10],
        'merciless purity': [5],
        'righteous fervor': [8],
        'burning light': [9],
        })

    def ImprovedSunder(self): self.character.feats.add(name='improved sunder', source=self, override=True)
    #TODO special rules for multiclassing, incl blackguards

    @staticmethod
    def prereq(character):
        return (character.alignment == 'lawful good' and
                character.BAB >= 5 and
                character.skills['Gather Information'].ranks >= 4 and
                character.skills['Knowledge (religion)'].ranks >= 2 and
                character.skills['Sense Motive'].ranks >= 8 and
                'Power Attack' in character.feats.active and
                # detect evil class feature or detect evil divine spell and #TODO
                all(x in character.features.active) for x in ['turn undead', 'sneak attack']
                )

class ShadowbaneStalker(core.PrestigeClass):
    _name = 'shadowbane stalker'
    _hit_die = 8; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Appraise', 'Balance', 'Climb', 'Concentration', 'Craft', 'Decipher Script',
                     'Disable Device', 'Escape Artist', 'Gather Information', 'Heal', 'Hide',
                     'Jump', 'Knowledge (history)', 'Knowledge (nature)', 'Knowledge (religion)',
                     'Knowledge (the planes)', 'Listen', 'Move Silently', 'Open Lock', 'Profession',
                     'Search', 'Sense Motive', 'Sleight of Hand', 'Spellcraft', 'Spot', 'Tumble',
                     'Use Magic Device', 'Use Rope']
    advancement = core.get_class_advancement({
        'DivineCasterClass': [1,2,3,5,6,7,8,10],
        'sacred stealth': [1,7],
        'detect evil': [1],
        'discover subterfuge': list(range(2,11,3)),
        'sneak attack': list(range(3,11,3)),
        'sacred defense': [4],
        'sacred strike': [10]
        })
    @staticmethod
    def prereq(character):
        return (character.alignment == 'lawful good' and
                character.skills['Gather Information'] >= 8 and
                all(character.skills[x].ranks >= 4 for x in ['Search', 'Sense Motive']) and
                # detect evil class feature or detect evil divine spell and #TODO
                'sneak attack' in character.features.active
                )

class AbsoluteConviction(core.Feature):
    _name = 'absolute conviction'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.alignment.attribute_.pipe(
            ops.map(lambda x: x=='lawful good'), ops.distinct_until_changed()
            ).subscribe(self.source.code_of_conduct_.on_next, util.log_error)

class PierceShadows(core.Feature):
    _name = 'pierce shadows'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SacredStealth(core.Feature):
    _name = 'sacred stealth'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class Smite(core.Feature):
    _name = 'smite'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.frequency = util.Frequency(self.grade,1,'day')
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class MercilessPurity(core.Feature):
    _name = 'merciless purity'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class RighteousFervor(core.Feature):
    _name = 'righteous fervor'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class BurningLight(core.Feature):
    _name = 'burning light'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class DiscoverSubterfuge(core.Feature):
    _name = 'discover subterfuge'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.bonus = util.LiveAttribute(self.grade, lambda x: x*2)
        for x in ['Search', 'Spot']:
            self.character.skills[x].add(self.bonus, 'competence', source=self)
    def escalate(self): self.grade.attribute += 1

class SacredDefense(core.Feature):
    _name = 'sacred defense'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SacredStrike(core.Feature):
    _name = 'sacred strike'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Shadowmind
class Shadowmind(core.PrestigeClass):
    _name = 'shadowmind'
    _hit_die = 6; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Autohypnosis', 'Bluff', 'Concentration', 'Craft', 'Disable Device',
        'Escape Artist', 'Hide', 'Jump', 'Knowledge (psionics)', 'Listen', 'Move Silently',
        'Open Lock', 'Psicraft', 'Search', 'Sense Motive', 'Sleight of Hand', 'Spot', 'Tumble']
    advancement = core.get_class_advancement({
        'ManifesterClass': [1,3,4,6,7,9,10],
        'read thoughts': [1],
        'sneak attack': list(range(2,11,3)),
        'cloud mind': [3],
        'mass cloud mind': [9],
        'mind stab': [10]
        })
    def __init__(self, character): raise NotImplementedError # ugh, psi

    @staticmethod
    def prereq(character):
        return (character.BAB >= 3 and
                all(character.skills[x].ranks >= 5 for x in ['Hide', 'Move Silently']) and
                character.skills['Sleight of Hand'].ranks >= 3 # and
                # manifester level 3rd and
                # able to manifest concealing amorpha
                )

class ReadThoughts(core.Feature):
    _name = 'read thoughts'
    _tags = ['psi-like']
    def __init__(self, character): raise NotImplementedError

class CloudMind(core.Feature):
    _name = 'cloud mind'
    _tags = ['psi-like']
    def __init__(self, character): raise NotImplementedError

class MassCloudMind(core.Feature):
    _name = 'mass cloud mind'
    _tags = ['psi-like']
    def __init__(self, character): raise NotImplementedError

class MindStab(core.Feature):
    _name = 'mind stab'
    _tags = ['supernatural']

#%% Spymaster
class Spymaster(core.PrestigeClass):
    _name = 'spymaster'
    _hit_die = 6; skill_points = 8; bab_type = 'three quarters'; good_saves = ['Reflex']
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Decipher Script', 'Diplomacy',
                     'Disable Device', 'Disguise', 'Escape Artist', 'Forgery', 'Gather Information',
                     'Hide', 'Intimidate', 'Jump', 'Knowledge (geography)', 'Knowledge (history)',
                     'Knowledge (local)', 'Knowledge (nobility and royalty)', 'Listen',
                     'Move Silently', 'Open Lock', 'Search', 'Sense Motive', 'Sleight of Hand',
                     'Speak Language', 'Spot', 'Swim', 'Tumble', 'Use Magic Device', 'Use Rope']
    proficiencies = ['simple', 'martial', 'light', 'medium']
    advancement = {
        1: ['cover identity', 'undetectable alignment'],
        2: ['quick change', 'scrying defense'],
        3: ['sneak attack', 'magic aura'],
        4: ['cover identity', 'slippery mind'],
        5: ['dispel scrying'],
        6: ['sneak attack'],
        7: ['cover identity', 'deep cover']
        }
    @staticmethod
    def prereq(character):
        return (all(character.skills[x].ranks >= 8 for x in ['Bluff', 'Disguise']) and
                all(character.skills[x].ranks >= 4
                    for x in ['Diplomacy', 'Forgery', 'Gather Information', 'Sense Motive']) and
                any(x.focus == 'Bluff'
                    for x in character.feats.get_all(name='Skill Focus', status='active'))
                )

class CoverIdentity(core.Feature):
    _name = 'cover identity'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class UndetectableAlignment(core.Feature):
    _name = 'undetectable alignment'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class QuickChange(core.Feature):
    _name = 'quick change'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ScryingDefense(core.Feature):
    _name = 'scrying defense'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class MagicAura(core.Feature):
    _name = 'magic aura'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

class DispelScrying(core.Feature):
    _name = 'dispel scrying'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class DeepCover(core.Feature):
    _name = 'deep cover'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Streetfighter
class Streetfighter(core.PrestigeClass):
    _name = 'streetfighter'
    _hit_die = 8; skill_points = 4; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Bluff', 'Climb', 'Disable Device', 'Hide', 'Intimidate', 'Jump',
                     'Knowledge (local)', 'Listen', 'Move Silently', 'Open Lock', 'Ride', 'Search',
                     'Spot', 'Tumble']
    advancement = {
        1: ['always ready', 'streetwise'],
        2: ['stand tough'],
        3: ['always ready', 'sneak attack'],
        4: ['stand tough'],
        5: ['always ready', 'Uncanny Dodge']
        }
    @staticmethod
    def prereq(character):
        return (character.BAB >= 5 and
                all(character.skills[x].ranks >= 5
                    for x in ['Bluff', 'Intimidate', 'Knowledge (local)']) and
                all(x in character.feats.active for x in ['Combat Expertise', 'Improved Feint'])
                )

class AlwaysReady(core.Feature):
    _name = 'always ready'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.initiative.add(self.grade, 'competence', source=self)
    def escalate(self): self.grade.attribute += 1

class StandTough(core.Feature):
    _name = 'stand tough'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Tempest
class Tempest(core.PrestigeClass):
    _name = 'tempest'
    _hit_die = 10; skill_points = 2; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Balance', 'Climb', 'Craft', 'Jump', 'Sleight of Hand', 'Tumble']
    advancement = core.get_class_advancement({
        'tempest defense': list(range(1,6,2)),
        'ambidexterity': list(range(2,6,2)),
        'two-weapon versatility': [3],
        'two-weapon spring attack': [5]
        })
    @staticmethod
    def prereq(character):
        return (character.BAB >= 6 and
                all(x in character.feats.active
                    for x in ['Dodge', 'Improved Two-Weapon Fighting', 'Mobility', 'Spring Attack',
                              'Two-Weapon Fighting'])
                )

class TempestDefense(core.Feature):
    _name = 'tempest defense'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class Ambidexterity(core.Feature):
    _name = 'ambidexterity'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class TwoWeaponVersatility(core.Feature):
    _name = 'two-weapon versatility'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class TwoWeaponSpringAttack(core.Feature):
    _name = 'two-weapon spring attack'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Thief-acrobat
class ThiefAcrobat(core.PrestigeClass):
    _name = 'thief-acrobat'
    _hit_die = 6; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex']
    _class_skills = ['Appraise', 'Balance', 'Climb', 'Craft', 'Disable Device', 'Escape Artist',
        'Hide', 'Jump', 'Move Silently', 'Open Lock', 'Perform', 'Search', 'Tumble', 'Use Rope']
    proficiencies = ['simple']
    advancement = {
        1: ['fast acrobatics', 'kip up', 'steady stance'],
        2: ['agile fighting', 'slow fall'],
        3: ['defensive roll', 'acrobatic charge'],
        4: ['agile fighting', 'slow fall', 'SkillMastery'],
        5: ['defensive roll', 'improved evasion']
        }
    def SkillMastery(self):
        sm = self.character.features.add(name='skill mastery', source=self)
        sm.add_skills(['Balance', 'Climb', 'Jump', 'Tumble'], source=self)
    @staticmethod
    def prereq(character):
        return (all(character.skills[x].ranks >= 8
                    for x in ['Balance', 'Climb', 'Jump', 'Tumble']) and
                'evasion' in character.features.active
                )

class FastAcrobatics(core.Feature):
    _name = 'fast acrobatics'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class KipUp(core.Feature):
    _name = 'kip up'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class AgileFighting(core.Feature):
    _name = 'agile fighting'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Vigilante
class Vigilante(core.PrestigeClass):
    _name = 'vigilante'
    _hit_die = 8; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Balance', 'Climb', 'Craft', 'Disable Device', 'Disguise', 'Escape Artist',
        'Gather Information', 'Hide', 'Intimidate', 'Jump', 'Knowledge (local)', 'Move Silently',
        'Open Lock', 'Perform', 'Search', 'Sense Motive', 'Tumble', 'Use Rope']
    proficiencies = ['simple', 'martial', 'net']
    advancement = core.get_class_advancement({
        ('detect evil', 'spellcasting'): [1],
        'streetwise': [1,7],
        'smite the guilty': list(range(2,11,4)),
        'quick search': [3],
        'SpeakWithDead': [4],
        'quick hide': [5],
        'DimensionalAnchor': [8],
        'mettle': [9]
        })
    def SpeakWithDead(self):
        self.character.magic.spell_like_abilities.add(name='speak with dead',
            caster_level=self.level, frequency=util.Frequency(1,1,'day'), source=self)

    def DimensionalAnchor(self):
        self.character.magic.spell_like_abilities.add(name='dimensional anchor',
            caster_level=self.level, frequency=util.Frequency(1,1,'day'), source=self)

    @staticmethod
    def prereq(character):
        return (character.alignment != 'evil' and
                character.BAB >= 4 and
                all(character.skills[x].ranks >= 8
                    for x in ['Gather Information', 'Knowledge (local)', 'Sense Motive']) and
                all(character.skills[x].ranks >= 4 for x in ['Intimidate', 'Search']) and
                'Alertness' in character.feats.active
                )

class VigilanteSpellcasting(dmg.prestige_classes.AssassinSpellcasting):
    _ability = 'charisma'
    clss = 'bard' # abj, div, ill, nec, trans ONLY; bard(0) becomes vigilante(1)
    retrain = [6,8,10]
    _spell_list = {
        1: ['accelerated movement', 'alarm', 'animate rope', 'cause fear', 'comprehend languages',
            'detect magic', 'detect secret doors', 'disguise self', 'distort speech', 'erase',
            'expeditious retreat', 'swift expeditious retreat', 'feather fall', 'ghost sound',
            'identify', 'joyful noise', 'know direction', 'mage hand', 'magic mouth',
            "master's touch", 'mending', 'message', "Nystul's magic aura", 'obscure object',
            'open/close', 'prestidigitation', 'read magic', 'remove fear', 'resistance',
            'silent image', 'undetectable alignment', 'ventriloquism'],
        2: ['alter self', 'bladeweave', 'blindness/deafness', 'blur', "cat's grace",
            'detect thoughts', "eagle's splendor", 'swift fly', "fox's cunning", 'hypnotic pattern',
            'invisibility', 'swift invisibility', 'iron silence', 'locate object', 'minor image',
            'mirror image', 'misdirection', 'pyrotechnics', 'scare', 'silence', 'sonic weapon',
            'tactical precision', 'tongues', 'whispering wind'],
        3: ['allegro', 'blink', 'clairaudience/clairvoyance', 'dispel magic', 'displacement',
            'fear', 'gaseous form', 'glibness', 'haste', 'illusory script', 'invisibility sphere',
            'major image', 'remove curse', 'scrying', 'sculpt sound', 'secret page',
            'see invisibility', 'slow', 'speak with animals', 'speechlink'],
        4: ['break enchantment', 'detect scrying', 'freedom of movement', 'hallucinatory terrain',
            'greater invisibility', 'legend lore', 'listening coin', 'locate creature',
            'rainbow pattern', 'repel vermin', 'shadow conjuration', 'speak with plants',
            'spectral weapon', 'zone of silence']
        }

class SmiteTheGuilty(core.Feature):
    _name = 'smite the guilty'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.frequency = util.Frequency(self.grade,1,'day')
        raise NotImplementedError

class QuickSearch(core.Feature):
    _name = 'quick search'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class QuickHide(core.Feature):
    _name = 'quick hide'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Mettle(core.Feature):
    _name = 'mettle'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        unconscious_ = self.character.conditions.register('unconscious')
        conscious_ = unconscious_.pipe(ops.map(lambda x: not x))
        for x in ['Fortitude', 'Will']:
            self.character.saves[x]._notes.add(name='Mettle', condition=conscious_, source=self)

#%% Virtuoso
class Virtuoso(core.PrestigeClass):
    _name = 'virtuoso'
    _hit_die = 6; skill_points = 6; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Balance', 'Bluff', 'Concentration', 'Craft', 'Diplomacy', 'Disguise',
                     'Escape Artist', 'Gather Information', 'Intimidate', 'Jump', 'Perform',
                     'Spellcraft', 'Tumble']
    advancement = core.get_class_advancement({
        ('bardic music', 'BardicFascinate', 'virtuoso performance', 'PersuasiveSong'): [1],
        # stack levels for inspire courage
        'ArcaneCasterClass': list(range(2,11)),
        'SustainingSong': [3],
        'JarringSong': [5],
        'SongOfFury': [7],
        'MindbendingMelody': [9],
        'RevealingMelody': [10]
        })

    def __init__(self, character): raise NotImplementedError # bardic music system needs an overhaul

    @staticmethod
    def prereq(character):
        return (all(character.skills[x].ranks >= 4 for x in ['Diplomacy', 'Intimidate']) and
                any(k.startswith('Perform') and v.ranks >= 10 for k,v in character.skills.items()) and
                any(sc.magic_type=='arcane' and sc.caster_level >= 1
                    for sc in character.features.get_all(name='spellcasting'))
                )

#%% Wild Plains Outrider
class WildPlainsOutrider(core.PrestigeClass):
    _name = 'wild plains outrider'
    _hit_die = 8; skill_points = 4; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Balance', 'Handle Animal', 'Jump', 'Knowledge (nature)', 'Listen',
                     'Move Silently', 'Ride', 'Spot', 'Survival', 'Swim']
    advancement = {
        1: ['AnimalCompanionOrSpecialMount', 'RideBonus', 'wild plains stalker'],
        2: ['wild plains swiftness'],
        3: ['wild plains offensive']
        } # multiclass freely with paladin
    mount_advancement = {
        1: ['Mount', 'HandleAnimalBonus']}

    def __init__(self, character):
        super().__init__(character)
        self.mount = None

    def AnimalCompanionOrSpecialMount(self):
        companions = [x for x in self.character.companions if util.is_a(x, 'animal companion')
                      and x.size['index'] > self.character.size['index']]
        mounts = [x for x in self.character.companions if util.is_a(x, 'special mount')]
        possibles = companions + mounts
        if len(possibles)==1:
            self.set_mount(possibles[0])
        else:
            def check_outrider_mount():
                if self.mount is None:
                    util.logger.warning('Wild plains outrider mount not declared.')
            self.character.add_to_build(-2, 1, check_outrider_mount)

    def RideBonus(self):
        self.character.skills['Ride'].add(self.level, 'competence', source=self)

    def set_mount(self, mount):
        if not (util.is_a(mount, 'special mount') or util.is_a(mount, 'animal companion')):
            raise util.NotEligible
        if util.is_a('animal companion') and mount.size['index'] <= self.character.size['index']:
            raise util.NotEligible
        self.mount = mount
        for lvl in range(1, self.level+1):
            for feature in self.mount_advancement.get(lvl, []):
                self._allocate_feature(feature)

    def Mount(self):
        if util.is_a(self.mount, 'special mount'):
            feature = self.character.features.get_one(name='special mount')
        if util.is_a(self.mount, 'animal companion'):
            feature = self.character.features.get_one(name='animal companion')
        feature.effective_level.add(self.level, 'base', source=self)

    def HandleAnimalBonus(self):
        mount_ = self.character.challenges.register(target=self.mount)
        self.character.skills['Handle Animal'].add(self.level, 'competence', condition=mount_,
                                                   source=self)

    @staticmethod
    def prereq(character):
        return (character.skills['Ride'].ranks >= 9 and
                all(x in character.feats.active for x in ['Mounted Combat', 'Track']) and
                (len([x for x in character.companions if util.is_a(x, 'animal companion')
                              and x.size['index'] > character.size['index']]) >= 1 or
                 'special mount' in character.features.active)
                )

class WildPlainsStalker(core.Feature):
    _name = 'wild plains stalker'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class WildPlainsSwiftness(core.Feature):
    _name = 'wild plains swiftness'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class WildPlainsOffensive(core.Feature):
    _name = 'wild plains offensive'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError
