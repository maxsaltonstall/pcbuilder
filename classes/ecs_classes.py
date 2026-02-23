#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 23:27:04 2025
@author: gtauxe
"""
import reactivex as rx
import reactivex.operators as ops

import core, phb, mm
from dmg.classes import AlternateClassFeature
import splat.eberron_campaign_setting.races as races
import splat.eberron_campaign_setting.dragonmarks as marks
import utilities as util

#%% Artificer
class Artificer(core.Class):
    _name = 'artificer'
    _hit_die = 6; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Will']
    _class_skills = ['Appraise', 'Concentration', 'Craft', 'Disable Device', 'Knowledge (arcana)',
                     'Knowledge (architecture and engineering)', 'Knowledge (the planes)',
                     'Open Lock', 'Profession', 'Search', 'Spellcraft', 'Use Magic Device']
    proficiencies = ['simple', 'light', 'medium', 'shield']
    starting_gold = '5d4x10'; start = 'complex'
    advancement = core.get_class_advancement({
        ('infusions', 'artificer knowledge', 'artisan bonus', 'DisableTrap', 'ItemCreation', 'ScribeScroll'): [1],
        'BrewPotion': [2],
        'CraftWondrousItem': [3],
        'CraftHomunculus': [4],
        'BonusFeat': [4,8,12,16,20],
        ('CraftMagicArmsAndArmor', 'RetainEssence'): [5],
        'CraftWand': [6],
        'MetamagicSpellTrigger': [7],
        'CraftRod': [9],
        'MetamagicSpellCompletion': [11],
        'CraftStaff': [12],
        'SkillMastery': [13],
        'ForgeRing': [14]
        })
    feats = ['metamagic', 'Attune Magic Weapon', 'Craft Construct', 'Exceptional Artisan',
             'Extra Rings', 'Extraordinary Artisan', 'Legendary Artisan', 'Wand Mastery']
    reserve_translator = [0,20,40,60,80,100,150,200,250,300,400,500,700,900,1200,1500,2000,2500,3000,4000,5000]

    def __init__(self, character):
        super().__init__(character)
        self.craft_reserve = util.Counter(0)

    def add_level(self):
        super().add_level()
        self.craft_reserve.reset()
        self.craft_reserve.update(self.reserve_translator[self.level], 'base')

    def SkillMastery(self):
        sm = self.character.features.add(name='skill mastery', source=self)
        sm.add_skills(['Spellcraft', 'Use Magic Device'], source=self)

    def BrewPotion(self): self._add_feat('Brew Potion')
    def CraftMagicArmsAndArmor(self): self._add_feat('Craft Magic Arms and Armor')
    def CraftRod(self): self._add_feat('Craft Rod')
    def CraftStaff(self): self._add_feat('Craft Staff')
    def CraftWand(self): self._add_feat('Craft Wand')
    def CraftWondrousItem(self): self._add_feat('Craft Wondrous Item')
    def ForgeRing(self): self._add_feat('Forge Ring')
    def ScribeScroll(self): self._add_feat('Scribe Scroll')
    def _add_feat(self, feat): self.character.feats.add(name=feat, override=True, source=self)

class Infusions(core.Feature):
    _name = 'infusions'
    _infusions_per_day = {
        1: [2], 2: [3], 3: [3,1], 4: [3,2], 5: [3,3,1], 6: [3,3,2], 7: [3,3,2], 8: [3,3,3,1],
        9: [3,3,3,2], 10: [3,3,3,2], 11: [3,3,3,2,1], 12: [3,3,3,2,2], 13: [3,3,3,3,2],
        14: [4,3,3,3,3,1], 15: [4,4,3,3,3,2], 16: [4,4,4,3,3,2], 17: [4,4,4,4,3,3],
        18: [4,4,4,4,4,3], 19: [4,4,4,4,4,4], 20: [4,4,4,4,4,4]
        }
    spell_list = {
        1: ['identify', 'light', 'magic stone', 'magic vestment', 'magic weapon', 'shield of faith'],
        2: ['align weapon', "bear's endurance", "bull's strength", "cat's grace", 'chill metal',
            "eagle's splendor", "fox's cunning", 'heat metal', "owl's wisdom"],
        3: ['greater magic weapon'],
        4: ['lesser globe of invulnerability', 'minor creation', 'rusting grasp'],
        5: ['disrupting weapon', 'fabricate', 'major creation', 'wall of force', 'wall of stone'],
        6: ['blade barrier', 'globe of invulnerability', 'move earth', 'wall of iron']
        }
    def __init__(self, character): raise NotImplementedError

class ArtificerKnowledge(core.Feature):
    _name = 'artificer knowledge'
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute()
        self.character.checks['artificer knowledge'].enabled = True
        self.character.checks['artificer knowledge'].add(self.effective_level, 'base', source=self)

    def add_source(self, source):
        super().add_source(source)
        self.effective_level.add(source.level, 'base', source=source)

class artificer_knowledge(core.Check):
    _name = 'artificer knowledge'
    _ability = 'intelligence'
    def __init__(self, character):
        super().__init__(character)
        self.enabled = False

class ArtisanBonus(core.Feature):
    _name = 'artisan bonus'
    def __init__(self, character):
        super().__init__(character)
        feat_ = self.character.challenges.register(challenge='item with creation feat', source=self)
        self.character.skills['Use Magic Device'].add(2, condition=feat_, source=self)

class DisableTrap(phb.classes.Trapfinding):
    _name = 'disable trap'

class ItemCreation(core.Feature):
    _name = 'item creation'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class CraftHomunculus(core.Feature):
    _name = 'craft homunculus'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class RetainEssence(core.Feature):
    _name = 'retain essence'
    _tags = ['supernatural']

class MetamagicSpellTrigger(core.Feature):
    _name = 'metamagic spell trigger'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class MetamagicSpellCompletion(core.Feature):
    _name = 'metamagic spell completion'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Bard
# optional: take a feat instead of bardic music ability at lvl 3,6,9,12,15, or 18
# from list: Haunting Melody, Music of Growth, Music of Making, Song of the Heart, Soothe the Beast
class MusicOfCreation(AlternateClassFeature):
    _name = 'music of creation'
    def __init__(self, character): raise NotImplementedError

#%% Cleric
# Clerics, Favored souls have no alignment restrictions based on deity

#%% Favored soul
# see cleric

#%% Monk
# good/neutral devoted to Dol Dorn may take Whirling Steel Strike as bonus feat at 2nd/6th; must meet prereqs
# evil devoted to Mockery may take Flensing Strike as bonus feat at 2nd/6th; must meet prereqs
# any monk may take Monastic Training as bonus feat at 1/2/6th lvl
class EberronMonk(AlternateClassFeature):
    _name = 'Eberron monk'
    def __init__(self, character): raise NotImplementedError

#%% Paladin
# Halfling from Talenta Plains calls a callfoot as special mount, rather than warpony
# warforged paladin can use lay on hounds to cure OR repair

#%% Dragonmark heir
class DragonmarkHeir(core.PrestigeClass):
    _name = 'dragonmark heir'
    _hit_die = 8; skill_points = 4; bab_type = 'three quarters'
    good_saves = ['Fortitude', 'Reflex', 'Will']
    advancement = {
        1: ['LesserDragonmark', 'house status'],
        2: ['additional action points (3)', 'improved least dragonmark'],
        3: ['improved lesser dragonmark'],
        4: ['GreaterDragonmark'],
        5: ['improved greater dragonmark']}

    def LesserDragonmark(self): self.feats.add(name='Lesser Dragonmark', override=True, source=self)
    def GreaterDragonmark(self): self.feats.add(name='Greater Dragonmark', override=True, source=self)

    @staticmethod
    def prereq(character):
        house = character.affilitions.get_instances('Dragonmarked House', status='active')
        if not house: return False
        house = house[0]

        skillz = []
        for skill in character.skills:
            if skill.ranks >= 7: skillz.append(skill)
            if len(skillz) >= 2: break

        return (any(x in character.build.active for x in house.races) and
                len(skillz) >= 2 and
                all(x in character.feats.active for x in ['Favored in House', 'Least Dragonmark']))

class HouseStatus(core.Feature):
    _name = 'house status'
    def __init__(self, character):
        super().__init__(character)
        self.house = self.character.affiliations.get_instances('Dragonmarked House', status='active')[0]
        house_ = self.character.challenges.register(target=f'{self.house} member')
        self.character.checks['charisma'].add(self.character.build.level_of('dragonmark heir'),
                                              condition=house_, source=self)

class ImprovedLeastDragonmark(core.Feature):
    _name = 'improved least dragonmark'
    def __init__(self, character): raise NotImplementedError

class ImprovedLesserDragonmark(core.Feature):
    _name = 'improved lesser dragonmark'
    def __init__(self, character): raise NotImplementedError

class ImprovedGreaterDragonmark(core.Feature):
    _name = 'improved greater dragonmark'
    def __init__(self, character): raise NotImplementedError

#%% Eldeen ranger
class EldeenRanger(core.Focus, core.PrestigeClass):
    _name = 'Eldeen ranger'
    _hit_die = 8; skill_points = 6; bab_type = 'full'; good_saves = ['Fortitude', 'Reflex']
    _class_skills = ['Climb', 'Craft', 'Handle Animal', 'Heal', 'Hide', 'Jump',
        'Knowledge (dungeoneering)', 'Knowledge (geography)', 'Knowledge (nature)', 'Listen',
        'Move Silently', 'Profession', 'Ride', 'Search', 'Spot', 'Survival', 'Swim', 'Use Rope']
    proficiencies = ['simple', 'martial', 'light', 'shield']
    advancement = core.get_class_advancement({
        'SectAbility': list(range(1,6,2)),
        'hated foe': [2],
        'favored enemy': [4]
        }) # add Gatekeeper spells to spell list for sect members
    eligible = {
        'Ashbound': ['resist the arcane', 'ferocity', 'spell resistance (20)'],
        'Children of Winter': ['resist poison', 'resist corruption (disease)', 'touch of contagion'],
        'Gatekeepers': ['resist corruption (aberrations)', 'darkvision (enhancement)', 'slippery mind'],
        'Greensingers': ["resist nature's lure", 'unearthly grace', 'damage reduction (3)'],
        'Wardens of the Wood': ['nature sense', 'ImprovedCritical', 'smite evil']
        }
    DR = 'cold iron'
    def __init__(self, character, focus=None):
        super().__init__(character, focus)
        self.grade = util.NumeralAttribute(1)
        self._allocated = []
        rx.combine_latest(self.focus_, self.grade.attribute_).subscribe(self._apply_ability)

    def _apply_ability(self, focus, grade):
        if focus is None: return
        features = self.eligible[focus]
        for f in features[:grade]:
            if f in self._allocated: continue
            self._allocate_feature(f)
            self._allocated.append(f)

    def SectAbility(self): self.grade.attribute += 1
    def ImprovedCritical(self):
        self.character.feats.add(name='Improved Critical', override=True, source=self)

    def _eligible(self, value):
        if not super()._eligible(value): return False
        if ((value=='Children of Winter' and self.character.alignment=='good') or
            (value=='Gatekeepers' and self.character.alignment=='evil') or
            (value=='Greensingers' and self.character.alignment!='chaotic') or
            (value=='Wardens of the Wood' and self.character.alignment=='evil')):
            return False
        return True

    @staticmethod
    def prereq(character, special=False):
        '''Special: must train in the Eldeen Reaches with the sect you wish to join.'''
        return (special, character.BAB >= 5,
                character.skills['Knowledge (nature)'].ranks >= 6,
                character.skills['Survival'].ranks >= 8,
                'Track' in character.feats.active,
                'favored enemy' in character.features.active)

class ResistTheArcane(core.Feature):
    _name = 'resist the arcane'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        arcane_ = self.character.challenges.register(challenge='arcane spells')
        self.character.saves['all'].add(2, condition=arcane_, source=self)

class ResistPoison(core.Feature):
    _name = 'resist poison'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        poison_ = self.character.challenges.register(challenge='poison')
        self.character.saves['all'].add(2, condition=poison_, source=self)

class ResistCorruption(core.Feature):
    _name = 'resist corruption'
    _tags = ['extraordinary']
    def __init__(self, character, variant='aberrations'):
        super().__init__(character)
        if variant not in ['aberrations', 'disease']: raise NotImplementedError(variant)
        self.variant = variant

        if self.variant=='aberrations':
            c_ = self.character.challenges.register(target='aberration',
                challenge=['spell-like ability', 'supernatural ability', 'psionic ability'])
            any_ = rx.combine_latest(*c_[1:]).pipe(ops.map(any), ops.distinct_until_changed())
            self.character.saves['all'].add(2, condition=[c_[0], any_], source=self)

        if self.variant=='disease':
            mind_ = self.character.challenges.register(challenge='Mind-Affecting')
            self.character.resistances.immunities.add(name='disease', source=self)
            self.character.saves['all'].add(2, condition=mind_, source=self)

class HatedFoe(core.Feature):
    _name = 'hated foe'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class TouchOfContagion(core.Feature):
    _name = 'touch of contagion'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.character.magic.supernatural.add(name='contagion', frequency=util.Frequency(3,1,'day'),
                                              source=self)

#%% Exorcist of the Silver Flame
class ExorcistOfTheSilverFlame(core.PrestigeClass):
    _name = 'exorcist of the Silver Flame'
    _hit_die = 8; skill_points = 2; bab_type = 'full'; good_saves = ['Fortitude', 'Will']
    _class_skills = ['Concentration', 'Craft', 'Intimidate', 'Knowledge (arcana)',
        'Knowledge (the planes)', 'Knowledge (religion)', 'Profession', 'Sense Motive', 'Spellcraft']
    advancement = core.get_class_advancement({
        'CasterLevel': [2,3,5,6,8,9],
        'flame of censure': [1],
        'weapon of the exorcist': [1,2,4,6,8,9],
        '_ExorcistDarkvision': [3,6],
        'resist possession': [3],
        'smite evil': [3,7],
        'DetectThoughts': [4],
        'silver exorcism': [5],
        'warding flame': [10]
        })
    #TODO smite evil also adds cleric levels (if any) to damage

    def DetectThoughts(self):
        dt = self.character.magic.spell_like_abilities.add(name='detect thoughts',
                                                           frequency='at will', source=self)
        dc = util.Attribute(10)
        dc.add(self.level, 'base')
        dc.add(self.character.CHA, 'CHA')
        dt.save_dc = dc

    @staticmethod
    def prereq(character):
        sc_list = character.features.get_all(name='spellcasting')
        first = any(sc.magic_type=='divine' and
                    max(spell.level for spell in sc.spells_known.active) >= 1
                    for sc in sc_list)

        return (character.alignment == 'good' and
                character.BAB >= 3 and
                character.skills['Knowledge (the planes)'].ranks >= 3 and
                character.skills['Knowledge (religion)'].ranks >= 8 and
                first and
                character.deity == 'The Silver Flame')

class FlameOfCensure(core.Feature):
    _name = 'flame of censure'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class WeaponOfTheExorcist(core.Focus, core.Feature):
    _name = 'weapon of the exorcist'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        def apply_benefit(weapon):
            is_focus_ = self.focus_.pipe(ops.map(lambda x: x is weapon), ops.distinct_until_changed())
            weapon.damage.add(1, 'sacred', condition=[is_focus_, self.grade.register(1)], source=self)
            weapon.damage._notes.add(name='magic', condition=[is_focus_, self.grade.register(1)], source=self)
            weapon.damage._notes.add(name='silver', condition=[is_focus_, self.grade.register(2)], source=self)
            weapon.damage._notes.add(name='good', condition=[is_focus_, self.grade.register(3)], source=self)
            weapon.extra_dice.add(1, 6, 'fire', condition=[is_focus_, self.grade.register(4)], source=self)
            weapon.damage._notes.add(name='law', condition=[is_focus_, self.grade.register(5)], source=self)
            weapon.extra_dice.add(1, 6, 'sacred', condition=[is_focus_, self.grade.register(6)], source=self)
        self.fpipe_.subscribe(apply_benefit)

    @property
    def focus(self): return self.focus_.value

    @focus.setter
    def focus(self, value):
        if value not in self.character.equipment: raise util.NotEligible(value)
        if isinstance(value, str):
            value = self.character.equipment.get_one(name='value')
        super().focus = value
    def escalate(self): self.grade.attribute += 1
    def _eligible(self, value): return (util.is_a(value, 'Weapon'), value.proficient)

class _ExorcistDarkvision(core.Feature):
    _name = 'darkvision'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.senses['darkvision'].add(util.LiveAttribute(self.grade, lambda x: x*30),
                                                'base', source=self)
    def escalate(self): self.grade.attribute += 1

class ResistPossession(core.Feature):
    _name = 'resist possession'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        poss_ = self.character.challenges.register(challenge='possession', source=self)
        self.character.saves['all'].add(4, 'sacred', condition=poss_, source=self)

        x_ = self.character.challenges.register(challenge=['Charm', 'Compulsion'], foe=['evil outsider', 'undead'])
        any_ = rx.combine_latest(*x_).pipe(ops.map(any), ops.distinct_until_changed())
        self.character.saves['all'].add(2, 'sacred', condition=any_, source=self)

class SilverExorcism(core.Feature):
    _name = 'silver exorcism'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class WardingFlame(core.Feature):
    _name = 'warding flame'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Extreme explorer
class ExtremeExplorer(core.PrestigeClass):
    _name = 'extreme explorer'
    _hit_die = 8; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex']
    _class_skills = ['Balance', 'Climb', 'Decipher Script', 'Disable Device', 'Escape Artist',
                     'Jump', 'Knowledge (arcana)', 'Knowledge (dungeoneering)',
                     'Knowledge (history)', 'Listen', 'Open Lock', 'Ride', 'Search',
                     'Speak Language', 'Survival', 'Swim', 'Tumble', 'Use Magic Device', 'Use Rope']
    advancement = {
        1: ['additional action points (2)', 'trap sense'],
        2: ['dodge bonus', 'evasion', 'extreme hustle'],
        3: ['trap sense', 'BonusFeat'],
        4: ['dodge bonus', 'extreme action'],
        5: ['trap sense', 'BonusFeat']
        }
    feats = ['Action Surge', 'Heroic Spirit', 'Pursue', 'Spontaneous Casting']
    @staticmethod
    def prereq(character):
        return (character.BAB >= 4 and
                all(character.skills[x].ranks >= 4 for x in ['Knowledge (dungeoneering)', 'Survival']),
                'Action Boost' in character.feats.active)

class DodgeBonus(core.Feature):
    _name = 'dodge bonus'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        light_ = self.character.equipment.encumbrance_.pipe(
            ops.map(lambda x: x in ['none', 'light']), ops.distinct_until_changed())
        no_shield_ = self.character.equipment.register('shield').pipe(ops.map(lambda x: not x), ops.distinct_until_changed())
        self.character.AC['all'].add(self.grade, 'dodge', conditions=[light_, no_shield_], source=self)
    def escalate(self): self.grade.attribute += 1

class ExtremeHustle(core.Feature):
    _name = 'extreme hustle'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ExtremeAction(core.Feature):
    _name = 'extreme action'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Heir of Siberys
class HeirOfSiberys(core.Focus, core.PrestigeClass):
    _name = 'heir of Siberys'
    _hit_die = 6; skill_points = 2; bab_type = 'three quarters'
    good_saves = ['Fortitude', 'Reflex', 'Will']
    advancement = core.get_class_advancement({
        ('CasterLevel', 'SiberysMark'): [2,3],
        ('additional action points (2)', 'BonusFeat'): [1],
        })
    feats = ['Action Boost', 'Action Surge', 'Favored in House', 'Pursue', 'Spontaneous Casting']
    def __init__(self, character):
        super().__init__(character, focus=self._autoload_mark())
        self.grade = util.NumeralAttribute(0)

        def apply_benefit(focus):
            mark = self.character.features.add(name=focus, source=self)
            mark.grade = 'Siberys'
            mark.frequency.add(self.grade, 'base', source=self)
        self.fpipe_.subscribe(apply_benefit)

    @property
    def class_skills(self):
        classes = self.character.build.get_all()
        classes = [x for x in classes if x is not self]
        classes = [x for x in classes if util.is_a(x, 'HitDie') and x.level > 0]
        class_skills = {skill for x in classes for skill in x.class_skills}
        return list(class_skills)

    def CasterLevel(self):
        if any('spellcasting' in self.character.features.active): super().CasterLevel()
        else: self.character.feats.feat_slots.add(1, source=self, override=False)

    def SiberysMark(self): self.grade.attribute += 1

    def _autoload_mark(self):
        race = self.character.build.get_instances('Race', status='active')[0]
        if len(marks.marked_races[race.name])==1:
            return marks.marked_races[race.name][0]
        house = self.character.affiliations.get_instances('Dragonmarked House', status='active')
        if not house: return None
        return house[0].mark

    @staticmethod
    def prereq(character):
        race = character.build.get_instances('Race', status='active')[0]
        return (sum(skill.ranks >= 15 for skill in character.skills.values()) >= 2 and
                race.name in marks.marked_races and
                'Heroic Spirit' in character.feats.active and
                not 'Dragonmark' in character.features.active)

#%% Master inquisitive
class MasterInquisitive(core.PrestigeClass):
    _name = 'master inquisitive'
    _hit_die = 8; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex']
    _class_skills = ['Bluff', 'Decipher Script', 'Gather Information', 'Knowledge (local)',
                     'Listen', 'Search', 'Sense Motive', 'Spot']
    advancement = core.get_class_advancement({
        'ZoneOfTruth': [1],
        ('BonusFeat', '_Contact'): list(range(2,6,2)),
        'DiscernLies': [3],
        'TrueSeeing': [5]
        })
    feats = ['Alertness', 'Deceitful', 'Heroid Spirit', 'Improved Initiative', 'Iron Will',
             'Negotiator', 'Persuasive', 'Recognize Impostor', 'Research', 'Toughness', 'Track',
             'Urban Tracking']
    def ZoneOfTruth(self): self._add_sla('zone of truth')
    def DiscernLies(self): self._add_sla('discern lies')
    def TrueSeeing(self): self._add_sla('true seeing')
    def _add_sla(self, sla):
        self.character.magic.spell_like_abilities.add(name=sla, frequency=util.Frequency(1,1,'day'))
        #TODO for 2 AP, gain additional use/day

    @staticmethod
    def prereq(character):
        return (character.skills['Search'].ranks >= 3 and
                all(character.skills[x].ranks >= 6 for x in ['Gather Information', 'Sense Motive']) and
                'Investigate' in character.feats.active)

class _Contact(core.Feature):
    _name = 'contact'
    def __init__(self, character):
        super().__init__(character)
        self.contacts = {}

        def check_contacts():
            if self.grade - len(self.contacts) > 0:
                util.logger.warning('Assign Master Inquisitive contacts: %s', self.contacts)
        self.character.add_to_build(-2, 1, check_contacts)

    def escalate(self): self.grade.attribute += 1

    def recruit(self, contact, level=None):
        if self.grade - len(self.contacts) < 1: raise util.NotEligible(contact)
        if not level and self.grade==1: level = 3
        elif not level and 3 in self.contacts: level = 6
        elif not level and 6 in self.contacts: level = 3
        try:
            contact = contact(self.character)
            if not level and 3 not in self.contacts and contact.build.level <= 3: level = 3
            else: level = 6
            if contact.build.level > level: raise util.NotEligible(contact)
        except TypeError: pass
        if (not level) or (level > self.grade * 3): raise util.NotEligible(contact)

        self.contacts[level] = contact
        self.character.contacts.add(obj=contact, level=level, source=self)

#%% Warforged juggernaut
class WarforgedJuggernaut(core.PrestigeClass):
    _name = 'warforged juggernaut'
    _hit_die = 12; skill_points = 2; bab_type = 'three quarters'; good_saves = ['Fortitude']
    _class_skills = ['Climb', 'Craft', 'Intimidate', 'Jump', 'Survival', 'Swim']
    advancement = {
        1: ['armor spikes', 'expert bull rush', 'PowerfulCharge', 'reserved'],
        2: ['_ChargeBonus', 'construct perfection', 'extended charge'],
        3: ['construct perfection', 'healing immunity', 'superior bull rush'],
        4: ['armor spikes', '_ChargeBonus', 'construct perfection'],
        5: ['construct perfection', 'GreaterPowerfulCharge']}

    def PowerfulCharge(self):
        self.character.feats.add(name='Powerful Charge', override=True, source=self)
    def GreaterPowerfulCharge(self):
        self.character.feats.add(name='Greater Powerful Charge', override=True, source=self)

    @staticmethod
    def prereq(character):
        return ('warforged' in character.build.active and
                character.BAB >= 5 and
                all(x in character.feats.active
                    for x in ['Adamantine Body', 'Improved Bull Rush', 'Power Attack']))

class ArmorSpikes(core.Feature):
    _name = 'armor spikes'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError
    # def escalate(self): pass # 1d6 dmg -> 1d8
    def escalate(self): self.grade.attribute += 1

class ExpertBullRush(core.Feature):
    _name = 'expert bull rush'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute()
        self.character.checks['bull rush'].add(self.effective_level, source=self)
        self.character.checks['resist bull rush'].add(self.effective_level, source=self)
        door_ = self.character.challenges.register(challenge='break door', source=self)
        self.character.checks['break things'].add(self.effective_level, condition=door_, source=self)

    def add_source(self, source):
        super().add_source(source)
        if hasattr(source, 'level'):
            self.effective_level.add(source.level, 'base', source=source)

class _ChargeBonus(core.Feature):
    _name = 'charge bonus'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        charge_ = self.character.challenges.register(action='charge', source=self)
        self.character.attacks.attack['melee'].add(self.grade, condition=charge_, source=self)
    def escalate(self): self.grade.attribute += 1

class ConstructPerfection(core.Feature):
    _name = 'construct perfection'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        def grade_I():
            self.character.resistances.immunities.add(name=['nonlethal', 'critical hits'], source=self)
            self.character.AC['fortification'].add(100, 'base', source=self)
        def grade_II():
            self.character.resistances.immunities.add(name='Mind-Affecting', source=self)
        def grade_III():
            self.character.resistances.immunities.add(name=['death effects', 'necromancy'],
                                                      source=self)
        def grade_IV():
            self.character.resistances.immunities.add(name=['ability damage', 'ability drain'],
                                                      source=self)

        self.grade.attribute_.pipe(ops.filter(lambda x: x==1)).subscribe(grade_I)
        self.grade.attribute_.pipe(ops.filter(lambda x: x==2)).subscribe(grade_II)
        self.grade.attribute_.pipe(ops.filter(lambda x: x==3)).subscribe(grade_III)
        self.grade.attribute_.pipe(ops.filter(lambda x: x==4)).subscribe(grade_IV)

    def escalate(self): self.grade.attribute += 1

class ExtendedCharge(core.Feature):
    _name = 'extended charge'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        charge_ = self.character.challenges.register(action='charge', source=self)
        self.character.speed['all'].add(5, condition=charge_, source=self)

class HealingImmunity(core.Feature):
    _name = 'healing immunity'
    def __init__(self, character):
        super().__init__(character)
        self.character.resistances.immunities.add(name=['Healing', 'all ingested effects', 'potion',
                                                        "heroes' feast"], source=self)

class SuperiorBullRush(core.Feature):
    _name = 'superior bull rush'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Weretouched master
class WeretouchedMaster(core.Focus, core.PrestigeClass):
    _name = 'weretouched master'
    _hit_die = 8; skill_points = 2; bab_type = 'three quarters'; good_saves = ['Fortitude', 'Reflex']
    _class_skills = ['Balance', 'Climb', 'Handle Animal', 'Hide', 'Intimidate', 'Jump',
                     'Knowledge (nature)', 'Listen', 'Move Silently', 'Spot', 'Survival', 'Swim']
    advancement = {
        1: ['Weretouched'],
        2: ['BonusFeat', 'wild empathy'],
        3: ['Weretouched'],
        4: ['BonusFeat', 'frightful shifting'],
        5: ['Weretouched', 'AlternateForm']
        }
    feats = ['Beasthide Elite', 'Cliffwalk Elite', 'Extra Shifter Trait', 'Great Bite',
             'Great Rend', 'Greater Shifter Defense', 'Healing Factor', 'Longstride Elite',
             'Shifter Defense', 'Shifter Ferocity', 'Shifter Multiattack']
    eligible = ['bear', 'boar', 'rat', 'tiger', 'wolf', 'wolverine']
    def __init__(self, character, focus=None):
        super().__init__(character, focus)
        self.grade = util.NumeralAttribute(1)
        self._allocated = []
        rx.combine_latest(self.focus_, self.grade.attribute_).subscribe(self._apply_ability)

    def Weretouched(self): self.grade.attribute += 1

    def WildEmpathy(self):
        self.character.features.add(name='wild empathy', source=self)
        def apply_benefit(focus):
            c_ = self.character.challenges.register(target=focus)
            self.character.checks['wild empathy'].add(4, condition=c_, source=self)
        self.fpipe_.subscribe(apply_benefit)

    def AlternateForm(self):
        def apply_benefit(focus):
            self.character.features.add(obj=_AlternateForm(self.character, focus), source=self)
        self.fpipe_.subscribe(apply_benefit)

    def _apply_ability(self, focus, grade):
        if focus is None: return
        features = ['I', 'II', 'III']
        for f in features[:grade]:
            if f in self._allocated: continue
            self._allocate_feature(f'weretouched {f} ({focus})')
            self._allocated.append(f)

    @staticmethod
    def prereq(character):
        return (character.BAB >= 4 and
                character.skills['Knowledge (nature)'].ranks >= 5 and
                character.skills['Survival'].ranks >= 8 and
                'shifter' in character.build.active and
                character.feats.get_instances('shifter', status='active'))

class FrightfulShifting(core.Feature):
    _name = 'frightful shifting'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute()

        self.dc = util.Attribute(10)
        self.dc.add(self.effective_level, 'base', source=self.sources)
        self.dc.add(self.character.CHA, 'CHA')

        shifted_ = self.character.conditions.register('shifted')
        form_ = self.character.conditions.register('alternate form')
        any_ = rx.combine_latest(shifted_, form_).pipe(ops.map(any), ops.distinct_until_changed())
        self.actions.reaction.add(name='Frighten opponents w/in 30 ft', condition=any_,
                                  trigger='attack', method=self.frighten)

    def frighten(self): #TODO update with better effect protocols
        '''When you attack or charge, opponents within 30 feet who witness the attack may become shaken for
5d6 rounds. This affects only opponents with fewer Hit Dice or levels than your character level. An
opponent can resist with a  Will save. An opponent who succeeds on the save is immune to your
frightful shifting for 24 hours. Frightful shifting is a mind-affecting fear effect.
'''
        print(f'Opponents within 30 ft and with fewer than {self.character.character_level} HD must \
              make a DC {self.dc} Will save or be shaken 5d6 rounds. On a successful save they are \
              immune for 24 hrs.')

    def add_source(self, source):
        super().add_source(source)
        self.effective_level.add(source.level, 'base', source=source)

class WeretouchedI(core.Focus, core.Feature):
    _name = 'weretouched I'
    _tags = ['supernatural']
    eligible = {'bear': ['strength', 'weretouched claws'],
                'boar': ['constitution', 'weretouched gore'],
                'rat': ['dexterity', 'weretouched bite'],
                'tiger': ['strength', 'weretouched claws'],
                'wolf': ['dexterity', 'weretouched bite'],
                'wolverine': ['constitution', 'weretouched bite']}
    def __init__(self, character, focus):
        super().__init__(character, focus)
        shifted_ = self.character.conditions.register('shifted')
        self.character.physical_features.add(name=['bestial appearance', 'fur', 'short tail'],
                                             condition=shifted_, source=self)
        abil, trait = self.eligible[self.focus]
        self.character.abilities[abil].add(2, condition=shifted_, source=self)

        self.character.features.get_one(name='shifting').grade.attribute += 1
        self.character.features.add(name=trait, source=self)

class WeretouchedClaws(races.Razorclaw):
    _name = 'weretouched claws'
    def __init__(self, character):
        if 'razorclaw' not in character.features.active: super().__init__(character)
        else: super(races.Razorclaw, self).__init__(character)
        claws_ = self.character.features.active_.pipe(
            ops.map(lambda p: [x for x in p if x!=self]),
            ops.map(lambda p: [x for x in p if util.is_a(x, 'razorclaw')]),
            ops.map(bool), ops.distinct_until_changed())
        test_ = rx.combine_latest(claws_, self.character.feats.register('Improved Natural Attack')).pipe(
            ops.map(any), ops.distinct_until_changed())

        for clw in ['first claw', 'second claw']:
            claw = self.character.equipment.get_one(name=clw)
            claw.size.add(1, condition=test_, source=self)

class WeretouchedBite(races.Longtooth):
    _name = 'weretouched bite'
    def __init__(self, character):
        if 'longtooth' not in self.character.features.active: super().__init__(character)
        else: super(races.Longtooth, self).__init__(character)
        bite_ = self.character.features.active_.pipe(
            ops.map(lambda p: [x for x in p if x!=self]),
            ops.map(lambda p: [x for x in p if util.is_a(x, 'longtooth')]),
            ops.map(bool), ops.distinct_until_changed())
        test_ = rx.combine_latest(bite_, self.character.feats.register('Improved Natural Attack')).pipe(
            ops.map(any), ops.distinct_until_changed())

        bite = self.character.equipment.get_one(name='bite')
        bite.size.add(1, condition=test_, source=self)

class WeretouchedGore(races.ShifterTrait):
    _name = 'weretouched gore'
    def __init__(self, character):
        super().__init__(character)
        self.gore = self.character.equipment.add(item='gore', condition=self.shifted_, source=self)
        self.gore.damage.add(util.LiveAttribute(self.character.build.level, lambda x: x//4),
                        'racial', source=self)

        test_ = rx.combine_latest(self.character.features.register('longtooth'),
                                  self.character.feats.register('Improved Natural Attack')).pipe(
            ops.map(any), ops.distinct_until_changed())

        gore = self.character.equipment.get_one(name='gore')
        gore.size.add(1, condition=test_)

class _ClimbSpeed(core.Feature):
    _name = 'climb speed'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        cliffwalk_ = self.character.features.active_.pipe(
            ops.map(lambda p: any(x.name=='cliffwalk' for x in p)),
            ops.distinct_until_changed()
            )
        not_cliffwalk_ = cliffwalk_.pipe(ops.map(lambda p: not p))

        self.character.speed['climb'].add(10, 'base', condition=cliffwalk_, source=self)
        self.character.speed['climb'].add(20, 'base', condition=not_cliffwalk_, source=self)
        self.character.skills['Climb'].take_better_of('STR', self.character.DEX, condition=self.active_)

class WeretouchedII(core.Focus, core.Feature):
    _name = 'weretouched II'
    eligible = {'bear': 'improved grab (claw)', 'boar': 'fierce will', 'rat': _ClimbSpeed,
                'tiger': 'pounce', 'wolf': 'trip', 'wolverine': mm.animals.Rage}
    def __init__(self, character, focus):
        super().__init__(character, focus)
        self.character.senses['scent'].add(True, 'base', source=self)
        shifted_ = self.character.conditions.register('shifted')
        feature = self.eligible[self.focus]
        if isinstance(feature, str):
            self.character.features.add(name=feature, condition=shifted_, source=self)
        else: self.character.features.add(obj=feature(self.character), condition=shifted_, source=self)

    def _enter_rage(self):
        '''If you take damage, you fly into a berserk rage on your next turn, biting madly until either you or
your opponent is dead, or until your shifting ends. Gains +2 to Strength, +2 to Constitution, and -2
to Armor Class while raging. You cannot end your rage voluntarily, but unlike a barbarian, you are
not winded after your rage ends.
'''
        self.character.conditions.activate(obj=self._rage)

    def _grab(self):
        '''If you hit with a claw attack, you deal normal damage and attempt to start a grapple as a free
action without provoking an attack of opportunity.
'''
class FierceWill(core.Feature):
    _name = 'fierce will'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.character.saves['Will'].add(4, source=self)

class WeretouchedIII(core.Focus, core.Feature):
    _name = 'weretouched III'
    _tags = ['extraordinary']
    eligible = {'bear': {'strength':4}, 'boar': {'constitution':6}, 'rat': {'dexterity':6},
                'tiger': {'strength':2, 'constitution':4},
                'wolf': {'strength':2, 'dexterity':2, 'constitution':2},
                'wolverine': {'dexterity':2, 'constitution':4}}
    def __init__(self, character, focus):
        super().__init__(character, focus)
        shifted_ = self.character.conditions.register('shifted')
        for k, v in self.eligible[self.focus]:
            self.character.abilities[k].add(v, condition=shifted_, source=self)

class _AlternateForm(core.Feature):
    _name = 'alternate form'
    _tags = ['supernatural']
    forms = {'bear':'BrownBear', 'boar':'DireBoar', 'rat':'DireRat', 'tiger':'Tiger', 'wolf':'DireWolf',
             'wolverine':'DireWolverine'}
    def __init__(self, character, heritage):
        super().__init__(character)
        self.shift = self.character.features.get_one_item(name='Shifting')
        self.form = self.forms[self.character.classes.get_one_item(name='weretouched master').heritage]
        self.effect = core.Polymorph()
        self.frequency = self.shift.frequency

        self.character.actions.swift.add(name='alternate form', method=self.alternate_form)
        #TODO add anti_condition (in alternate form)
        #TODO add modified shift frequency to action counter

    def alternate_form(self):
        self.effect.start(duration=self.shift.duration)
        self.effect.apply(self.character)
        #TODO this should activate condition tag 'wereformed'
        #TODO make this an anti_condition for shifting

#%% Adept

# add 1 domain; no bonus spells, but include spells in adept spell list
# multiclass adept/clerics don't get excess domains

#%% Magewright
class Magewright(core.NPCClass):
    _name = 'magewright'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Handle Animal', 'Knowledge', 'Profession', 'Spellcraft']
    proficiencies = ['simple']
    starting_gold = '2d4x10'
    advancement = core.get_class_advancement({
        'Spellcasting': [1],
        '_SpellMastery': [1]+list(range(4,21,4)) #TODO uhh...
        })

class MagewrightSpellcasting(core.Spellcasting):
    _ability = 'intelligence'
    magic_type = 'arcane'
    caster_type = 'prepared'
    clss = 'magewright'
    cantrips = True
    _spells_per_day = {
        1: [3,1], 2: [3,1], 3: [3,2], 4: [3,2,0], 5: [3,2,1], 6: [3,2,1], 7: [3,3,2], 8: [3,3,2,0],
        9: [3,3,2,1], 10: [3,3,2,1], 11: [3,3,3,2], 12: [3,3,3,2,0], 13: [3,3,3,2,1],
        14: [3,3,3,2,1], 15: [3,3,3,3,2], 16: [3,3,3,3,2,0], 17: [3,3,3,3,2,1], 18: [3,3,3,3,2,1],
        19: [3,3,3,3,3,2], 20: [3,3,3,3,3,2],
        }
    _spell_list = {
        0: ['arcane mark', 'detect magic', 'light', 'mage hand', 'mending', 'message', 'open/close',
            'prestidigitation', 'read magic'],
        1: ['alarm', 'animate rope', 'comprehend languages', 'erase', 'grease', 'hold portal',
            'identify', 'magecraft', 'mount', "Nystul's magic aura", "Tenser's floating disk",
            'unseen servant'],
        2: ['arcane lock', 'augury', "Leomund's trap", 'locate object', 'magic mouth', 'make whole',
            'misdirection', 'obscure object', 'whispering wind'],
        3: ['arcane sight', 'clairaudience/clairvoyance', 'daylight', 'dispel magic',
            'explosive runes', 'gentle repose', 'glyph of warding', 'illusory script',
            'nondetection', 'phantom steed', 'secret page', 'sepia snake sigil', 'tongues'],
        4: ['animate dead', 'detect scrying', 'divination', 'fire trap', 'hardening',
            'illusory wall', 'imbue with spell ability', 'locate creature', 'minor creation',
            'remove curse', 'scrying', 'stone shape'],
        5: ['contact other plane', 'fabricate', 'false vision', "Leomund's secret chest",
            'major creation', 'permanency', 'sending', 'symbol of pain', 'symbol of sleep',
            'wall of stone']
        }

class _SpellMastery(core.Feature):
    _name = 'spell mastery'
    def __init__(self, character): raise NotImplementedError(self._name)

#%% Shared features
class AdditionalActionPoints(core.Feature):
    _name = 'additional action points'
    def __init__(self, character, points=2):
        super().__init__(character)
        self.character.actions.action_points.action_points.add(points, source=self)
