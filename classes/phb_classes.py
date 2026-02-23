#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:44:25 2025
@author: gtauxe
"""

import reactivex as rx
import reactivex.operators as ops
from reactivex.subject import BehaviorSubject
import string

import core
import utilities as util
sourcebook = "Player's Handbook"

#%% Barbarian
class Barbarian(core.Class):
    _name = 'barbarian'
    _hit_die = 12; skill_points = 4; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Climb', 'Craft', 'Handle Animal', 'Intimidate', 'Jump', 'Listen', 'Ride',
                     'Survival', 'Swim']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'shield']
    starting_gold = '4d4 x 10'; start = 'simple'
    advancement = core.get_class_advancement({
        'Rage': [1,4,8,12,16,20],
        ('Illiteracy', 'BarbarianFastMovement'): [1],
        'UncannyDodge': [2,5],
        'TrapSense': list(range(3,21,3)),
        'DamageReduction': list(range(7,21,3)),
        'GreaterRage': [11],
        'IndomitableWill': [14],
        'TirelessRage': [17],
        'MightyRage': [20]
        })

    def DamageReduction(self):
        dr = self.character.features.add_if_missing(item='DamageReduction', source=self)
        dr.add(1, 'slash', source=self)

    def Rage(self):
        rage = self.character.features.add(name='rage', source=self)
        rage.add_condition(self.code_of_conduct_)

    @staticmethod
    def _prereqs(character):
        return [character.alignment.attribute_.pipe(
            ops.map(lambda x: 'lawful' not in x), ops.distinct_until_changed())]

    def live_prereq(self):
        self._prereqs(self.character)[0].subscribe(self.code_of_conduct_.on_next, util.log_error)

class Illiteracy(core.Feature):
    _name = 'illiteracy'
    def __init__(self, character):
        super().__init__(character)
        self.character.build._sum_attribute('literate').pipe(
            ops.map(lambda p: not p),
            ops.distinct_until_changed()
            ).subscribe(self.active_.on_next, on_error=util.log_error)

class BarbarianFastMovement(core.Feature):
    _name = 'fast movement'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        encumbrance_test_ = self.character.equipment.encumbrance_.pipe(
            ops.map(lambda p: p!='heavy')
            )
        self.character.speed['land'].add(10, source=self, condition=encumbrance_test_)

class DamageReduction(core.Feature):
    _name ='damage reduction'
    def add(self, value, damage_type, source):
        self.character.damage_reduction[damage_type].add(value, 'base', source=source)
        #TODO: per MM.errata
        #slashing/piercing/bludgeoning/adamantine/slash -> Extraordinary
        #magic/epic/silver/cold iron/aligned -> Supernatural

class IndomitableWill(core.Feature):
    _name = 'indomitable will'
    def __init__(self, character):
        super().__init__(character)
        c_ = self.character.challenges.register(challenge='enchantment')[0]
        self.character.saves['Will'].add(4, condition=c_, source=self)

class Rage(core.Feature):
    _name = 'rage'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.rage = self.character.conditions.add(obj=_Rage(self.character))
        not_rage_ = self.rage.active_.pipe(ops.map(lambda p: not p))
        self.frequency = util.Frequency(self.grade, 1, 'day')
        self.character.actions.free.add(name='rage', source=self, frequency=self.frequency,
            method=self.rage, condition=not_rage_)
    def rage(self): self.character.conditions.activate(name='rage')

class _Rage(core.Condition):
    _name = 'rage'
    _tags = ['extraordinary']
    _duration = 3

    def __init__(self, character):
        super().__init__(character)
        self.duration.add(character.CON, 'CON')
        self.grade = util.NumeralAttribute(2)
        self.tireless = False
        self.fatigue_counter = 0

    def _initialize(self):
        rage_bonus = util.LiveAttribute(self.grade, lambda x: 2*x)
        self.character.abilities['strength'].add(rage_bonus, source=self)
        self.character.abilities['constitution'].add(rage_bonus, source=self)
        self.character.saves['Will'].add(self.grade, 'morale', source=self)
        self.character.AC['all'].add(-2, source=self)

        self.character.actions.free.add(name='end rage', source=self, method=self.end_rage)
        self.character.actions.restricted.add(name=['Cha-based checks except Intimidate',
            'Int-based checks', 'Dex-based checks except balance, escape artist, ride',
            'Spellcasting', 'Metamagic', 'Item creation', 'Concentration', 'Combat expertise',
            'Any abilities requiring patience or concentration', 'Magic item (spell completion)',
            'Magic item (spell trigger)', 'Magic item (command word)'], source=self)

    def end_rage(self): self.character.conditions.deactivate(obj=self)

    def activate(self):
        if not self.tireless: self.fatigue_counter += 1
        return super().activate()

    def deactivate(self):
        dur = util.Duration(1, 'encounter')
        if self.fatigue_counter > 1:
            self.character.conditions.activate(name='exhausted', duration=dur)
        elif self.fatigue_counter > 0:
            self.character.conditions.activate(name='fatigued', duration=dur)
        self.fatigue_counter = 0

class GreaterRage(core.Feature):
    _name = 'greater rage'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.conditions.get_one_item(name='rage').grade.attribute += 1
    def live_prereq(self): self.add_condition(self.character.features.register('Rage'))

class TirelessRage(core.Feature):
    _name = 'tireless rage'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.conditions.get_one_item(name='rage').tireless = True
    def live_prereq(self): self.add_condition(self.character.features.register('Rage'))

class MightyRage(core.Feature):
    _name = 'mighty rage'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.conditions.get_one_item(name='rage').grade.attribute += 1
    def live_prereq(self): self.add_condition(self.character.features.register('Rage'))

#%% Bard
class Bard(core.Class):
    _name = 'bard'
    _hit_die = 6; skill_points = 6; bab_type = 'three quarters'; good_saves = ['Reflex', 'Will']
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Concentration', 'Craft',
        'Decipher Script', 'Diplomacy', 'Disguise', 'Escape Artist', 'Gather Information', 'Hide',
        'Jump', 'Knowledge', 'Listen', 'Move Silently', 'Perform', 'Profession', 'Sense Motive',
        'Sleight of Hand', 'Speak Language', 'Spellcraft', 'Swim', 'Tumble', 'Use Magic Device']
    proficiencies = ['simple', 'longsword', 'rapier', 'sap', 'short sword', 'shortbow', 'whip',
                     'light', 'shield']
    starting_gold = '4d4 x 10'; start = 'moderate'
    advancement = core.get_class_advancement({
        ('Spellcasting', 'BardicMusic', 'BardicKnowledge', 'Countersong', 'Fascinate'): [1],
        'InspireCourage': [1,8,14,20],
        'InspireCompetence': [3],
        'Suggestion': [6],
        'InspireGreatness': [9],
        'SongOfFreedom': [12],
        'InspireHeroics': [15],
        'MassSuggestion': [18],
        })
    def __init__(self, character):
        super().__init__(character)
        initial_performs = [v.base_ for k,v in self.character.skills.items() if k.startswith('Perform')]
        self.max_ranks_in_perform_ = self.character.skills.new_items_.pipe(
            ops.filter(lambda kv: kv[0].startswith('Perform')),
            ops.map(lambda kv: kv[1].base_),
            ops.scan(lambda acc, p: acc + [p], seed=initial_performs),
            ops.map(lambda p: (rx.combine_latest(*p) if p else rx.of([0]))),
            ops.switch_latest(),
            ops.map(max),
            ops.distinct_until_changed()
            )

    def BardicKnowledge(self):
        self.character.features.add_if_missing(item='BardicKnowledge', source=self)
        self.character.checks['bardic knowledge'].add(self.level, 'base', source=self)

    def Countersong(self): self.music('Countersong')
    def Fascinate(self): self.music('Fascinate')
    def InspireCourage(self):
        if 'Inspire courage' in self.character.features:
            self.character.features.get_one(name='Inspire courage').escalate()
        else: self.music('InspireCourage')
    def InspireCompetence(self): self.music('InspireCompetence')
    def BardicSuggestion(self): self.music('Suggestion')
    def InspireGreatness(self): self.music('InspireGreatness')
    def SongOfFreedom(self): self.music('SongOfFreedom')
    def InspireHeroics(self): self.music('InspireHeroics')
    def BardicMassSuggestion(self): self.music('MassSuggestion')

    def music(self, bardic_music_ability):
        min_ranks = self.character.lib.get(bardic_music_ability).minimum_perform_ranks
        enough_perform_ = self.max_ranks_in_perform_.pipe(
            ops.map(lambda p: p >= min_ranks), ops.distinct_until_changed()
            )
        self.character.features.add(item=bardic_music_ability, source=self, condition=enough_perform_)

    def live_prereq(self):
        self.character.alignment.attribute_.pipe(
            ops.map(lambda x: 'lawful' not in x), ops.distinct_until_changed()
            ).subscribe(self.code_of_conduct_.on_next, util.log_error)

    @staticmethod
    def prereq(character): return character.alignment!='lawful'

class BardSpellcasting(core.Spellcasting):
    _ability = 'charisma'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    clss = 'bard'
    retrain = [5,8,11,14,17,20]
    _spells_per_day = {
        1: [2], 2: [3,0], 3: [3,1],
        4: [3,2,0], 5: [3,3,1], 6: [3,3,2],
        7: [3,3,2,0], 8: [3,3,3,1], 9: [3,3,3,2],
        10: [3,3,3,2,0], 11: [3,3,3,3,1], 12: [3,3,3,3,2],
        13: [3,3,3,3,2,0], 14: [4,3,3,3,3,1], 15: [4,4,3,3,3,2],
        16: [4,4,4,3,3,2,0], 17: [4,4,4,4,3,3,1], 18: [4,4,4,4,4,3,2],
        19: [4,4,4,4,4,4,3], 20: [4,4,4,4,4,4,4],
        }
    _spells_known = {
        1: [4], 2: [5,2], 3: [6,3],
        4: [6,3,2], 5: [6,4,3], 6: [6,4,3],
        7: [6,4,4,2], 8: [6,4,4,3], 9: [6,4,4,3],
        10: [6,4,4,4,2], 11: [6,4,4,4,3], 12: [6,4,4,4,3],
        13: [6,4,4,4,4,2], 14: [6,4,4,4,4,3], 15: [6,4,4,4,4,3],
        16: [6,5,4,4,4,4,2], 17: [6,5,5,4,4,4,3], 18: [6,5,5,5,4,4,3],
        19: [6,5,5,5,5,4,4], 20: [6,5,5,5,5,5,4],
        }

    def __init__(self, character):
        super().__init__(character)
        self._apply_armor_exception_to_ASF()
        #TODO impose verbal component requirement

    def _apply_armor_exception_to_ASF(self):
        '''light armor does not contribute to Arcane Spell Failure'''
        asf = self.ASF
        asf._inherit__.dispose()
        std_inheritance_ = rx.combine_latest(asf._observed_collection_, asf.parent_collection_).pipe(
            ops.map(lambda p: p[0] + p[1])
            )
        non_light_armor_ = self.character.equipment.armor_.pipe(
            ops.map(lambda p: [x for x in p if x.weight_category != 'light']),
            ops.distinct_until_changed()
            )
        asf._inherit__ = rx.combine_latest(std_inheritance_, non_light_armor_).pipe(
            ops.map(lambda p: [x for x in p[0] if x.source in p[1]]),
            ops.distinct_until_changed()
            ).subscribe(asf.collection_.on_next, on_error=util.log_error)

class BardicKnowledge(core.Feature):
    _name = 'bardic knowledge'
    def __init__(self, character):
        super().__init__(character)
        self.character.checks['bardic knowledge'].enabled = True

class bardic_knowledge(core.Check):
    _name = 'bardic knowledge'
    _ability = 'intelligence'
    def __init__(self, character):
        super().__init__(character)
        self.enabled = False

class BardicMusic(core.Feature):
    _name = 'bardic music'
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute(self.source.level)
        self.frequency = util.Frequency(self.effective_level, 1, 'day')
        #TODO 20% failure chance with deafened condition

class BardicMusicAbility(core.Feature):
    minimum_perform_ranks = 0
    _performance_duration = -1

    def __init__(self, character):
        super().__init__(character)
        self.performance_duration = self._performance_duration
        bm = self.character.features.get_one(name='Bardic music')
        self.character.actions.standard.add(name=self.name, frequency=bm.frequency,
                                            method=self.start_music)
        self.character.conditions.add(obj=performing(self.character))

    def start_music(self):
        performing = self.character.conditions.get_one(name='performing')
        if performing.music: performing.stop()
        self.character.conditions.activate(obj=performing, duration=self.performance_duration)
        performing.music = self.character.conditions.activate(name=self._condition)

class performing(core.Condition):
    _name = 'performing'
    def __init__(self, character):
        super().__init__(character)
        self.music = None

    def _initialize(self):
        self.character.free.add(name='stop bardic music', source=self, method=self.stop)
        self.character.actions.restricted.add(name=['Spellcasting',
                                               'Magic item (spell completion)',
                                               'Magic item (spell trigger)'], source=self)

    def stop(self):
        self.character.conditions.deactivate(obj=self)
        if self.music.lingering_duration==0:
            self.character.conditions.deactivate(obj=self.music)
            return

        idx, info = self.character.conditions.get_info(obj=self.music)
        self.character.conditions.collection.loc[idx, 'duration'] = util.Duration(self.music.lingering_duration)

class Countersong(BardicMusicAbility):
    _name = 'countersong'
    _tags = ['supernatural']
    minimum_perform_ranks = 3
    _condition = 'countersong'
    _performance_duration = 10

class countersong(core.Condition):
    '''Counter magical effects that depend on sound (but not spells that simply have verbal
components). Make a Perform check each round. Any creature within 30' (including yourself) that is
affected by a sonic or language-dependent magical attack may use your Perform result in place of its
saving throw if, after rolling, the Perform result is higher. If a creature within range is already
under the effect of a noninstantaneous attack, it gains another saving throw against the effect each
round it hears the countersong, but must use your Perform result. Countersong has no effect against
effects that don't allow saves.'''
    _name = 'countersong'
    _tags = ['supernatural']
    lingering_duration = 0
    def _initialize(self):
        self.character.actions.free.add(name='Perform check to counter sonic/language attacks', source=self)

class Fascinate(BardicMusicAbility):
    '''Cause one or more creatures to become fascinated with you. Each creature must be within 90', able to
see and hear you, and able to pay attention. You must also be able to see them. The distraction of
nearby combat or other danger prevents the ability from working.

Your Perform result is the DC for each affected creature's Will save. If a creature's save succeeds,
you cannot attempt to fascinate that creature again for 24 hrs. If the save fails, the creature sits
quietly and listens to the song, taking no other actions, and takes a -4 penalty on skill checks
made as reactions, such as Listen and Spot. Any potential threat requires you to make another
Perform check and allows the creature a new saving throw.

Any obvious threat, such as someone drawing a weapon, casting a spell, or aiming a ranged weapon at
the target, automatically breaks the effect. Fascinate is an enchantment (compulsion), mind-
affecting ability.'''
    _name = 'fascinate'
    _tags = ['spell-like']
    minimum_perform_ranks = 3
    _condition = 'bardic_fascinate'
    _performance_duration = 0
    def __init__(self, character):
        super().__init__(character) #TODO figure out spell casting
        bard_level = self.character.build.level_of('bard')
        self.performance_duration = bard_level
        # creatures_affected = math.ceil(bard_level / 3)

class bardic_fascinate(core.Condition): #TODO keep track of spells cast on others
    _name = 'bardic fascinate'
    _tags = ['spell-like']
    lingering_duration = 0

class InspireCourage(BardicMusicAbility):
    _name = 'inspire courage'
    _tags = ['supernatural']
    minimum_perform_ranks = 3
    _condition = 'inspire_courage'
    _performance_duration = -1
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError
    def escalate(self): self.grade.attribute += 1

class inspire_courage(core.Condition):
    '''Inspire courage in your allies (including yourself), bolstering them against fear and improving
their combat abilities. To be affected, an ally must be able to hear you sing. The effect lasts for
as long as the ally hears you sing and for 5 rounds thereafter. An affected ally receives a morale
bonus on saving throws against charm and fear effects, attacks, and weapon damage rolls. This is a
mind-affecting ability.'''
    _name = 'inspire courage'
    _tags = ['supernatural']
    lingering_duration = 5
    def __init__(self, character):
        super().__init__(character)
        self.bonus = self.character.features.get_one(name='Inspire courage').bonus #TODO this won't work on others

    def _initialize(self):
        c_ = self.character.challenges.register(challenge=['charm','fear'])
        self.character.saves['all'].add(self.bonus, 'morale', condition=c_[0], source=self)
        self.character.saves['all'].add(self.bonus, 'morale', condition=c_[1], source=self)
        self.character.attacks.attack['all'].add(self.bonus, 'morale', source=self)
        self.character.attacks.damage['all'].add(self.bonus, 'morale', source=self)

class InspireCompetence(BardicMusicAbility):
    '''Help an ally succeed at a task. The ally must be within 3' and able to see and hear you. You must be
able to see the ally. They get a +2 competence bonus on checks with a particular skill as long as
they continue to hear your music. Certain uses of this ability are infeasible. The effect lasts as
long as you concentrate, to a maximum of 2 minutes. You can't inspire competence in yourself. This
is a mind-affecting ability.'''
    _name = 'inspire competence'
    _tags = ['supernatural']
    minimum_perform_ranks = 6
    _performance_duration = 20
    #TODO track effects cast on others

class Suggestion(BardicMusicAbility):
    '''Make a suggestion (as the spell) to a creature that you have already fascinated. Using this ability
does not break your concentration on the fascinate effect, nor does it allow a second saving throw
against it. Making a suggestion doesn't count against your daily uses of bardic music. This ability
affects only a single creature. Will save negates. This is an enchantment (compulsion), mind-
affecting, language dependent ability.'''
    _name = 'suggestion'
    _tags = ['spell-like']
    minimum_perform_ranks = 9
    def __init__(self, character):
        super().__init__(character)
        # will_DC = 10 + math.floor(int(self.character.classes.level_of('bard'))/2) + self.character.CHA
        raise NotImplementedError

class InspireGreatness(BardicMusicAbility):
    '''Inspire greatness in yourself or a willing ally within 30', granting them extra fighting capability.
You must sing and the ally must hear you. The effect lasts for as long as the ally hears you sing
and 5 rounds thereafter. A creature inspired with greatness gains 2 bonus HD (d10s), the
commensurate number of temporary HP (includiing CON), a +2 competence bonus to attacks, and a +1
competence bonus to Fort saves. This is a mind-affecting ability.'''
    _name = 'inspire greatness'
    _tags = ['supernatural']
    minimum_perform_ranks = 12
    def __init__(self, character):
        super().__init__(character)
        # creatures_affected = math.floor(int(self.character.classes.level_of('bard'))/3) - 2
        raise NotImplementedError

class SongOfFreedom(BardicMusicAbility):
    '''Create an effect equivalent to the break enchantment spell. This requires 1 min of uninterrupted
concentration and music, and it functionson a single target within 30'. You can't use this on
yourself.'''
    _name = 'song of freedom'
    _tags = ['spell-like']
    minimum_perform_ranks = 15
    def __init__(self, character):
        super().__init__(character)
        # caster_level = self.character.classes.level_of('bard')
        raise NotImplementedError

class InspireHeroics(BardicMusicAbility):
    '''Inspire tremendous heroism in yourself or a willing ally within 30'. You must perform and an ally
must hear you for a full round. A creature so inspired gains a +4 morale bonus to saves and a +4
dodge bonus to AC. The effect lasts for as long as the ally hears you perform and for up to 5 rounds
thereafter. This is a mind-affecting ability.'''
    _name = 'inspire heroics'
    _tags = ['supernatural']
    minimum_perform_ranks = 18
    def __init__(self, character):
        super().__init__(character)
        # creatures_affected = math.floor(int(self.character.classes.level_of('bard'))/3) - 4
        raise NotImplementedError

class MassSuggestion(BardicMusicAbility):
    '''As suggestion, except you can make the suggestion simultaneously to any number creatures you have
already fascinated.'''
    _name = 'mass suggestion'
    _tags = ['spell-like']
    minimum_perform_ranks = 21
    def __init__(self, character):
        super().__init__(character)
        raise NotImplementedError

#%% Cleric
class Cleric(core.Class):
    _name = 'cleric'
    _hit_die = 8; skill_points = 2; bab_type = 'three quarters'; good_saves = ['Fortitude', 'Will']
    _class_skills = ['Concentration', 'Craft', 'Diplomacy', 'Heal', 'Knowledge (arcana)',
        'Knowledge (history)', 'Knowledge (the planes)', 'Knowledge (religion)', 'Profession',
        'Spellcraft']
    starting_gold = '5d4 x 10'; start = 'complex'
    advancement = {1: ['Spellcasting', 'TurnRebukeUndead']}
    def __init__(self, character):
        super().__init__(character)
        self.orientation = self._check_alignment()
        self.character.skills.bonus_languages.add(name=['Celestial', 'Abyssal', 'Infernal'], source=self)
        def check_energy_type():
            if not self.orientation:
                print('Declare a positive or negative energy orientation for your cleric class.')
        self.character.add_to_build(-2, 1, check_energy_type)

        #TODO Aura of deity alignment / alignment domain

    def add_feature(self, feature):
        self.character.features.add(item=feature, source=self, condition=self._code_of_conduct)

    def declare_energy_orientation(self, energy):
        if self.orientation:
            util.logger.warning('Your energy orientation is already set to %s', self.orientation); return
        energy = energy.lower()
        energy = 'positive' if energy=='good' else 'negative' if energy=='evil' else energy
        if energy not in ['positive', 'negative']:
            util.logger.warning('Energy orientation not valid or not recognized. %s', energy); return
        self.orientation = energy
        self._apply_orientation()

    def _apply_orientation(self):
        if self.orientation is None: return
        self.TurnRebukeUndead()
        #TODO apply to spontaneous spellcasting

    def _check_alignment(self):
        if self.character.alignment=='good': return 'positive'
        if self.character.alignment=='evil': return 'negative'
        if not self.character.deity: return None
        if self.character.deity.alignment=='good': return 'positive'
        if self.character.deity.alignment=='evil': return 'negative'

    def TurnRebukeUndead(self):
        match self.orientation:
            case 'positive': self.add_feature('TurnUndead')
            case 'negative': self.add_feature('RebukeUndead')
            case _:
                util.logger.warning('Declare an energy orientation to activate turn/rebuke undead')

    def live_prereq(self):
        rx.combine_latest(self.character.alignment_, self.character.deity_).pipe(
            ops.map(lambda p: p[0].distance(p[1].alignment) <= 1 if hasattr(p[1], 'alignment') else True),
            ops.distinct_until_changed(),
            ops.filter(lambda x: x is False)
            ).subscribe(self.code_of_conduct_.on_next, util.log_error)

    def prereq(self):
        if not self.character.deity: return True
        if self.character.alignment=='true neutral' and self.character.deity.alignment!='true neutral': return False
        return self.character.alignment.distance(self.character.deity.alignment) <= 1
        #TODO cleric race must match racial deity's preferred race

class ClericSpellcasting(core.Spellcasting):
    _ability = 'wisdom'
    magic_type = 'divine'
    caster_type = 'prepared'
    clss = 'cleric'
    _spells_per_day = {
        1: [3,1], 2: [4,2],
        3: [4,2,1], 4: [5,3,2],
        5: [5,3,2,1], 6: [5,3,3,2],
        7: [6,4,3,2,1], 8: [6,4,3,3,2],
        9: [6,4,4,3,2,1], 10: [6,4,4,3,3,2],
        11: [6,5,4,4,3,2,1], 12: [6,5,4,4,3,3,2],
        13: [6,5,5,4,4,3,2,1], 14: [6,5,5,4,4,3,3,2],
        15: [6,5,5,5,4,4,3,2,1], 16: [6,5,5,5,4,4,3,3,2],
        17: [6,5,5,5,5,4,4,3,2,1], 18: [6,5,5,5,5,4,4,3,3,2],
        19: [6,5,5,5,5,5,4,4,3,3], 20: [6,5,5,5,5,5,4,4,4,4],
        }
    def __init__(self, character):
        super().__init__(character)
        self.domains = self.character.features.add(item='DomainCasting', source=self)
        #TODO Spontaneous casting
        #TODO restrict alignment spells

class DomainCasting(core.Spellcasting):
    _name = 'domain casting'
    _ability = 'wisdom'
    magic_type = 'divine'
    caster_type = 'prepared'
    clss = 'cleric'
    cantrips = False

    def __init__(self, character):
        super().__init__(character)
        self.spell_list = core.SpellList(self)
    @property
    def spells_per_day(self):
        return [1]*(len(self._spells_per_day[int(self.class_level)]) - 1)

#%% Druid
class Druid(core.Class):
    _name = 'druid'
    _hit_die = 8; skill_points = 4; bab_type = 'three quarters'; good_saves = ['Fortitude', 'Will']
    _class_skills = ['Concentration', 'Craft', 'Diplomacy', 'Handle Animal', 'Heal',
        'Knowledge (nature)', 'Listen', 'Profession', 'Ride', 'Spellcraft', 'Spot', 'Survival',
        'Swim']
    proficiencies = ['club', 'dagger', 'dart', 'quarterstaff', 'scimitar', 'sickle', 'shortspear',
        'sling', 'spear', 'light', 'medium', 'shield']
    starting_gold = '2d4 x 10'; start = 'complex'
    advancement = core.get_class_advancement({
        ('Spellcasting', 'AnimalCompanion', 'NatureSense', 'WildEmpathy'): [1],
        'WoodlandStride': [2],
        'TracklessStep': [3],
        'ResistNaturesLure': [4],
        'WildShape': [5,6,7,10,14,18],
        'WildShapeLarge': [8],
        'VenomImmunity': [9],
        'WildShapeTiny': [11],
        'WildShapePlant': [12],
        'AThousandFaces': [13],
        ('TimelessBody', 'WildShapeHuge'): [15],
        'ElementalWildShape': [16,18,20],
        'ElementalWildShapeHuge': [20]
        })

    def __init__(self, character):
        super().__init__(character)
        self.character.skills.languages.add(name='Druidic', source=self, override=True)
        self.character.skills.bonus_languages.add(name='Sylvan', source=self)

        self.eschewing_metal_armor_ = BehaviorSubject(True)
        timer = util.Duration(1, 'day')
        timer.trigger(lambda: self.eschewing_metal_armor_.on_next(True))
        metal_armor_ = self.character.equipment.armor_.pipe(
            ops.map(lambda p: all(x.material!='metal' for x in p)), #TODO this won't catch adamantine, cold iron, etc
            ops.distinct_until_changed(),
            ops.filter(lambda p: p is False)
            )
        metal_armor_.pipe(ops.filter(lambda p: p is False)
            ).subscribe(self.eschewing_metal_armor_.on_next, util.log_error)
        metal_armor_.pipe(ops.filter(lambda p: p is True)
            ).subscribe(timer.reset(), util.log_error)

    def add_feature(self, feature):
        feature = self.character.lib.get(item=feature)
        if any(util.is_a(feature, cat) for cat in ['spellcasting', 'spell-like', 'supernatural']):
            self.character.features.add(item=feature, source=self, condition=[
                self.code_of_conduct_, self.eschewing_metal_armor_])
        else:
            self.character.features.add(item=feature, source=self, condition=self.code_of_conduct_)

    def AnimalCompanion(self):
        ac = self.character.features.add_if_missing(item='AnimalCompanionFeature', source=self)
        ac.effective_level.add(self.level, 'base', source=self, condition=self.code_of_conduct_)

    def WildShapeLarge(self): self.character.features.get_one(name='Wild shape').valid_sizes.append('Large')
    def WildShapeTiny(self): self.character.features.get_one(name='Wild shape').valid_sizes.append('Tiny')
    def WildShapePlant(self): self.character.features.get_one(name='Wild shape').valid_types.append('plant')
    def WildShapeHuge(self): self.character.features.get_one(name='Wild shape').valid_sizes.append('Huge')

    def live_prereq(self):
        self.character.alignment.attribute_.pipe(
            ops.map(lambda x: 'neutral' in x), ops.filter(lambda x: x is False)
            ).subscribe(self.code_of_conduct_.on_next, util.log_error)
    def prereq(self): return self.character.alignment=='neutral'

class DruidSpellcasting(core.Spellcasting):
    _ability = 'wisdom'
    magic_type = 'divine'
    caster_type = 'prepared'
    clss = 'druid'
    _spells_per_day = ClericSpellcasting._spells_per_day
    #TODO restrict opposed alignments
    #TODO Spontaneous casting

class NatureSense(core.Feature):
    _name = 'nature sense'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.skills['Knowledge (nature)'].add(2, source=self)
        self.character.skills['Survival'].add(2, source=self)

class TracklessStep(core.Feature):
    _name = 'trackless step'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class ResistNaturesLure(core.Feature):
    _name = "resist nature's lure"
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        chall_ = self.character.challenges.register(target='fey', challenge='spell-like ability')
        self.character.saves['all'].add(4, condition=chall_)

class WildShape(core.Feature): #TODO
    _name = 'wild shape'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.frequency = util.Frequency(self.grade, 1, 'day')
        self.level = util.Attribute()
        self.level.add(self.character.classes.level_of('druid'), 'base')
        self.valid_types = ['animal']
        self.valid_sizes = ['Small', 'Medium']
        self.max_hit_dice = util.Attribute()
        self.max_hit_dice.add(self.level, 'base')
    def escalate(self): self.grade.attribute += 1

class VenomImmunity(core.Feature):
    _name = 'venom immunity'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.immunities.add(name='poison', source=self)

class AThousandFaces(core.Feature):
    _name = 'a thousand faces'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class ElementalWildShape(WildShape):
    _name = 'elemental wild shape'
    def __init__(self, character):
        super().__init__(character)
        self.valid_types = ['elemental']
        self.valid_sizes = ['Small', 'Medium', 'Large']

#%% Fighter
class Fighter(core.Class):
    _name = 'fighter'
    _hit_die = 10; skill_points = 2; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Climb', 'Craft', 'Handle Animal', 'Intimidate', 'Jump', 'Ride', 'Swim']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield', 'tower shield']
    starting_gold = '6d4 x 10'; start = 'moderate'
    advancement = {lvl: ['BonusFeat'] for lvl in [1]+list(range(2,21,2))}
    def BonusFeat(self):
        is_fighter_feat = lambda x: util.is_a(x, 'fighter')
        self.character.feats.feat_slots.add(1, source=self, restriction=is_fighter_feat)

#%% Monk
class Monk(core.Class):
    _name = 'monk'
    _hit_die = 8; skill_points = 4; bab_type = 'three quarters'
    good_saves = ['Fortitude', 'Reflex', 'Will']
    _class_skills = ['Balance', 'Climb', 'Concentration', 'Craft', 'Diplomacy', 'Escape Artist',
        'Hide', 'Jump', 'Knowledge (arcana)', 'Knowledge (religion)', 'Listen', 'Move Silently',
        'Perform', 'Profession', 'Sense Motive', 'Spot', 'Swim', 'Tumble']
    proficiencies = ['club', 'light crossbow', 'heavy crossbow', 'dagger', 'handae', 'javelin',
        'kama', 'nunchaku', 'quarterstaff', 'sai', 'shuriken', 'siangham', 'sling',
        'unarmed strike']
    starting_gold = '5d4'; start = 'complex'
    advancement = core.get_class_advancement({
        'BonusFeat': [1,2,6],
        ('ACBonus', 'FlurryOfBlows', 'UnarmedStrike'): [1],
        'Evasion': [2], 'ImprovedEvasion': [9],
        ('StillMind', 'MonkFastMovement'): [3],
        ('KiStrike', 'Magic'): [4], 'Lawful': [10], 'Adamantine': [16],
        'SlowFall': [4,6,8,10,12,14,16,18], 'SlowFallAny': [20],
        'PurityOfBody': [5],
        'WholenessOfBody': [7],
        ('DiamondBody', 'GreaterFlurry'): [11],
        'AbundantStep': [12],
        'DiamondSoul': [13],
        'QuiveringPalm': [15],
        ('TimelessBody', 'TongueOfTheSunAndMoon'): [17],
        'EmptyBody': [19],
        'PerfectSelf': [20],
        })

    def __init__(self, character):
        super().__init__(character)
        self.features_test_ = rx.combine_latest(self.character.equipment.active_,
                                                self.character.equipment.encumbrance_,
                                                self.character.conditions.active_).pipe(
            ops.map(lambda p: not any(util.is_a(f, 'Armor') for f in p[0]) and
                        p[1]=='light' and
                        not any(f.name=='helpless' for f in p[2])
                        )
            )
        self.ki = None

    def advance(self):
        if self.multiclass_.value: raise util.NotEligible
        super().advance()

    def ACBonus(self):
        x = self.character.features.add(item='AC bonus', condition=self.features_test_, source=self)
        x.level.add(self.level, source=self) #TODO rejigger to get level from source

    def BonusFeat(self):
        def monk_feat_req(feat_clss):
            monk_feats = {
                1: ['Improved grapple', 'Stunning fist'],
                2: ['Combat reflexes', 'Deflect arrows'],
                6: ['Improved disarm', 'Improved trip']
            }

            feats = monk_feats.get(self.level, [])
            return any(util.is_a(feat_clss, monk_feat) for monk_feat in feats)

        self.character.feats.feat_slots.add(1, source=self, override=True,
                                            restriction=monk_feat_req)

    def FlurryOfBlows(self): raise NotImplementedError
    def UnarmedStrike(self): raise NotImplementedError

    def Evasion(self): #TODO features_test_ is not quite right-- can wear light armor
        self.character.features.add(item='Evasion', condition=self.features_test_, source=self)

    def KiStrike(self): self.ki = self.character.features.add(item='KiStrike', source=self)
    def Magic(self): self.ki.add_quality('magic')
    def Lawful(self): self.ki.add_quality('lawful')
    def Adamantine(self): self.ki.add_quality('adamantine')

    def SlowFallAny(self): self.character.features.get_one(name='Slow fall').remove_limit()

    def live_prereq(self):
        self.character.alignment.attribute_.pipe(
            ops.map(lambda x: x=='lawful'), ops.distinct_until_changed(),
            ).subscribe(self.code_of_conduct_.on_next, util.log_error)
    def prereq(self): return self.character.alignment=='lawful'

class ACBonus(core.Feature):
    _name = 'AC bonus'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.level = util.FeatureList()
        def check_AC_bonus_slots():
            if len(self.level < self.grade):
                util.logger.warning('AC bonus feature missing level info from relevant classes.')
        self.character.add_to_build(-2, 1, check_AC_bonus_slots)

        WIS_bonus = util.LiveAttribute(self.character.WIS, lambda x: max(0, x))
        self.character.AC['all'].add(WIS_bonus, 'WIS', source=self)

        AC_bonus = util.NumeralAttribute(0)
        self.level.active_.pipe(
            ops.map(lambda p: sum(x//5 for x in p)), ops.distinct_until_changed()
            ).subscribe(AC_bonus.value_.on_next, util.log_error)
        self.character.AC['all'].add(AC_bonus, 'untyped', source=self)
    def escalate(self): self.grade.attribute += 1

class StillMind(core.Feature):
    _name = 'still mind'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        chall_ = self.character.challenges.register(challenge='enchantment')
        self.character.saves['all'].add(2, source=self, condition=chall_)

class MonkFastMovement(core.Feature):
    _name = 'fast movement'
    _tags = ['extraordinary']
    def __init__(self, character): #TODO rejigerr: calc level from sources
        super().__init__(character)
        monk_level = self.character.classes.level_of('monk')
        self.character.speed['all'].add(util.LiveAttribute(monk_level, lambda x: 10 * x//3),
                                        'enhancement', source=self)

class KiStrike(core.Feature):
    _name = 'ki strike'
    _tags = ['supernatural']
    def add_quality(self, quality):
        self.character.equipment.get_one_item(name='unarmed strike').damage._notes.add(name=quality, source=self)

class SlowFall(core.Feature):
    _name = 'slow fall'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.speed['slow fall'] = util.Attribute()
        self.character.speed['slow fall'].add(util.LiveAttribute(self.grade, lambda x: x*10),
                                              'base', source=self)

    def add_source(self, source):
        super().add_source(source)
        self.character.speed['slow fall'].add(10, 'base', source=self)

    def escalate(self): self.grade.attribute += 1

    def remove_limit(self):
        self.character.speed['slow fall'] = util.BooleanAttribute()
        self.character.speed['slow fall'].add(1, source=self)
        self.character.speed['slow fall']._notes.add(name='unlimited', source=self)

class PurityOfBody(core.Feature):
    _name = 'purity of body'
    def __init__(self, character): raise NotImplementedError

class WholenessOfBody(core.Feature):
    _name = 'wholeness of body'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError # calc effective level from sources

class DiamondBody(core.Feature):
    _name = 'diamond body'
    _tags = ['supernatural']
    def __init__(self, character):
        super().__init__(character)
        self.character.immunities.add(name='poison', source=self)

class GreaterFlurry(core.Feature):
    _name = 'greater flurry'
    def __init__(self, character): raise NotImplementedError

class AbundantStep(core.Feature):
    _name = 'abundant step'
    _tags = ['supernatural']
    def __init__(self, character): # calc level from sources
        super().__init__(character)
        monk_level = self.character.classes.level_of('monk')
        self.character.magic.spell_like_abilities.add(item='DimensionDoor',
            caster_level=util.LiveAttribute(monk_level, lambda x: x//2),
            frequency=util.Frequency(1, 1, 'day'), source=self)

class DiamondSoul(core.Feature):
    _name = 'diamond soul'
    _tags = ['extraordinary']
    def __init__(self, character): # rejigger off of source
        super().__init__(character)
        self.character.spell_resistance['normal'].add(10, 'base', source=self)
        self.character.spell_resistance['normal'].add(self.character.classes.level_of('monk'), 'base', source=self)

class QuiveringPalm(core.Feature):
    _name = 'quivering palm'
    _tags = ['attack', 'supernatural']
    def __init__(self, character): raise NotImplementedError # calc level from sources

class TongueOfTheSunAndMoon(core.Feature):
    _name = 'tongue of the sun and moon'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class EmptyBody(core.Feature):
    _name = 'empty body'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError  # calc level from sources

class perfectSelf(core.Feature):
    _name = 'perfect self'
    def __init__(self, character):
        super().__init__(character)
        self.character.creature_type = 'outsider'
        self.character.damage_reduction['magic'].add(10, 'base', source=self)

#%% Paladin
class Paladin(core.Class):
    _name = 'paladin'
    _hit_die = 10; skill_points = 2; bab_type = 'full'; good_saves = ['Fortitude']
    _class_skills = ['Concentration', 'Craft', 'Diplomacy', 'Handle Animal', 'Heal',
        'Knowledge (nobility and royalty)', 'Knowledge (religion)', 'Profession', 'Ride',
        'Sense Motive']
    proficiencies = ['simple', 'martial', 'light', 'medium', 'heavy', 'shield']
    starting_gold = '6d4 x 10'; start = 'moderate'
    advancement = core.get_class_advancement({
        ('AuraOfGood', 'DetectEvil'): [1],
        'SmiteEvil': [1,5,10,15,20],
        ('DivineGrace', 'LayOnHands'): [2],
        ('AuraOfCourage', 'DivineHealth'): [3],
        ('Spellcasting', 'TurnUndead'): [4],
        'SpecialMountFeature': [5],
        'RemoveDisease': [6,9,12,15,18],
        })

    def add_feature(self, feature):
        self.character.features.add(item=feature, source=self, condition=self.code_of_conduct_)

    def advance(self):
        if self.multiclass_.value: raise util.NotEligible
        super().advance()

    def DetectEvil(self):
        self.character.magic.spell_like_abilities.add(item='DetectEvil', frequency='at will',
            caster_level=self.character.build.level, source=self, condition=self.code_of_conduct_)

    def live_prereq(self):
        self.character.alignment.attribute_.pipe(
            ops.map(lambda x: x=='lawful good'), ops.filter(lambda x: x is False)
            ).subscribe(self.code_of_conduct_.on_next, util.log_error)

    def prereq(self): return self.character.alignment=='lawful good'

class AuraOfGood(core.Feature):
    _name = 'aura of good'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class SmiteEvil(core.Feature):
    _name = 'smite evil'
    _tags = ['attack', 'supernatural']
    def __init__(self, character): # calc level from sources
        raise NotImplementedError
        super().__init__(character)
        self.frequency = util.Frequency(self.grade, 1, 'day')
    def escalate(self): self.grade.attribute += 1

class DivineGrace(core.Feature):
    _name = 'divine grace'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class LayOnHands(core.Feature):
    _name = 'lay on hands'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError # calc level from sources

class AuraOfCourage(core.Feature):
    _name = 'aura of courage'
    _tags = ['supernatural']
    def __init__(self, character): raise NotImplementedError

class DivineHealth(core.Feature):
    _name = 'divine health'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.immunities.add(name='disease', source=self)

class PaladinSpellcasting(core.Spellcasting):
    _ability = 'wisdom'
    magic_type = 'divine'
    caster_type = 'prepared'
    _caster_level = 'half'
    clss = 'paladin'
    cantrips = False
    _spells_per_day = {
        4: [0], 5: [0], 6: [1], 7: [1],
        8: [1,0], 9: [1,0], 10: [1,1],
        11: [1,1,0], 12: [1,1,1], 13: [1,1,1],
        14: [2,1,1,0], 15: [2,1,1,1], 16: [2,2,1,1],
        17: [2,2,2,1], 18: [3,2,2,1], 19: [3,3,3,2], 20: [3,3,3,3],
        }

class SpecialMountFeature(core.Feature):
    _name = 'special mount'
    _tags = ['spell-like']
    def __init__(self, character): raise NotImplementedError
    def default_mount(self): pass #TODO
    def check_eligibility(self, mount_class, aquatic=False):
        if any (util.is_a(mount_class, standard_mount) for standard_mount in ['Warpony', 'HeavyWarhorse']):
            return True
        if util.is_a(mount_class, 'RidingDog') and self.character.race=='halfling': return True
        if util.is_a(mount_class, 'LargeShark') and aquatic: return True
        raise util.NotEligible(mount_class._name)

    def recruit(self, mount_class, override=False):
        if not override: self.check_eligibility(mount_class)
        mount = mount_class(self.character)
        self.character.companions.add(obj=mount, source=self)
        return mount

class RemoveDisease(core.Feature):
    _name = 'remove disease'
    _tags = ['spell-like']
    def __init__(self, character):
        super().__init__(character)
        self.frequency = util.Frequency(self.grade, 1, 'week')
        self.character.magic.spell_like_abilities.add(item='RemoveDisease',
            caster_level=self.character.build.level, frequency=self.frequency, source=self)
    def escalate(self): self.grade.attribute += 1

#%% Ranger
class Ranger(core.Class):
    _name = 'ranger'
    _hit_die = 8; skill_points = 6; bab_type = 'full'; good_saves = ['Fortitude', 'Reflex']
    _class_skills = ['Climb', 'Concentration', 'Craft', 'Handle Animal', 'Heal', 'Hide', 'Jump',
        'Knowledge (dungeoneering)', 'Knowledge (geography)', 'Knowledge (nature)', 'Listen',
        'Move Silently', 'Profession', 'Ride', 'Search', 'Spot', 'Survival', 'Swim', 'Use Rope']
    proficiencies = ['simple', 'martial', 'light', 'shield']
    starting_gold = '6d4 x 10'; start = 'moderate'
    special_ability_options = [{'archery': ['RapidShot', 'Manyshot', 'ImprovedPreciseShot']},
           {'twf': ['TwoWeaponFighting', 'ImprovedTwoWeaponFighting', 'GreaterTwoWeaponFighting']}]
    advancement = core.get_class_advancement({
        'FavoredEnemy': [1,5,10,15,20],
        ('Track', 'WildEmpathy'): [1],
        'CombatStyle': [2,6,11],
        'Endurance': [3],
        ('Spellcasting', 'AnimalCompanion'): [4],
        'WoodlandStride': [7],
        'SwiftTracker': [8],
        'Evasion': [9],
        'camouflage': [13],
        'HideInPlainSight': [17],
        })

    def __init__(self, character):
        super().__init__(character)
        self.combat_style = None

        self._light_armor_ = self.character.equipment.armor_encumbrance_.pipe(
            ops.map(lambda p: p in ['none', 'light']), ops.distinct_until_changed()
            )

        def check_combat_style():
            if self.combat_style is None and self.level >= 2:
                util.logger.warning('Declare a ranger combat style.')
        self.character.add_to_build(-2, 1, check_combat_style)

    def set_combat_style(self, style):
        if self.combat_style:
            util.logger.warning(f'Your combat style is already set to {self.combat_style}'); return

        style = 'twf' if style.lower() in ['two-weapon combat', 'two-weapon fighting'] else style.lower()
        if any(style in styles for styles in self.special_ability_options):
            self.combat_style = style
        else: raise NotImplementedError(style)

        self._apply_style_feats()

    def AnimalCompanion(self):
        ac = self.character.features.add_if_missing(item='AnimalCompanionFeature', source=self)
        ac.effective_level.add(util.LiveAttribute(self.level, lambda x: x//2), 'base', source=self)

    def CombatStyle(self):
        self.grade.attribute += 1
        self._apply_style_feats()

    def Endurance(self): self.character.feats.add(item='Endurance', source=self, override=True)

    def HideInPlainSight(self):
        hips = self.character.features.add_if_missing(item='HideInPlainSight', source=self)
        hips.set_terrain('natural terrain')

    def Track(self): self.character.feats.add(item='Track', source=self, override=True)

    def _apply_style_feats(self):
        if self.combat_style is None: return

        style = next(x[self.combat_style] for x in self.special_ability_options if self.combat_style in x)
        for feat in style[0:self.grade]:
            self.character.feats.add_if_missing(item=feat, override=True, condition=self._light_armor_)

class FavoredEnemy(core.Feature):
    '''At 1st level, a ranger may select a type of creature from among those given on Table: Ranger Favored
Enemies. The ranger gains a +2 bonus on Bluff, Listen, Sense Motive, Spot, and Survival checks when
using these skills against creatures of this type. Likewise, he gets a +2 bonus on weapon damage
rolls against such creatures.

At 5th level and every five levels thereafter (10th, 15th, and 20th level), the ranger may select an
additional favored enemy from those given on the table. In addition, at each such interval, the
bonus against any one favored enemy (including the one just selected, if so desired) increases by 2.

If the ranger chooses humanoids or outsiders as a favored enemy, he must also choose an associated
subtype, as indicated on the table. If a specific creature falls into more than one category of
favored enemy, the ranger's bonuses do not stack; he simply uses whichever bonus is higher.'''
    _name = 'favored enemy'
    _tags = ['extraordinary']
    valid_types = util.bane_types = ['outsider (native)']
    skill_checks = ['Bluff', 'Listen', 'Sense Motive', 'Spot', 'Survival']

    def __init__(self, character):
        super().__init__(character)
        self.grade = util.NumeralAttribute(1)
        self.enemies_ = BehaviorSubject([])

        self.checks = [self.character.skills[check] for check in self.skill_checks]
        self.checks.append(self.character.attacks.damage['all'])

        def check_favored_enemies():
            if len(self.enemies) < self.grade:
                util.logger.warning('Favored enemies are not all assigned.'); return
            if len(self.enemies_.value) < self.grade * 2 - 1:
                util.logger.warning('Favored enemy upgrades are not all assigned.')
        self.character.add_to_build(-2, 1, check_favored_enemies)

    @property
    def enemies(self):
        return set(self.enemies_.value)

    def add_favored_enemy(self, creature_type):
        if len(self.enemies)==self.grade:
            util.logger.warning('All favored enemies are already assigned.'); return
        typ = self._check_enemy_type(creature_type)
        self.enemies_.on_next(self.enemies_.value + [typ])

        bonus = util.NumeralAttribute(2)
        self.enemies_.pipe(
            ops.map(lambda lst: 2 * lst.count(typ)), ops.distinct_until_changed()
            ).subscribe(bonus.value_.on_next, util.log_error)

        challenge_types = creature_type
        if creature_type not in util.creature_types:
            challenge_types = creature_type.translate(str.maketrans('','',string.punctuation)).split()

        c_ = self.character.challenges.register(target=challenge_types)
        for check in self.checks:
            check.add(bonus, condition=c_, source=self)

    def escalate(self): self.grade.attribute += 1
    def escalate_favored_enemy(self, creature_type):
        if len(self.enemies_.value)==self.grade * 2 - 1:
            util.logger.warning('All favored enemy upgrades are already assigned.'); return
        typ = self._check_enemy_type(creature_type)
        if typ not in self.enemies: raise util.NotEligible(typ)
        self.enemies_.on_next(self.enemies_.value + [typ])

    def _check_enemy_type(self, creature_type):
        creature_type = creature_type.lower()
        if creature_type not in self.valid_types:
            util.logger.warning('Unrecognized creature type: %s', creature_type); return None
        return creature_type

class RangerSpellcasting(core.Spellcasting):
    _ability = 'wisdom'
    magic_type = 'divine'
    caster_type = 'prepared'
    _caster_level = 'half'
    clss = 'ranger'
    cantrips = False
    _spells_per_day = PaladinSpellcasting._spells_per_day

class SwiftTracker(core.Feature):
    _name = 'swift tracker'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.checks['track']._notes.add(name='Move at normal speed without penalty')
        self.character.checks['track']._notes.add(name='Move at 2x speed with only -10 penalty')

class Camouflage(core.Feature):
    _name = 'camouflage'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.skills['Hide']._notes.add(name='No cover needed', condition='natural terrain')

#%% Rogue
class Rogue(core.Class):
    _name = 'rogue'
    _hit_die = 6; skill_points = 8; bab_type = 'three quarters'; good_saves = ['Reflex']
    _class_skills = ['Appraise', 'Balance', 'Bluff', 'Climb', 'Craft', 'Decipher Script',
        'Diplomacy', 'Disable Device', 'Disguise', 'Escape Artist', 'Forgery', 'Gather Information',
        'Hide', 'Intimidate', 'Jump', 'Knowledge (local)', 'Listen', 'Move Silently', 'Open Lock',
        'Perform', 'Profession', 'Search', 'Sense Motive', 'Sleight of Hand', 'Spot', 'Swim',
        'Tumble', 'Use Magic Device', 'Use Rope' ]
    proficiencies = ['simple', 'hand crossbow', 'rapier', 'sap', 'shortbow', 'short sword', 'light']
    starting_gold = '5d4 x 10'; start = 'simple'
    advancement = core.get_class_advancement({
        'SneakAttack': list(range(1,21,2)),
        'Trapfinding': [1],
        'Evasion': [2],
        'TrapSense': list(range(3,21,3)),
        'UncannyDodge': [4,8],
        'SpecialAbility': list(range(10,21,3)),
        })
    special_ability_options = ['CripplingStrike', 'DefensiveRoll', 'ImprovedEvasion', 'Opportunist',
        'SkillMastery', 'SlipperyMind', 'BonusFeat']

    def SkillMastery(self):
        sm = self.add_feature('skill mastery')
        sm.grade.add(3, 'base')
        sm.grade.add(self.character.INT.attribute, 'INT')

class SneakAttack(core.Feature):
    '''If a rogue can catch an opponent when he is unable to defend himself effectively from her attack,
she can strike a vital spot for extra damage.

The rogue's attack deals extra damage any time her target would be denied a Dexterity bonus to AC
(whether the target actually has a Dexterity bonus or not), or when the rogue flanks her target.
This extra damage is 1d6 at 1st level, and it increases by 1d6 every two rogue levels thereafter.
Should the rogue score a critical hit with a sneak attack, this extra damage is not multiplied.

Ranged attacks can count as sneak attacks only if the target is within 30 feet.

With a sap (blackjack) or an unarmed strike, a rogue can make a sneak attack that deals nonlethal
damage instead of lethal damage. She cannot use a weapon that deals lethal damage to deal nonlethal
damage in a sneak attack, not even with the usual -4 penalty.

A rogue can sneak attack only living creatures with discernible anatomies—undead, constructs, oozes,
plants, and incorporeal creatures lack vital areas to attack. Any creature that is immune to
critical hits is not vulnerable to sneak attacks. The rogue must be able to see the target well
enough to pick out a vital spot and must be able to reach such a spot. A rogue cannot sneak attack
while striking a creature with concealment or striking the limbs of a creature whose vitals are
beyond reach.'''
    _name = 'sneak attack'; _tags = ['attack', 'extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.Attribute(1)
        c_ = character.challenges.register(action='flanking', target=['flat-footed', 'within 30 ft.'])
        character.attacks.extra_dice['melee'].add(self.grade, 6, 'precision', condition=c_[0], source=self)
        character.attacks.extra_dice['melee'].add(self.grade, 6, 'precision', condition=c_[1], source=self)
        character.attacks.damage['melee']._notes.add(name='Sneak attack', condition=c_[0], source=self)
        character.attacks.damage['melee']._notes.add(name='Sneak attack', condition=c_[1], source=self)
        character.attacks.extra_dice['ranged'].add(self.grade, 6, 'precision', condition=[c_[1], c_[2]], source=self)
        character.attacks.damage['ranged']._notes.add(name='Sneak attack', condition=[c_[1], c_[2]], source=self)

        self.grade.attribute_.pipe(ops.map(lambda x: f'{self._name} +{x}d6')).subscribe(self.name_.on_next, util.log_error)

    def escalate(self): self.grade.add(1, 'base')

class Trapfinding(core.Feature):
    '''Rogues (and only rogues) can use the Search skill to locate traps when the task has a Difficulty
Class higher than 20.

Finding a nonmagical trap has a DC of at least 20, or higher if it is well hidden. Finding a magic
trap has a DC of 25 + the level of the spell used to create it.

Rogues (and only rogues) can use the Disable Device skill to disarm magic traps. A magic trap
generally has a DC of 25 + the level of the spell used to create it.

A rogue who beats a trap's DC by 10 or more with a Disable Device check can study a trap, figure out
how it works, and bypass it (with her party) without disarming it.'''
    _name = 'trapfinding'
    def __init__(self, character):
        super().__init__(character)
        self.character.checks['find trap'].enabled = True
        self.character.checks['disable magical trap'].enabled = True

class disable_magical_trap(core.Check):
    _name = 'disable magical trap'
    def __init__(self, character):
        super().__init__(character)
        self.parent = self.character.skills['Disable Device']
        self.enabled = False

class find_trap(core.Check):
    _name = 'find trap'
    def __init__(self, character):
        super().__init__(character)
        self.parent = self.character.skills['Search']
        self.enabled = False

class CripplingStrike(core.Feature):
    '''A rogue with this ability can sneak attack opponents with such precision that her blows weaken and
hamper them. An opponent damaged by one of her sneak attacks also takes 2 points of Strength damage.
Ability points lost to damage return on their own at the rate of 1 point per day for each damaged
ability.'''
    _name = 'crippling strike'
    _tags = ['attack', 'extraordinary']
    def __init__(self, character): raise NotImplementedError
        # handle ability damage; link up with sneak attack when it's enabled

class DefensiveRoll(core.Feature):
    '''The rogue can roll with a potentially lethal blow to take less damage from it than she otherwise
would. Once per day, when she would be reduced to 0 or fewer hit points by damage in combat (from a
weapon or other blow, not a spell or special ability), the rogue can attempt to roll with the
damage. To use this ability, the rogue must attempt a Reflex saving throw (DC = damage dealt). If
the save succeeds, she takes only half damage from the blow; if it fails, she takes full damage. She
must be aware of the attack and able to react to it in order to execute her defensive roll—if she is
denied her Dexterity bonus to AC, she can't use this ability. Since this effect would not normally
allow a character to make a Reflex save for half damage, the rogue's evasion ability does not apply
to the defensive roll.'''
    _name = 'defensive roll'
    _tags = ['extraordinary']
    def __init__(self, character):
        self.frequency = util.Frequency(self.grade, 1, 'day')
        self.actions.reaction.add(name='defensive roll', condition='<0HP after physical damage',
                                  frequency=self.frequency, method=self.roll)
    def escalate(self): self.grade.attribute += 1

    def roll(self):
        print('Reflex save (DC = damage dealt) for half damage.')

class Opportunist(core.Feature):
    '''Once per round, the rogue can make an attack of opportunity against an opponent who has just been
struck for damage in melee by another character. This attack counts as the rogue's attack of
opportunity for that round. Even a rogue with the Combat Reflexes feat can't use the opportunist
ability more than once per round.'''
    _name = 'opportunist'
    _tags = ['attack', 'extraordinary']
    def __init__(self, character): raise NotImplementedError

class SkillMastery(core.Feature):
    '''You are so certain in the use of certain skills that you can use them reliably even under adverse
conditions. When making a skill check with one of these skills, you may take 10 even if stress and
distractions would normally prevent you from doing so.'''
    _name = 'skill mastery'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.grade = util.Counter(0)
        self.skills = util.FeatureList()

        self.skills.active_.pipe(
            ops.map(lambda p: ', '.join(p)),
            ops.map(lambda string: self.__doc__+'\nSkills: '+string),
            ).subscribe(self.doc_.on_next, util.log_error)

        def check_skill_mastery():
            if self.grade.remaining > 0:
                util.logger.warning('Unallocated slots remaining on skill mastery: %s', self.grade.remaining)
        self.character.add_to_build(-2, 1, check_skill_mastery)

    def add_skills(self, skills, source=None):
        for skill in skills: self.add_skill(skill, source)

    def add_skill(self, skill, source=None):
        if source is None and self.grade.remaining < 1:
            util.logger.warning('All skill mastery slots available have been allocated.'); return
        if source is None:
            x = self.skills.add(name=skill)
            self.grade.use(1)
        else:
            x = self.skills.add(name=skill, source=source)
        self.character.skills[skill]._notes.add(name='Mastery', condition=x.active_)

class SlipperyMind(core.Feature):
    '''This ability represents the rogue's ability to wriggle free from magical effects that would
otherwise control or compel her. If a rogue with slippery mind is affected by an enchantment spell
or effect and fails her saving throw, she can attempt it again 1 round later at the same DC. She
gets only this one extra chance to succeed on her saving throw. '''
    _name = 'slippery mind'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

#%% Sorcerer
class Sorcerer(core.Class):
    _name = 'sorcerer'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Bluff', 'Concentration', 'Craft', 'Knowledge (arcana)', 'Profession',
                     'Spellcraft']
    proficiencies = ['simple']
    starting_gold = '3d4 x 10'; start = 'simple'
    advancement = {1: ['Spellcasting', 'SummonFamiliar']}

class SorcererSpellcasting(core.Spellcasting):
    _ability = 'charisma'
    magic_type = 'arcane'
    caster_type = 'spontaneous'
    clss = 'sorcerer'
    _spell_list = 'sorwiz'
    _spells_per_day = {
        1: [5,3], 2: [6,4], 3: [6,5], 4: [6,6,3], 5: [6,6,4], 6: [6,6,5,3], 7: [6,6,6,4],
        8: [6,6,6,5,3], 9: [6,6,6,6,4], 10: [6,6,6,6,5,3], 11: [6,6,6,6,6,4], 12: [6,6,6,6,6,5,3],
        13: [6,6,6,6,6,6,4], 14: [6,6,6,6,6,6,5,3], 15: [6,6,6,6,6,6,6,4], 16: [6,6,6,6,6,6,6,5,3],
        17: [6,6,6,6,6,6,6,6,4], 18: [6,6,6,6,6,6,6,6,5,3], 19: [6,6,6,6,6,6,6,6,6,4],
        20: [6,6,6,6,6,6,6,6,6,6],
        }
    _spells_known = {
        1: [4,2], 2: [5,2], 3: [5,3], 4: [6,3,1], 5: [6,4,2], 6: [7,4,2,1], 7: [7,5,3,2],
        8: [8,5,3,2,1], 9: [8,5,4,3,2], 10: [9,5,4,3,2,1], 11: [9,5,5,4,3,2], 12: [9,5,5,4,3,2,1],
        13: [9,5,5,4,4,3,2], 14: [9,5,5,4,4,3,2,1], 15: [9,5,5,4,4,4,3,2], 16: [9,5,5,4,4,4,3,2,1],
        17: [9,5,5,4,4,4,3,3,2], 18: [9,5,5,4,4,4,3,3,2,1], 19: [9,5,5,4,4,4,3,3,3,2],
        20: [9,5,5,4,4,4,3,3,3,3],
        }

#%% Wizard
class Wizard(core.Class):
    _name = 'wizard'
    _hit_die = 4; skill_points = 2; bab_type = 'half'; good_saves = ['Will']
    _class_skills = ['Concentration', 'Craft', 'Decipher Script', 'Knowledge', 'Profession',
                     'Spellcraft']
    proficiencies = ['club', 'dagger', 'heavy crossbow', 'light crossbow', 'quarterstaff']
    starting_gold = '3d4 x 10'; start = 'complex'
    advancement = core.get_class_advancement({
        'BonusFeat': list(range(5,21,5)),
        ('Spellcasting', 'SummonFamiliar', 'ScribeScroll'): [1]
        })
    feats = ['metamagic', 'item creation', 'Spell Mastery']

    def __init__(self, character):
        super().__init__(character)
        self.character.skills.bonus_languages.add(name='Draconic', source=self)
        self.specialty = None
        self.prohibited = None

    def specialize(self, school, prohibited_schools):
        self.spellcasting.specialize(school, prohibited_schools)
        self.specialty = self.spellcasting.specialty
        self.prohibited_schools = self.spellcasting.prohibited_schools

    def ScribeScroll(self):
        self.character.feats.add(item='ScribeScroll', source=self, override=True)

    def __str__(self):
        if not self.specialty:
            return super().__str__()
        match self.specialty:
            case 'abjuration': return 'abjurer'
            case 'conjuration': return 'conjurer'
            case 'divination': return 'diviner'
            case 'enchantment': return 'enchanter'
            case 'evocation': return 'evoker'
            case 'illusion': return 'illusionist'
            case 'necromancy': return 'necromancer'
            case 'transmutation': return 'transmuter'

class WizardSpellcasting(core.Spellcasting):
    _ability = 'intelligence'
    magic_type = 'arcane'
    caster_type = 'prepared'
    _spell_list = 'sorwiz'
    clss = 'wizard'
    _spells_per_day = {
        1: [3,1], 2: [4,2],
        3: [4,2,1], 4: [4,3,2],
        5: [4,3,2,1], 6: [4,3,3,2],
        7: [4,4,3,2,1], 8: [4,4,3,3,2],
        9: [4,4,4,3,2,1], 10: [4,4,4,3,3,2],
        11: [4,4,4,4,3,2,1], 12: [4,4,4,4,3,3,2],
        13: [4,4,4,4,4,3,2,1], 14: [4,4,4,4,4,3,3,2],
        15: [4,4,4,4,4,4,3,2,1], 16: [4,4,4,4,4,4,3,3,2],
        17: [4,4,4,4,4,4,4,3,2,1], 18: [4,4,4,4,4,4,4,3,3,2],
        19: [4,4,4,4,4,4,4,4,3,3], 20: [4,4,4,4,4,4,4,4,4,4],
        }

    def __init__(self, character):
        super().__init__(character)
        self.specialty = None
        self.prohibited_schools = []

        self.spells_known = core.Spellbooks(self)
        self.spells_known.add(item=['AcidSplash', 'ArcaneMark', 'DancingLights', 'Daze',
            'DetectMagic', 'DetectPoison', 'DisruptUndead', 'Flare', 'GhostSound', 'Light',
            'MageHand', 'Mending', 'Message', 'OpenClose', 'Prestidigitation', 'RayOfFrost',
            'ReadMagic', 'Resistance', 'TouchOfFatigue'], source='free')

    def specialize(self, school, prohibited_schools):
        spec = school.title()
        prhbt = [school.title() for school in prohibited_schools]

        if (spec not in util.schools) or any(school not in util.schools for school in prhbt):
            print('School not recognized'); return
        if (len(prhbt) != (1 if spec=='divination' else 2)):
            print('Invalid number of prohibited schools'); return
        if 'divination' in prohibited_schools:
            print("Invalid prohibited school: 'divination'"); return

        self.specialty = spec
        self.prohibited_schools = prhbt
        chall_ = self.character.challenges.register(check=f'learn {spec} spell')
        self.character.skills['Spellcraft'].add(2, condition=chall_)
        self.spells_known._add_prohibited_schools(prhbt)

#%% Shared features

class AnimalCompanion(core.Feature):
    _name = 'animal companion'
    def __init__(self, character):
        super().__init__(character) # grade, # companions = []
        self.effective_level = util.Attribute()
        effective_ = self.effective_level.attribute_.pipe(
            ops.map(lambda x: x > 0), ops.distinct_until_changed()
            )
        self.add_condition(effective_)
        raise NotImplementedError
        # you get a cohort
        self.companion = None

    def available_animals(self, aquatic=False):
        if hasattr(self.character.region, 'animals') and len(self.character.region.animals) > 0:
            return self.character.region.animals

        else: return self._get_default_animals(self, aquatic)

    def _get_default_animals(self, aquatic=False):
        if aquatic:
            return {
                1: ['Porpoise', 'MediumShark', 'Squid'], 4: ['Crocodile', 'LargeShark'], 7: ['Elasmosaurus'],
                10: ['HugeShark', 'Orca'], 13: ['GiantOctopus'], 18: ['DireShark', 'GiantSquid']
                }

        return {
            1: ['Badger', 'Camel', 'DireRat', 'Dog', 'RidingDog', 'Eagle', 'Hawk', 'LightHorse', 'HeavyHorse',
                'Owl', 'Pony', 'SmallViper', 'MediumViper', 'Wolf'],
            4: ['Ape', 'BlackBear', 'Bison', 'Boar', 'Cheetah', 'DireBadger', 'DireBat', 'DireWeasel', 'Leopard',
                'MonitorLizard', 'Constrictor', 'LargeViper', 'Wolverine'],
            7: ['BrownBear', 'GiantCrocodile', 'Deinonychus', 'DireApe', 'DireBoar', 'DireWolf', 'DireWolverine',
                'Lion', 'Rhinoceros', 'HugeViper', 'Tiger'],
            10: ['PolarBear', 'DireLion', 'Megaraptor', 'GiantConstrictor'],
            13: ['DireBear', 'Elephant'], 16: ['DireTiger', 'Triceratops', 'Tyrannosaurus']
            }

class Evasion(core.Feature):
    '''At 2nd level and higher, a rogue can avoid even magical and unusual attacks with great agility. If
she makes a successful Reflex saving throw against an attack that normally deals half damage on a
successful save, she instead takes no damage. Evasion can be used only if the rogue is wearing light
armor or no armor. A helpless rogue does not gain the benefit of evasion. '''
    _name = 'evasion'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        armor_ = self.character.equipment.armor_encumbrance_.pipe(
            ops.map(lambda x: x in ['none', 'light']), ops.distinct_until_changed()
            )
        not_helpless_ = self.character.conditions.register('helpless').pipe(ops.map(lambda p: not p))

        self.character.saves['Reflex']._notes.add(name='Evasion', condition=[armor_, not_helpless_])

class ImprovedEvasion(core.Feature):
    '''This ability works like evasion, except that while the rogue still takes no damage on a successful
Reflex saving throw against attacks henceforth she takes only half damage on a failed save. A
helpless rogue does not gain the benefit of improved evasion.'''
    _name = 'improved evasion'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        encumbrance_test_ = self.character.equipment.encumbrance_.pipe(
            ops.map(lambda x: x=='light'),
            ops.distinct_until_changed()
            )
        not_helpless_ = self.character.conditions.register('helpless').pipe(ops.map(lambda p: not p))

        self.character.saves['Reflex']._notes.add(name=self.name,
                                                  condition=[encumbrance_test_, not_helpless_])

class HideInPlainSight(core.Feature):
    _name = 'hide in plain sight'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.benefit = self.character.skills['Hide']._notes.add(name='Hide while observed', active=False)

    def set_terrain(self, terrain):
        terrain_ = self.character.challenges.register(location=terrain)
        self.benefit.add_condition(terrain_)

class SummonFamiliar(core.Feature):
    _name = 'summon familiar'
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute()

    def summon(self, familiar_class):
        fam = familiar_class(self.character)
        fam.master_level = self.effective_level
        self.character.equipment.add(obj=core.CustomGear(self.character, self.name, 100))
        self.character.companions.add(obj=fam, source=self)

    def add_source(self, source):
        super().add_source(source)
        self.effective_level.add(source.level, 'base', source=source)

class TimelessBody(core.Feature):
    _name = 'timeless body'
    _tags = ['extraordinary']
    def __init__(self, character): raise NotImplementedError

class TrapSense(core.Feature):
    '''At 3rd level, a rogue gains an intuitive sense that alerts her to danger from traps, giving her a +1
bonus on Reflex saves made to avoid traps and a +1 dodge bonus to AC against attacks made by traps.
These bonuses rise to +2 when the rogue reaches 6th level, to +3 when she reaches 9th level, to +4
when she reaches 12th level, to +5 at 15th, and to +6 at 18th level.

Trap sense bonuses gained from multiple classes stack.'''
    _name = 'trap sense'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        trap_ = self.character.challenges.register(challenge='trap')
        self.character.saves['Reflex'].add(self.grade, condition=trap_)
        self.character.AC['all'].add(self.grade, condition=trap_)

        self.grade.attribute_.pipe(ops.map(lambda x: f'{self._name} +{x}')).subscribe(self.name_.on_next, util.log_error)
    def escalate(self): self.grade.attribute += 1

class TurnRebukeUndead(core.Feature):
    _name = 'turn/rebuke undead'
    _tags = ['supernatural']

class RebukeUndead(TurnRebukeUndead):
    _name = 'rebuke undead'
    def __init__(self, character): raise NotImplementedError

class TurnUndead(TurnRebukeUndead):
    _name = 'turn undead'
    def __init__(self, character): raise NotImplementedError

class turn_undead(core.Check):
    _name = 'turn undead'
    def __init__(self, character):
        super().__init__(character)
        self.parent = self.character.checks['charisma']
        self.enabled = False

class UncannyDodge(core.Feature):
    '''Starting at 4th level, a rogue can react to danger before her senses would normally allow her to do
so. She retains her Dexterity bonus to AC (if any) even if she is caught flat-footed or struck by an
invisible attacker. However, she still loses her Dexterity bonus to AC if immobilized.

If a rogue already has uncanny dodge from a different class she automatically gains improved uncanny
dodge instead.'''
    _name = 'uncanny dodge'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.AC['flat-footed'] = self.character.AC['normal']

    def escalate(self):
        self.character.features.add_if_missing(item='ImprovedUncannyDodge', source=self)

class ImprovedUncannyDodge(core.Feature):
    ''' A rogue of 8th level or higher can no longer be flanked.

This defense denies another rogue the ability to sneak attack the character by flanking her, unless
the attacker has at least four more rogue levels than the target does.

If a character already has uncanny dodge from a second class, the character automatically gains
improved uncanny dodge instead, and the levels from the classes that grant uncanny dodge stack to
determine the minimum rogue level required to flank the character.'''
    _name = 'improved uncanny dodge'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.effective_level = util.Attribute(4)
        self.character.AC['all']._notes.add(source=self, name=f'Only flanked by {self.effective_level}th level rogue')

    def add_source(self, source):
        super().add_source(source)
        self.effective_level.add(source.level, 'base', source=source)

class WildEmpathy(core.Feature):
    '''You can improve the attitude of an animal. This ability functions just like a Diplomacy check to
improve the attitude of a person. You roll 1d20 and adds your class levels and Charisma modifier to
determine the wild empathy check result. The typical domestic animal has a starting attitude of
indifferent, while wild animals are usually unfriendly.

To use wild empathy, you and the animal must be able to study each other, which means that you must
be within 30 feet of one another under normal visibility conditions. Generally, influencing an
animal in this way takes 1 minute, but, as with influencing people, it might take more or less time.

You can also use this ability to influence a magical beast with an Intelligence score of 1 or 2, but
you take a -4 penalty on the check.'''
    _name = 'wild empathy'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.check = self.character.checks['wild empathy']
        self.check.enabled = True
        self.effective_level = util.Attribute()
        self.check.add(self.effective_level, 'base', source=self)

    def add_source(self, source):
        super().add_source(source)
        self.effective_level.add(source.level, 'base', source=source)

class wild_empathy(core.Check):
    _name = 'wild empathy'
    _ability = 'charisma'
    _enabled = False
    def __init__(self, character):
        super().__init__(character)
        self.add(-4, condition=self.character.challenges.register(target='magical beast'), source=self)

class WoodlandStride(core.Feature):
    _name = 'woodland stride'
    _tags = ['extraordinary']
    def __init__(self, character):
        super().__init__(character)
        self.character.speed['land']._notes.add(name='Ignore difficult terrain due to underbrush',
            condition=self.character.challenges.register(location='natural terrain'))
