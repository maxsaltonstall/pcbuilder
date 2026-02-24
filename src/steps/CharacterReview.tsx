import {
  Box,
  Button,
  Typography,
  Paper,
  Grid,
  Chip,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  LinearProgress,
  Tooltip,
  Card,
  CardContent,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SaveIcon from '@mui/icons-material/Save';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import PersonIcon from '@mui/icons-material/Person';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import SchoolIcon from '@mui/icons-material/School';
import { useState } from 'react';
import { useCharacter } from '../context/CharacterContext';
import { CharacterState } from '../types/character';
import { calculateTotalSkillPoints, getAbilityModifier, getSkillPointsPerLevel, getMagicItemIntBonus } from '../services/skillCalculator';
import { allocateSkillPoints } from '../services/skillRecommendations';
import { recommendFeats } from '../services/featRecommendations';
import { calculateCombatStats, calculateSpellSlots } from '../services/combatCalculations';
import { recommendEquipment } from '../services/equipmentRecommendations';
import { calculateSpellcasting } from '../services/spellcastingCalculator';
import { generateEquipmentRecommendations } from '../services/equipmentCalculator';
import { detectActiveFeatChains, analyzeFeatSynergies } from '../services/featChainDetector';
import { saveCharacterToFile, loadCharacterFromFile } from '../services/characterStorage';
import { SpellList } from '../components/SpellList';
import CharacterComparison from '../components/CharacterComparison';
import ProgressionTimeline from '../components/ProgressionTimeline';
import ClassDistribution from '../components/ClassDistribution';
import AbilityGrowthChart from '../components/AbilityGrowthChart';
import SkillsDisplay from '../components/SkillsDisplay';

interface CharacterReviewProps {
  onBack: () => void;
}

function CharacterReview({ onBack }: CharacterReviewProps) {
  const { state, resetCharacter, loadCharacter } = useCharacter();
  const [comparisonCharacter, setComparisonCharacter] = useState<CharacterState | null>(null);
  const [showComparison, setShowComparison] = useState(false);

  const handleSave = () => {
    try {
      saveCharacterToFile(state, state.concept);
      // Show success message
      alert('Character saved successfully!');
    } catch (error) {
      console.error('Error saving character:', error);
      alert('Failed to save character. Please try again.');
    }
  };

  const handleLoad = async () => {
    if (state.concept && !window.confirm('Load a character? This will replace your current character.')) {
      return;
    }

    try {
      const savedCharacter = await loadCharacterFromFile();
      loadCharacter(savedCharacter);
      alert(`Character "${savedCharacter.characterName}" loaded successfully!`);
    } catch (error) {
      console.error('Error loading character:', error);
      if (error instanceof Error) {
        alert(`Failed to load character: ${error.message}`);
      } else {
        alert('Failed to load character. Please check the file and try again.');
      }
    }
  };

  const handleNewCharacter = () => {
    if (window.confirm('Are you sure? This will clear all character data.')) {
      resetCharacter();
    }
  };

  const handleCompare = async () => {
    try {
      const savedCharacter = await loadCharacterFromFile();
      setComparisonCharacter(savedCharacter);
      setShowComparison(true);
    } catch (error) {
      console.error('Error loading character for comparison:', error);
      alert('Failed to load character for comparison.');
    }
  };

  const progression = state.optimizedProgression;

  // Calculate class distribution from progression
  const classDistribution: Record<string, number> = {};
  progression.forEach(level => {
    const className = level.class.name;
    classDistribution[className] = (classDistribution[className] || 0) + 1;
  });

  // Calculate total skill points
  const totalSkillPoints = state.abilityScores && progression.length > 0
    ? calculateTotalSkillPoints(progression, state.abilityScores, state.assumeMagicItems)
    : 0;

  // Get skill points per level breakdown
  const skillPointsPerLevel = state.abilityScores && progression.length > 0
    ? getSkillPointsPerLevel(progression, state.abilityScores, state.assumeMagicItems)
    : [];

  // Calculate running total and INT tracking for display
  const skillPointBreakdown = progression.map((level, index) => {
    const characterLevel = index + 1;
    let currentInt = state.abilityScores?.intelligence || 10;

    // Account for INT increases at levels 4, 8, 12, 16, 20, etc.
    for (let i = 0; i < index; i++) {
      if ((i + 1) % 4 === 0 && progression[i].abilityIncrease === 'int') {
        currentInt += 1;
      }
    }

    // Add magic item bonus if enabled
    const magicItemBonus = state.assumeMagicItems ? getMagicItemIntBonus(characterLevel) : 0;
    const effectiveInt = currentInt + magicItemBonus;

    const intMod = getAbilityModifier(effectiveInt);
    const basePoints = level.class.skillPointsPerLevel;
    const multiplier = characterLevel === 1 ? 4 : 1;
    const pointsThisLevel = skillPointsPerLevel[index] || 0;
    const runningTotal = skillPointsPerLevel.slice(0, index + 1).reduce((sum, pts) => sum + pts, 0);

    return {
      level: characterLevel,
      className: level.class.name,
      basePoints,
      intMod,
      currentInt,
      magicItemBonus,
      effectiveInt,
      multiplier,
      pointsThisLevel,
      runningTotal,
      intIncreased: characterLevel % 4 === 0 && level.abilityIncrease === 'int',
    };
  });

  // Generate skill recommendations
  const skillAllocations = state.abilityScores && progression.length > 0
    ? allocateSkillPoints(
        totalSkillPoints,
        state.keySkills,
        progression,
        state.abilityScores,
        state.focus
      )
    : [];

  // Generate feat recommendations
  const featRecommendations = recommendFeats(
    progression,
    state.desiredFeats,
    state.focus
  );

  // Get all feats from progression
  const allFeats = progression
    .filter(l => l.featGained)
    .map(l => l.featGained!);

  // Calculate combat stats
  const combatStats = state.abilityScores && progression.length > 0
    ? calculateCombatStats(
        progression,
        state.abilityScores,
        state.assumeMagicItems || false,
        allFeats
      )
    : null;

  // Calculate spell slots for casters
  const spellSlots = state.abilityScores && progression.length > 0
    ? calculateSpellSlots(progression, state.abilityScores)
    : [];

  // Get equipment recommendations
  const recommendedEquipment = recommendEquipment(
    state.totalLevel,
    state.focus,
    state.assumeMagicItems || false
  );

  // Detect feat chains and synergies
  const featChainProgress = detectActiveFeatChains(allFeats, state.focus);
  const featSynergies = analyzeFeatSynergies(allFeats);

  // Get ability score increases
  const abilityIncreases = progression
    .filter(l => l.abilityIncrease)
    .map(l => ({ level: l.levelNumber, ability: l.abilityIncrease! }));

  // Show comparison view if active
  if (showComparison && comparisonCharacter) {
    return (
      <CharacterComparison
        character1={state}
        character2={comparisonCharacter}
        onClose={() => setShowComparison(false)}
      />
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Character Review
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Review your completed character and export when ready.
      </Typography>

      <Paper elevation={3} sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <PersonIcon sx={{ mr: 1, fontSize: 32 }} />
          <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
            {state.concept || 'Unnamed Character'}
          </Typography>
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: 'rgba(255,255,255,0.95)' }}>
              <CardContent>
                <Typography variant="caption" color="text.secondary">Level</Typography>
                <Typography variant="h4" color="primary">
                  {state.totalLevel}
                  {state.totalLevel > 20 && (
                    <Chip label="EPIC" size="small" color="warning" sx={{ ml: 1 }} />
                  )}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {combatStats && (
            <>
              <Grid item xs={12} sm={6} md={3}>
                <Tooltip title="Hit Points - Your character's health pool">
                  <Card sx={{ bgcolor: 'rgba(255,255,255,0.95)' }}>
                    <CardContent>
                      <Typography variant="caption" color="text.secondary">HP</Typography>
                      <Typography variant="h4" color="error.main">
                        {combatStats.hp}
                      </Typography>
                    </CardContent>
                  </Card>
                </Tooltip>
              </Grid>

              <Grid item xs={12} sm={6} md={3}>
                <Tooltip title="Base Attack Bonus - Your accuracy in combat">
                  <Card sx={{ bgcolor: 'rgba(255,255,255,0.95)' }}>
                    <CardContent>
                      <Typography variant="caption" color="text.secondary">BAB</Typography>
                      <Typography variant="h4" color="success.main">
                        +{combatStats.baseAttackBonus}
                      </Typography>
                    </CardContent>
                  </Card>
                </Tooltip>
              </Grid>

              <Grid item xs={12} sm={6} md={3}>
                <Tooltip title="Armor Class - Your defense against attacks">
                  <Card sx={{ bgcolor: 'rgba(255,255,255,0.95)' }}>
                    <CardContent>
                      <Typography variant="caption" color="text.secondary">AC</Typography>
                      <Typography variant="h4" color="info.main">
                        {combatStats.ac}
                      </Typography>
                    </CardContent>
                  </Card>
                </Tooltip>
              </Grid>
            </>
          )}
        </Grid>

        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" sx={{ opacity: 0.9, fontWeight: 500 }}>
            {Object.entries(classDistribution)
              .map(([className, levels]) => `${className} ${levels}`)
              .join(' / ')}
          </Typography>
          {state.race && (
            <Chip
              label={state.race.raceName}
              size="small"
              color="secondary"
              sx={{ mt: 1 }}
            />
          )}
        </Box>

        <Divider sx={{ my: 2 }} />

        {state.race && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Racial Traits
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {Object.entries(state.race.abilityModifiers).length > 0 && (
                Object.entries(state.race.abilityModifiers).map(([ability, modifier]) => (
                  <Chip
                    key={ability}
                    label={`${ability.substring(0, 3).toUpperCase()} ${modifier > 0 ? '+' : ''}${modifier}`}
                    size="small"
                    color={modifier > 0 ? 'success' : 'default'}
                  />
                ))
              )}
              {state.race.traits.slice(0, 3).map((trait, index) => (
                <Chip
                  key={index}
                  label={trait.name}
                  size="small"
                  variant="outlined"
                />
              ))}
            </Box>
          </Box>
        )}

        {state.deity && (() => {
          const deitiesData = require('@data/deities.json');
          const domainsData = require('@data/domains.json');
          const deity = deitiesData.find((d: any) => d.id === state.deity!.deityId);
          const selectedDomains = state.deity.selectedDomains
            .map((domainId: string) => domainsData.find((d: any) => d.id === domainId))
            .filter(Boolean);

          const getAlignmentColor = (alignment: string): string => {
            if (alignment.includes('G')) return '#4caf50';
            if (alignment.includes('E')) return '#f44336';
            return '#9e9e9e';
          };

          return (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                Deity & Domains
              </Typography>
              <Box sx={{ mb: 1 }}>
                <Typography variant="body2" component="span">
                  <strong>{deity?.name}</strong> - {deity?.title}
                </Typography>
                <Chip
                  label={deity?.alignment}
                  size="small"
                  sx={{
                    bgcolor: getAlignmentColor(deity?.alignment || ''),
                    color: 'white',
                    ml: 1,
                    fontSize: '0.75rem'
                  }}
                />
              </Box>
              <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
                {deity?.portfolio}
              </Typography>
              <Box sx={{ mb: 1 }}>
                <Typography variant="caption" color="text.secondary" component="span">
                  Domains:{' '}
                </Typography>
                {selectedDomains.map((domain: any, index: number) => (
                  <Chip
                    key={index}
                    label={domain.name}
                    size="small"
                    variant="outlined"
                    sx={{ mr: 0.5 }}
                  />
                ))}
              </Box>
              {selectedDomains.map((domain: any) => (
                <Box key={domain.id} sx={{ mt: 1, pl: 2, borderLeft: '2px solid #1976d2' }}>
                  <Typography variant="caption" display="block">
                    <strong>{domain.name}:</strong> {domain.grantedPower}
                  </Typography>
                </Box>
              ))}
            </Box>
          );
        })()}

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Selected Classes (Priorities)
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {state.targetClasses.map((cls, index) => (
              <Chip
                key={index}
                label={`${cls.className} (${cls.priority || 'medium'})`}
                size="small"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Visualizations */}
        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6" color="primary">
              📊 Character Visualizations
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <ProgressionTimeline progression={progression} />
              </Grid>
              <Grid item xs={12} md={6}>
                <ClassDistribution progression={progression} />
              </Grid>
              <Grid item xs={12}>
                <AbilityGrowthChart
                  progression={progression}
                  baseAbilityScores={state.baseAbilityScores}
                  finalAbilityScores={state.abilityScores}
                />
              </Grid>
            </Grid>
          </AccordionDetails>
        </Accordion>

        <Divider sx={{ my: 2 }} />

        {/* Skills Section */}
        {(() => {
          // Calculate class skills from all classes in progression
          const classSkills: string[] = [];
          const classSkillSet = new Set<string>();
          progression.forEach(level => {
            level.class.classSkills.forEach(skill => classSkillSet.add(skill));
          });
          classSkillSet.forEach(skill => classSkills.push(skill));

          // For now, show key skills with estimated max ranks
          // TODO: Replace with actual skill allocation when implemented
          const skillRanks: Record<string, number> = {};
          const characterLevel = progression.length;
          const maxRanks = characterLevel + 3;

          state.keySkills.forEach(skillId => {
            // Allocate max ranks to key skills as a demonstration
            skillRanks[skillId] = maxRanks;
          });

          return (
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6" color="primary">
                  🎯 Skills ({totalSkillPoints} total points)
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <SkillsDisplay
                  skillRanks={skillRanks}
                  classSkills={classSkills}
                />
              </AccordionDetails>
            </Accordion>
          );
        })()}

        {/* Spells Section */}
        {(() => {
          const spellcasting = state.abilityScores && progression.length > 0
            ? calculateSpellcasting(progression, state.abilityScores)
            : undefined;

          if (!spellcasting || spellcasting.spellcastingClasses.length === 0) {
            return null;
          }

          return (
            <Accordion defaultExpanded sx={{ mt: 2 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6" color="primary">
                  ✨ Spellcasting ({spellcasting.spellcastingClasses.length} {spellcasting.spellcastingClasses.length === 1 ? 'class' : 'classes'})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                {spellcasting.spellcastingClasses.map((casterInfo, idx) => (
                  <Card key={idx} sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom sx={{ textTransform: 'capitalize' }}>
                        {casterInfo.className} (CL {casterInfo.casterLevel})
                      </Typography>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Spells Per Day:
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {Object.entries(casterInfo.spellsPerDayByLevel).map(([level, count]) => (
                            <Chip
                              key={level}
                              label={`${level}: ${count === Infinity ? '∞' : count}`}
                              size="small"
                              color="primary"
                              variant="outlined"
                            />
                          ))}
                        </Box>
                      </Box>

                      {casterInfo.spellsKnownByLevel && (
                        <Box>
                          <Typography variant="subtitle2" gutterBottom>
                            Spells Known:
                          </Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {Object.entries(casterInfo.spellsKnownByLevel).map(([level, count]) => (
                              <Chip
                                key={level}
                                label={`${level}: ${count === Infinity ? 'All' : count}`}
                                size="small"
                                color="secondary"
                                variant="outlined"
                              />
                            ))}
                          </Box>
                        </Box>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </AccordionDetails>
            </Accordion>
          );
        })()}

        {/* Equipment Section */}
        {(() => {
          if (!state.focus) return null;

          const equipment = generateEquipmentRecommendations(state.totalLevel, state.focus);

          return (
            <Accordion defaultExpanded sx={{ mt: 2 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6" color="primary">
                  💰 Equipment & Wealth ({equipment.totalBudget.toLocaleString()} gp)
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2} sx={{ mb: 2 }}>
                  <Grid item xs={12} sm={6} md={4}>
                    <Chip
                      label={`Weapons: ${equipment.allocations.weapons.toLocaleString()} gp`}
                      color="primary"
                      sx={{ width: '100%' }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <Chip
                      label={`Armor: ${equipment.allocations.armor.toLocaleString()} gp`}
                      color="primary"
                      sx={{ width: '100%' }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <Chip
                      label={`Ability Items: ${equipment.allocations.abilityItems.toLocaleString()} gp`}
                      color="secondary"
                      sx={{ width: '100%' }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <Chip
                      label={`Protection: ${equipment.allocations.protectionItems.toLocaleString()} gp`}
                      color="secondary"
                      sx={{ width: '100%' }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <Chip
                      label={`Utility: ${equipment.allocations.utilityItems.toLocaleString()} gp`}
                      sx={{ width: '100%' }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <Chip
                      label={`Consumables: ${equipment.allocations.consumables.toLocaleString()} gp`}
                      sx={{ width: '100%' }}
                    />
                  </Grid>
                </Grid>

                {equipment.recommendedItems.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom fontWeight="bold">
                      Priority Items:
                    </Typography>
                    {equipment.recommendedItems.map((item, idx) => (
                      <Card key={idx} sx={{ mb: 1, bgcolor: 'warning.50' }}>
                        <CardContent sx={{ py: 1 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="subtitle2" fontWeight="bold">
                              {item.name}
                            </Typography>
                            <Chip label={`${item.cost.toLocaleString()} gp`} size="small" />
                          </Box>
                          <Typography variant="caption" color="text.secondary">
                            {item.description}
                          </Typography>
                        </CardContent>
                      </Card>
                    ))}
                  </Box>
                )}
              </AccordionDetails>
            </Accordion>
          );
        })()}

        <Divider sx={{ my: 2 }} />

        {state.abilityScores && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Ability Scores (Final)
            </Typography>
            <Grid container spacing={1}>
              {[
                { label: 'STR', value: state.abilityScores.strength, key: 'strength' },
                { label: 'DEX', value: state.abilityScores.dexterity, key: 'dexterity' },
                { label: 'CON', value: state.abilityScores.constitution, key: 'constitution' },
                { label: 'INT', value: state.abilityScores.intelligence, key: 'intelligence' },
                { label: 'WIS', value: state.abilityScores.wisdom, key: 'wisdom' },
                { label: 'CHA', value: state.abilityScores.charisma, key: 'charisma' },
              ].map(({ label, value }) => {
                const modifier = getAbilityModifier(value);
                return (
                  <Grid item xs={4} sm={2} key={label}>
                    <Paper variant="outlined" sx={{ p: 1, textAlign: 'center' }}>
                      <Typography variant="caption" color="text.secondary">
                        {label}
                      </Typography>
                      <Typography variant="h6">
                        {value}
                      </Typography>
                      <Typography variant="caption" color={modifier >= 0 ? 'success.main' : 'error.main'}>
                        {modifier >= 0 ? '+' : ''}{modifier}
                      </Typography>
                    </Paper>
                  </Grid>
                );
              })}
            </Grid>
          </Box>
        )}

        <Divider sx={{ my: 2 }} />

        {combatStats && (
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <FitnessCenterIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6" color="primary">
                Combat Statistics
              </Typography>
            </Box>

            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={6} sm={3}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center', bgcolor: 'error.50' }}>
                  <Typography variant="subtitle2" color="text.secondary">Hit Points</Typography>
                  <Typography variant="h4" color="error.main">{combatStats.hp}</Typography>
                </Paper>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center', bgcolor: 'primary.50' }}>
                  <Typography variant="subtitle2" color="text.secondary">Armor Class</Typography>
                  <Typography variant="h4" color="primary.main">{combatStats.ac}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Touch {combatStats.touchAC}, FF {combatStats.flatFootedAC}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="subtitle2" color="text.secondary">Initiative</Typography>
                  <Typography variant="h4">{combatStats.initiative >= 0 ? '+' : ''}{combatStats.initiative}</Typography>
                </Paper>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="subtitle2" color="text.secondary">BAB</Typography>
                  <Typography variant="h4">+{combatStats.baseAttackBonus}</Typography>
                </Paper>
              </Grid>
            </Grid>

            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={12} sm={6}>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">Melee Attack</Typography>
                  <Typography variant="h5">{combatStats.meleeAttack}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    BAB + STR{allFeats.includes('weapon-focus') ? ' + Weapon Focus' : ''}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">Ranged Attack</Typography>
                  <Typography variant="h5">{combatStats.rangedAttack}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    BAB + DEX{allFeats.includes('weapon-focus') ? ' + Weapon Focus' : ''}
                  </Typography>
                </Paper>
              </Grid>
            </Grid>

            <Grid container spacing={2}>
              <Grid item xs={4}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center', bgcolor: 'success.50' }}>
                  <Typography variant="subtitle2" color="text.secondary">Fortitude</Typography>
                  <Typography variant="h5">+{combatStats.saves.fortitude}</Typography>
                </Paper>
              </Grid>
              <Grid item xs={4}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center', bgcolor: 'warning.50' }}>
                  <Typography variant="subtitle2" color="text.secondary">Reflex</Typography>
                  <Typography variant="h5">+{combatStats.saves.reflex}</Typography>
                </Paper>
              </Grid>
              <Grid item xs={4}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center', bgcolor: 'info.50' }}>
                  <Typography variant="subtitle2" color="text.secondary">Will</Typography>
                  <Typography variant="h5">+{combatStats.saves.will}</Typography>
                </Paper>
              </Grid>
            </Grid>

            {state.assumeMagicItems && (
              <Alert severity="info" sx={{ mt: 2 }}>
                AC includes wealth-appropriate magic armor, shield, natural armor bonus, and ring of protection
              </Alert>
            )}
          </Box>
        )}

        {spellSlots.length > 0 && (
          <>
            <Divider sx={{ my: 2 }} />
            <Box sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AutoFixHighIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" color="primary">
                  Spells Per Day
                </Typography>
              </Box>
              {spellSlots.map((caster) => (
                <Paper key={caster.casterClass} variant="outlined" sx={{ p: 2, mb: 2 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    <strong>{caster.casterClass}</strong> (Caster Level {caster.casterLevel})
                  </Typography>
                  <Grid container spacing={1}>
                    {Object.entries(caster.spellsPerDay)
                      .sort(([a], [b]) => Number(a) - Number(b))
                      .map(([level, slots]) => (
                        <Grid item xs={6} sm={4} md={3} key={level}>
                          <Paper variant="outlined" sx={{ p: 1, textAlign: 'center', bgcolor: 'secondary.50' }}>
                            <Typography variant="caption" color="text.secondary">
                              {level === '0' ? 'Cantrips' : `Level ${level}`}
                            </Typography>
                            <Typography variant="h6">
                              {slots}
                            </Typography>
                          </Paper>
                        </Grid>
                      ))}
                  </Grid>
                  {caster.spellsKnown && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        Spells Known: {Object.entries(caster.spellsKnown)
                          .sort(([a], [b]) => Number(a) - Number(b))
                          .map(([level, known]) => `${level}: ${known}`)
                          .join(', ')}
                      </Typography>
                    </Box>
                  )}

                  {/* Spell List */}
                  <Box sx={{ mt: 2 }}>
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="subtitle2">
                          📜 Available Spells
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <SpellList
                          casterClass={caster.casterClass}
                          casterLevel={caster.casterLevel}
                          highestSpellLevel={Math.max(...Object.keys(caster.spellsPerDay).map(Number))}
                        />
                      </AccordionDetails>
                    </Accordion>
                  </Box>
                </Paper>
              ))}
            </Box>
          </>
        )}

        {recommendedEquipment.length > 0 && (
          <>
            <Divider sx={{ my: 2 }} />
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6" color="primary" gutterBottom>
                Recommended Equipment
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Wealth-appropriate magic items for level {state.totalLevel} ({state.focus} focus)
              </Typography>

              <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="subtitle1">
                    🎒 Equipment List ({recommendedEquipment.length} items)
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell><strong>Item</strong></TableCell>
                          <TableCell><strong>Slot</strong></TableCell>
                          <TableCell><strong>Bonus</strong></TableCell>
                          <TableCell align="right"><strong>Cost (gp)</strong></TableCell>
                          <TableCell><strong>Purpose</strong></TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {recommendedEquipment.map((item, index) => (
                          <TableRow key={index}>
                            <TableCell>
                              <strong>{item.name}</strong>
                            </TableCell>
                            <TableCell>
                              <Chip
                                label={item.slot}
                                size="small"
                                variant="outlined"
                                sx={{ fontSize: '0.7rem' }}
                              />
                            </TableCell>
                            <TableCell>{item.bonus}</TableCell>
                            <TableCell align="right">
                              {item.cost.toLocaleString()}
                            </TableCell>
                            <TableCell>
                              <Typography variant="caption" color="text.secondary">
                                {item.reason}
                              </Typography>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>

                  <Alert severity="info" sx={{ mt: 2 }}>
                    <strong>The "Big 6" Priority:</strong> Weapon, Armor, Ability Booster, Cloak of Resistance, Ring of Protection, Amulet of Natural Armor.
                    These items provide the most essential bonuses for any build.
                  </Alert>
                </AccordionDetails>
              </Accordion>
            </Box>
          </>
        )}

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <SchoolIcon sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h6" color="primary">
              Skill Points
            </Typography>
          </Box>
          <Typography variant="h5" gutterBottom>
            Total: {totalSkillPoints} points
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Priority Skills: {state.keySkills.join(', ') || 'None selected'}
          </Typography>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1">
                📊 Detailed Level-by-Level Breakdown
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                This shows how your skill points accumulate through multiclassing.
                The optimizer front-loads high skill-point classes to maximize your total.
                Level 1 gets ×4 multiplier. INT increases at levels 4, 8, 12, 16, 20+ apply forward from that level onwards (not retroactive).
              </Typography>

              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Level</strong></TableCell>
                      <TableCell><strong>Class</strong></TableCell>
                      <TableCell align="right"><strong>Base</strong></TableCell>
                      <TableCell align="right"><strong>INT</strong></TableCell>
                      <TableCell align="right"><strong>Multiplier</strong></TableCell>
                      <TableCell align="right"><strong>Points</strong></TableCell>
                      <TableCell align="right"><strong>Total</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {skillPointBreakdown.map((row) => (
                      <TableRow
                        key={row.level}
                        sx={{
                          backgroundColor: row.level === 1 ? 'success.50' :
                                          row.intIncreased ? 'info.50' :
                                          'inherit'
                        }}
                      >
                        <TableCell>{row.level}</TableCell>
                        <TableCell>
                          {row.className}
                          {row.intIncreased && (
                            <Chip
                              label="INT +1"
                              size="small"
                              color="info"
                              sx={{ ml: 1, height: 20, fontSize: '0.7rem' }}
                            />
                          )}
                        </TableCell>
                        <TableCell align="right">{row.basePoints}</TableCell>
                        <TableCell align="right">
                          {row.effectiveInt} ({row.intMod >= 0 ? '+' : ''}{row.intMod})
                          {row.magicItemBonus > 0 && (
                            <Typography variant="caption" display="block" color="success.main">
                              +{row.magicItemBonus} item
                            </Typography>
                          )}
                        </TableCell>
                        <TableCell align="right">
                          {row.multiplier > 1 ? (
                            <strong style={{ color: 'green' }}>×{row.multiplier}</strong>
                          ) : (
                            '×1'
                          )}
                        </TableCell>
                        <TableCell align="right">
                          <strong>{row.pointsThisLevel}</strong>
                        </TableCell>
                        <TableCell align="right">
                          <strong>{row.runningTotal}</strong>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>

              <Box sx={{ mt: 2, p: 2, backgroundColor: 'info.50', borderRadius: 1 }}>
                <Typography variant="subtitle2" gutterBottom>
                  💡 Why This Class Order?
                </Typography>
                <Typography variant="body2">
                  <strong>Front-loading high skill-point classes</strong> (like Rogue, Bard, Ranger)
                  maximizes total points due to the level 1 ×4 multiplier.
                  A Rogue 1 with 14 INT gets (8+2)×4 = <strong>40 points</strong>,
                  while Fighter 1 gets only (2+2)×4 = <strong>16 points</strong>.
                  The optimizer arranges your classes to give you the most skill points possible.
                </Typography>
              </Box>
            </AccordionDetails>
          </Accordion>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 2 }}>
          <Typography variant="h6" color="primary" gutterBottom>
            Recommended Skills
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Optimized allocation based on your priorities and class skills
          </Typography>

          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1">
                📋 Skill Allocations ({skillAllocations.length} skills)
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Skill</strong></TableCell>
                      <TableCell align="center"><strong>Ranks</strong></TableCell>
                      <TableCell align="center"><strong>Ability</strong></TableCell>
                      <TableCell align="center"><strong>Class</strong></TableCell>
                      <TableCell align="center"><strong>Total</strong></TableCell>
                      <TableCell><strong>Why?</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {skillAllocations.map((skill) => (
                      <TableRow key={skill.skillId}>
                        <TableCell>
                          <strong>{skill.skillName}</strong>
                          {state.keySkills.includes(skill.skillId) && (
                            <Chip
                              label="Priority"
                              size="small"
                              color="primary"
                              sx={{ ml: 1, height: 18, fontSize: '0.65rem' }}
                            />
                          )}
                        </TableCell>
                        <TableCell align="center">{skill.ranks}</TableCell>
                        <TableCell align="center">
                          {skill.abilityMod >= 0 ? '+' : ''}{skill.abilityMod}
                        </TableCell>
                        <TableCell align="center">
                          {skill.classSkillBonus > 0 ? (
                            <Chip
                              label={`+${skill.classSkillBonus}`}
                              size="small"
                              color="success"
                              sx={{ height: 18, fontSize: '0.65rem' }}
                            />
                          ) : (
                            '-'
                          )}
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="body2" fontWeight="bold" color="primary">
                            {skill.totalModifier >= 0 ? '+' : ''}{skill.totalModifier}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="caption" color="text.secondary">
                            {skill.explanation}
                          </Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </AccordionDetails>
          </Accordion>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 2 }}>
          <Typography variant="h6" color="primary" gutterBottom>
            Recommended Feats
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Build-optimized feat progression for your {state.focus} focus
          </Typography>

          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1">
                ⚔️ Feat Progression ({featRecommendations.length} feats)
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Level</strong></TableCell>
                      <TableCell><strong>Feat</strong></TableCell>
                      <TableCell><strong>Why?</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {featRecommendations.map((feat, index) => (
                      <TableRow
                        key={index}
                        sx={{
                          backgroundColor: feat.isUserRequested ? 'primary.50' : 'inherit'
                        }}
                      >
                        <TableCell>{feat.level}</TableCell>
                        <TableCell>
                          <strong>{feat.featName}</strong>
                          {feat.isUserRequested && (
                            <Chip
                              label="Your Choice"
                              size="small"
                              color="primary"
                              sx={{ ml: 1, height: 18, fontSize: '0.65rem' }}
                            />
                          )}
                        </TableCell>
                        <TableCell>
                          <Typography variant="caption" color="text.secondary">
                            {feat.reason}
                          </Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </AccordionDetails>
          </Accordion>
        </Box>

        {(featChainProgress.length > 0 || featSynergies.synergies.length > 0 || featSynergies.recommendations.length > 0) && (
          <>
            <Divider sx={{ my: 2 }} />
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6" color="primary" gutterBottom>
                Feat Chain Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Track your progress through feat chains and discover synergies
              </Typography>

              {featChainProgress.length > 0 && (
                <Accordion defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1">
                      🔗 Active Feat Chains ({featChainProgress.length})
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    {featChainProgress.map((chain, index) => (
                      <Paper key={index} variant="outlined" sx={{ p: 2, mb: 2 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                          <Typography variant="subtitle1">
                            <strong>{chain.chain.chainName}</strong>
                          </Typography>
                          <Chip
                            label={`${chain.completed}/${chain.total} complete`}
                            color={chain.percentComplete === 100 ? 'success' : chain.percentComplete > 0 ? 'primary' : 'default'}
                            size="small"
                          />
                        </Box>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          {chain.chain.description}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={chain.percentComplete}
                          sx={{ mb: 2, height: 8, borderRadius: 1 }}
                          color={chain.percentComplete === 100 ? 'success' : 'primary'}
                        />
                        <TableContainer>
                          <Table size="small">
                            <TableHead>
                              <TableRow>
                                <TableCell width="40">Status</TableCell>
                                <TableCell>Feat</TableCell>
                                <TableCell>Suggested Level</TableCell>
                                <TableCell>Purpose</TableCell>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {chain.chain.feats.map((feat, featIndex) => (
                                <TableRow
                                  key={featIndex}
                                  sx={{
                                    backgroundColor: feat.acquired ? 'success.50' :
                                                    chain.nextFeat?.featId === feat.featId ? 'warning.50' :
                                                    'inherit'
                                  }}
                                >
                                  <TableCell>
                                    {feat.acquired ? (
                                      <Chip label="✓" color="success" size="small" sx={{ width: 32, height: 24 }} />
                                    ) : chain.nextFeat?.featId === feat.featId ? (
                                      <Chip label="→" color="warning" size="small" sx={{ width: 32, height: 24 }} />
                                    ) : (
                                      <Chip label="○" variant="outlined" size="small" sx={{ width: 32, height: 24 }} />
                                    )}
                                  </TableCell>
                                  <TableCell>
                                    <strong>{feat.featName}</strong>
                                    {chain.nextFeat?.featId === feat.featId && (
                                      <Chip
                                        label="Next"
                                        color="warning"
                                        size="small"
                                        sx={{ ml: 1, height: 18, fontSize: '0.65rem' }}
                                      />
                                    )}
                                  </TableCell>
                                  <TableCell>{feat.level}</TableCell>
                                  <TableCell>
                                    <Typography variant="caption" color="text.secondary">
                                      {feat.reason}
                                    </Typography>
                                  </TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </Paper>
                    ))}
                  </AccordionDetails>
                </Accordion>
              )}

              {(featSynergies.synergies.length > 0 || featSynergies.recommendations.length > 0) && (
                <Box sx={{ mt: 2 }}>
                  {featSynergies.synergies.length > 0 && (
                    <Alert severity="success" sx={{ mb: 1 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        <strong>✨ Synergies Detected:</strong>
                      </Typography>
                      {featSynergies.synergies.map((synergy, index) => (
                        <Typography key={index} variant="body2">
                          • {synergy}
                        </Typography>
                      ))}
                    </Alert>
                  )}
                  {featSynergies.recommendations.length > 0 && (
                    <Alert severity="info">
                      <Typography variant="subtitle2" gutterBottom>
                        <strong>💡 Chain Recommendations:</strong>
                      </Typography>
                      {featSynergies.recommendations.map((rec, index) => (
                        <Typography key={index} variant="body2">
                          • {rec}
                        </Typography>
                      ))}
                    </Alert>
                  )}
                </Box>
              )}
            </Box>
          </>
        )}

        {abilityIncreases.length > 0 && (
          <>
            <Divider sx={{ my: 2 }} />
            <Box>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                Ability Score Increases
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {abilityIncreases.map((inc, index) => (
                  <Chip
                    key={index}
                    label={`Level ${inc.level}: ${inc.ability.toUpperCase()} +1`}
                    size="small"
                    color="secondary"
                  />
                ))}
              </Box>
            </Box>
          </>
        )}
      </Paper>

      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack}>Back</Button>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <Button
            startIcon={<FolderOpenIcon />}
            onClick={handleLoad}
            variant="outlined"
          >
            Load Character
          </Button>
          <Button
            startIcon={<SaveIcon />}
            onClick={handleSave}
            variant="contained"
            color="success"
          >
            Save Character
          </Button>
          <Button
            startIcon={<CompareArrowsIcon />}
            onClick={handleCompare}
            variant="outlined"
            color="info"
          >
            Compare
          </Button>
          <Button onClick={handleNewCharacter} color="warning">
            New Character
          </Button>
        </Box>
      </Box>
    </Box>
  );
}

export default CharacterReview;
