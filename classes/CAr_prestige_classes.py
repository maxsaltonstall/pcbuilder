#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 13:53:36 2025
@author: gtauxe
"""

import reactivex as rx
import reactivex.operators as ops
from reactivex.subject import BehaviorSubject

import core, phb.classes
import phb.spells as spells
import splat.epic_level_handbook as elh
import utilities as util
sourcebook = 'Complete Arcane'

#%% Acolyte of the skin
class AcolyteOfTheSkin(core.PrestigeClass):
    _name = 'acolyte of the skin'
    _hit_die = 8; skill_points = 2; bab_type = 'three quarters'; good_saves = ['Fortitude', 'Will']
    _class_skills = ['Concentration', 'Craft', 'Intimidate', 'Knowledge (arcana)',
                     'Knowledge (the planes)', 'Profession', 'Spellcraft']
    advancement = {
        1: ['poison', 'wear fiend'],
        2: ['CasterLevel', 'flame resistant'],
        3: ['fiendish glare'],
        4: ['CasterLevel'],
        5: ['poison', 'skin adaptation'],
        6: ['CasterLevel', 'cold resistant'],
        7: ['glare of the pit'],
        8: ['CasterLevel'],
        9: ['summon fiend'],
        10: ['CasterLevel', 'fiendish symbiosis']
        }
    @staticmethod
    def prereq(character, special=False):
        '''Special: Must have peaceful contact with a summon evil outsider and undergo the Ritual of Bonding.'''
        return (character.alignment != 'good' and
                character.skills['Knowledge (the planes)'].ranks >= 6 and
                character.magic.caster_level >= 5 and
                special)

class WearFiend(core.Feature):
    _name = 'wear fiend'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.character.AC.natural_armor.add(1, source=self)
        self.character.abilities['dexterity'].add(2, 'inherent', source=self)
        self.character.senses['darkvision'].add(60, 'base', source=self)

class Poison(core.Feature):
    _name = 'poison'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.Frequency(1,1,'day')
        sla = spells.Poison()
        sla.DC = util.Attribute(14)

        key_abil = self.character.features.active_.pipe(
            ops.map(lambda p: [x for x in p if util.is_a(x, 'spellcasting')]),
            ops.map(lambda p: {sc.ability for sc in p}),
            ops.map(lambda p: max(p, key=lambda x: self.character.abilities[x])),
            ops.distinct_until_changed(),
            )
        INT_ = key_abil.pipe(ops.map(lambda x: x=='intelligence'))
        sla.DC.add(self.character.INT, 'INT', condition=INT_, source=self)
        WIS_ = key_abil.pipe(ops.map(lambda x: x=='wisdom'))
        sla.DC.add(self.character.WIS, 'WIS', condition=WIS_, source=self)
        CHA_ = key_abil.pipe(ops.map(lambda x: x=='charisma'))
        sla.DC.add(self.character.CHA, 'CHA', condition=CHA_, source=self)

        self.character.magic.spell_like_abilities.add(name='poison', obj=sla, caster_level=8,
                                                      frequency=self.grade, source=self)

    def escalate(self): self.grade.attribute += 1

class FlameResistant(core.Feature):
    _name = 'flame resistant'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.resistances.energy_resistance['fire'].add(10, 'base', source=self)

class FiendishGlare(core.Feature):
    _name = 'fiendish glare'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SkinAdaptation(core.Feature):
    _name = 'skin adaptation'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.character.AC.natural_armor.add(1, source=self)
        self.character.abilities['constitution'].add(2, 'inherent', source=self)
        self.character.senses['darkvision'].add(60, 'base', source=self)

class ColdResistant(core.Feature):
    _name = 'cold resistant'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.resistances.energy_resistance['cold'].add(10, 'base', source=self)

class GlareOfThePit(core.Feature):
    _name = 'glare of the pit'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SummonFiend(core.Feature):
    _name = 'summon fiend'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

class FiendishSymbiosis(core.Feature):
    _name = 'fiendish symbiosis'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Alienist
class Alienist(core.PrestigeClass):
    _name = 'alienist'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Gather Information', 'Knowledge', 'Listen', 'Profession',
                     'Spellcraft', 'Spot']
    advancement = {
        1: ['CasterLevel', 'familiar abilities', 'summon alien'],
        2: ['CasterLevel', 'alien blessing'],
        3: ['CasterLevel', 'metamagic secret'],
        4: ['CasterLevel', 'mad certainty'],
        5: ['CasterLevel', 'pseudonatural familiar'],
        6: ['CasterLevel', 'extra summoning'],
        7: ['CasterLevel', 'metamagic secret'],
        8: ['CasterLevel', 'insane certainty'],
        9: ['CasterLevel', 'timeless body'],
        10: ['CasterLevel', 'alient transcendence']
        }
    @staticmethod
    def prereq(character, special=False):
        '''Special: Must have made peaceful contact with an alienist or a pseudonatural creature.'''
        summons = [x for x in character.magic.spells_known if 'Summoning' in x.descriptors]
        summons = [x for x in summons if x.level >= 3]
        return (character.alignment != 'lawful' and
                character.skills['Knowledge (the planes)'].ranks >= 8 and
                'Augment Summoning' in character.feats.active and
                len(summons) and
                special)

class FamiliarAbilities(core.Feature):
    _name = 'familiar abilities'
    def __init__(self, character): raise NotImplementedError

class SummonAlien(core.Feature):
    _name = 'summon alien'
    def __init__(self, character): raise NotImplementedError

class AlienBlessing(core.Feature):
    _name = 'alien blessing'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.saves['all'].add(1, 'insight', source=self)
        self.character.abilities['wisdom'].add(-2, source=self)

class MetamagicSecret(core.Feature):
    _name = 'metamagic secret'
    def __init__(self, character):
        super().__init__(character)
        self._add_feat_slot()

    def escalate(self): self._add_feat_slot()

    def _add_feat_slot(self):
        is_metamagic_feat = lambda x: hasattr(x, '_metamagic' and x._metamagic)
        self.character.feats.feat_slots.add(1, source=self, restriction=is_metamagic_feat)

class MadCertainty(core.Feature):
    _name = 'mad certainty'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.max_HP.add(3, source=self)

        pseudo_ = self.character.challenges.register(target='pseudonatural')
        not_pseudo_ = pseudo_.pipe(ops.map(lambda x: not x))
        for x in ['Bluff', 'Diplomacy', 'Handle Animal']:
            self.character.skills[x].add(-4, condition=not_pseudo_, source=self)

class PseudonaturalFamiliar(core.Feature):
    _name = 'pseudonatural familiar'
    def __init__(self, character): raise NotImplementedError

class ExtraSummoning(core.Feature):
    _name = 'extra summoning'
    def __init__(self, character): raise NotImplementedError

class InsaneCertainty(core.Feature):
    _name = 'insane certainty'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.max_HP.add(3, source=self)

        pseudo_ = self.character.challenges.register(target='pseudonatural')
        not_pseudo_ = pseudo_.pipe(ops.map(lambda x: not x))
        for x in ['Bluff', 'Diplomacy', 'Handle Animal']:
            self.character.skills[x].add(-6, condition=not_pseudo_, source=self)

class AlienTranscendence(core.Feature):
    _name = 'alien transcendence'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Argent savant
class ArgentSavant(core.PrestigeClass):
    _name = 'argent savant'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Knowledge', 'Profession', 'Spellcraft']
    advancement = {
        1: ['ArcaneCasterLevel', 'force specialization'],
        2: ['ArcaneCasterLevel', 'force armor'],
        3: ['ArcaneCasterLevel', 'enduring force'],
        4: ['ArcaneCasterLevel', 'ablate force'],
        5: ['ArcaneCasterLevel', 'unbind force']
        }
    @staticmethod
    def prereq(character):
        force_spells = [x for x in character.magic.spells_known if 'Force' in x.descriptors]
        return (character.skills['Knowledge (arcana)'].ranks >= 6 and
                character.skills['Spellcraft'].ranks >= 12 and
                len(force_spells) >= 5 and
                any(x.level >= 5 for x in force_spells))

class ForceSpecialization(core.Feature):
    _name = 'force specialization'
    def __init__(self, character): raise NotImplementedError

class ForceArmor(core.Feature):
    _name = 'force armor'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class EnduringForce(core.Feature):
    _name = 'extended force'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class AblateForce(core.Feature):
    _name = 'ablate force'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class UnbindForce(core.Feature):
    _name = 'unbind force'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Blood magus
class BloodMagus(core.PrestigeClass):
    _name = 'blood magus'
    _hit_die = 6; skill_points = 2; bab_type = 'half'; good_saves = ['Fortitude']
    _class_skills = ['Bluff', 'Concentration', 'Craft', 'Heal', 'Spellcraft']
    advancement = {
        1: ['ArcaneCasterLevel', 'blood component', 'durable casting', 'stanch'],
        2: ['ArcaneCasterLevel', 'scarification'],
        3: ['ArcaneCasterLevel', 'DeathKnell'],
        4: ['ArcaneCasterLevel', 'blood draught'],
        5: ['homunculus'],
        6: ['ArcaneCasterLevel', 'bloodseeking spell'],
        7: ['ArcaneCasterLevel', 'thicker than water'],
        8: ['ArcaneCasterLevel', 'awaken blood'],
        9: ['ArcaneCasterLevel' 'infusion'],
        10: ['bloodwalk']
        }
    def __init__(self, character):
        super().__init__(character)
        unlocks = ['BloodComponent','DurableCasting','Stanch','Scarification','BloodDraught','HomunculusFeature','BloodseekingSpell',
                   'ThickerThanWater','AwakenBlood','Infusion','Bloodwalk','Draught','Scar']
        if hasattr(self.character, 'unlocks'):
            self.character.unlocks.add(item=unlocks, source=self)

    def DeathKnell(self):
        frequency = util.Frequency(1, 1, 'day')
        self.character.magic.spell_like_abilities.add(item='DeathKnell',
            caster_level=self.character.build.level, frequency=frequency, source=self)

    def prereq(character, special=False):
        '''Special: The character must have been killed, then returned to life.'''
        return (character.alignment != 'lawful good' and
                all(x in character.feats.active for x in ['Great Fortitude', 'Toughness']) and
                character.skills['Concentration'].ranks >= 4 and
                any(sc.magic_type=='arcane' and sc.caster_level >= 5
                    for sc in character.features.get_instances('spellcasting')) and
                special)

class BloodComponent(core.Feature):
    _name = 'blood component'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class DurableCasting(core.Feature):
    _name = 'durable casting'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Stanch(core.Feature):
    _name = 'stanch'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Scarification(core.Feature):
    _name = 'scarification'
    _tags = ['extraordinary']

class Scar(core.Scroll):
    _name = 'scar'
    _feats = ['scarification']
    # slot management: max 6 of these

class BloodDraught(core.Feature):
    _name = 'blood draught'
    _tags = ['extraordinary']

class Draught(core.Potion):
    _name = 'draught'
    _feats = ['blood draught']
    # slot management: max class level + Con score

class Homunculus(core.Feature):
    _name = 'homunculus'
    _tags = ['supernatural']

    def create(self, homunculus):
        hom = homunculus(self.character)
        self.character.max_HP.add(-1, source=self)
        self.character.companions.add(obj=hom, source=self)

        #TODO
        '''Crafting a homunculus requires 1 hour. A blood magus enjoys a stronger than normal link with
        his homunculus. By touching the homunculus, a blood magus can transfer his wounds to the creature
        (up to 1 hp per level with each touch). This is a standard action that provokes attacks of
        opportunity. Each time a blood magus gains a class level, his homunculus advances 1 Hit Die,
        as described on page 290 of the Monster Manual, and it gains all the normal benefits of its
        increased Hit Dice (increased base attack bonus, saves, and so on). The homunculus advances
        to a maximum of 6 Hit Dice when the blood magus reaches 9th level. If his homunculus is
        destroyed, a blood magus takes 2d10 points of damage, as noted in the Monster Manual.
        A blood magus?s death results in the death of his homunculus. A blood magus can have only
        one homunculus at any given time.'''

class BloodseekingSpell(core.Feature):
    _name = 'bloodseeking spell'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class ThickerThanWater(core.Feature):
    _name = 'thicker than water'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.character.damage_reduction['bludgeoning'].add(1, source=self)

class AwakenBlood(core.Feature):
    _name = 'awaken blood'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class Infusion(core.Feature):
    _name = 'infusion'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.abilities['constitution'].add(2, source=self)

class Bloodwalk(core.Feature):
    _name = 'bloodwalk'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Effigy master
class EffigyMaster(core.PrestigeClass):
    _name = 'effigy master'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Knowledge', 'Profession', 'Spellcraft']
    advancement = core.get_class_advancement({
        'CasterLevel': list(range(2,6)),
        'craft effigy': [1],
        'improved effigy': [3],
        'effigy link': [5]
        })

    @staticmethod
    def prereq(character):
        return (any(character.skills[f'Craft ({x})'].ranks >= 10
                    for x in ['leatherworking', 'metalworking', 'woodworking']) and
                all(character.skills[x].ranks >= 5 for x in ['Knowledge (arcana)', 'Spellcraft']) and
                character.skills['Use Magic Device'].ranks >= 2 and
                'Craft Wondrous Item' in character.feats.active and
                True) # simulacrum on any spell list, even if you can't cast it

class CraftEffigy(core.Feature):
    _name = 'craft effigy'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute()
        self.effective_level.add(self.magic.caster_level, 'base')
        self.effective_level.add(self.source.level, source=self)
        raise NotImplementedError

class ImprovedEffigy(core.Feature):
    _name = 'improved effigy'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class EffigyLink(core.Feature):
    _name = 'effigy link'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Elemental savant
class ElementalSavant(core.PrestigeClass):
    _name = 'elemental savant'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Knowledge (arcana)', 'Knowledge (the planes)',
                     'Profession', 'Spellcraft']
    advancement = core.get_class_advancement({
        'CasterLevel': [1,2,3,4,6,7,8,9],
        'elemental specialty': [1],
        'EnergyResistance': [1,4,7,10],
        'immunity (sleep)': [2],
        'energy penetration': [3,8],
        'energy focus': [5,10],
        'darkvision (60)': [6],
        ('immunity (paralysis)', 'immunity (poison)'): [9],
        ('elemental perfection'): [10]
        })
    def __init__(self, character):
        super().__init__(character)
        energy_map = {'electricity':'Air', 'acid':'Earth', 'fire':'Fire', 'cold':'Water', None:None}
        self.energy_ = BehaviorSubject(None)
        # self.element_ = BehaviorSubject(None)
        # self.energy_.pipe(ops.map(lambda x: energy_map[x])
        #                   ).subscribe(self.element_.on_next, util.log_error)

        self.grade = util.NumeralCounter(0)
        rx.combine_latest(self.grade.attribute_, self.energy_).pipe(ops.filter(all)
            ).subscribe(self._set_er)

    @property
    def energy(self): return self.energy_.value

    @energy.setter
    def energy(self, value):
        if value not in ['electricity', 'acid', 'fire', 'cold']: return
        self.energy_.on_next(value)

    def EnergyResistance(self): self.grade.attribute += 1

    def _set_er(self, pipes):
        grade, energy = pipes
        to_allocate = [1,2,3,4]
        to_allocate = [x for x in to_allocate if x not in self.abilities]
        er_map = {1:5, 2:5, 3:10, 4:'immunity'}
        for x in to_allocate:
            if x < 4:
                self.character.resistances.energy_resistance[energy].add(er_map[x], 'base', source=self)
            else:
                self.character.resistances.immunities.add(name=x, source=self)

    @staticmethod
    def prereq(character, special=False):
        '''Special: Must have made peaceful contact with an elemental or outsider with an elemental subtype.'''
        acid = [x for x in character.magic.spells_known if 'Acid' in x.descriptors]
        cold = [x for x in character.magic.spells_known if 'Cold' in x.descriptors]
        electricity = [x for x in character.magic.spells_known if 'Electricity' in x.descriptors]
        fire = [x for x in character.magic.spells_known if 'Fire' in x.descriptors]

        return (character.skills['Knowledge (arcana)'].ranks >= 8 and
                character.skills['Knowledge (the planes)'].ranks >= 4 and
                'Energy Substitution' in character.feats.active and
                any(len(x) >= 3 and max(y.level >= 3 for y in x)
                    for x in [acid, cold, electricity, fire]) and
                special)

class ElementalSpecialty(core.Feature):
    _name = 'elemental specialty'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class EnergyPenetration(core.Feature):
    _name = 'energy penetration'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class EnergyFocus(core.Feature):
    _name = 'energy focus'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ElementalPerfection(core.Feature):
    _name = 'elemental perfection'
    def __init__(self, character): raise NotImplementedError

#%% Enlightened fist
class EnlightenedFist(core.PrestigeClass):
    _name = 'enlightened fist'
    _hit_die = 8; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Balance', 'Climb', 'Concentration', 'Craft', 'Escape Artist', 'Hide', 'Jump',
                     'Knowledge (arcana)', 'Knowledge (religion)', 'Listen', 'Move Silently',
                     'Profession', 'Spellcraft', 'Spot', 'Swim', 'Tumble']
    advancement = core.get_class_advancement({
        'ArcaneCasterLevel': [2,3,4,5,7,8,9,10],
        ('MonkAbilities', 'KiStrike', 'Magic') : [1],
        'fist of energy': [2,6],
        'arcane fist': [3],
        'arcane rejuvenation': [5],
        'hold ray': [7],
        'diamond soul': [9]
        })
    # monks may advance after taking EL; likewise arcane casting classes do not prevent advancing

    def __init__(self, character):
        super().__init__(character)
        self.ki = None

    def MonkAbilities(self): raise NotImplementedError
    def KiStrike(self): self.ki = self.character.features.add(item='KiStrike', source=self)
    def Magic(self): self.ki.add_quality('magic')

    @staticmethod
    def prereq(character):
        return (character.skills['Concentration'].ranks >= 8 and
                all(character.skills[x].ranks >= 5
                    for x in ['Knowledge (arcana)', 'Spellcraft']) and
                all(x in character.feats.active
                    for x in ['Combat Casting', 'Improved Unarmed Strike', 'Stunning Fist']) and
                any(sc.magic_type=='arcane' and sc.caster_level >= 3
                    for sc in character.features.get_instances('spellcasting'))
                )

class FistOfEnergy(core.Feature):
    _name = 'fist of energy'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class ArcaneFist(core.Feature):
    _name = 'arcane fist'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class ArcaneRejuvenation(core.Feature):
    _name = 'arcane rejuvenation'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class HoldRay(core.Feature):
    _name = 'hold ray'
    _tags = ['extraordinary']

#%% Fatespinner
class Fatespinner(core.PrestigeClass):
    _name = 'fatespinner'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Appraise', 'Concentration', 'Craft', 'Knowledge (arcana)', 'Profession',
                     'Sleight of Hand', 'Spellcraft']
    advancement = {
        1: ['CasterLevel', 'spin fate'],
        2: ['CasterLevel', 'fickle finger of fate'],
        3: ['CasterLevel', 'spin destiny'],
        4: ['CasterLevel', 'deny fate', 'resist fate'],
        5: ['seal fate']
        }

class SpinFate(core.Feature):
    _name = 'spin fate'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class FickleFingerOfFate(core.Feature):
    _name = 'fickle finger of fate'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SpinDestiny(core.Feature):
    _name = 'spin destiny'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class DenyFate(core.Feature):
    _name = 'deny fate'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ResistFate(core.Feature):
    _name = 'resist fate'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SealFate(core.Feature):
    _name = 'seal fate'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Geometer
class Geometer(core.PrestigeClass):
    _name = 'geometer'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Decipher Script', 'Disable Device', 'Knowledge',
                     'Profession', 'Search', 'Spellcraft']
    advancement = {
        1: ['ArcaneCasterLevel', 'glyph of warding', 'spellglyph'],
        2: ['ArcaneCasterLevel', 'book of geometry'],
        3: ['ArcaneCasterLevel', 'sigilsight'],
        4: ['ArcaneCasterLevel', 'pass sigil'],
        5: ['ArcaneCasterLevel', 'powerful spellglyph', 'greater glyph of warding']
        }
    @staticmethod
    def prereq(character):
        castings = [sc for sc in character.features.get_instances('spellcasting')
                   if sc.magic_type=='arcane' and sc.caster_type=='prepared']
        return (all(character.skills[x].ranks >= 9
                    for x in ['Decipher Script', 'Knowledge (arcana)']) and
                all(character.skills[x].ranks >= 4 for x in ['Disable Device', 'Search']) and
                'Scribe Scroll' in character.feats.active and
                any(any(x.level >= 3 for x in sc) for sc in castings)
                )

class GlyphOfWarding(core.Feature):
    _name = 'glyph of warding'
    def __init__(self, character):
        super().__init__(character)
        castings = [sc for sc in character.features.get_instances('spellcasting')
                   if sc.magic_type=='arcane' and sc.caster_type=='prepared']
        spellbooks = [sc.spell_list for sc in castings]
        for book in spellbooks:
            book.add(name='glyph of warding', level=3, override=True)

class Spellglyph(core.Feature):
    _name = 'spellglyph'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class BookOfGeometry(core.Feature):
    _name = 'book of geometry'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Sigilsight(core.Feature):
    _name = 'sigilsight'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class PassSigil(core.Feature):
    _name = 'pass sigil'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class PowerfulSpellglyph(core.Feature):
    _name = 'powerful spellglyph'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class GreaterGlyphOfWarding(core.Feature):
    _name = 'greater glyph of warding'
    def __init__(self, character):
        super().__init__(character)
        castings = [sc for sc in character.features.get_instances('spellcasting')
                   if sc.magic_type=='arcane' and sc.caster_type=='prepared']
        spellbooks = [sc.spell_list for sc in castings]
        for book in spellbooks:
            book.add(name='glyph of warding', level=6, override=True)

#%% Green star adept
class GreenStarAdept(core.PrestigeClass):
    _name = 'Green Star adept'
    _hit_die = 8; skill_points = 2; bab_type = 'three quarters'; good_saves = ['Will']
    _class_skills = ['Appraise', 'Concentration', 'Craft', 'Decipher Script', 'Knowledge (arcana)',
                     'Knowledge (architecture and engineering)', 'Knowledge (geography)',
                     'Knowledge (history)', 'Profession', 'Spellcraft']
    advancement = core.get_class_advancement({
        'ArcaneCasterClass': list(range(2,11,2)),
        ('DamageReduction', 'improved caster level', 'starmetal dependency'): [1],
        'starmetal rigor': list(range(1,11,3)),
        'natural attack': [2],
        'unnatural metabolism': list(range(2,11,3)),
        'fortification': list(range(3,11,3)),
        'otherworldly vision': [4],
        'null metabolism': [7],
        ('emerald perfection', 'rapid repair'): [10]
        })

    def DamageReduction(self):
        self.character.resistances.damage_reduction['adamantine'].add(self.level, 'base', source=self)

    @staticmethod
    def prereq(character, special=False):
        '''Special: Must acquire a piece of starmetal weighing at least 2 oz, powder it, and consume it in a
specially prepared infusion costing 1,000 gp and one week to prepare.'''
        return (character.BAB >= 4 and
                character.skills['Knowledge (arcana)'].ranks >= 8 and
                all(character.skills[x].ranks >= 2
                    for x in ['Decipher Script', 'Knowledge (architecture and engineering)',
                              'Knowledge (geography)', 'Knowledge (history)']) and
                'Combat Casting' in character.feats.active and
                any(sc.magic_type=='arcane' and sc.caster_level >= 1
                    for sc in character.features.get_instances('spellcasting')) and
                special)

class ImprovedCasterLevel(core.Feature):
    _name = 'improved caster level'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class StarmetalDependency(core.Feature):
    _name = 'starmetal dependency'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class StarmetalRigor(core.Feature):
    _name = 'starmetal rigor'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)

        benefit_map = {1:1, 2:2, 3:4, 4:6}
        self.benefit = util.LiveAttribute(self.grade, lambda x: benefit_map[x])
        self.character.abilities['strength'].add(self.benefit, source=self)
        self.character.AC.natural_armor.add(self.benefit, source=self)

        penalty_map = {1:-1, 2:-1, 3:-2, 4:-3}
        self.penalty = util.LiveAttribute(self.grade, lambda x: penalty_map[x])
        assert self.character.abilities['dexterity'].permanent
        max_pen = util.NumeralAttribute(0)
        self.character.abilities['dexterity'].permanent_.pipe(ops.map(lambda x: 3-x)
            ).subscribe(max_pen.value_.on_next, util.log_error)
        self.penalty.minimum = max_pen
        self.character.abilities['dexterity'].add(self.penalty, source=self)

    def escalate(self): self.grade.attribute += 1

class NaturalAttack(core.Feature):
    _name = 'natural attack'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class UnnaturalMetabolism(core.Feature):
    _name = 'unnatural metabolism'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(2)
        c_ = self.character.challenges.register(challenge=['poison', 'sleep', 'paralysis',
                 'stunning', 'disease', 'death', 'necromancy'])
        any_ = rx.combine_latest(*c_).pipe(ops.map(any), ops.distinct_until_changed())
        self.character.saves['all'].add(2, condition=any_, source=self)

    def escalate(self): self.grade.attribute += 2

class Fortification(core.Feature):
    _name = 'fortification'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(25)
        self.character.AC['fortification'].add(self.grade, source=self)

    def escalate(self): self.grade.attribute += 25

class OtherworldlyVision(core.Feature):
    _name = 'otherworldly vision'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.senses['low-light vision'].add(True, source=self)
        self.character.senses['darkvision'].add(60, 'base', source=self)

class NullMetabolism(core.Feature):
    _name = 'null metabolism'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.build.add(name=['breathless', 'uneating', 'sleepless'], source=self)
        self.character.resistances.immunities.add(name=['inhaled poison', 'drowning', 'suffocation',
            'sleep', 'fatigue', 'exhaustion'], source=self)

class EmeraldPerfection(core.Feature):
    _name = 'emerald perfection'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class RapidRepair(core.Feature):
    _name = 'rapid repair'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Initiate of the sevenfold veil
class InitiateOfTheSevenfoldVeil(core.PrestigeClass):
    _name = 'initiate of the Sevenfold Veil'
    _hit_die =  4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Appraise', 'Concentration', 'Craft', 'Decipher Script', 'Knowledge',
                     'Profession', 'Spellcraft']
    advancement = {
        1: ['ArcaneCasterLevel', 'veil', 'warding', 'unimpeachable abjuration'],
        2: ['ArcaneCasterLevel', 'veil', 'unanswerable strike'],
        3: ['ArcaneCasterLevel', 'veil', 'warding'],
        4: ['ArcaneCasterLevel', 'veil', 'reactive warding'],
        5: ['ArcaneCasterLevel', 'veil', 'warding'],
        6: ['ArcaneCasterLevel', 'veil', 'unanswerable strike', 'double warding'],
        7: ['ArcaneCasterLevel', 'veil', 'warding', 'kaleidoscopic doom']
        }
    @staticmethod
    def prereq(character):
        abj = [x for x in character.magic.spells_known if x.school=='abjuration']
        abj_4 = [x for x in abj if x.level >= 4]
        return (all(character.skills[x].ranks >= 12 for x in ['Knowledge (arcana)', 'Spellcraft']) and
                character.skills['Knowledge (nature)'].ranks >= 4 and
                any(x.school=='abjuration' for x in character.feats.get_instances('Greater Spell Focus')) and
                any(x.school=='abjuration' for x in character.feats.get_instances('Spell Focus')) and
                any(x.skill=='Spellcraft' for x in character.feats.get_instances('Skill Focus')) and
                len(abj) >= 5 and len(abj_4) >= 2)

class Warding(core.Feature):
    _name = 'warding'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.Frequency(1,1,'day')
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

class Veil(core.Feature):
    _name = 'veil'
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

class UnimpeachableAbjuration(core.Feature):
    _name = 'unimpeachable abjuration'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError

class UnanswerableStrike(core.Feature):
    _name = 'unanswerable strike'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(2)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 2

class ReactiveWarding(core.Feature):
    _name = 'reactive warding'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

class DoubleWarding(core.Feature):
    _name = 'double warding'
    def __init__(self, character): raise NotImplementedError

class KaleidoscopicDoom(core.Feature):
    _name = 'kaleidoscopic doom'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

#%% Mage of the arcane order
class MageOfTheArcaneOrder(core.PrestigeClass):
    _name = 'mage of the Arcane Order'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Decipher Script', 'Knowledge', 'Profession',
                     'Speak Language', 'Spellcraft']
    advancement = core.get_class_advancement({
        'ArcaneCasterLevel': list(range(1,11)),
        'guild member': [1],
        'spellpool': [1,4,7],
        'BonusFeat': [2,9],
        'BonusLanguage': [3,6],
        'NewSpell': [5,8],
        'regent': [10]
        })
    feats = ['metamagic'] #TODO huh?
    def __init__(self, character):
        super().__init__(character)
        self.character.equipment.add(core.CustomGear('Guild membership', 750))
        self._order = None

    @property
    def order(self): return self._order

    @order.setter
    def order(self, value):
        if value in self.character.lib['Organization']: #TODO implement organizations
            value = self.character.lib['Organization'][value](self.character)
        self.character.affiliations.append(value)
        self._order = value

    def BonusLanguage(self): self.character.skills.languages.slots.add(1, source=self)

    def NewSpell(self): raise NotImplementedError('New spell')

    @staticmethod
    def prereq(character):
        sc_list = character.features.get_all(name='spellcasting')
        return all([
            character.skills['Knowledge (arcana)'].ranks >= 8,
            'Cooperative spell' in character.feats.active,
            ('Metamagic School Focus' in character.feats.active or character.feats.metamagic_feats>= 1),
            any(sc.magic_type=='arcane' and sc.spells_known.collection['level'].max() >= 2 for sc in sc_list),
            character.equipment.wealth >= 750
            ])

class EpicMageOfTheArcaneOrder(elh.EpicClass, MageOfTheArcaneOrder):
    _name = 'epic mage of the arcane order'
    def __init__(self, character): raise NotImplementedError
    # bonus language every 14+4
    # bonus feat every 14+4
    # epic spellcasting + spellpool (10th-lvl)

class GuildMember(core.Feature):
    _name = 'guild member'
    def __init__(self, character): raise NotImplementedError

class Spellpool(core.Feature):
    _name = 'spellpool'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class Regent(core.Feature):
    '''The regents set the Arcane Order's rules and policies, meeting each month in the Council of
    Regents. A regent must attend six council meetings in one year or be removed from the council
    and lose his regent status (he loses no other benefits of guild membership, nor does he lose his
    level in the prestige class). Enacting new policies or eradicating old ones requires a three-
    fifths majority vote to pass.
    '''
    _name = 'regent'
    def __init__(self, character):
        super().__init__(character)
        chall_ = self.character.challenges.register(target='Arcane Guild member')
        self.character.checks['charisma'].add(2, 'competence', condition=chall_)
        #Must attend 6 council mtgs/year; enacting policies requires 3/5 majority
        #TODO add mechanism to leave the council

class ArcaneOrder(core.Organization):
    _name = 'The Arcane Order'
    # stronghold = Mathghamhna
    # dues 30/month
    # 'associates': nonresident
    # 'students' +200/month tuition
    # 'collegians': >= 5th level caster; 30 gp x caster_level / month in residence
    # other residents: 'scholars'
    # 'regents': at least 10th level arcanist
    # important people:
        # Master Collegian, Master Librarian, Master of the Spellpool, Master Diviner, Master Warder
        # Chancellor Japheth

#%% Master transmogrifist
class MasterTransmogrifist(core.PrestigeClass):
    _name = 'master transmogrifist'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Bluff', 'Concentration', 'Craft', 'Disguise', 'Knowledge (arcana)',
                     'Profession', 'Spellcraft']
    advancement = core.get_class_advancement({
        'ArcaneCasterLevel': [2,3,5,6,8,9],
        ('favored shape', 'extended change'): [1],
        'manifest senses': [2],
        'battle mastery': list(range(3,11,3)),
        'effortless change': [4],
        'shapechanger': [5],
        'reflexive change': [7],
        'manifest qualities': [8],
        'infinite variety': [10]
        })
    @staticmethod
    def prereq(character):
        return (character.alignment != 'lawful' and
                character.skills['Bluff'].ranks >= 2 and
                character.skills['Disguise'].ranks >= 5 and
                'Eschew Materials' in character.feats.active and
                all(x in character.magic.spells_known for x in ['alter self', 'polymorph'])
                )

class ExtendedChange(core.Feature):
    _name = 'extended change'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class FavoredShape(core.Feature):
    _name = 'favored shape'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class ManifestSenses(core.Feature):
    _name = 'manifest senses'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class BattleMastery(core.Feature):
    _name = 'battle mastery'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(2)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 2

class EffortlessChange(core.Feature):
    _name = 'effortless change'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Shapechanger(core.Feature):
    _name = 'shapechanger'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ReflexiveChange(core.Feature):
    _name = 'reflexive change'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ManifestQualities(core.Feature):
    _name = 'manifest qualities'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class InfiniteVariety(core.Feature):
    _name = 'infinite variety'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Mindbender
class Mindbender(core.PrestigeClass):
    _name = 'mindbender'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Fortitude', 'Will']
    _class_skills = ['Bluff', 'Concentration', 'Diplomacy', 'Intimidate', 'Knowledge', 'Profession',
                     'Sense Motive', 'Spellcraft']
    advancement = core.get_class_advancement({
        'ArcaneCasterLevel': list(range(1,11,2)),
        'telepathy': [1],
        'push the weak mind': list(range(2,11,3)),
        'skill boost': [2],
        'mindread': [3,7],
        'eternalcharm': list(range(4,11,2)),
        'enchantment spell power': [6,10],
        'dominate feature': [7],
        'thrall': [10]
        })
    @staticmethod
    def prereq(character):
        return (character.alignment != 'good' and
                all(character.skills[x].ranks >= 4
                    for x in ['Bluff', 'Diplomacy', 'Intimidate', 'Sense Motive']) and
                # charm person spell; sla; or charm invocation and
                any(sc.magic_type=='arcane' and sc.caster_level >= 5
                    for sc in character.features.get_instances('spellcasting'))
                )

class Telepathy(core.Feature):
    _name = 'telepathy'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class PushTheWeakMind(core.Feature):
    _name = 'Push the weak mind'
    _tags = ['spell-like']
    def __init__(self, character):
        self.frequency = util.Frequency(1, 1, 'day')
        raise NotImplementedError

    def escalate(self):
        self.frequency.add(1, 'base')

class SkillBoost(core.Feature):
    _name = 'skill boost'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        lvl = self.character.classes.level_of('mindbender')
        bonus = util.LiveAttribute(lvl, lambda x: x//2)
        for skill in ['Bluff', 'Diplomacy', 'Intimidate', 'Sense Motive']:
            self.character.skills[skill].add(bonus, 'competence', source=self)

class Dominate(core.Feature):
    _name = 'dominate'
    _tags = ['spell-like']
    def __init__(self, character):
        raise NotImplementedError

class EnchantmentSpellPower(core.Feature):
    _name = 'enchantment spell power'
    _tags = ['extraordinary']
    def __init__(self, character):
        self.bonus = util.NumeralAttribute(2)
        raise NotImplementedError

    def escalate(self):
        self.bonus.attribute += 2

class EternalCharm(core.Feature):
    _name = 'eternal charm'
    _tags = ['spell-like']
    def __init__(self, character):
        raise NotImplementedError
        self.grade = util.NumeralAttribute(1)

    def escalate(self):
        self.grade.attribute += 1

class Mindread(core.Feature):
    _name = 'mindread'
    _tags = ['spell-like']
    def __init__(self, character):
        raise NotImplementedError
        self.frequency = util.Frequency(2, 1, 'day')

    def escalate(self):
        self.frequency.add(2, 'base')

class Thrall(core.Feature):
    _name = 'thrall'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Seeker of the song
class SeekerOfTheSong(core.PrestigeClass):
    _name = 'seeker of the song'
    _hit_die = 6; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Will']
    _class_skills = ['Climb', 'Concentration', 'Craft', 'Diplomacy', 'Jump', 'Knowledge (arcana)',
                     'Listen', 'Perform', 'Profession', 'Ride', 'Sense Motive', 'Spot', 'Swim']
    advancement = core.get_class_advancement({
        'rapture of the song': list(range(1,11,3)),
        'seeker music': [1],
        'combine songs': [2],
        'subvocalize': [5],
        })
    music = {1: 'burning melody',
             2: 'song of unmaking',
             3: 'dirge of frozen loss',
             4: 'song of life',
             5: 'anthem of thunder and pain',
             6: 'hymn of spelldeath',
             7: 'ballad of agony reborn',
             8: 'aria of everywhere',
             9: 'dirge of songdeath',
             10: 'note of solitude'
             }
    features.update(music)
    def __init__(self, character): raise NotImplementedError # need to overhaul bardic music

    def advance(self):
        if self.multiclass_.value: raise util.NotEligible
        super().advance()

    @staticmethod
    def prereq(character, special=False):
        '''Special: must have heard a seeker of a song use seeker music.'''
        return (character.skills['Knowledge (arcana)'].ranks >= 13 and
                any(character.skills[x].ranks >= 13
                    for x in character.skills if x.startswith('Perform')) and
                any(x.skill.startswith('Perform')
                    for x in character.feats.get_instances('Skill Focus')) and
                'bardic music' in character.features.active and
                special)

class RaptureOfTheSong(core.Feature):
    _name = 'rapture of the song'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SeekerMusic(phb.classes.BardicMusic):
    _name = 'seeker music'
    def __init__(self, character): raise NotImplementedError

class CombineSongs(core.Feature):
    _name = 'combine songs'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class Subvocalize(core.Feature):
    _name = 'subvocalize'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SeekerMusicAbility(phb.classes.BardicMusicAbility): ...

class BurningMelody(SeekerMusicAbility):
    _name = 'burning melody'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SongOfUnmaking(SeekerMusicAbility):
    _name = 'song of unmaking'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class DirgeOfFrozenLoss(SeekerMusicAbility):
    _name = 'dirge of frozen loss'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SongOfLife(SeekerMusicAbility):
    _name = 'song of life'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class AnthemOfThunderAndPain(SeekerMusicAbility):
    _name = 'anthem of thunder and pain'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class HymnOfSpelldeath(SeekerMusicAbility):
    _name = 'hymn of spelldeath'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class BalladOfAgonyReborn(SeekerMusicAbility):
    _name = 'ballad of agony reborn'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class AriaOfEverywhere(SeekerMusicAbility):
    _name = 'aria of everywhere'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError

class DirgeOfSongdeath(SeekerMusicAbility):
    _name = 'dirge of songdeath'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class NoteOfSolitude(SeekerMusicAbility):
    _name = 'note of solitude'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SeekersOfTheSong(core.Organization):
    _name = 'Seekers of the Song'
    # +4 bardic knowledge while using library
    # spellcasting at 2-5% below market price

    @staticmethod
    def prereqs(character): return any(x in character.build.active for x in ['sorcerer', 'wizard'])

#%% Sublime chord
class SublimeChord(core.PrestigeClass):
    _name = 'sublime chord'
    _hit_die = 6; skill_points = 4; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Decipher Script', 'Diplomacy', 'Knowledge',
        'Listen', 'Perform', 'Profession', 'Search', 'Speak Language', 'Spellcraft', 'Spot']
    advancement = core.get_class_advancement({
        ('Spellcasting', 'bardic knowledge', 'BardicMusic'): [1],
        'song of arcane power': [2],
        'song of timelessness': [6],
        'song of cosmic fire': [10]
        })

    def __init__(self, character): raise NotImplementedError # bardic music needs an overhaul

    @staticmethod
    def prereq(character):
        arcane = [x for x in character.features.get_instances('spellcasting') if x.magic_type=='arcane']
        return (all(character.skills[x].ranks >= 13 for x in ['Knowledge (arcana)', 'Listen']) and
                any(v.ranks >= 10 for k,v in character.skills if k.startswith('Perform')) and
                all(character.skills[x].ranks >= 6 for x in ['Profession (astrologer)', 'Spellcraft']) and
                any(any(spell.level >= 3 for spell in sc) for sc in arcane) and
                'bardic music' in character.features.active
                )

    def BardicMusic(self):
        bm = self.character.features.get_one(name='bardic music')
        bm.effective_level.add(util.LiveAttribute(self.level, lambda x: x//2), 'base', source=self)

class SublimeChordSpellcasting(core.Spellcasting):
    _name = 'spellcasting'
    _ability = 'charisma'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    # _spell list = bard + sorwiz (if both, use bard level); 4th level + ONLY
    # ignore ASF from light armor (as a bard)
    # stack caster levels (for both classes) with 1 previous arcane spellcasting class
    retrain = [4,6,8,10]
    cantrips = False # also 1st, 2nd, 3rd level spells
    _spells_known = {
        1: [3,1], 2: [4,2], 3: [4,2,1], 4: [4,3,2], 5: [4,3,2,1],
        6: [4,4,3,2], 7: [4,4,3,2,1], 8: [4,4,4,3,2], 9: [4,4,4,3,2,1], 10: [4,4,4,4,3,2]
        }
    _spells_per_day = {
        1: [2,1], 2: [2,2], 3: [3,2,1], 4: [3,3,2], 5: [3,3,2,1],
        6: [4,3,3,2], 7: [4,4,3,2,1], 8: [4,4,3,3,2], 9: [4,4,4,3,2,1], 10: [5,4,4,3,3,2]
        }

class SongOfArcanePower(phb.classes.BardicMusicAbility):
    _name = 'song of arcane power'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SongOfTimelessness(phb.classes.BardicMusicAbility):
    _name = 'song of timelessness'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class SongOfCosmicFire(phb.classes.BardicMusicAbility):
    _name = 'song of cosmic fire'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Suel archanamach
class SuelArchanamach(core.PrestigeClass):
    _name = 'Suel archanamach'
    _hit_die = 8; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Bluff', 'Climb', 'Concentration', 'Craft', 'Disguise', 'Escape Artist',
                     'Hide', 'Jump', 'Knowledge (arcana)', 'Knowledge (history)',
                     'Knowledge (the planes)', 'Listen', 'Move Silently', 'Profession', 'Search',
                     'Spellcraft', 'Spot', 'Swim', 'Tumble', 'Use Rope']
    advancement = core.get_class_advancement({
        ('Spellcasting', 'tenacious spells'): [1],
        'ignore spell failure chance': list(range(1,11,3)),
        'dispelling strike': [2,6,10],
        'extended spellstrength': [3],
        })
    @staticmethod
    def prereq(character, special=False):
        '''Special: Must read the Grimoire Arcanamacha (requiring 1 week of uninterrupted study) or study with an instructor who has done so for four weeks.'''
        return (character.BAB >= 6 and
                all(character.skills[x].ranks >= 4 for x in ['Concentration', 'Jump', 'Tumble']) and
                character.skills['Spellcraft'].ranks >= 5 and
                all(x in character.feats.active for x in ['Combat Casting', 'Iron Will']) and
                any(x in character.skills.languages
                    for x in ['Ancient Suloise', 'Loross', 'Roushoum', 'Thorass', 'Mulhorandi']) and
                #('martial' in character.proficiencies or ##) proficient in >=4 martial or exotic weapons
                special
                )

class SuelArcanamachSpellcasting(core.Spellcasting):
    _name = 'spellcasting'
    _ability = 'charisma'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    # _spell list = sorwiz Abj, Div, Ill, Tra ONLY
    retrain = [4,6,8,10]
    cantrips = False
    _spells_known = {
        1: [1], 2: [2,1], 3: [2,2], 4: [2,2,1], 5: [3,2,2],
        6: [3,3,2,1], 7: [3,3,2,2], 8: [4,3,3,2,1], 9: [4,4,3,2,2], 10: [4,4,3,3,2]
        }
    _spells_per_day = {
        1: [1], 2: [1,0], 3: [2,1], 4: [2,2,0], 5: [3,2,1],
        6: [3,3,2,0], 7: [3,3,2,1], 8: [4,3,3,2,0], 9: [4,4,3,2,1], 10: [4,4,3,3,2]
        }

class IgnoreSpellFailureChance(core.Feature):
    _name = 'ignore spell failure chance'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(5)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 5

class TenaciousSpells(core.Feature):
    _name = 'tenacious spells'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class DispellingStrike(core.Feature):
    _name = 'dispelling strike'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

class ExtendedSpellstrength(core.Feature):
    _name = 'extended spellstrength'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Wayfarer guide
class WayfarerGuide(core.PrestigeClass):
    _name = 'wayfarer guide'
    _hit_die = 6; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Knowledge', 'Profession', 'Speak Language', 'Spellcraft']
    advancement = {
        1: ['CasterLevel', 'enhanced capacity', 'improved range'],
        2: ['extra teleportation'],
        3: ['enhanced accuracy']
        }
    @staticmethod
    def prereq(character, special=False):
        '''Special: a prospective wayfarer's guide must join the Wayfarers Union (though they can later quit).'''
        return (all(character.skills[x].ranks >= 10 for x in ['Knowledge (arcana)', 'Knowledge (geography)']) and
                'teleport' in character.magic.spells_known and
                special)

class EnhancedCapacity(core.Feature):
    _name = 'enhanced capacity'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ImprovedRange(core.Feature):
    _name = 'improved range'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ExtraTeleportation(core.Feature):
    _name = 'extra teleportation'
    def __init__(self, character): raise NotImplementedError

class EnhancedAccuracy(core.Feature):
    _name = 'enhanced accuracy'
    def __init__(self, character): raise NotImplementedError

class WayfarersUnion(core.Organization):
    _name = 'The Wayfarers Union'
    # initiation fee 200 gp
    # 20% of union-related income (remitted quarterly)
    # active members serve 2 mo/yr on Travel Board for local chapter

    @staticmethod
    def prereqs(character): return 'teleport' in character.magic.spells_known
    # by any means

#%% Wild mage
class WildMage(core.PrestigeClass):
    _name = 'wild mage'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Reflex']
    _class_skills = ['Bluff', 'Concentration', 'Craft', 'Intimidate', 'Knowledge', 'Profession',
                     'Spellcraft', 'Use Magic Device']
    advancement = core.get_class_advancement({
        'ArcaneCasterLevel': list(range(1,11)),
        'wild magic': [1],
        'random deflector': list(range(2,11,3)),
        'student of chaos': [3],
        'chaotic mind': [6],
        'reckless dweomer': [9],
        'wildstrike': [10]
        })
    @staticmethod
    def prereq(character):
        return (character.alignment=='chaotic' and
                all(character.skills[x].ranks >= 4 for x in ['Knowledge (the planes)', 'Use Magic Device']) and
                character.skills['Spellcraft'].ranks >= 8 and
                'Magical Aptitude' in character.feats.active and
                character.feats.metamagic_feats >= 1 and
                any(sc.magic_type=='arcane' and sc.caster_level >= 1
                    for sc in character.features.get_instances('spellcasting'))
                )

class WildMagic(core.Feature):
    _name = 'wild magic'
    def __init__(self, character): raise NotImplementedError

class RandomDeflector(core.Feature):
    _name = 'random deflector'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.frequency = util.Frequency(1,1,'day')
        raise NotImplementedError

    def escalate(self): self.frequency.attribute += 1

class StudentOfChaos(core.Feature):
    _name = 'student of chaos'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ChaoticMind(core.Feature):
    _name = 'chaotic mind'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.character.resistances.immunities.add(name=['confusion', 'insanity'], source=self)
        raise NotImplementedError

class RecklessDweomer(core.Feature):
    _name = 'reckless dweomer'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class Wildstrike(core.Feature):
    _name = 'wildstrike'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError
