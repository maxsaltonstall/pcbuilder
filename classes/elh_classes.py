#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 00:31:53 2026
@author: gtauxe
"""

import core, phb, dmg
from splat.epic_level_handbook.core import EpicClass
import splat.expanded_psionics_handbook as eph
import utilities as util
sourcebook = 'Epic Level Handbook'

#%% PHB classes
class EpicBarbarian(EpicClass, phb.classes.Barbarian):
    pattern = [(24, 4, 'rage'),
               (22, 3, 'trap sense'),
               (23, 3, 'DamageReduction'),
               (24, 4, 'BonusFeat')]
    feats = ['Armor Skin', 'Chaotic Rage', 'Damage Reduction', 'Devastating Critical',
        'Dire Charge', 'Epic Endurance', 'Epic Prowess', 'Epic Speed', 'Epic Toughness',
        'Epic Weapon Focus', 'Fast Healing', 'Incite Rage', 'Legendary Climber', 'Legendary Leaper',
        'Legendary Rider', 'Legendary Tracker', 'Legendary Wrestler', 'Mighty Rage',
        'Overwhelming Critical', 'Ruinous Rage', 'Terrifying Rage', 'Thundering Rage']

class EpicBard(EpicClass, phb.classes.Bard):
    pattern = [(23, 3, 'BonusFeat')]
    feats = ['Augmented Alchemy', 'Deafening Song', 'Epic Inspiration', 'Epic Leadership',
             'Epic Reputation', 'Epic Skill Focus', 'Group Inspiration', 'Hindering Song',
             'Improved Combat Casting', 'Improved Metamagic', 'Improved Spell Capacity',
             'Inspire Excellence', 'Lasting Inspiration', 'Master Staff', 'Master Wand',
             'Music of the Gods', 'Permanent Emanation', 'Polyglot', 'Ranged Inspiration',
             'Rapid Inspiration', 'Reactive Countersong', 'Spell Knowledge', 'Spell Stowaway',
             'Spell Opportunity', 'Tenacious Magic']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='bardic knowledge').add_source(self)

class EpicCleric(EpicClass, phb.classes.Cleric):
    pattern = [(23, 3, 'BonusFeat')]
    feats = ['Armor Skin', 'Automatic Quicken Spell', 'Automatic Silent Spell',
        'Automatic Still Spell', 'Bonus Domain', 'Enhance Spell', 'Epic Spell Focus',
        'Epic Spell Penetration', 'Epic Spellcasting', 'Ignore Material Components',
        'Improved Alignment-Based Casting', 'Improved Combat Casting', 'Improved Heighten Spell',
        'Improved Metamagic', 'Improved Spell Capacity', 'Intensify Spell', 'Multispell',
        'Negative Energy Burst', 'Permanent Emanation', 'Planar Turning', 'Positive Energy Aura',
        'Spectral Strike', 'Spell Stowaway', 'Spell Opportunity', 'Spontaneous Domain Access',
        'Spontaneous Spell', 'Tenacious Magic', 'Undead Mastery', 'Zone of Animation']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='turn/rebuke undead').add_source(self)

class EpicDruid(EpicClass, phb.classes.Druid): #TODO compare animal companion feature with 3.0 book
    pattern = [(22, 4, 'wild shape'),
               (24, 4, 'BonusFeat')]
    # modify wild shape: gain all extraordinary abilities of new form
    feats = ['Automatic Quicken Spell', 'Automatic Silent Spell', 'Automatic Still Spell',
            'Beast Companion', 'Beast Shape', 'Colossal Wild Shape', 'Diminutive Wild Shape',
            'Dragon Shape', 'Energy Resistance', 'Enhance Spell', 'Epic Spell Focus',
            'Epic Spell Penetration', 'Epic Spellcasting', 'Fast Healing', 'Fine Wild Shape',
            'Gargantuan Wild Shape', 'Ignore Material Components', 'Improved Combat Casting',
            'Improved Elemental Wild Shape', 'Improved Heighten Spell', 'Improved Metamagic',
            'Improved Spell Capacity', 'Intensify Spell', 'Magical Beast Shape', 'Multispell',
            'Perfect Health', 'Permanent Emanation', 'Plant Shape', 'Spell Stowaway',
            'Spell Opportunity', 'Spontaneous Spell', 'Tenacious Magic', 'Vermin Shape']

class EpicFighter(EpicClass, phb.classes.Fighter):
    pattern = [(22, 2, 'BonusFeat')]
    feats = ['fighter', 'Armor Skin', 'Combat Archery', 'Damage Reduction', 'Devastating Critical',
            'Dire Charge', 'Distant Shot', 'Epic Endurance', 'Epic Leadership', 'Epic Prowess',
            'Epic Toughness', 'Epic Weapon Focus', 'Epic Weapon Specialization',
            'Exceptional Deflection', 'Improved Combat Reflexes', 'Improved Manyshot',
            'Improved Stunning Fist', 'Improved Whirlwind Attack', 'Infinite Deflection',
            'Instant Reload', 'Legendary Commander', 'Legendary Rider', 'Legendary Wrestler',
            'Overwhelming Critical', 'Penetrate Damage Reduction', 'Perfect Two-Weapon Fighting',
            'Reflect Arrows', 'Spellcasting Harrier', 'Storm of Throws', 'Superior Initiative',
            'Swarm of Arrows', 'Two-Weapon Rend', 'Uncanny Accuracy']

class EpicMonk(EpicClass, phb.classes.Monk):
    pattern = [(25, 5, 'BonusFeat')]
    feats = ['Armor Skin', 'Blinding Speed', 'Damage Reduction', 'Energy Resistance',
            'Epic Prowess', 'Epic Speed', 'Epic Toughness', 'Exceptional Deflection',
            'Fast Healing', 'Improved Combat Reflexes', 'Improved Ki Strike',
            'Improved Spell Resistance', 'Improved Stunning Fist', 'Infinite Deflection',
            'Keen Strike', 'Legendary Climber', 'Legendary Wrestler', 'Reflect Arrows',
            'Righteous Strike', 'Self-Concealment', 'Shattering Strike', 'Vorpal Strike']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='AC bonus').add_source(self)
        self.character.features.get_one(name='MonkFastMovement').add_source(self)
        self.character.features.get_one(name='wholeness of body').add_source(self)
        self.character.features.get_one(name='abundant step').add_source(self)
        self.character.features.get_one(name='diamond soul').add_source(self)
        self.character.features.get_one(name='quivering palm').add_source(self)
        self.character.features.get_one(name='empty body').add_source(self)
        # Stunning attack doesn't seem to have a direct parallel in 3.5 (?)

class EpicPaladin(EpicClass, phb.classes.Paladin):
    pattern = [(21, 3, 'remove disease'),
               (23, 3, 'BonusFeat')]
    feats = ['Armor Skin', 'Devastating Critical', 'Epic Leadership', 'Epic Prowess',
        'Epic Reputation', 'Epic Toughness', 'Epic Weapon Focus', 'Great Smiting', 'Holy Strike',
        'Improved Aura of Courage', 'Improved Combat Casting', 'Improved Spell Capacity',
        'Legendary Commander', 'Legendary Rider', 'Overwhelming Critical', 'Perfect Health',
        'Permanent Emanation', 'Planar Turning', 'Positive Energy Aura', 'Spectral Strike',
        'Spontaneous Spell', 'Widen Aura of Courage']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='lay on hands').add_source(self)
        self.character.features.get_one(name='smite evil').add_source(self)
        self.character.features.get_one(name='turn undead').add_source(self)
        # Special mount advancement -- ???

class EpicRanger(EpicClass, phb.classes.Ranger):
    pattern = [(23, 3, 'BonusFeat'),
               (25, 5, 'favored enemy')]
    feats = ['Bane of Enemies', 'Blinding Speed', 'Combat Archery', 'Death of Enemies',
             'Distant Shot', 'Epic Endurance', 'Epic Prowess', 'Epic Speed', 'Epic Toughness',
             'Epic Weapon Focus', 'Fast Healing', 'Improved Combat Casting',
             'Improved Favored Enemy', 'Improved Manyshot', 'Improved Spell Capacity',
             'Legendary Climber', 'Legendary Rider', 'Legendary Tracker', 'Perfect Health',
             'Perfect Two-Weapon Fighting', 'Permanent Emanation', 'Spontaneous Spell',
             'Storm of Throws', 'Swarm of Arrows', 'Two-Weapon Rend', 'Uncanny Accuracy']

class EpicRogue(EpicClass, phb.classes.Rogue):
    pattern = [(21, 2, 'sneak attack'),
               (23, 3, 'trap sense'),
               (24, 4, 'SpecialAbility')]
    special_ability_options = ['crippling strike', 'defensive roll', 'improved evasion',
                               'opportunist', 'skill mastery', 'slippery mind']
    feats = ['Blinding Speed', 'Combat Archery', 'Dexterous Fortitude', 'Dexterous Will',
             'Epic Dodge', 'Epic Reputation', 'Epic Skill Focus', 'Epic Speed',
             'Improved Combat Reflexes', 'Improved Sneak Attack', 'Legendary Climber',
             'Lingering Damage', 'Self-Concealment', 'Sneak Attack of Opportunity',
             'Spellcasting Harrier', 'Superior Initiative', 'Trap Sense', 'Uncanny Accuracy']

class EpicSorcerer(EpicClass, phb.classes.Sorcerer):
    pattern = [(23, 3, 'BonusFeat')]
    feats = ['Augmented Alchemy', 'Automatic Quicken Spell', 'Automatic Silent Spell',
             'Automatic Still Spell', 'Energy Resistance', 'Enhance Spell', 'Epic Spell Focus',
             'Epic Spell Penetration', 'Epic Spellcasting', 'Familiar Spell',
             'Ignore Material Components', 'Improved Combat Casting', 'Improved Heighten Spell',
             'Improved Metamagic', 'Improved Spell Capacity', 'Intensify Spell', 'Master Staff',
             'Master Wand', 'Multispell', 'Permanent Emanation', 'Spell Knowledge',
             'Spell Stowaway', 'Spell Opportunity']
    # epic familiar

class EpicWizard(EpicClass, phb.classes.Wizard):
    pattern = [(23, 3, 'BonusFeat')]
    feats = ['item creation', 'metamagic', 'Augmented Alchemy', 'Automatic Quicken Spell',
             'Automatic Silent Spell', 'Automatic Still Spell', 'Combat Casting',
             'Craft Epic Magic Arms and Armor', 'Craft Epic Rod', 'Craft Epic Staff',
             'Craft Epic Wondrous Item', 'Efficient Item Creation', 'Enhance Spell',
             'Epic Spell Focus', 'Epic Spell Penetration', 'Epic Spellcasting', 'Familiar Spell',
             'Forge Epic Ring', 'Ignore Material Components', 'Improved Combat Casting',
             'Improved Heighten Spell', 'Improved Metamagic', 'Improved Spell Capacity',
             'Intensify Spell', 'Multispell', 'Permanent Emanation', 'Scribe Epic Scroll',
             'Spell Focus', 'Spell Knowledge', 'Spell Mastery', 'Spell Penetration',
             'Spell Stowaway', 'Spell Opportunity', 'Spontaneous Spell', 'Tenacious Magic']

#%% DMG prestige classes
class EpicArcaneArcher(EpicClass, dmg.prestige_classes.ArcaneArcher):
    pattern = [(11, 2, 'enhance arrow'),
               (14, 4, 'BonusFeat')]
    feats = ['Blinding Speed', 'Combat Archery', 'Distant Shot', 'Epic Prowess', 'Epic Speed',
             'Epic Toughness', 'Epic Weapon Focus', 'Improved Arrow of Death',
             'Improved Combat Casting', 'Improved Low-Light Vision', 'Improved Manyshot',
             'Swarm of Arrows', 'Uncanny Accuracy'] # EpWF only for any type of bow (not xbow)
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='hail of arrows').add_source(self)

class EpicAssassin(EpicClass, dmg.prestige_classes.Assassin):
    pattern = [(11, 2, 'sneak attack'),
               (12, 2, 'poison save'),
               (14, 4, 'BonusFeat')]
    feats = ['Dexterous Fortitude', 'Dexterous Will', 'Improved Combat Casting',
        'Improved Death Attack', 'Improved Sneak Attack', 'Improved Spell Capacity',
        'Legendary Tracker', 'Lingering Damage', 'Sneak Attack of Opportunity', 'Spell Knowledge',
        'Spontaneous Spell', 'Superior Initiative', 'Tenacious Magic', 'Uncanny Accuracy']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='death attack').add_source(self) # half level

class EpicBlackguard(EpicClass, dmg.prestige_classes.Blackguard):
    pattern = [(13, 3, 'sneak attack'),
               (13, 3, 'BonusFeat')]
    feats = ['Armor Skin', 'Devastating Critical', 'Epic Leadership', 'Epic Prowess',
             'Epic Reputation', 'Epic Toughness', 'Epic Weapon Focus', 'Great Smiting',
             'Improved Aura of Despair', 'Improved Combat Casting', 'Improved Sneak Attack',
             'Improved Spell Capacity', 'Legendary Commander', 'Legendary Rider',
             'Lingering Damage', 'Negative Energy Burst', 'Overwhelming Critical', 'Perfect Health',
             'Permanent Emanation', 'Planar Turning', 'Spontaneous Spell', 'Undead Mastery',
             'Unholy Strike', 'Widen Aura of Despair', 'Zone of Animation']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='smite good').add_source(self)
        self.character.features.get_one(name='command undead').add_source(self)
        # epic fiendish servant
        # fallen paladins

class EpicDwarvenDefender(EpicClass, dmg.prestige_classes.DwarvenDefender):
    pattern = [(11, 2, 'defensive stance'),
               (13, 3, 'BonusFeat'),
               (14, 4, 'DamageReduction')]
    feats = ['Armor Skin', 'Bulwark of Defense', 'Damage Reduction', 'Devastating Critical',
             'Energy Resistance', 'Epic Endurance', 'Epic Prowess', 'Epic Toughness',
             'Epic Weapon Focus', 'Fast Healing', 'Improved Combat Reflexes', 'Improved Darkvision',
             'Instant Reload', 'Mobile Defense', 'Overwhelming Critical', 'Perfect Health',
             'Spellcasting Harrier']

class EpicLoremaster(EpicClass, dmg.prestige_classes.Loremaster):
    pattern = [(11, 1, 'CasterLevel'),
               (13, 3, 'SpecialAbility')]
    special_ability_options = ['secret', 'BonusFeat']
    feats = ['Augmented Alchemy', 'Automatic Quicken Spell', 'Automatic Silent Spell',
             'Automatic Still Spell', 'Craft Epic Magic Arms and Armor', 'Craft Epic Rod',
             'Craft Epic Staff', 'Craft Epic Wondrous Item', 'Efficient Item Creation',
             'Enhance Spell', 'Epic Spell Focus', 'Epic Spell Penetration', 'Epic Spellcasting',
             'Forge Epic Ring', 'Ignore Material Components', 'Improved Combat Casting',
             'Improved Heighten Spell', 'Improved Metamagic', 'Improved Spell Capacity',
             'Intensify Spell', 'Master Staff', 'Master Wand', 'Multispell', 'Permanent Emanation',
             'Polyglot', 'Scribe Epic Scroll', 'Spell Knowledge', 'Spell Stowaway',
             'Spell Opportunity', 'Spontaneous Spell', 'Tenacious Magic']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='lore').add_source(self)

class EpicRedWizard(EpicClass, dmg.prestige_classes.RedWizard):
    pattern = [(11, 1, 'ArcaneCasterLevel'),
               (12, 2, 'spell power'),
               (14, 4, 'BonusFeat')]
    feats = ['item creation', 'metamagic', 'Augmented Alchemy', 'Automatic Quicken Spell',
             'Automatic Silent Spell', 'Automatic Still Spell', 'Craft Epic Magic Arms and Armor',
             'Craft Epic Rod', 'Craft Epic Staff', 'Craft Epic Wondrous Item',
             'Efficient Item Creation', 'Enhance Spell', 'Epic Spell Focus', 'Forge Epic Ring',
             'Ignore Material Components', 'Improved Combat Casting', 'Improved Heighten Spell',
             'Improved Metamagic', 'Improved Spell Capacity', 'Intensify Spell', 'Multispell',
             'Permanent Emanation', 'Scribe Epic Scroll', 'Spell Knowledge', 'Spell Opportunity',
             'Spontaneous Spell', 'Combat Casting', 'Spell Focus', 'Spell Mastery',
             'Spell Penetration', 'Greater Spell Focus', 'Greater Spell Penetration',
             'Improved Counterspell', 'Improved Familiar', 'Innate Spell', 'Magical Artisan',
             'Signature Spell']

class EpicShadowdancer(EpicClass, dmg.prestige_classes.Shadowdancer):
    pattern = [(12, 2, 'shadow jump'),
               (13, 3, 'BonusFeat')]
    feats = ['Blinding Speed', 'Dexterous Fortitude', 'Dexterous Will', 'Epic Dodge',
             'Epic Skill Focus', 'Epic Speed', 'Exceptional Deflection', 'Improved Combat Reflexes',
             'Improved Darkvision', 'Improved Whirlwind Attack', 'Infinite Deflection',
             'Legendary Leaper', 'Reflect Arrows', 'Self-Concealment', 'Spellcasting Harrier',
             'Superior Initiative']
    def __init__(self, character):
        super().__init__(character)
        self.character.features.get_one(name='summon shadow').add_source(self)

#%% EPH psionic classes
class EpicPsion(EpicClass, eph.Psion):
    pattern = [(23, 3, 'BonusFeat')]
    # epic psicrystal
    feats = ['item creation', 'metapsionic', 'Augmented Alchemy', 'Automatic Quicken Spell',
             'Automatic Silent Spell', 'Automatic Still Spell', 'Combat Casting',
             'Craft Epic Magic Arms and Armor', 'Craft Epic Rod', 'Craft Epic Staff',
             'Craft Epic Wondrous Item', 'Efficient Item Creation', 'Enhance Spell',
             'Epic Spell Focus', 'Epic Spell Penetration', 'Epic Spellcasting', 'Familiar Spell',
             'Forge Epic Ring', 'Ignore Material Components', 'Improved Combat Casting',
             'Improved Heighten Spell', 'Improved Metamagic', 'Improved Manifestation',
             'Intensify Spell', 'Multispell', 'Permanent Emanation', 'Scribe Epic Scroll',
             'Spell Focus', 'Spell Knowledge', 'Spell Mastery', 'Spell Penetration', 'Spell Stowaway',
             'Spell Opportunity', 'Spontaneous Spell', 'Tenacious Magic']

class EpicPsychicWarrior(EpicClass, eph.PsychicWarrior):
    pattern = [(21, 3, 'BonusFeat')]
    feats = ['fighter', 'psionic', 'Armor Skin', 'Combat Archery', 'Damage Reduction',
        'Devastating Critical', 'Dire Charge', 'Distant Shot', 'Epic Endurance', 'Epic Leadership',
        'Epic Prowess', 'Epic Toughness', 'Epic Weapon Focus', 'Epic Weapon Specialization',
        'Exceptional Deflection', 'Improved Combat Reflexes', 'Improved Stunning Fist',
        'Improved Manifestation', 'Improved Whirlwind Attack', 'Infinite Deflection',
        'Instant Reload', 'Legendary Commander', 'Legendary Rider', 'Legendary Wrestler',
        'Overwhelming Critical', 'Penetrate Damage Reduction', 'Perfect Two-Weapon Fighting',
        'Reflect Arrows', 'Spellcasting Harrier', 'Storm of Throws', 'Spell Knowledge',
        'Superior Initiative', 'Swarm of Arrows', 'Two-Weapon Rend', 'Uncanny Accuracy']

#%% Agent retriever
class AgentRetriever(EpicClass, core.PrestigeClass):
    _name = 'agent retriever'
    _hit_die = 6; skill_points = 6
    _class_skills = ['Appraise', 'Decipher Script', 'Diplomacy', 'Forgery', 'Gather Information',
                     'Knowledge (arcana)', 'Knowledge (geography)', 'Knowledge (history)',
                     'Knowledge (local)', 'Knowledge (the planes)', 'Listen', 'Search', 'Spot',
                     'Survival']
    pattern = [(1, 1, 'CasterLevel'),
               (1, 0, 'uncanny location'),
               (1, 5, 'tracking bonus'),
               (2, 5, 'plane shift'),
               (3, 5, 'force sphere'),
               (4, 5, 'ethereal jaunt'),
               (5, 5, 'BonusFeat')]
    feats = ['Epic Endurance', 'Epic Prowess', 'Epic Speed', 'Epic Toughness', 'Epic Weapon Focus',
        'Fast Healing', 'Improved Combat Casting', 'Improved Spell Capacity', 'Legendary Climber',
        'Legendary Rider', 'Legendary Tracker', 'Perfect Health', 'Permanent Emanation',
        'Spontaneous Spell', 'Storm of Throws', 'Swarm of Arrows', 'Uncanny Accuracy']

    @staticmethod
    def prereq(character):
        return ('epic' in character.build.active and
                character.alignment=='lawful' and
                character.skills['Gather Information'].ranks >= 24 and
                character.skills['Knowledge (the planes)'].ranks >= 15 and
                'Track' in character.feats.active)

class UncannyLocation(core.Feature):
    _name = 'uncanny location'
    _tags = ['spell-like']

class TrackingBonus(core.Feature):
    _name = 'tracking bonus'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(10)

    def escalate(self): self.grade.attribute += 10

class PlaneShift(core.Feature):
    _name = 'plane shift'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)

    def escalate(self): self.grade.attribute += 1

class ForceSphere(core.Feature):
    _name = 'force sphere'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)

    def escalate(self): self.grade.attribute += 1

class EtherealJaunt(core.Feature):
    _name = 'ethereal jaunt'
    _tags = ['spell-like']
    feats = ['Epic Endurance', 'Epic Prowess', 'Epic Speed', 'Epic Toughness', 'Epic Weapon Focus',
        'Fast Healing', 'Improved Combat Casting', 'Improved Spell Capacity', 'Legendary Climber',
        'Legendary Rider', 'Legendary Tracker', 'Perfect Health', 'Permanent Emanation',
        'Spontaneous Spell', 'Storm of Throws', 'Swarm of Arrows', 'Uncanny Accuracy']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
    def escalate(self): self.grade.attribute += 1

#%% Cosmic descryer
class CosmicDescryer(EpicClass, core.PrestigeClass):
    _name = 'cosmic descryer'
    _hit_die = 4; skill_points = 2
    _class_skills = ['Bluff', 'Concentration', 'Craft', 'Diplomacy', 'Knowledge (arcana)',
                     'Knowledge (religion)', 'Knowledge (the planes)', 'Profession', 'Sense Motive',
                     'Spellcraft']
    pattern = [(1, 4, 'superior planar summoning'),
               (2, 2, 'CasterLevel'),
               (2, 2, 'naturalization'),
               (3, 3, 'enduring gate'),
               (5, 5, 'BonusFeat'),
               (7, 5, 'cosmic connection')]
    feats = ['Augmented Alchemy', 'Automatic Quicken Spell', 'Automatic Silent Spell',
             'Automatic Still Spell', 'Combat Casting', 'Craft Epic Magic Arms and Armor',
             'Craft Epic Rod', 'Craft Epic Staff', 'Craft Epic Wondrous Item',
             'Efficient Item Creation', 'Enhance Spell', 'Epic Spell Focus',
             'Epic Spell Penetration', 'Epic Spellcasting', 'Familiar Spell', 'Forge Epic Ring',
             'Ignore Material Components', 'Improved Combat Casting', 'Improved Heighten Spell',
             'Improved Metamagic', 'Improved Spell Capacity', 'Intensify Spell', 'Multispell',
             'Permanent Emanation', 'Scribe Epic Scroll', 'Spell Focus', 'Spell Knowledge',
             'Spell Mastery', 'Spell Opportunity', 'Spell Penetration', 'Spell Stowaway',
             'Spontaneous Spell', 'Tenacious Magic']
    @staticmethod
    def prereq(character, special=False):
        '''Special: Must have previously traveled to any other plane of existince.'''
        return (special and 'epic' in character.build.active and
                character.skills['Knowledge (the planes)'].ranks >= 24 and
                all(x in character.feats.active
                    for x in ['Spell Focus (conjuration)', 'Energy Resistance']) and
                'gate' in character.magic.spells_known and
                any(x in character.magic.spells_known for x in ['planar ally', 'planar binding']))

class SuperiorPlanarSummoning(core.Feature):
    _name = 'superior planar summoning'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class Naturalization(core.Feature):
    _name = 'naturalization'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class EnduringGate(core.Feature):
    _name = 'enduring gate'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

class CosmicConnection(core.Feature):
    _name = 'cosmic connection'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

#%% Divine emissary
class DivineEmissary(EpicClass, core.PrestigeClass):
    _name = 'divine emissary'
    _hit_die = 10; skill_points = 4
    _class_skills = ['Concentration', 'Craft', 'Diplomacy', 'Disguise', 'Gather Information',
                     'Heal', 'Intimidate', 'Knowledge (religion)', 'Profession', 'Search',
                     'Sense Motive', 'Spellcraft', 'Spot', 'Use Magic Device']
    pattern = [(1, 1, 'CasterLevel'),
               (1, 0, 'granted domain'),
               (1, 3, 'divine inspiration'),
               (2, 3, 'extra smite'),
               (3, 10, 'greater planar ally'),
               (6, 10, 'BonusFeat'),
               (9, 10, 'divine hand')]
    feats = ['Armor Skin', 'Devastating Critical', 'Epic Leadership', 'Epic Prowess',
             'Epic Reputation', 'Epic Toughness', 'Epic Weapon Focus', 'Great Smiting',
             'Holy Strike', 'Improved Aura of Courage', 'Improved Combat Casting',
             'Improved Spell Capacity', 'Legendary Commander', 'Legendary Rider',
             'Overwhelming Critical', 'Perfect Health', 'Permanent Emanation', 'Planar Turning',
             'Positive Energy Aura', 'Spectral Strike', 'Spontaneous Casting',
             'Widen Area of Courage']
    # special mount

    @staticmethod
    def prereq(character, special=False):
        '''Special: Must complete a quest that impresses your patron deity, who may not have another emissary.'''
        return (special and 'epic' in character.build.active and
                character.BAB >= 23 and
                character.deity and
                all(x in character.feats.active
                    for x in [f'Weapon focus ({character.deity.weapon})', 'Great Smiting']) and
                character.skills['Knowledge (religion)'].ranks >= 10)

#%% Epic infiltrator
class EpicInfiltrator(EpicClass, core.PrestigeClass):
    _name = 'epic infiltrator'
    _hit_die = 6; skill_points = 8
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Craft', 'Decipher Script',
                     'Diplomacy', 'Disable Device', 'Disguise', 'Escape Artist', 'Forgery',
                     'Gather Information', 'Hide', 'Intimidate', 'Jump', 'Listen', 'Move Silently',
                     'Open Lock', 'Profession', 'Sense Motive', 'Sleight of Hand', 'Spot']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield', 'tower shield']
    pattern = [(1, 4, 'improved cover identity'),
               (1, 3, 'sneak attack'),
               (2, 3, 'specialist training'),
               (3, 4, 'read thoughts'),
               (4, 2, 'far senses'),
               (3, 8, 'mind blank')]

    @staticmethod
    def prereq(character, special=False):
        '''Special: Must have successfully spent one month posing as someone else.'''
        return (special and 'epic' in character.build.active and
                character.alignment!='chaotic' and
                all(character.skills[x].ranks >= 24 for x in ['Bluff', 'Disguise']) and
                all(character.skills[x].ranks >= 10 for x in ['Diplomacy', 'Spot']) and
                all(x in character.feats.active for x in ['Alertness', 'Polyglot']))

class ImprovedCoverIdentity(core.Feature):
    _name = 'improved cover identity'
    def escalate(self): self.grade.attribute += 1

class SpecialistTraining(core.Feature):
    _name = 'specialist training'
    _tags = ['extraordinary']
    options = {'concealment': ['Bluff', 'Disguise', 'Forgery'],
               'subterfuge': ['Hide', 'Move Silently', 'Open Lock', 'Sleight of Hand'],
               'espionage': ['Listen', 'Search', 'Spot'],
               'interaction': ['Diplomacy', 'Gather Information', 'Intimidate', 'Sense Motive']}
    def escalate(self): self.grade.attribute += 1

class ReadThoughts(core.Feature):
    _name = 'read thoughts'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

class FarSenses(core.Feature):
    _name = 'far senses'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

class MindBlank(core.Feature):
    _name = 'mind blank'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

#%% Guardian paramount
class GuardianParamount(EpicClass, core.PrestigeClass):
    _hit_die = 10; skill_points = 4
    _class_skills = ['Bluff', 'Climb', 'Diplomacy', 'Intimidate', 'Jump', 'Listen', 'Profession',
                     'Spot']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield', 'tower shield']
    pattern = [(1, 3, 'BonusFeat'),
               (1, 3, 'uncanny dodge enabler'),
               (2, 3, 'evasive preceptor'),
               (3, 3, 'protective aura'),
               (5, 3, 'adjust probability'),
               (6, 6, 'call back')]
    feats = ['Bulwark of Defense', 'Combat Archery', 'Damage Reduction', 'Dexterous Fortitude',
        'Dexterous Will', 'Epic Dodge', 'Epic Fortitude', 'Epic Reflexes', 'Epic Reputation',
        'Epic Skill Focus', 'Epic Speed', 'Epic Toughness', 'Epic Will', 'Exceptional Deflection',
        'Fast Healing', 'Great Dexterity', 'Improved Combat Reflexes', 'Improved Sneak Attack',
        'Improved Spell Resistance', 'Infinite Deflection', 'Legendary Climber', 'Lingering Damage',
        'Mobile Defense', 'Perfect Health', 'Reflect Arrows', 'Self-Concealment',
        'Sneak Attack of Opportunity', 'Spellcasting Harrier', 'Trap Sense', 'Uncanny Accuracy']

    @staticmethod
    def prereq(character):
        return ('epic' in character.build.active and
                character.BAB >= 15 and
                character.skills['Spot'].ranks >= 13 and
                all(x in character.feats.active
                    for x in ['Alertness', 'Lightning Reflexes', 'Blinding Speed', 'Superior Initiative']) and
                all(x in character.features.active for x in ['uncanny dodge', 'evasion']))

class UncannyDodgeEnabler(core.Feature):
    _name = 'uncanny dodge enabler'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class EvasivePreceptor(core.Feature):
    _name = 'evasive preceptor'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class ProtectiveAura(core.Feature):
    _name = 'protective aura'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class AdjustProbability(core.Feature):
    _name = 'adjust probability'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class CallBack(core.Feature):
    _name = 'call back'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

#%% High proselytizer
class HighProselytizer(EpicClass, core.PrestigeClass):
    _name = 'high proselytizer'
    _hit_die = 8; skill_points = 2
    _class_skills = ['Concentration', 'Craft', 'Diplomacy', 'Heal', 'Knowledge (arcana)',
                     'Knowledge (religion)', 'Profession', 'Sense Motive', 'Spellcraft']
    proficiencies = ['simple', 'light', 'medium', 'heavy', 'shield', 'tower shield']
    pattern = [(2, 2, 'DivineCasterLevel'),
               (1, 10, 'proselytize'),
               (3, 10, 'deific touch'),
               (5, 10, 'deific word'),
               (7, 10, 'deific face'),
               (9, 10, 'deific aura'),
               (2, 4, 'heal'),
               (4, 4, 'BonusFeat')]
    feats = ['Armor Skin', 'Automatic Quicken Spell', 'Automatic Silent Spell',
             'Automatic Still Spell', 'Bonus Domain', 'Enhance Spell', 'Epic Reputation',
             'Epic Spell Focus', 'Epic Spell Penetration', 'Epic Spellcasting', 'Epic Will',
             'Extended Life Span', 'Great Charisma', 'Great Wisdom', 'Ignore Material Components',
             'Improved Alignment-Based Casting', 'Improved Combat Casting',
             'Improved Heighten Spell', 'Improved Metamagic', 'Improved Spell Capacity',
             'Intensify Spell', 'Legendary Commander', 'Multispell', 'Negative Energy Burst',
             'Permanent Emanation', 'Planar Turning', 'Polyglot', 'Positive Energy Aura',
             'Spectral Strike', 'Spell Stowaway', 'Spell Opportunity', 'Spontaneous Domain Access',
             'Spontaneous Spell', 'Tenacious Magic', 'Undead Mastery', 'Zone of Animation']
    @staticmethod
    def prereq(character):
        divine = [x for x in character.features.active
                  if util.is_a(x, 'spellcasting') and x.magic_type=='divine']
        return ('epic' in character.build.active and
                character.skills['Diplomacy'].ranks >= 12 and
                any(character.skills[x].ranks >= 24 for x in ['Knowledge (nature)', 'Knowledge (religion)']) and
                all(x in character.feats.active for x in ['Leadership', 'Epic Leadership']) and
                any(any(spell.level >= 5 for spell in x.spells_known) for x in divine) and
                character.deity)

class Proselytize(core.Feature):
    _name = 'proselytize'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class ProselytizeAbility(core.Feature):
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class DeificTouch(ProselytizeAbility): _name = 'deific touch'
class DeificWord(ProselytizeAbility): _name = 'deific word'
class DeificFace(ProselytizeAbility): _name = 'deific face'
class DeificAura(ProselytizeAbility): _name = 'deific aura'

class Heal(core.Feature):
    _name = 'heal'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

#%% Legendary dreadnought
class LegendaryDreadnought(EpicClass, core.PrestigeClass):
    _name = 'legendary dreadnought'
    _hit_die = 12; skill_points = 2
    _class_skills = ['Climb', 'Craft', 'Intimidate', 'Jump', 'Swim']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield', 'tower shield']
    pattern = [(1, 5, 'unstoppable'),
               (2, 5, 'unmovable'),
               (3, 5, 'shrug off punishment'),
               (4, 5, 'thick skinned'),
               (5, 5, 'BonusFeat')]
    feats = ['Armor Skin', 'Devastating Critical', 'Dire Charge', 'Epic Fortitude', 'Epic Prowess',
             'Epic Toughness', 'Epic Weapon Focus', 'Epic Weapon Specialization', 'Fast Healing',
             'Great Constitution', 'Great Strength', 'Improved Combat Reflexes',
             'Overwhelming Critical', 'Penetrate Damage Reduction']

    @staticmethod
    def prereq(character):
        return ('epic' in character.build.active and
                character.BAB >= 23 and
                character.skills['Intimidate'].ranks >= 15 and
                all(x in character.feats.active for x in [
                    'Combat Reflexes', 'Great Cleave', 'Improved Bull Rush', 'Improved Critical']))

class Unstoppable(core.Feature):
    _name = 'unstoppable'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class Unmovable(core.Feature):
    _name = 'unmovable'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class ShrugOffPunishment(core.Feature):
    _name = 'shrug off punishment'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

class ThickSkinned(core.Feature):
    _name = 'thick skinned'
    _tags = ['extraordinary']
    def escalate(self): self.grade.attribute += 1

#%% Perfect wight
class PerfectWight(EpicClass, core.PrestigeClass):
    _name = 'perfect wight'
    _hit_die = 6; skill_points = 8
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Craft', 'Disable Device',
                     'Diplomacy', 'Disguise', 'Escape Artist', 'Gather Information', 'Hide', 'Jump',
                     'Knowledge', 'Listen', 'Move Silently', 'Open Lock', 'Search', 'Sense Motive',
                     'Spot', 'Survival', 'Tumble', 'Use Rope']
    pattern = [(1, 5, 'improved invisibility'),
               (2, 5, 'improved legerdemain'),
               (3, 5, 'incorporeal'),
               (4, 5, 'shadow form'),
               (5, 5, 'BonusFeat')]
    feats = ['Blinding Speed', 'Combat Archery', 'Dexterous Fortitude', 'Dexterous Will',
             'Epic Dodge', 'Epic Reputation', 'Epic Skill Focus', 'Epic Speed',
             'Improved Combat Reflexes', 'Improved Sneak Attack', 'Legendary Climber',
             'Lingering Damage', 'Self-Concealment', 'Sneak Attack of Opportunity',
             'Spellcasting Harrier', 'Superior Initiative', 'Trap Sense', 'Uncanny Accuracy']

    @staticmethod
    def prereq(character):
        if 'sneak attack' not in character.features.active: return False
        sa = character.features.get_one(name='sneak attack', status='active')
        return ('epic' in character.build.active and
                all(character.skills[x].ranks >= 24 for x in ['Hide', 'Move Silently']) and
                'Self-Concealment' in character.feats.active and
                sa.grade >= 10)

class ImprovedInvisibility(core.Feature):
    _name = 'improved invisibility'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

class ImprovedLegerdemain(core.Feature):
    _name = 'improved legerdemain'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

class Incorporeal(core.Feature):
    _name = 'incorporeal'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

class ShadowForm(core.Feature):
    _name = 'shadow form'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

#%% Union sentinel
class UnionSentinel(EpicClass, core.PrestigeClass):
    _name = 'union sentinel'
    _hit_die = 10; skill_points = 2
    _class_skills = ['Diplomacy', 'Gather Information', 'Intimidate', 'Knowledge (local)', 'Listen',
                     'Profession', 'Search', 'Sense Motive', 'Spot']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield', 'tower shield']
    pattern = [(1, 7, 'sending'),
               (1, 3, 'shield of law'),
               (2, 6, 'freedom'),
               (2, 4, 'knock'),
               (3, 3, 'dimensional anchor'),
               (4, 6, 'portal guardian'),
               (5, 5, 'forcecage'),
               (7, 5, 'imprisonment')]

    @staticmethod
    def prereq(character, special=False):
        '''Special: Must reside in the demiplane-city of Union.'''
        return (special and 'epic' in character.build.active and
                character.alignment=='lawful' and
                character.BAB >= 21 and
                character.skills['Diplomacy'].ranks >= 8 and
                character.skills['Knowledge (local)'].ranks >= 3 and
                all(x in character.feats.active
                    for x in ['Alertness', 'Improved Disarm', 'Armor Skin']))

class Sending(core.Feature):
    _name = 'sending'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class ShieldOfLaw(core.Feature):
    _name = 'shield of law'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class Freedom(core.Feature):
    _name = 'freedom'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class Knock(core.Feature):
    _name = 'knock'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class DimensionalAnchor(core.Feature):
    _name = 'dimensional anchor'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class PortalGuardian(core.Feature):
    _name = 'portal guardian'
    _tags = ['supernatural']
    def escalate(self): self.grade.attribute += 1

class Forcecage(core.Feature):
    _name = 'forcecage'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1

class Imprisonment(core.Feature):
    _name = 'imprisonment'
    _tags = ['spell-like']
    def escalate(self): self.grade.attribute += 1
