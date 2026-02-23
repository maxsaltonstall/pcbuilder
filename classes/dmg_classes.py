# -*- coding: utf-8 -*-

import core, phb
import utilities as util
sourcebook = "Dungeon Master's Guide"

class AlternateClassFeature(): ... # mix-in

class Witch(phb.classes.Sorcerer): _name = 'witch'
class WitchSpellcasting(core.Focus, phb.classes.SorcererSpellcasting):
    _spell_list = {
        0: ['arcane mark', 'cure minor wounds', 'dancing lights', 'daze', 'detect magic',
            'detect poison', 'flare', 'ghost sound', 'light', 'mending', 'read magic', 'resistance',
            'virtue'],
        1: ['cause fear', 'change self', 'charm person', 'command', 'comprehend languages',
            'cure light wounds', 'doom', 'endure elements', 'hypnotism', 'identify', 'silent image',
            'sleep', 'speak with animals', 'ventriloquism'],
        2: ['alter self', 'blindness/deafness', 'calm emotions', 'cure moderate wounds',
            'delay poison', 'detect throughts', 'enthrall', 'invisibility', 'locate object',
            'minor image', 'scare', 'whispering wind'],
        3: ['bestow curse', 'clairaudience/clairvoyance', 'contagion', 'create food and water',
            'dispel magic', "Leomund's tiny hut", 'major image', 'rage',
            'remove blindness/deafness', 'suggestion', 'tongues'],
        4: ['charm monster', 'crushing despair', 'discern lies', 'divination', 'fear',
            'giant vermin', 'good hope', 'locate creature', 'minor creation', 'neutralize poison',
            'polymorph', 'remove curse', 'scrying'],
        5: ['baleful polymorph', 'dream', 'false vision', 'feeblemind', 'greater command',
            'magic jar', 'major creation', 'mirage arcana', 'nightmare', 'seeming', 'sending'],
        6: ['animate objects', 'control weather', 'eyebite', 'find the path', 'geas/quest',
            'greater scrying', "heroes' feast", 'legend lore', 'mass suggestion', 'mislead',
            'repulsion', 'shadow image', "Tenser's transformation", 'true seeing'],
        7: ['creeping doom', 'finger of death', 'insanity', 'liveoak', 'repel wood',
            'transport via plants'],
        8: ['antipathy', 'demand', 'discern location', 'horrid wilting', 'polymorph any object',
            'sympathy', 'trap the soul'],
        9: ['earthquake', 'foresight', 'refuge', 'shapechange', 'wail of the banshee', 'weird']}
    def __init__(self, character, focus=None):
        super().__init__(character, focus)
        self.fpipe_.subscribe(lambda x: self.spell_list[3].append(f'magic circle against {x}'),
                              util.log_error)
    def eligible(self, focus):
        if focus not in ['good', 'evil', 'chaos', 'law']: return False
        return not self.character.alignment==focus

class WitchSpellcastingACF(AlternateClassFeature, WitchSpellcasting):
    _name = 'witch'; level = 1; replaces = {1:'spellcasting'}

#%% NPC classes
class Adept(core.NPCClass):
    _name = 'adept'
    _hit_die = 6; skill_points = 2; proficiencies = ['simple']; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Handle Animal', 'Heal', 'Knowledge', 'Profession',
                     'Spellcraft', 'Survival']
    features = {1: ['Spellcasting'], 2: ['summon familiar']}

class AdeptSpellcasting(core.Spellcasting):
    _ability = 'wisdom'
    magic_type = 'divine'
    caster_type = 'prepared'
    _spells_per_day = {
        1: [3,1], 2: [3,1], 3: [3,2],
        4: [3,2,0], 5: [3,2,1], 6: [3,2,1], 7: [3,3,2],
        8: [3,3,2,0], 9: [3,3,2,1], 10: [3,3,2,1], 11: [3,3,3,2],
        12: [3,3,3,2,0], 13: [3,3,3,2,1], 14: [3,3,3,2,1], 15: [3,3,3,3,2],
        16: [3,3,3,3,2,0], 17: [3,3,3,3,2,1], 18: [3,3,3,3,2,1],
        19: [3,3,3,3,3,2], 20: [3,3,3,3,3,2],
        }
    _spell_list = {
        0: ['create water', 'cure minor wounds', 'detect magic', 'ghost sound', 'guidance', 'light',
            'mending', 'purify food and drink', 'read magic', 'touch of fatigue'],
        1: ['bless', 'burning hands', 'cause fear', 'command', 'comprehend languages',
            'cure light wounds', 'detect chaos', 'detect evil', 'detect good', 'detect law',
            'endure elements', 'obscuring mist', 'protection from chaos', 'protection from evil',
            'protection from good', 'protection from law', 'sleep'],
        2: ['aid', 'animal trance', "bear's endurance", "bull's strength", "cat's grace",
            'cure moderate wounds', 'darkness', 'delay poison', 'invisibility', 'mirror image',
            'resist energy', 'scorching ray', 'see invisibility', 'web'],
        3: ['animate dead', 'bestow curse', 'contagion', 'continual flame', 'cure serious wounds',
            'daylight', 'deeper darkness', 'lightning bolt', 'neutralize poison', 'remove curse',
            'remove disease', 'tongues'],
        4: ['cure critical wounds', 'minor creation', 'polymorph', 'restoration', 'stoneskin',
            'wall of fire'],
        5: ['baleful polymorph', 'break enchantment', 'commune', 'heal', 'major creation',
            'raise dead', 'true seeing', 'wall of stone']}
    def __init__(self, character):
        super().__init__(character)
        self.spell_list = core.SpellList()
        for level, spells in self._spell_list:
            self.spell_list.add(item=spells, level=level)

class Aristocrat(core.NPCClass):
    _name = 'aristocrat'
    _hit_die = 8; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Will']
    _class_skills = ['Appraise', 'Bluff', 'Diplomacy', 'Disguise', 'Forgery', 'Gather Information',
        'Handle Animal', 'Intimidate', 'Knowledge', 'Listen', 'Perform', 'Ride', 'Sense Motive',
        'Speak Language', 'Spot', 'Swim', 'Survival']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield', 'tower shield']

class _Sentinel(util.StatusItem):
    _name = 'sentinel item'
    def __init__(self, check, replace):
        super().__init__()
        self._check = check
        self._replace = replace

    def __eq__(self, other):
        if self._check(other):
            self._replace(other)
            return True
        else: return False

class Commoner(core.NPCClass):
    _name = 'commoner'
    _hit_die = 4; skill_points = 2; bab_type = 'half'
    _class_skills = ['Climb', 'Craft', 'Handle Animal', 'Jump', 'Listen', 'Profession', 'Ride',
                    'Spot', 'Swim', 'Use Rope']

    def __init__(self, character):
        super().__init__(character)

        def check_weapon_type(other):
            try: x = self.character.lib.get(other)
            except StopIteration: return False
            return 'simple' in x.proficiency_categories

        def replace_sentinel_proficiency(other):
            util.logger.info('Replacing sentinel item with %s', other)
            self.character.proficiencies.remove_all(source=self)
            self.character.proficiencies.add(name=other, source=self)

        sentinel_proficiency = _Sentinel(check_weapon_type, replace_sentinel_proficiency)
        self.character.proficiencies.add(obj=sentinel_proficiency)

class _LazyList(list):
    def __init__(self, limit):
        super().__init__()
        self._limit = limit

    def __contains__(self, item):
        x = super().__contains__(item)
        if not x:
            if len(self < self._limit):
                self.append(item)
                util.logger.info('Added new item to lazy list: %s', item)
                return True
        return x

class Expert(core.NPCClass):
    _name = 'expert'
    _hit_die = 6
    skill_points = 6
    proficiencies = ['simple', 'light']
    bab_type = 'three quarters'
    good_saves = ['Will']
    def __init__(self, character):
        super().__init__(character)
        self.class_skills = _LazyList(10)

class Warrior(core.NPCClass):
    _name = 'warrior'
    _hit_die = 8; skill_points = 2; bab_type = 'full'; good_saves = ['Fortitude']
    class_skills = ['Climb', 'Handle Animal', 'Intimidate', 'Jump', 'Ride', 'Swim']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield', 'tower shield']
