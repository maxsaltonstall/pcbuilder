#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 13:52:28 2025
@author: gtauxe
"""

import core, phb.classes
import splat.epic_level_handbook as elh
import utilities as util
sourcebook = 'Complete Arcane'

#%% Warlock
class Warlock(core.Class):
    _name = 'warlock'
    _hit_die = 6; skill_points = 2; bab_type = 'three quarters'; good_saves = ['Will']
    _class_skills = ['Bluff', 'Concentration', 'Craft', 'Disguise', 'Intimidate', 'Jump',
                     'Knowledge (arcana)', 'Knowledge (the planes)', 'Knowledge (religion)',
                     'Profession', 'Sense Motive', 'Spellcraft', 'Use Magic Device']
    proficiencies = ['simple', 'light']
    advancement = core.get_class_advancement({
        'eldritch blast': [1,3,5,7,9,11,14,17,20],
        'invocations': [1,6,11,16],
        'DetectMagic': [2],
        'DamageReduction': list(range(3,21,4)),
        'deceive item': [4],
        'fiendish resilience': [8,13,18],
        'WarlockER': [10,20],
        'imbue item': [12]
        })

    def DetectMagic(self):
        self.character.magic.spell_like_abilities.add(name='detect magic', frequency='at will',
            caster_level=self.level, source=self)

    def DamageReduction(self):
        self.character.resistances.damage_reduction['cold iron'].add(self.grade, 'base', source=self)

    @staticmethod
    def prereq(character): return character.alignment=='evil' or character.alignment=='chaotic'

class EpicWarlock(elh.EpicClass, Warlock):
    _name = 'epic warlock'
    def __init__(self, character): raise NotImplementedError
    # eldritch blast dmg improves every 22+2
    # DR improves every 23+4
    # bonus feat every 23+3

class EldritchBlast(core.Feature):
    _name = 'eldritch blast'
    _tags = ['spell-like']
    # spell level = 1st, it is an invocation (see errata)

class Invocations(core.Spellcasting):
    _name = 'invocations'
    # ignore ASF from light armor only
    # caster level = warlock level
    retrain = [6,11,16]
    _invocations_known = {
        1: [1], 2: [2], 4: [3], 6:[4], 8:[5], 10:[6], 11:[7], 13:[8], 15:[9], 16:[10], 18:[11], 20:[12]
        }

class DeceiveItem(phb.classes.SkillMastery):
    _name = 'deceive item'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.add_skills('use magic device', source=self)

class FiendishResilience(core.Feature):
    _name = 'fiendish resilience'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class WarlockER(core.Feature):
    _name = 'energy resistance'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(5)
        self.types = []
        def check_ER_types():
            if len(self.types) < 2:
                util.logger.warning('Declare 2 energy types to apply warlock energy resistance.')
        self.character.add_to_build(-2, 1, check_ER_types)

    def add_types(self, types):
        if isinstance(types, list):
            for x in types: self.add_types(x)
            return
        x = types
        if x in self.types: return
        if len(self.types) >= 2: raise util.NotEligible(x)
        if x not in ['acid', 'cold', 'electricity', 'fire', 'sonic']: raise util.NotEligible
        self.character.resistances.energy_resistance[x].add(self.grade, 'base', source=self)
        self.types.append(x)

    def escalate(self): self.grade.attribute += 5

class ImbueItem(core.Feature):
    _name = 'imbue item'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

#%% Warmage
class Warmage(core.Class):
    _name = 'warmage'
    _hit_die = 6; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Intimidate', 'Knowledge (arcana)',
                     'Knowledge (history)', 'Profession', 'Spellcraft']
    proficiencies = ['simple', 'light', 'light shield']
    advancement = core.get_class_advancement({
        ('Spellcasting', 'warmage edge'): [1],
        'armored mage': [1,8],
        'advanced learning': [3,6,11,16],
        'SuddenEmpower': [7],
        'SuddenEnlarge': [10],
        'SuddenWiden': [15],
        'SuddenMaximize': [20]
        })
    def SuddenEmpower(self): self.BonusFeat('Sudden Empower')
    def SuddenEnlarge(self): self.BonusFeat('Sudden Enlarge')
    def SuddenWiden(self): self.BonusFeat('Sudden Widen')
    def SuddenMaximize(self): self.BonusFeat('Sudden Maximize')

    def BonusFeat(self, feat):
        if feat in self.character.feats.active:
            is_metamagic = lambda x: util.is_a(x, 'metamagic')
            self.character.feats.feat_slots.add(1, source=self, restriction=is_metamagic)
        else:
            self.character.feats.add(name=feat, source=self, override=True)

class EpicWarmage(elh.EpicClass, Warmage):
    _name = 'epic warmage'
    def __init__(self, character): raise NotImplementedError
    # advanced learning every 21+4
    #bonus feat (23+3) from list; override=True
    bonus_feats = ['Automatic Silent Spell', 'Automatic Still Spell', 'Craft Epic Magic Arms and Armor',
                   'Craft Epic Rod', 'Craft Epic Staff', 'Craft Epic Wondrous Item', 'Efficient Item Creation',
                   'Energy Resistance', 'Enhance Spell', 'Epic Spell Focus', 'Epic Spell Penetration',
                   'Epic Spellcasting', 'Ignore Material Components', 'Improved Combat Casting',
                   'Improved Heighten Spell', 'Improved Metamagic', 'Improved Spell Capacity',
                   'Intensify Spell', 'Master Staff', 'Master Wand', 'Scribe Epic Scroll', 'Spell Opportunity',
                   'Spell Stowaway', 'Spellcasting Harrier', 'Tenacious Magic']

class WarmageSpellcasting(core.Spellcasting):
    _name = 'spellcasting'
    _ability = 'charisma'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    # spells known = spell list
    _spells_per_day = dict(phb.classes.SorcererSpellcasting._spells_per_day)
    _spells_per_day[20] = [6,6,6,6,6,6,6,6,6,5]
    _spell_list = {
        0: ['acid splash', 'disrupt undead', 'light', 'ray of frost'],
        1: ['accuracy', 'burning hands', 'chill touch', 'fist of stone', 'hail of stone',
            'magic missile', 'lesser orb of acid', 'lesser orb of cold',
            'lesser orb of electricity', 'lesser orb of fire', 'lesser orb of sound',
            'shocking grasp', 'true strike'],
        2: ['blades of fire', 'continual flame', 'fire trap', 'fireburst', 'flaming sphere',
            'ice knife', "Melf's acid arrow", 'pyrotechnics', 'scorching ray', 'shatter',
            'whirling blade'],
        3: ['fire shield', 'fireball', 'flame arrow', 'gust of wind', 'ice storm', 'lightning bolt',
            'poison', 'ring of blades', 'sleet storm', 'stinking cloud'],
        4: ['blast of flame', 'contagion', "Evard's black tentacles", 'orb of acid', 'orb of cold',
            'orb of electricity', 'orb of fire', 'orb of force', 'orb of sound',
            'phantasmal killer', 'shout', 'wall of fire'],
        5: ['arc of lightning', 'cloudkill', 'cone of cold', 'mass fire shield',
            'greater fireburst', 'flame strike', 'prismatic ray'],
        6: ['acid fog', 'blade barrier', 'chain lightning', 'circle of death', 'disintegrate',
            'fire seeds', "Otiluke's freezing sphere", "Tenser's transformation"],
        7: ['delayed blast fireball', 'earthquake', 'finger of death', 'fire storm',
            "Mordenkainen's sword", 'prismatic spray', 'sunbeam', 'waves of exhaustion'],
        8: ['horrid wilting', 'incendiary cloud', 'polar ray', 'prismatic wall',
            'scintillating pattern', 'greater shout', 'sunburst'],
        9: ['elemental swarm', 'implosion', 'meteor swarm', 'prismatic sphere',
            'wail of the banshee', 'weird']
        }

class ArmoredMage(core.Feature):
    _name = 'armored mage'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

    def escalate(self): raise NotImplementedError

class WarmageEdge(core.Feature):
    _name = 'warmage edge'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.Attribute()
        self.grade.add(self.character.INT, 'INT')
        raise NotImplementedError

class AdvancedLearning(core.Feature):
    _name = 'advanced learning'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Wu jen
class WuJen(core.Class):
    _name = 'wu jen'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Knowledge', 'Profession', 'Spellcraft']
    proficiencies = ['simple']
    bonus_languages = ['Draconic', 'Giant']
    advancement = core.get_class_advancement({
        ('watchful spirit', 'BonusFeat'): [1],
        'spell secret': [3,9,12,15,18],
        'elemental mastery': [6]
        })
    feats = ['metamagic']
    def __init__(self, character):
        super().__init__(character)
        self.taboos = util.FeatureList() # 1 at first level + 1 with every spell secret
            # violating taboos cuts off spellcasting for that day

    def Spellcasting(self):
        super().Spellcasting()
        self.spellcasting.add_condition(self.code_of_conduct_)

    @staticmethod
    def prereq(character): return character.alignment != 'lawful'

class EpicWuJen(elh.EpicClass, WuJen):
    _name = 'epic wu jen'
    def __init__(self, character): raise NotImplementedError
    # learn 2 new spells every level
    # spell secret every 21+3 from
        # Enlarge Spell, 'Extend Spell', 'Still Spell', 'Silent Spell'
        # + taboo
    # bonus feats every 23+3, override=True
    bonus_feats = ['Augmented Alchemy', 'Automatic Quicken Spell', 'Automatic Silent Spell',
                   'Automatic Still Spell', 'Enhance Spell', 'Epic Spell Focus', 'Epic Spell Penetration',
                   'Epic Spellcasting', 'Ignore Material Components', 'Improved Combat Casting',
                   'Improved Heighten Spell', 'Improved Metamagic', 'Improved Spell Capacity',
                   'Intensify Spell', 'Multispell', 'Permanent Emanation', 'Spell Knowledge',
                   'Spell Opportunity', 'Spell Stowaway', 'Spontaneous Spell', 'Superior Initiative',
                   'Tenacious Magic']

class WuJenSpellcasting(core.Spellcasting):
    _name = 'spellcasting'
    _ability = 'intelligence'
    magic_type = 'arcane'
    caster_type = 'prepared'
    _spells_per_day = dict(phb.classes.WizardSpellcasting._spells_per_day)
    _spell_list = {
        0: ['arcane mark', 'daze', 'detect magic', 'detect poison', 'disrupt undead', 'ghost sound',
            'light', 'mage hand', 'mending', 'message', 'open/close', 'prestidigitation',
            'read magic', 'resistance'],
        1: ['animate rope', 'charm person', 'comprehend languages', 'detect chaos', 'detect evil',
            'detect good', 'detect law', 'disguise self', 'hold portal', 'hypnotism', 'jump',
            'magic missile', 'protection from chaos', 'protection from evil',
            'protection from good', 'protection from law', 'shield', 'silent image', 'sleep',
            'summon monster I', 'true strike', 'unseen servant', 'ventriloquism'],
        2: ['alter self', 'arcane lock', 'blur', 'detect thoughts', 'hold person',
            'hypnotic pattern', 'invisibility', 'knock', 'locate object', 'minor image',
            'misdirection', 'rope trick', 'see invisibility', 'spider climb', 'summon monster II',
            'whispering wind'],
        3: ['dispel magic', 'displacement', 'haste', 'illusory script',
            'magic circle against chaos', 'magic circle against evil', 'magic circle against good',
            'magic circle against law', 'major image', 'remove curse', 'suggestion',
            'summon monster III', 'tongues'],
        4: ['animate dead', 'charm monster', 'confusion', 'crushing despair', 'dismissal',
            'lesser globe of invulnerability', 'good hope', 'greater invisibility',
            'locate creature', 'minor creation', 'polymorph', 'shout', 'summon monster IV'],
        5: ['animal growth', 'baleful polymorph', 'dominate person', 'dream', 'fabricate',
            'feeblemind', 'hold monster', 'major creation', 'nightmare', 'passwall', 'permanency',
            'persistent image', 'summon monster V', 'symbol of pain', 'symbol of sleep',
            'telekinesis', 'teleport', 'wall of force'],
        6: ['control weather', 'greater dispel magic', 'geas/quest', 'globe of invulnerability',
            'permanent image', 'programmed image', 'repulsion', 'speak with dead',
            'mass suggestion', 'summon monster VI', 'symbol of fear', 'symbol of persuasion',
            'true seeing', 'veil'],
        7: ['disintegrate', 'ethereal jaunt', 'limited wish', 'power word blind',
            'summon monster VII', 'symbol of stunning', 'symbol of weakness', 'greater teleport',
            'teleport object'],
        8: ['antipathy', 'mind blank', 'polymorph any object', 'power word stun',
            'summon monster VIII', 'symbol of death', 'symbol of insanity', 'sympathy',
            'whirlwind'],
        9: ['astral projection', 'dominate monster', 'etherealness', 'freedom', 'gate',
            'imprisonment', 'power word kill', 'shapechange', 'summon monster IX',
            'teleportation circle', 'time stop', 'wish']
        }
    _all_spells = {
        1: ['endure elements'], 2: ['resist energy'], 3: ['protection from energy'],
        4: ['scrying'], 7: ['greater scrying']
        }
    _earth_spells = {
        2: ["bear's endurance", "bull's strength"], 4: ['dimension door', 'stoneskin'],
        5: ['stone shape', 'wall of stone'], 6: ['flesh to stone', 'move earth', 'stone to flesh'],
        7: ['statue'], 8: ['earthquake']
        }
    _fire_spells = {
        0: ['dancing lights', 'flare'], 2: ["cat's grace", 'pyrotechnics'], 3: ['fireball'],
        4: ['fire shield', 'fire trap', 'wall of fire'], 6: ['fire seeds'],
        7: ['delayed blast fireball'], 8: ['incendiary cloud']
        }
    _metal_spells = {
        1: ['magic weapon'], 2: ['protection from arrows'],
        3: ['keen edge', 'greater magic weapon'], 4: ['rusting grasp'], 6: ['wall of iron'],
        8: ['repel metal or stone']
        }
    _water_spells = {
        0: ['ray of frost'], 1: ['obscuring mist'], 2: ['fog cloud'],
        3: ['gaseous form', 'stinking cloud', 'water breathing'],
        4: ['ice storm', 'solid fog', 'wall of ice'], 5: ['cone of cold'], 6: ['control water'],
        8: ['horrid wilting']
        }
    _wood_spells = {
        2: ['warp wood', 'wood shape'], 3: ['plant growth'],
        4: ['antiplant shell', 'command plants'], 6: ['ironwood', 'repel wood'],
        7: ['transmute metal to wood'], 8: ['control plants']
        }

class WatchfulSpirit(core.Feature):
    _name = 'watchful spirit'
    def __init__(self, character): raise NotImplementedError

class SpellSecret(core.Feature):
    _name = 'spell secret'
    def __init__(self, character): raise NotImplementedError

class ElementalMastery(core.Feature):
    _name = 'elemental mastery'
    def __init__(self, character): raise NotImplementedError

# Spellbook:
    # start with all 0th level wu jen spells + 3+INT 1st-level spells
    # gain 2 spells at each level up
    # add new spells as a wizard
