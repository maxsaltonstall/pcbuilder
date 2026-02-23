import { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Grid,
  Paper,
  Alert,
} from '@mui/material';
import { useCharacter } from '../context/CharacterContext';
import { AbilityScores } from '../types/character';

interface AbilityScoresProps {
  onNext: () => void;
  onBack: () => void;
}

function AbilityScoresComponent({ onNext, onBack }: AbilityScoresProps) {
  const { state, updateAbilityScores } = useCharacter();
  const [scores, setScores] = useState<AbilityScores>(
    state.abilityScores || {
      strength: 10,
      dexterity: 10,
      constitution: 10,
      intelligence: 10,
      wisdom: 10,
      charisma: 10,
    }
  );

  const handleScoreChange = (ability: keyof AbilityScores, value: string) => {
    const numValue = parseInt(value) || 0;
    setScores({ ...scores, [ability]: numValue });
  };

  const handleNext = () => {
    updateAbilityScores(scores);
    onNext();
  };

  const getModifier = (score: number): number => {
    return Math.floor((score - 10) / 2);
  };

  const formatModifier = (score: number): string => {
    const mod = getModifier(score);
    return mod >= 0 ? `+${mod}` : `${mod}`;
  };

  const isValid = Object.values(scores).every((score) => score >= 3 && score <= 25);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Ability Scores
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Enter your character's base ability scores (before racial modifiers or magic items).
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        For high-level characters, you may want to use elite array (15, 14, 13, 12, 10, 8) or
        point buy. Remember to account for ability increases at levels 4, 8, 12, 16, and 20.
      </Alert>

      <Grid container spacing={2} sx={{ mb: 4 }}>
        {[
          { key: 'strength', label: 'Strength' },
          { key: 'dexterity', label: 'Dexterity' },
          { key: 'constitution', label: 'Constitution' },
          { key: 'intelligence', label: 'Intelligence' },
          { key: 'wisdom', label: 'Wisdom' },
          { key: 'charisma', label: 'Charisma' },
        ].map(({ key, label }) => (
          <Grid item xs={12} sm={6} md={4} key={key}>
            <Paper elevation={1} sx={{ p: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                {label}
              </Typography>
              <TextField
                fullWidth
                type="number"
                value={scores[key as keyof AbilityScores]}
                onChange={(e) => handleScoreChange(key as keyof AbilityScores, e.target.value)}
                inputProps={{ min: 3, max: 25 }}
                helperText={`Modifier: ${formatModifier(scores[key as keyof AbilityScores])}`}
              />
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack}>Back</Button>
        <Button variant="contained" onClick={handleNext} disabled={!isValid}>
          Next
        </Button>
      </Box>
    </Box>
  );
}

export default AbilityScoresComponent;
