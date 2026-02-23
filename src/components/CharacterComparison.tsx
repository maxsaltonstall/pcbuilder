import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Divider,
} from '@mui/material';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import { CharacterState } from '../types/character';
import { calculateCombatStats } from '../services/combatCalculations';
import { calculateTotalSkillPoints } from '../services/skillCalculator';

interface CharacterComparisonProps {
  character1: CharacterState;
  character2: CharacterState;
  onClose: () => void;
}

function CharacterComparison({ character1, character2, onClose }: CharacterComparisonProps) {
  // Calculate stats for both characters
  const stats1 = character1.abilityScores && character1.optimizedProgression.length > 0
    ? calculateCombatStats(
        character1.optimizedProgression,
        character1.abilityScores,
        character1.assumeMagicItems || false,
        character1.optimizedProgression.filter(l => l.featGained).map(l => l.featGained!)
      )
    : null;

  const stats2 = character2.abilityScores && character2.optimizedProgression.length > 0
    ? calculateCombatStats(
        character2.optimizedProgression,
        character2.abilityScores,
        character2.assumeMagicItems || false,
        character2.optimizedProgression.filter(l => l.featGained).map(l => l.featGained!)
      )
    : null;

  const skillPoints1 = character1.abilityScores && character1.optimizedProgression.length > 0
    ? calculateTotalSkillPoints(character1.optimizedProgression, character1.abilityScores, character1.assumeMagicItems)
    : 0;

  const skillPoints2 = character2.abilityScores && character2.optimizedProgression.length > 0
    ? calculateTotalSkillPoints(character2.optimizedProgression, character2.abilityScores, character2.assumeMagicItems)
    : 0;

  // Calculate class distribution
  const getClassDistribution = (progression: any[]) => {
    const dist: Record<string, number> = {};
    progression.forEach(level => {
      const name = level.class.name;
      dist[name] = (dist[name] || 0) + 1;
    });
    return Object.entries(dist).map(([name, levels]) => `${name} ${levels}`).join(' / ');
  };

  const renderComparisonRow = (
    label: string,
    value1: string | number,
    value2: string | number,
    better?: 'higher' | 'lower'
  ) => {
    let winner: 'left' | 'right' | 'tie' = 'tie';

    if (better && typeof value1 === 'number' && typeof value2 === 'number') {
      if (better === 'higher') {
        winner = value1 > value2 ? 'left' : value1 < value2 ? 'right' : 'tie';
      } else {
        winner = value1 < value2 ? 'left' : value1 > value2 ? 'right' : 'tie';
      }
    }

    return (
      <TableRow>
        <TableCell>{label}</TableCell>
        <TableCell
          align="center"
          sx={{
            bgcolor: winner === 'left' ? 'success.50' : 'inherit',
            fontWeight: winner === 'left' ? 'bold' : 'normal',
          }}
        >
          {value1}
        </TableCell>
        <TableCell
          align="center"
          sx={{
            bgcolor: winner === 'right' ? 'success.50' : 'inherit',
            fontWeight: winner === 'right' ? 'bold' : 'normal',
          }}
        >
          {value2}
        </TableCell>
      </TableRow>
    );
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <CompareArrowsIcon sx={{ mr: 1, fontSize: 32 }} />
          <Typography variant="h5">Character Comparison</Typography>
        </Box>
        <Button onClick={onClose} variant="outlined">
          Close
        </Button>
      </Box>

      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Typography variant="h6" color="primary" gutterBottom>
              {character1.concept || 'Character 1'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {getClassDistribution(character1.optimizedProgression)}
            </Typography>
            {character1.race && (
              <Chip label={character1.race.raceName} size="small" sx={{ mt: 1 }} />
            )}
          </Grid>
          <Grid item xs={6}>
            <Typography variant="h6" color="secondary" gutterBottom>
              {character2.concept || 'Character 2'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {getClassDistribution(character2.optimizedProgression)}
            </Typography>
            {character2.race && (
              <Chip label={character2.race.raceName} size="small" sx={{ mt: 1 }} />
            )}
          </Grid>
        </Grid>
      </Paper>

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Combat Statistics
      </Typography>
      <TableContainer component={Paper} sx={{ mb: 3 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>Stat</strong></TableCell>
              <TableCell align="center"><strong>Character 1</strong></TableCell>
              <TableCell align="center"><strong>Character 2</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {renderComparisonRow('Level', character1.totalLevel, character2.totalLevel, 'higher')}
            {stats1 && stats2 && (
              <>
                {renderComparisonRow('HP', stats1.hp, stats2.hp, 'higher')}
                {renderComparisonRow('AC', stats1.ac, stats2.ac, 'higher')}
                {renderComparisonRow('BAB', stats1.baseAttackBonus, stats2.baseAttackBonus, 'higher')}
                {renderComparisonRow('Fort Save', stats1.saves.fortitude, stats2.saves.fortitude, 'higher')}
                {renderComparisonRow('Ref Save', stats1.saves.reflex, stats2.saves.reflex, 'higher')}
                {renderComparisonRow('Will Save', stats1.saves.will, stats2.saves.will, 'higher')}
                {renderComparisonRow('Initiative', stats1.initiative, stats2.initiative, 'higher')}
              </>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="h6" gutterBottom>
        Ability Scores
      </Typography>
      <TableContainer component={Paper} sx={{ mb: 3 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>Ability</strong></TableCell>
              <TableCell align="center"><strong>Character 1</strong></TableCell>
              <TableCell align="center"><strong>Character 2</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {character1.abilityScores && character2.abilityScores && (
              <>
                {renderComparisonRow('Strength', character1.abilityScores.strength, character2.abilityScores.strength, 'higher')}
                {renderComparisonRow('Dexterity', character1.abilityScores.dexterity, character2.abilityScores.dexterity, 'higher')}
                {renderComparisonRow('Constitution', character1.abilityScores.constitution, character2.abilityScores.constitution, 'higher')}
                {renderComparisonRow('Intelligence', character1.abilityScores.intelligence, character2.abilityScores.intelligence, 'higher')}
                {renderComparisonRow('Wisdom', character1.abilityScores.wisdom, character2.abilityScores.wisdom, 'higher')}
                {renderComparisonRow('Charisma', character1.abilityScores.charisma, character2.abilityScores.charisma, 'higher')}
              </>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="h6" gutterBottom>
        Other Statistics
      </Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>Stat</strong></TableCell>
              <TableCell align="center"><strong>Character 1</strong></TableCell>
              <TableCell align="center"><strong>Character 2</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {renderComparisonRow('Total Skill Points', skillPoints1, skillPoints2, 'higher')}
            {renderComparisonRow('Feats', character1.optimizedProgression.filter(l => l.featGained).length, character2.optimizedProgression.filter(l => l.featGained).length, 'higher')}
            {renderComparisonRow('Focus', character1.focus, character2.focus)}
          </TableBody>
        </Table>
      </TableContainer>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
        <Button onClick={onClose} variant="contained">
          Done
        </Button>
      </Box>
    </Box>
  );
}

export default CharacterComparison;
