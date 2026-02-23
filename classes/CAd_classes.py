#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 12:30:28 2025
@author: gtauxe
"""

import reactivex as rx
import reactivex.operators as ops

import core
import utilities as util
sourcebook = 'Complete Adventurer'

#%% Ninja
class Ninja(core.Class):
    _name = 'ninja'
    _hit_die = 6; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex']
    # starting gold 4d4x10
    _class_skills = ['Balance', 'Bluff', 'Climb', 'Concentration', 'Craft', 'Disable Device',
                     'Disguise', 'Escape Artist', 'Gather Information', 'Hide', 'Jump', 'Listen',
                     'Move Silently', 'Open Lock', 'Search', 'Sense Motive', 'Sleight of Hand',
                     'Spot', 'Swim', 'Tumble']
    proficiencies = ['simple', 'hand crossbow', 'kama', 'kukri', 'nunchaku', 'sai', 'shortbow',
                     'short sword', 'shuriken', 'siangham']
    advancement = core.get_class_advancement({
        ('ACBonus', 'KiPower', 'trapfinding'): [1],
        'sudden strike': list(range(1,20,2)),
        'ghost step': [2,10],
        'poison use': [3],
        'GreatLeap': [4],
        ('acrobatics', 'ki dodge'): [6],
        'speed climb': [7],
        'ghost strike': [8],
        'improved poison use': [9],
        ('acrobatics', 'Evasion'): [12],
        'ghost mind': [14],
        'ghost sight': [16],
        ('acrobatics', 'greater ki dodge'): [18],
        'ghost walk': [20]
        })

    def __init__(self, character):
        super().__init__(character)
        self.features_test_ = rx.combine_latest(self.character.equipment.active_,
                                                self.character.equipment.encumbrance_,
                                                self.character.conditions.active_).pipe(
            ops.map(lambda p: not any(util.is_a(f, 'Armor') for f in p[0]) and
                        p[1]=='light' and
                        not any(f.name=='helpless' for f in p[2])
                        ),
            ops.distinct_until_changed()
            )

    def ACBonus(self):
        x = self.character.features.add(item='AC bonus', condition=self.features_test_, source=self)
        x.level.add(self.level, source=self)
    def KiPower(self):
        self.character.features.add(item='ki power', condition=self.features_test_, source=self)
    def GreatLeap(self):
        self.character.features.add(item='great leap', condition=self.features_test_, source=self)
    def Evasion(self):
        self.character.features.add(item='evasion', condition=self.features_test_, source=self)

class KiPower(core.Feature):
    _name = 'ki power'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        lvls = util.NumeralAttribute(0)
        rx.combine_latest(self.character.build.level_of('ninja').attribute_,
                          self.character.WIS.attribute_).pipe(
            ops.map(lambda p: max(p[0]//2, 1) + max(p[1], 0)), ops.distinct_until_changed()
            ).subscribe(lvls.value_.on_next, util.log_error)
        self.frequency = util.Frequency(lvls, 1, 'day')
        remaining_ = self.frequency.register(1)
        self.character.saves['Will'].add(2, condition=remaining_, source=self)

class KiAbility(core.Feature):
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.ki = self.character.features.get_one(name='ki power')

class SuddenStrike(core.Feature):
    _name = 'sudden strike'
    #TODO qualifies for sneak attack prereqs
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError

class GhostStep(KiAbility):
    _name = 'ghost step'
    def __init__(self, character):
        super().__init__(character)
        self.character.actions.add(name='become invisible', time='swift', method=self.invisibile,
                                   condition=self.ki.active_, frequency=self.ki.frequency, source=self)

    def escalate(self):
        self.character.actions.add(name='become ethereal', time='swift', method=self.ethereal,
                                   condition=self.ki.active_, frequency=self.ki.frequency, source=self)

    def invisible(self): raise NotImplementedError
    def ethereal(self): raise NotImplementedError

class GreatLeap(core.Feature):
    _name = 'great leap'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class Acrobatics(core.Feature):
    _name = 'acrobatics'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.bonus = util.LiveAttribute(self.grade, lambda x: x*2)
        for skill in ['Climb', 'Jump', 'Tumble']:
            self.character.skills[skill].add(self.bonus, source=self)
    def escalate(self): self.grade.attribute += 1

class KiDodge(KiAbility):
    _name = 'ki dodge'
    def __init__(self, character): raise NotImplementedError

class SpeedClimb(core.Feature):
    _name = 'speed climb'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class GhostStrike(KiAbility):
    _name = 'ghost strike'
    def __init__(self, character): raise NotImplementedError

class ImprovedPoisonUse(core.Feature):
    _name = 'improved poison use'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class GhostMind(core.Feature):
    _name = 'ghost mind'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class GhostSight(core.Feature):
    _name = 'ghost sight'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class GreaterKiDodge(KiAbility):
    _name = 'greater ki dodge'
    def __init__(self, character): raise NotImplementedError

class GhostWalk(KiAbility):
    _name = 'ghost walk'
    def __init__(self, character): raise NotImplementedError

#%% Scout
class Scout(core.Class):
    _name = 'scout'
    _hit_die = 8; skill_points = 8; bab_type = 'three quarters'; good_saves = ['Reflex']
    # starting gold 5d4x10
    _class_skills = ['Balance', 'Climb', 'Craft', 'Disable Device', 'Escape Artist', 'Hide', 'Jump',
        'Knowledge (dungeoneering)', 'Knowledge (geography)', 'Knowledge (nature)', 'Listen',
        'Move Silently', 'Ride', 'Search', 'Sense Motive', 'Speak Language', 'Spot', 'Survival',
        'Swim', 'Tumble', 'Use Rope']
    proficiencies = ['simple', 'handaxe', 'throwing axe', 'short sword', 'shortbow', 'light']
    advancement = core.get_class_advancement({
        'skirmish': list(range(1,20,2)),
        'trapfinding': [1],
        'BattleFortitude': [2, 11, 20],
        'UncannyDodge': [2],
        'FastMovement': [3,11],
        'trackless step': [3],
        'BonusFeat': list(range(4,21,4)),
        'evasion': [5],
        'flawless stride': [6],
        'Camouflage': [8],
        'blindsense (30)': [10],
        'HideInPlainSight': [14],
        'FreeMovement': [18],
        'blindsight (30)': [20]
        })
    feats = ['Acrobatic', 'Agile', 'Alertness', 'Athletic', 'Blind-Fight', 'Brachiation',
            'Combat Expertise', 'Danger Sense', 'Dodge', 'Endurance', 'Far Shot', 'Great Fortitude',
            'Hear the Unseen', 'Improved Intiative', 'Improved Swimming', 'Iron Will',
            'Lightning Reflexes', 'Mobility', 'Point Blank Shot', 'Precise Shot', 'Quick Draw',
            'Quick Reconnoiter', 'Rapid Reload', 'Shot on the Run', 'Skill Focus', 'Spring Attack',
            'Track']
    def __init__(self, character):
        super().__init__(character)
        self.features_test_ = self.character.equipment.encumbrance_.pipe(
            ops.map(lambda x: x in ['none', 'light']), ops.distinct_until_changed()
            )

    def BattleFortitude(self):
        if 'battle fortitude' in self.character.features.active:
            self.character.features.get_one(name='battle fortitude', source=self).escalate()
        else:
            self.character.features.add(name='battle fortitude', condition=self.features_test_, source=self)

    def FastMovement(self):
        if 'ScoutFastMovement' in self.character.features.active:
            self.character.features.get_one(name='fast movement', source=self).escalate()
        else:
            self.character.features.add(obj=ScoutFastMovement(self.character),
                                        condition=self.features_test_, source=self)

    def Camouflage(self):
        self.character.features.add(name='camouflage', condition=self.features_test_, source=self)

    def HideInPlainSight(self):
        hips = self.character.features.add_if_missing(item='HideInPlainSight', source=self)
        hips.set_terrain('natural terrain')
        hips.add_condition(self.features_test_)

    def FreeMovement(self):
        self.character.features.add(name='free movement', condition=self.features_test_, source=self)

class Skirmish(core.Feature):
    _name = 'skirmish'
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
        # errata: extra dmg applies AFTER moving at least 10 feet. cannot be used mounted.
    def escalate(self): self.grade.attribute += 1

class BattleFortitude(core.Feature):
    _name = 'battle fortitude'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        for x in [self.character.saves['Fortitude'], self.character.initiative]:
            x.add(self.grade, 'competence', source=self)
    def escalate(self): self.grade.attribute += 1

class ScoutFastMovement(core.Feature):
    _name = 'fast movement'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.speed['land'].add(util.LiveAttribute(self.grade, lambda x: x*10),
                                         'enhancement', source=self)
    def escalate(self): self.grade.attribute += 1

class FlawlessStride(core.Feature):
    _name = 'flawless stride'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class FreeMovement(core.Feature):
    _name = 'free movement'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Spellthief
class Spellthief(core.Class):
    _name = 'spellthief'
    _hit_die = 6; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Will']
    # starting gold 4d4x10
    _class_skills = ['Appraise', 'Bluff', 'Concentration', 'Craft', 'Decipher Script',
        'Disable Device', 'Escape Artist', 'Gather Information', 'Hide', 'Jump',
        'Knowledge (arcana)', 'Knowledge (local)', 'Listen', 'Move Silently', 'Open Lock', 'Search',
        'Speak Language', 'Spellcraft', 'Spot', 'Swim', 'Tumble', 'Use Magic Device']
    proficiencies = ['simple', 'light']
    advancement = core.get_class_advancement({
        'sneak attack': list(range(1,21,4)),
        'steal spell': [1]+list(range(4,19,2)),
        'trapfinding': [1],
        'spellgrace': [2,11,20],
        'steal spell effect': [2],
        'steal energy resistance': [3, 11, 19],
        'spellcasting': [4],
        'steal spell-like ability': [5],
        'absorb spell': [7, 20],
        'arcane sight': [9],
        'discover spells': [13],
        'steal spell resistance': [15]
        })
    def __init__(self, character): raise NotImplementedError

class StealSpell(core.Feature):
    _name = 'steal spell'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class Spellgrace(core.Feature):
    _name = 'spellgrace'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        spell_ = self.character.challenges.register(challenge='spell', source=self)
        self.character.saves['all'].add(self.grade, 'competence', condition=spell_, source=self)
    def escalate(self): self.grade.attribute += 1

class StealSpellEffect(core.Feature):
    _name = 'steal spell effect'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class StealEnergyResistance(core.Feature):
    _name = 'steal energy resistance'
    _tags = ['supernatural']
    def __init__(self, character):
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class SpellthiefSpellcasting(core.Spellcasting):
    _ability = 'charisma'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    _caster_level = 'half'
    clss = 'sorwiz' # TODO prohibited schools: conjuration, evocation, necromancy, universal
    cantrips = False
    retrain = [12,15,18]
    _spells_per_day = {
        4: [0], 6: [1], 8: [1,0], 10: [1,1], 11: [1,1,0], 12: [1,1,1],
        14: [2,1,1,0], 15: [2,1,1,1], 16: [2,2,1,1], 17: [2,2,2,1],
        18: [3,2,2,1], 19: [3,3,3,2], 20: [3,3,3,3]
        }
    _spells_known = {
        4: [2], 6: [3], 8: [4,2], 10: [4,3], 11: [4,3,2], 12: [4,4,3],
        14: [4,4,4,2], 15: [4,4,4,3], 17: [5,4,4,4], 18: [5,5,4,4], 19: [5,5,5,4], 20: [5,5,5,5]
        }

class StealSpellLikeAbility(core.Feature):
    _name = 'steal spell-like ability'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class AbsorbSpell(core.Feature):
    _name = 'absorb spell'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class ArcaneSight(core.Feature):
    _name = 'arcane sight'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        freq = util.LiveAttribute(self.character.CHA)
        freq.minimum = 1
        lvl = self.character.build.level_of('spellthief')
        self.character.magic.spell_like_abilities.add(name='arcane sight', caster_level=lvl,
                                                      frequency=freq, source=self, time='swift')

class DiscoverSpells(core.Feature):
    _name = 'discover spells'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class StealSpellResistance(core.Feature):
    _name = 'steal spell resistance'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Shared features
class AcrobaticCharge(core.Feature):
    _name = 'acrobatic charge'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SpeakWithAnimals(core.Feature): # Animal Lord
    _name = 'speak with animals'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

class SpeakWithAnimals(core.Feature): # Beastmaster
    _name = 'speak with animals'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        lvl = self.character.build.level_of('beastmaster')
        self.frequency = util.NumeralFrequency(self.grade,1,'day')
        self.character.magic.spell_like_abilities.add(name='speak with animals',
            caster_level=lvl, frequency=self.frequency, source=self)
    def escalate(self): self.grade.attribute += 1

class FastWildShape(core.Feature):
    _name = 'fast wild shape'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SteadyStance(core.Feature):
    _name = 'steady stance'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class GhostStep(core.Feature):
    _name = 'ghost step' #TODO this conflicts with ninja Ki Ability
    _tags = ['supernatural']

class DetectMagic(core.Feature): # Spellthief
    _name = 'detect magic'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        freq = util.LiveAttribute(self.character.CHA, lambda x: x)
        freq.minimum = 1
        self.frequency = util.Frequency(freq, 1, 'day')
        self.character.magic.spell_like_abilities.add(name='detect magic', frequency=self.frequency,
            caster_level=self.character.build.level_of('spellthief'), source=self)

class DetectMagic(core.Feature): # Nightsong infiltrator
    _name = 'detect magic'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.character.magic.spell_like_abilities.add(name='detect magic', frequency='at will', source=self)

class Streetwise(core.Feature):
    _name = 'streetwise'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.bonus = util.LiveAttribute(self.grade, lambda x: x*2)
        for x in ['Gather Information', 'Knowledge (local)']:
            self.character.skills[x].add(self.bonus, 'competence', source=self)
    def escalate(self): self.grade.attribute += 1
