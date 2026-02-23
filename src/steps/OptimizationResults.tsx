import { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert,
  Chip,
} from '@mui/material';
import { useCharacter } from '../context/CharacterContext';
import { optimizeClassProgression } from '../services/optimizationEngine';
import { LevelProgression } from '../types/classes';

interface OptimizationResultsProps {
  onNext: () => void;
  onBack: () => void;
}

function OptimizationResults({ onNext, onBack }: OptimizationResultsProps) {
  const { state, setOptimizedProgression } = useCharacter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progression, setProgression] = useState<LevelProgression[]>([]);

  useEffect(() => {
    // Run optimization when component mounts
    runOptimization();
  }, []);

  const runOptimization = () => {
    setLoading(true);
    setError(null);

    try {
      if (!state.abilityScores) {
        throw new Error('Ability scores not set');
      }

      if (state.targetClasses.length === 0) {
        throw new Error('No classes selected');
      }

      // Run the optimization engine
      const result = optimizeClassProgression(
        state.totalLevel,
        state.targetClasses,
        state.desiredFeats,
        state.keySkills,
        state.abilityScores,
        state.focus
      );

      setProgression(result);
      setOptimizedProgression(result);
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Optimization failed');
      setLoading(false);
    }
  };

  const handleAccept = () => {
    onNext();
  };

  if (loading) {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Optimization Results
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Computing optimal class progression...
        </Typography>

        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>

        <Typography align="center" color="text.secondary">
          Analyzing {state.targetClasses.length} classes, {state.desiredFeats.length} feats, and {state.keySkills.length} skills...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Optimization Results
        </Typography>

        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button onClick={onBack}>Back</Button>
          <Button variant="contained" onClick={runOptimization}>
            Retry
          </Button>
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Optimization Results
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Here's your optimized level progression. Review and accept to continue.
      </Typography>

      <Alert severity="success" sx={{ mb: 3 }}>
        Successfully generated progression for level {state.totalLevel} character!
        {state.totalLevel > 20 && ' (Epic Level)'}
      </Alert>

      {state.totalLevel > 20 && (
        <Alert severity="info" sx={{ mb: 2 }}>
          Epic levels (21-30): Feats gained every 3 levels. Some prestige class features may need Epic Level Handbook reference.
        </Alert>
      )}

      <TableContainer component={Paper} sx={{ mb: 3, maxHeight: 400 }}>
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>Level</strong></TableCell>
              <TableCell><strong>Class</strong></TableCell>
              <TableCell><strong>BAB</strong></TableCell>
              <TableCell><strong>Fort/Ref/Will</strong></TableCell>
              <TableCell><strong>Skill Points</strong></TableCell>
              <TableCell><strong>Feat</strong></TableCell>
              <TableCell><strong>Ability</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {progression.map((level) => (
              <TableRow key={level.levelNumber}>
                <TableCell>{level.levelNumber}</TableCell>
                <TableCell>{level.class.name}</TableCell>
                <TableCell>+{level.baseAttackBonus}</TableCell>
                <TableCell>
                  +{level.saves.fortitude}/+{level.saves.reflex}/+{level.saves.will}
                </TableCell>
                <TableCell>{level.skillPoints}</TableCell>
                <TableCell>
                  {level.featGained ? (
                    <Chip label={level.featGained} size="small" color="primary" />
                  ) : (
                    '-'
                  )}
                </TableCell>
                <TableCell>
                  {level.abilityIncrease ? (
                    <Chip label={level.abilityIncrease.toUpperCase()} size="small" color="secondary" />
                  ) : (
                    '-'
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack}>Back to Goals</Button>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button onClick={runOptimization}>Regenerate</Button>
          <Button variant="contained" onClick={handleAccept}>
            Accept Progression
          </Button>
        </Box>
      </Box>
    </Box>
  );
}

export default OptimizationResults;
