import { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import { useCharacter } from '../context/CharacterContext';
import racesData from '@data/races.json';
import { Race, CharacterRace } from '../types/races';

interface RaceSelectionProps {
  onNext: () => void;
  onBack: () => void;
}

function RaceSelection({ onNext, onBack }: RaceSelectionProps) {
  const { state, updateRace } = useCharacter();
  const [selectedRace, setSelectedRace] = useState<Race | null>(
    state.race ? (racesData as Race[]).find(r => r.id === state.race?.raceId) || null : null
  );

  const handleRaceSelect = (race: Race) => {
    setSelectedRace(race);
  };

  const handleNext = () => {
    if (!selectedRace) return;

    const characterRace: CharacterRace = {
      raceId: selectedRace.id,
      raceName: selectedRace.name,
      abilityModifiers: selectedRace.abilityModifiers,
      traits: selectedRace.traits,
      skillBonuses: selectedRace.skillBonuses || [],
    };

    updateRace(characterRace);
    onNext();
  };

  const races = racesData as Race[];

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Race Selection
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Choose your character's race. Each race provides ability modifiers and special traits.
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        {races.map((race) => (
          <Grid item xs={12} sm={6} md={4} key={race.id}>
            <Card
              variant="outlined"
              sx={{
                border: selectedRace?.id === race.id ? '2px solid' : '1px solid',
                borderColor: selectedRace?.id === race.id ? 'primary.main' : 'divider',
                height: '100%',
              }}
            >
              <CardActionArea onClick={() => handleRaceSelect(race)}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {race.name}
                  </Typography>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="caption" color="text.secondary">
                      Size: {race.size} | Speed: {race.speed} ft
                    </Typography>
                  </Box>

                  <Typography variant="body2" sx={{ mb: 2, minHeight: 60 }}>
                    {race.description.substring(0, 120)}...
                  </Typography>

                  <Box sx={{ mb: 1 }}>
                    <Typography variant="caption" fontWeight="bold">
                      Ability Modifiers:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                      {Object.keys(race.abilityModifiers).length === 0 ? (
                        <Chip label="None (Versatile)" size="small" />
                      ) : (
                        Object.entries(race.abilityModifiers).map(([ability, modifier]) => (
                          <Chip
                            key={ability}
                            label={`${ability.substring(0, 3).toUpperCase()} ${modifier > 0 ? '+' : ''}${modifier}`}
                            size="small"
                            color={modifier > 0 ? 'success' : 'error'}
                          />
                        ))
                      )}
                    </Box>
                  </Box>

                  <Typography variant="caption" color="text.secondary">
                    Favored Class: {race.favoredClass === 'any' ? 'Any' : race.favoredClass.charAt(0).toUpperCase() + race.favoredClass.slice(1)}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>

      {selectedRace && (
        <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: 'primary.50' }}>
          <Typography variant="h6" gutterBottom>
            {selectedRace.name} - Racial Traits
          </Typography>
          <List dense>
            {selectedRace.traits.map((trait, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={trait.name}
                  secondary={trait.description}
                />
              </ListItem>
            ))}
          </List>
          {selectedRace.skillBonuses && selectedRace.skillBonuses.length > 0 && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Skill Bonuses:
              </Typography>
              {selectedRace.skillBonuses.map((bonus, index) => (
                <Chip
                  key={index}
                  label={`+${bonus.bonus} ${bonus.skillId}${bonus.condition ? ` (${bonus.condition})` : ''}`}
                  size="small"
                  sx={{ mr: 1, mb: 1 }}
                />
              ))}
            </Box>
          )}
        </Paper>
      )}

      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack}>
          Back
        </Button>
        <Button variant="contained" onClick={handleNext} disabled={!selectedRace}>
          Next
        </Button>
      </Box>
    </Box>
  );
}

export default RaceSelection;
