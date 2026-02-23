#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 21:55:05 2025
@author: gtauxe
"""

import reactivex as rx
import reactivex.operators as ops
from reactivex.subject import BehaviorSubject

import core, phb, mm
from dmg.classes import AlternateClassFeature
import splat.frostburn as fb
import utilities as util
sourcebook = "Player's Handbook II"

#%% Beguiler
class Beguiler(core.Class):
    _name = 'beguiler'
    _hit_die = 6; skill_points = 6; bab_type = 'half'; good_saves = ['Will']
    # starting gold 6d4+10gp
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Concentration', 'Decipher Script',
        'Diplomacy', 'Disable Device', 'Escape Artist', 'Forgery', 'Gather Information', 'Hide',
        'Jump', 'Knowledge (arcana)', 'Knowledge (local)', 'Listen', 'Move Silently', 'Open Lock',
        'Profession', 'Search', 'Sense Motive', 'Sleight of Hand', 'Speak Language', 'Spellcraft',
        'Spot', 'Swim', 'Tumble', 'Use Magic Device']
    proficiencies = ['simple', 'hand crossbow', 'rapier', 'shortbow', 'short sword', 'light']
    advancement = core.get_class_advancement({
        ('Spellcasting', 'armored mage', 'trapfinding'): [1],
        'cloaked casting': [2,8,14,20],
        'surprise casting': [2,6],
        'advanced learning': [3,7,11,15,19],
        'SilentSpell': [5],
        'StillSpell': [10]
        })
    def SilentSpell(self): self.character.feats.add(name='Silent Spell', source=self, override=True)
    def StillSpell(self): self.character.feats.add(name='Still Spell', source=self, override=True)

class BeguilerSpellcasting(core.Spellcasting):
    _ability = 'intelligence'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    clss = 'beguiler'
    _spell_list = {
        0: ['dancing lights', 'daze', 'detect magic', 'ghost sound', 'message', 'open/close',
            'read magic'],
        1: ['charm person', 'color spray', 'comprehend languages', 'detect secret doors',
            'disguise self', 'expeditious retreat', 'hypnotism', 'mage armor', 'obscuring mist',
            'silent image', 'sleep', 'undetectable alignment'],
        2: ['blur', 'daze monster', 'detect thoughts', 'fog cloud', 'glitterdust',
            'hypnotic pattern', 'invisibility', 'knock', 'minor image', 'mirror image',
            'misdirection', 'see invisibility', 'silence', 'spider climb', 'touch of idiocy'],
        3: ['arcane sight', 'clairaudience/clairvoyance', 'deep slumber', 'dispel magic',
            'displacement', 'glibness', 'haste', 'hold person', 'invisibility sphere',
            'major image', 'nondetection', 'slow', 'suggestion', 'zone of silence'],
        4: ['charm monster', 'confusion', 'crushing despair', 'freedom of movement',
            'greater invisibility', 'locate creature', 'rainbow pattern', 'solid fog'],
        5: ['break enchantment', 'dominate person', 'feeblemind', 'hold monster', 'mind fog',
            "Rary's telepathic bond", 'seeming', 'sending'],
        6: ['greater dispel magic', 'mass suggestion', 'mislead', 'repulsion', 'shadow walk',
            'trueseeing', 'veil'],
        7: ['ethereal jaunt', 'greater arcane sight', 'mass hold person', 'mass invisibility',
            'phase door', 'power word blind', 'project image', 'spell turning'],
        8: ['demand', 'discern location', 'mind blank', 'moment of prescience', 'power word stun',
            'scintillating pattern', 'screen'],
        9: ['dominate monster', 'etherealness', 'foresight', 'mass hold monster', 'power word kill',
            'time stop']
        }
    _spells_known = _spell_list
    _spells_per_day = dict(phb.classes.SorcererSpellcasting._spells_per_day)
    _spells_per_day[20] = [6,6,6,6,6,6,6,6,6,5]

class CloakedCasting(core.Feature):
    _name = 'cloaked casting'
    _tags = ['extraordinary']
    def escalate(self): raise NotImplementedError

class SurpriseCasting(core.Feature):
    _name = 'surprise casting'
    _tags = ['extraordinary']
    def escalate(self): raise NotImplementedError

#%% Dragon shaman
class DragonShaman(core.Class):
    _name = 'dragon shaman'
    _hit_die = 10; skill_points = 2; bab_type = 'three quarters'; good_saves = ['Fortitude', 'Will']
    _class_skills = ['Climb', 'Craft', 'Intimidate', 'Knowledge (arcana)', 'Knowledge (nature)',
                     'Search']
    proficiencies = ['simple', 'light', 'medium', 'shield']; bonus_languages = ['Draconic']
    advancement = core.get_class_advancement({ # starting gold 4d4x10
        'TotemDragon': [1],
        'draconic aura': [1,5,10,15,20],
        'SkillFocus': [2,8,16],
        'draconic adaptation': [3,13],
        'BreathWeapon': list(range(4,21,2)),
        'draconic resolve': [4],
        'touch of vitality': [6,11],
        'natural armor': [7,12,17],
        'energy immunity': [9],
        'CommuneWithDragonSpirit': [14],
        'draconic wings': [19]
        })
    def __init__(self, character):
        super().__init__(character)
        self.totem_ = BehaviorSubject(None)
        self.breath_weapon = None

    @property
    def totem(self): return self.totem_.value

    @totem.setter
    def totem(self, value): self.character.features.get_one(name='totem dragon').set_totem(value)

    def add_feature(self, feature):
        self.character.features.add(item=feature, source=self, condition=self.code_of_conduct_)

    def TotemDragon(self): super().add_feature('totem dragon')

    def SkillFocus(self):
        sf = phb.feats.SkillFocus(self.character)
        dt = self.character.features.get_one(name='dragon totem')
        match_ = rx.combine_latest(sf.skill_, dt.skills_).pipe(
            ops.map(lambda p: p[0] in p[1]), ops.distinct_until_changed())
        sfs_ = self.character.feats.active_.pipe(
            ops.map(lambda p: [x for x in p if util.is_a(x, 'Skill Focus')]),
            ops.distinct_until_changed())
        sfs_all_ = rx.combine_latest(dt.skills_, sfs_,).pipe(
            ops.map(lambda p: all(any(ft.skill==skill for ft in p[1]) for skill in dt.skills_)),
            ops.distinct_until_changed()
            )
        congruent_ = rx.combine_latest(match_, sfs_all_).pipe(
            ops.map(any), ops.distinct_until_changed())
        self.character.feats.add(obj=sf, override=True, condition=congruent_, source=self)

    def BreathWeapon(self):
        if self.breath_weapon is None:
            self.breath_weapon = self.character.features.add(obj=_BreathWeapon(self.character, self.totem_),
                                                     condition=self.code_of_conduct_, source=self)

        else:
            self.breath_weapon.escalate()

    def CommuneWithDragonSpirit(self):
        self.character.magic.spell_like_abilities.add(name='commune with dragon spirit',
            obj=phb.spells.Commune(), caster_level=util.LiveAttribute(self.level, lambda x: x//3),
            frequency=util.Frequency(1,7,'days'), condition=self.code_of_conduct_, source=self)

    def live_prereq(self):
        rx.combine_latest(self.totem_, self.character.alignment.attribute_).pipe(
            ops.map(lambda p: core.Alignment(p[0].alignment).distance(core.Alignment(p[1])) <= 1),
            ops.distinct_until_changed()
            ).subscribe(self.code_of_conduct_.on_next, util.log_error)

    @staticmethod
    def prereq(character): return character.alignment!='true neutral'

class TotemDragon(core.Feature):
    _name = 'totem dragon'
    eligible = {'black': 'line of acid', 'blue': 'line of electricity', 'green': 'cone of acid',
                'red': 'cone of fire', 'white': 'cone of cold', 'brass': 'line of fire',
                'bronze': 'line of electricity', 'copper': 'line of acid', 'gold': 'cone of fire',
                'silver': 'cone of cold'}
    def __init__(self, character):
        super().__init__(character)
        self.totem_ = self.character.build.get_one(name='dragon shaman').totem_
        self.skills_ = BehaviorSubject([])
        self.breath_weapon_ = BehaviorSubject(None)

        def check_totem():
            if self.totem is None:
                util.logger.warning('You must set a dragon type for your dragon shaman class.')
        self.character.add_to_build(-2, 1, check_totem)

        def set_skills(dragon):
            if dragon is None: self.skills_.on_next([]); return
            true_skills = self.character.lib['Race']['true dragon']._class_skills
            bonus_skills = [x for x in dragon._class_skills if x not in true_skills]
            ds = self.character.build.get_one(name='dragon shaman')
            ds.class_skills = [x for x in ds.class_skills if x not in self.skills]
            ds.extend(bonus_skills)
            self.skills_.on_next(bonus_skills)
        self.totem_.subscribe(set_skills)

        def set_breath_weapon(dragon):
            if dragon is None: self.breath_weapon_.on_next(None); return
            dragon_type = dragon._name.split()[0]
            self.breath_weapon_.on_next(self.eligible[dragon_type])
        self.totem_.subscribe(set_breath_weapon)

    @property
    def breath_weapon(self): return self.breath_weapon_.value

    @property
    def skills(self): return self.skills_.value

    @property
    def totem(self): return self.totem_.value

    @totem.setter
    def totem(self, value): self.set_totem(value)

    def set_totem(self, value):
        value = value.split()[0].lower()
        if value not in self.eligible: raise util.NotEligible(value)
        if self.totem:
            util.logger.warning('Warning! Overwriting an existing dragon totem: %s', value)
        dragon = self.character.lib['Race'].get(value + ' dragon')
        if dragon.alignment.distance(self.character.alignment) > 1: raise util.NotEligible(value)
        self.totem_.on_next(dragon)

class DraconicAura(core.Feature):
    _name = 'draconic aura'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

class DraconicAdaptation(core.Feature):
    _name = 'draconic adaptation'
    def __init__(self, character):
        super().__init__(character)
        totem_ = self.character.features.get_one(name='dragon totem', status='active').totem_
        cl = sum(x.level for x in self.sources)

        wb_ = totem_.pipe(
            ops.map(lambda x: any(util.is_a(x, variety)
                for variety in [var+' dragon' for var in ['black', 'bronze', 'gold', 'green']])),
            ops.distinct_until_changed())
        wb = self.character.features.add(obj=_WaterBreathing(self.character), condition=wb_, source=self)

        vq_ = totem_.pipe(ops.map(lambda x: util.is_a(x, 'blue dragon')), ops.distinct_until_changed())
        vq = self.character.magic.spell_like_abilities.add(name='ventriloquism', caster_level=cl,
                                                           frequency='at will', condition=vq_, source=self)

        ee_ = totem_.pipe(ops.map(lambda x: util.is_a(x, 'brass dragon')), ops.distinct_until_changed())
        ee = self.character.magic.spell_like_abilities.add(name='endure elements', caster_level=cl,
                                                           frequency='at will', condition=ee_, source=self)
        #TODO ee is self only

        sc_ = totem_.pipe(ops.map(lambda x: util.is_a(x, 'copper dragon')), ops.distinct_until_changed())
        sc = self.character.magic.spell_like_abilities.add(name='spider climb', caster_level=cl,
                                                           frequency='at will', condition=sc_, source=self)
        #TODO sc is self only

        ts_ = totem_.pipe(ops.map(lambda x: util.is_a(x, 'red dragon')), ops.distinct_until_changed())
        ts = self.character.features.add(name='treasure seeker', condition=ts_, source=self)

        ff_ = totem_.pipe(ops.map(lambda x: util.is_a(x, 'silver dragon')), ops.distinct_until_changed())
        ff = self.character.magic.spell_like_abilities.add(name='feather fall', caster_level=cl,
                                                           frequency='at will', condition=ff_, source=self)
        #TODO ff is self only

        iw_ = totem_.pipe(ops.map(lambda x: util.is_a(x, 'white dragon')), ops.distinct_until_changed())
        iw = self.character.features.add(name='icewalker', condition=iw_, source=self)

        self.features = [wb, vq, ee, sc, ts, ff, iw]

    def escalate(self): raise NotImplementedError

class _WaterBreathing(core.Feature):
    _name = 'water breathing'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class TreasureSeeker(core.Feature):
    _name = 'treasure seeker'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        for x in ['Appraise', 'Search']:
            self.character.skills[x].add(5, 'competence', source=self)

class Icewalker(core.Feature):
    _name = 'icewalker'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError

class _BreathWeapon(mm.features.BreathWeapon):
    def __init__(self, character, totem_):
        super().__init__(character)
        self.totem_ = totem_
        self.grade = util.NumeralAttribute(2)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

class DraconicResolve(core.Feature):
    _name = 'draconic resolve'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.resistances.immunities.add(name=['paralysis', 'sleep', 'frightful presence'],
                                                  source=self)

class TouchOfVitality(core.Feature):
    _name = 'touch of vitality'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError
    def escalate(self): raise NotImplementedError

class NaturalArmor(core.Feature):
    _name = 'natural armor'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
        self.character.AC.natural_armor.add(self.grade, source=self)

    def escalate(self): self.grade.attribute += 1

class EnergyImmunity(core.Feature):
    _name = 'energy immunity'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.energy_ = BehaviorSubject(None)

        def set_immunity(energy_type):
            congruent_ = self.energy_.pipe(ops.map(lambda x: x==energy_type), ops.distinct_until_changed())
            self.character.resistances.immunities.add(energy_type, condition=congruent_, source=self)

        totem_energy = self.character.features.get_one(name='totem dragon').breath_weapon_.pipe(
            ops.filter(lambda x: x is not None),
            ops.map(lambda x: x.split()[-1]),
            ops.distinct_until_changed()
            )
        totem_energy.subscribe(self.energy_.on_next, util.log_error)
        totem_energy.subscribe(set_immunity, util.log_error)

class DraconicWings(core.Feature):
    _name = 'draconic wings'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.build.add(name='winged', source=self)

        weight_map = {'none':60, 'light':60, 'medium':40, 'heavy':0}
        speed = util.NumeralAttribute(60)
        self.character.equipment.weight_encumbrance_.pipe(
            ops.map(lambda x: weight_map[x]), ops.distinct_until_changed()
            ).subscribe(speed.value_.on_next, util.log_error)

        self.character.speed['fly'].add(speed, 'base', source=self)
        self.character.speed['maneuverability'].add('good', 'base', source=self)
    #TODO manage ability to choose which set of wings to use when option presents

#%% Duskblade
class Duskblade(core.Class):
    _name = 'duskblade'
    _hit_die = 8; skill_points = 2; bab_type = 'full'; good_saves = ['Fortitude', 'Will']
    _class_skills = ['Climb', 'Concentration', 'Craft', 'Decipher Script', 'Jump', 'Knowledge',
                     'Ride', 'Sense Motive', 'Spellcraft', 'Swim']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield']
    advancement = core.get_class_advancement({
        ('Spellcasting', 'arcane attunement'): [1],
        'armored mage': [1,4,7],
        'CombatCasting': [2],
        'arcane channeling': [3,13],
        'quick cast': [5,10,15,20],
        'spell power': [6,11,16,18]
        })

    def CombatCasting(self): self.character.feats.add(name='Combat casting', source=self, override=True)

class DuskbladeSpellcasting(core.Spellcasting):
    _ability = 'intelligence'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    clss = 'duskblade'
    retrain = list(range(5,21,2))
    _spell_list = {
        0: ['acid splash', 'disrupt undead', 'ray of frost', 'touch of fatigue'],
        1: ['burning hands', 'cause fear', 'chill touch', 'color spray', 'jump', 'magic wWeapon',
            'obscuring mist', 'ray of enfeeblement', 'resist energy', 'shocking grasp',
            'swift expeditious retreat', 'true strike'],
        2: ["bear's endurance", "bull's strength", "cat's grace", 'darkvision', 'ghoul touch',
            "Melf's acid arrow", 'scorching ray', 'see invisibility', 'spider climb', 'swift fly',
            'swift invisibility', 'touch of idiocy'],
        3: ['greater magic weapon', 'keen edge', 'protection from energy', 'ray of exhaustion',
            'vampiric touch'],
        4: ["Bigby's interposing hand", 'dimension door', 'dispel magic', 'enervate', 'fire shield',
            'phantasmal killer', 'shout'],
        5: ["Bigby's clenched fist", 'chain lLightning', 'disintegrate', 'hold monster',
            'polar ray', 'waves of fatigue']
        }
    _spells_known = {1: [2,2]}  # + 1 0th-lvl for each point of INT bonus; learn one more at each level
    _spells_per_day = {
        1: [3,2], 2: [4,3], 3: [5,4], 4: [6,5], 5: [6,5,2], 6: [6,6,3], 7: [6,6,5], 8: [6,7,6],
        9: [6,7,6,2], 10: [6,8,7,3], 11: [6,8,7,5], 12: [6,8,8,6], 13: [6,9,8,6,2], 14: [6,9,8,7,3],
        15: [6,9,8,7,5], 16: [6,9,9,8,6], 17: [6,10,9,8,6,2], 18: [6,10,9,8,7,3],
        19: [6,10,10,9,7,5], 20: [6,10,10,10,8,6],
        }

class ArcaneAttunement(core.Feature):
    _name = 'arcane attunement'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.frequency = util.Frequency(3)
        self.frequency.add(self.character.INT, 'INT')
        self.character.magic.spell_like_abilities.add(source=self, frequency=self.frequency,
            name=['dancing lights', 'detect magic', 'flare', 'ghost sound', 'read magic'],
            caster_level=self.character.build.level)

class ArcaneChanneling(core.Feature):
    _name = 'arcane channeling'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError
    def escalate(self): raise NotImplementedError

class QuickCast(core.Feature):
    _name = 'quick cast'
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.Frequency(1,1,'day')
        raise NotImplementedError

    def escalate(self): self.grade.add(1, 'base')

class SpellPower(core.Feature):
    _name = 'spell power'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(2)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

#%% Knight
class Knight(core.Class):
    _name = 'knight'
    _hit_die = 12; skill_points = 2; bab_type = 'full'; good_saves = ['Will']
    _class_skills = ['Climb', 'Handle Animal', 'Intimidate', 'Jump',
                     'Knowledge (nobility and royalty)', 'Ride', 'Swim']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield']
    advancement = core.get_class_advancement({
        ('KnightsChallenge', "knight's code"): [1], # see also bardic music
        'fighting challenge': list(range(1,21,6)),
        'MountedCombat': [2],
        'shield block': [2,11,20],
        'bulwark of defense': [3],
        'armor mastery': [4,9],
        'test of mettle': [4],
        'BonusFeat': [5,10,15],
        'vigilant defender': [5],
        'shield ally': [6],
        'call to battle': [8],
        'daunting challenge': [12],
        'improved shield ally': [14],
        'bond of loyalty': [16],
        'impetuous endurance': [17],
        'loyal beyond death': [20]
        })
    feats = ['Animal Affinity', 'Diehard', 'Endurance', 'Great Fortitude', 'Iron Will',
             'Quick Draw', 'Ride-By Attack', 'Spirited Charge', 'Trample', 'Weapon Focus (lance)']
    def KnightsChallenge(self):
        kc = self.add_feature("knight's challenge")
        kc.add_condition(self.code_of_conduct_)

    def MountedCombat(self):
        self.character.feats.add(name='Mounted Combat', override=True, source=self)

    def live_prereq(self):
        self.character.alignment.attribute_.pipe(
            ops.map(lambda x: 'lawful' in x), ops.distinct_until_changed()
            ).subscribe(self.code_of_conduct_.on_next, util.log_error)

class KnightsChallenge(core.Feature):
    _name = "knight's challenge"
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute()
        self.frequency = util.Frequency()
        self.frequency.add(util.LiveAttribute(self.effective_level, lambda x: x//2), 'base')
        self.frequency.add(util.LiveAttribute(self.character.CHA, lambda x: max(x, 0)), 'CHA')
        self.frequency.minimum = 1

    def add_source(self, source):
        super().add_source(source)
        if hasattr(source, 'level'):
            self.effective_level.add(source.level, 'base')

class KnightsChallengeAbility(core.Feature): ...

class FightingChallenge(KnightsChallengeAbility):
    _name = 'fighting challenge'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

class TestOfMettle(KnightsChallengeAbility):
    _name = 'test of mettle'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class CallToBattle(KnightsChallengeAbility):
    _name = 'call to battle'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class DauntingChallenge(KnightsChallengeAbility):
    _name = 'daunting challenge'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class BondOfLoyalty(KnightsChallengeAbility):
    _name = 'bond of loyalty'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class LoyalBeyondDeath(KnightsChallengeAbility):
    _name = 'loyal beyond death'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class KnightsCode(core.Feature):
    _name = "knight's code"
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError

class ShieldBlock(core.Feature):
    _name = 'shield block'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
        raise NotImplementedError

    def escalate(self): self.grade.attribute += 1

class BulwarkOfDefense(core.Feature):
    _name = 'bulwark of defense'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ArmorMastery(core.Feature):
    _name = 'armor mastery'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class VigilantDefender(core.Feature):
    _name = 'vigilant defender'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ShieldAlly(core.Feature):
    _name = 'shield ally'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ImprovedShieldAlly(core.Feature):
    _name = 'improved shield ally'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ImpetuousEndurance(core.Feature):
    _name = 'impetuous endurance'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Barbarian
class BerserkerStrength(AlternateClassFeature, phb.classes.Rage):
    _name = 'berserker strength'
    replaces = {1: 'rage'}
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.NumeralAttribute(0)
        threshold_ = rx.combine_latest(self.character.HP.HP.attribute_, self.effective_level.attribute_).pipe(
            ops.map(lambda p: p[0] < (p[1] * 5)), ops.distinct_until_changed())

        self.character.abilities['strength'].add(4, condition=threshold_, source=self)
        self.character.saves['all'].add(2, condition=threshold_, source=self)
        self.character.resistances.damage_resistance['slash'].add(2, 'base', condition=threshold_, source=self)
        self.character.AC['all'].add(-2, condition=threshold_, source=self)

        #TODO add same behavior restrictions as rage

    def add_source(self, source):
        super().add_source(source)
        if hasattr(source, 'level'):
            self.effective_level.add(source.level, 'base')

#%% Bard
class BardicKnack(AlternateClassFeature, core.Feature):
    _name = 'bardic knack'
    def __init__(self, character): raise NotImplementedError

#%% Cleric
class SpontaneousDomainCasting(AlternateClassFeature, core.Feature):
    _name = 'spontaneous domain casting'
    def __init__(self, character): raise NotImplementedError

#%% Druid
class SpontaneousRejuvenation(AlternateClassFeature, core.Feature):
    _name = 'spontaneous rejuvenation'
    def __init__(self, character): raise NotImplementedError

class Shapeshift(AlternateClassFeature, core.Feature):
    _name = 'shapeshift'
    def __init__(self, character): raise NotImplementedError

##%% Animal companions
class Brixashulty:
    def companion(self):
        comp = 0 if 'halfling' in self.primary.build.active else -3
        ac = self.character.primary.features.get_one(name='animal companion')
        self.character.effective_level.add(comp, source=self)
        return ac.effective_level >= 1 - comp
class Caribou(fb.Caribou):
    advancement = dict(fb.Caribou.advancement); advancement['companion'] = 0

class Chordevoc:
    def companion(self):
        comp = 0 if 'halfling' in self.primary.build.active else -3
        ac = self.character.primary.features.get_one(name='animal companion')
        self.character.effective_level.add(comp, source=self)
        return ac.effective_level >= 1 - comp
class Climbdog: advancement = {'companion':0}
class Jackal: advancement = {'companion':0}
class Serval: advancement = {'companion':0}
class Swindlespitter: advancement = {'companion':0}
class Vulture: advancement = {'companion':0}
class Axebeak: advancement = {'companion':-3}
class Fleshraker: advancement = {'companion':-3}
class DireHawk:
    def companion(self):
        comp = -3 if 'raptor' in self.primary.build.active else -6
        ac = self.character.primary.features.get_one(name='animal companion')
        self.character.effective_level.add(comp, source=self)
        return ac.effective_level >= 1 - comp
class DireJackal: advancement = {'companion':-3}
class DireToad: advancement = {'companion':-3}
class CaveAnkylosaurus: advancement = {'companion':-6}
class DireEagle: advancement = {'companion':-6}
class Megaloceros: advancement = {'companion':-6}
class Protoceratops: advancement = {'companion':-6}
class TerrorBird: advancement = {'companion':-6}
class Allosaurus: advancement = {'companion':-9}
class Bloodstriker: advancement = {'companion':-9}
class Glyptodon: advancement = {'companion':-9}
class Hippopotamus: advancement = {'companion':-9}
class DireHorse: advancement = {'companion':-9}
class DirePuma: advancement = {'companion':-9}
class DireSnake: advancement = {'companion':-9}
class SaberToothedTiger: advancement = {'companion':-9}
class DireTortoise: advancement = {'companion':-9}
class CaveTriceratops: advancement = {'companion':-9}
class CaveTyrannosaurus: advancement = {'companion':-9}
class DireVulture: advancement = {'companion':-9}
class Ankylosaurus: advancement = {'companion':-12}
class Diprotodon: advancement = {'companion':-12}
class DireElk: advancement = {'companion':-12}
class Fhorge: advancement = {'companion':-12}
class GiantBandedLizard: advancement = {'companion':-12}
class DirePolarBear: advancement = {'companion':-15}
class DireElephant: advancement = {'companion':-15}
class DireHippopotamus: advancement = {'companion':-15}
class Indricothere: advancement = {'companion':-15}
class WoollyMammoth: advancement = {'companion':-15}
class Mastodon: advancement = {'companion':-15}
class GrizzlyMastodon: advancement = {'companion':-15}
class Megatherium: advancement = {'companion':-15}
class Quetzalcoatlus: advancement = {'companion':-15}
class DireRhinoceros: advancement = {'companion':-15}

#%% Favored soul
# errata on starting package 2: The Healer; replace Spontaneous Healer w/ Augment Healing
# NPC feat progression: ['Combat Casting', 'Brew Potion', 'Spontaneous Healing'] (reordered)
class DeitysFavor(AlternateClassFeature, core.Feature):
    _name = "deity's favor"
    def __init__(self, character): raise NotImplementedError

#%% Fighter
class ElusiveAttack(AlternateClassFeature, core.Feature):
    _name = 'elusive attack'
    def __init__(self, character): raise NotImplementedError

class Counterattack(AlternateClassFeature, core.Feature):
    _name = 'counterattack'
    def __init__(self, character): raise NotImplementedError

class OverpoweringAttack(AlternateClassFeature, core.Feature):
    _name = 'overpowering attack'
    def __init__(self, character): raise NotImplementedError

#%% Hexblade
class DarkCompanion(AlternateClassFeature, core.Feature):
    _name = 'dark companion'
    def __init__(self, character): raise NotImplementedError

#%% Marshal
class AdrenalineBoost(AlternateClassFeature, core.Feature):
    _name = 'adrenaline boost'
    def __init__(self, character): raise NotImplementedError

#%% Monk
# errata starting package:
    # feats: ['Improved Grapple, "Improved Unarmed Strike', 'Power Attack']
# destroyer build feat tree: [Power Attack', 'Improved Bull Rush', 'Improved Natural Attack']

class DecisiveStrike(AlternateClassFeature, core.Feature):
    _name = 'decisive strike'
    def __init__(self, character): raise NotImplementedError

#%% Paladin
class ChargingSmite(AlternateClassFeature, core.Feature):
    _name = 'charging smite'
    def __init__(self, character): raise NotImplementedError

#%% Ranger
class DistractingAttack(AlternateClassFeature, core.Feature):
    _name = 'distracting attack'
    def __init__(self, character): raise NotImplementedError

#%% Rogue
class DisruptiveAttack(AlternateClassFeature, core.Feature):
    '''Beginning at 4th level, through careful study you're able to find exploitable flaws in any
creature's tactics and defenses. Whenever you hit a target that is flat-footed against your attack,
or whenever you hit a target that you flank, you can choose to sacrifice your sneak attack damage in
order to apply a -5 penalty to that creature's AC for 1 round. Multiple hits on the same target
don't stack. This extraordinary ability works even against creatures normally immune to extra damage
from sneak attacks, such as undead.'''
    _name = 'disruptive attack'
    replaces = {4: 'uncanny dodge'}
    level = 4
    def __init__(self, character):
        super().__init__(character)
        c_ = self.character.challenges.register(action='flanking', target='flat-footed')
        self.character.actions.attack.add(name=self.name, condition=c_[0], source=self)
        self.character.actions.attack.add(name=self.name, condition=c_[1], source=self)

        self.character.attacks.damage['all']._notes.add(name=self.name, condition=c_[0], source=self)
        self.character.attacks.damage['all']._notes.add(name=self.name, condition=c_[1], source=self)

#%% Scout
# errata starting package: no Open Lock or Disable Device

class DungeonSpecialist(AlternateClassFeature, core.Feature):
    _name = 'dungeon specialist'
    def __init__(self, character): raise NotImplementedError

#%% Sorcerer
# errata starting package: too many spells. Remove rayof enveeblement, read magic from package 1,
# obscuring mist, disrupt undead from package 2; grease, acid splash from package 3.

class MetamagicSpecialist(AlternateClassFeature, core.Feature):
    _name = 'metamagic specialist'
    def __init__(self, character): raise NotImplementedError

#%% Swashbuckler
class ShieldOfBlades(AlternateClassFeature, core.Feature):
    _name = 'shield of blades'
    def __init__(self, character): raise NotImplementedError

#%% Warlock
# errata: 'Blaster' build: substitute Combat Coasting for 2nd Point Blank Shot.

class FiendishFlamewreath(AlternateClassFeature, core.Feature):
    _name = 'fiendish flamewreath'
    def __init__(self, character): raise NotImplementedError

#%% Warmage
class EclecticLearning(AlternateClassFeature, core.Feature):
    _name = 'eclectic learning'
    def __init__(self, character): raise NotImplementedError

#%% Wizard
class ImmediateMagic(AlternateClassFeature, core.Feature):
    '''You gain a supernatural ability that reflects your chosen school of magic. Activating this ability is
an immediate action, and you can use this ability a number of times per day equal to your
Intelligence bonus (minimum 1). Its equivalent spell level is equal to one-half your wizard level
(minimum 1st) and the caster level is your wizard level. The save DC (if any) is equal to 10 + 1/2
your wizard level + your Int modifier.

You can't activate this ability in response to an attack that you aren't aware of. For instance, if
an invisible rogue strikes at you, you can't activate urgent shield to gain a bonus to your AC
against the attack. All effects last until the start of your next turn unless otherwise noted.

To select this ability, you must also choose to specialize in a school of magic. The spell-like
ability gained depends on your specialty.'''
    _name = 'immediate magic'
    replaces = {1: 'summon familiar'}
    level = 1
    def __init__(self, character):
        super().__init__(character)
        match self.character.build.get_one(name='wizard').specialty:
            case 'evocation':
                ability = 'Counterfire'
            case _:
                raise NotImplementedError

        self.sla = self.character.features.add_if_missing(item='SpellLikeAbilities', source=self)

        int_min_1 = util.NumeralAttribute()
        self.character.INT.attribute_.subscribe(int_min_1.value_.on_next, util.log_error)
        int_min_1.minimum = 1
        frequency = util.Frequency(int_min_1, 1, 'day')

        caster_level = self.classes.get_one(name='wizard').level

        #TODO spell_level equivalent = 1/2 wizard level minimum 1

        save_dc = util.Attribute(10)
        save_dc.add(self.character.INT, 'INT')
        save_dc.add(util.LiveAttribute(caster_level, lambda x: x//2), 'base', source='wizard')

        abil = self.sla.add(item=ability, caster_level=caster_level, frequency=frequency, source=self)
        abil.save_dc = save_dc
        abil.casting_time = 'immediate'

    def prereq(self): self.character.build.get_one(name='wizard').specialty is not None

class Counterfire(core.Feature):
    '''When a visible enemy within 60 feet targets you with à ranged attack or spell, you can respond with
a glowing arrow of force. This requires a ranged touch attack to hit and deals idé points of damage
per three wizard levels. Both attacks resolve simultaneously (neither can disrupt the other).'''
    _name = 'counterfire'; _tags = ['supernatural']
    def __init__(self, caster_level, **kwargs):
        super().__init__(caster_level)
        util.logger.warning('Counterfire is not enabled yet.')
