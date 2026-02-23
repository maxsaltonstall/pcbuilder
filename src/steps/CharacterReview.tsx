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
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useCharacter } from '../context/CharacterContext';
import { calculateTotalSkillPoints, getAbilityModifier, getSkillPointsPerLevel, getMagicItemIntBonus } from '../services/skillCalculator';
import { allocateSkillPoints } from '../services/skillRecommendations';
import { recommendFeats } from '../services/featRecommendations';

interface CharacterReviewProps {
  onBack: () => void;
}

function CharacterReview({ onBack }: CharacterReviewProps) {
  const { state, resetCharacter } = useCharacter();

  const handleExport = () => {
    // Export functionality to be implemented
    const characterData = {
      concept: state.concept,
      level: state.totalLevel,
      classes: state.targetClasses,
      abilityScores: state.abilityScores,
      progression: state.optimizedProgression,
      desiredFeats: state.desiredFeats,
      keySkills: state.keySkills,
    };

    const dataStr = JSON.stringify(characterData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${state.concept.replace(/\s+/g, '_')}_level_${state.totalLevel}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleNewCharacter = () => {
    if (window.confirm('Are you sure? This will clear all character data.')) {
      resetCharacter();
    }
  };

  const progression = state.optimizedProgression;
  const finalLevel = progression.length > 0 ? progression[progression.length - 1] : null;

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
      if ((i + 1) % 4 === 0 && progression[i].abilityIncrease === 'intelligence') {
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
      intIncreased: characterLevel % 4 === 0 && level.abilityIncrease === 'intelligence',
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

  // Get ability score increases
  const abilityIncreases = progression
    .filter(l => l.abilityIncrease)
    .map(l => ({ level: l.levelNumber, ability: l.abilityIncrease! }));

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Character Review
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Review your completed character and export when ready.
      </Typography>

      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom color="primary">
          {state.concept || 'Unnamed Character'}
        </Typography>

        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="text.secondary">Level</Typography>
            <Typography variant="h4">
              {state.totalLevel}
              {state.totalLevel > 20 && (
                <Typography component="span" variant="caption" color="warning.main" sx={{ ml: 1 }}>
                  Epic
                </Typography>
              )}
            </Typography>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="text.secondary">Classes</Typography>
            <Typography variant="body1">
              {Object.entries(classDistribution)
                .map(([className, levels]) => `${className} ${levels}`)
                .join(' / ')}
            </Typography>
          </Grid>
        </Grid>

        <Divider sx={{ my: 2 }} />

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

        {finalLevel && (
          <Grid container spacing={2}>
            <Grid item xs={6} sm={3}>
              <Typography variant="subtitle2" color="text.secondary">Base Attack</Typography>
              <Typography variant="h6">+{finalLevel.baseAttackBonus}</Typography>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Typography variant="subtitle2" color="text.secondary">Fort Save</Typography>
              <Typography variant="h6">+{finalLevel.saves.fortitude}</Typography>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Typography variant="subtitle2" color="text.secondary">Ref Save</Typography>
              <Typography variant="h6">+{finalLevel.saves.reflex}</Typography>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Typography variant="subtitle2" color="text.secondary">Will Save</Typography>
              <Typography variant="h6">+{finalLevel.saves.will}</Typography>
            </Grid>
          </Grid>
        )}

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 2 }}>
          <Typography variant="h6" color="primary" gutterBottom>
            Skill Points
          </Typography>
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
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button onClick={handleNewCharacter} color="warning">
            New Character
          </Button>
          <Button variant="contained" onClick={handleExport}>
            Export JSON
          </Button>
        </Box>
      </Box>
    </Box>
  );
}

export default CharacterReview;
