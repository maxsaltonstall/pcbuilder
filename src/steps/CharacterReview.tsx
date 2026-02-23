import { Box, Button, Typography, Paper, Grid, Chip, Divider } from '@mui/material';
import { useCharacter } from '../context/CharacterContext';
import { calculateTotalSkillPoints, getAbilityModifier } from '../services/skillCalculator';

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
    ? calculateTotalSkillPoints(progression, state.abilityScores)
    : 0;

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
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Total Skill Points: {totalSkillPoints}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Priority Skills: {state.keySkills.join(', ') || 'None selected'}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Feats ({allFeats.length})
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {allFeats.map((feat, index) => (
              <Chip key={index} label={feat} size="small" color="primary" />
            ))}
            {allFeats.length === 0 && (
              <Typography variant="body2" color="text.secondary">No feats selected</Typography>
            )}
          </Box>
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
