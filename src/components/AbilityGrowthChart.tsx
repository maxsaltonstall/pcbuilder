import { Box, Typography, Chip } from '@mui/material';
import { LevelProgression } from '../types/classes';
import { AbilityScores } from '../types/character';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

interface AbilityGrowthChartProps {
  progression: LevelProgression[];
  baseAbilityScores?: AbilityScores;
  finalAbilityScores?: AbilityScores;
}

function AbilityGrowthChart({ progression, baseAbilityScores, finalAbilityScores }: AbilityGrowthChartProps) {
  if (!baseAbilityScores || !finalAbilityScores) return null;

  // Find all ability increases
  const increases = progression
    .filter(l => l.abilityIncrease)
    .map(l => ({
      level: l.levelNumber,
      ability: l.abilityIncrease!,
    }));

  // Calculate changes
  const abilities: Array<{
    name: string;
    key: keyof AbilityScores;
    base: number;
    final: number;
    change: number;
  }> = [
    { name: 'STR', key: 'strength', base: 0, final: 0, change: 0 },
    { name: 'DEX', key: 'dexterity', base: 0, final: 0, change: 0 },
    { name: 'CON', key: 'constitution', base: 0, final: 0, change: 0 },
    { name: 'INT', key: 'intelligence', base: 0, final: 0, change: 0 },
    { name: 'WIS', key: 'wisdom', base: 0, final: 0, change: 0 },
    { name: 'CHA', key: 'charisma', base: 0, final: 0, change: 0 },
  ];

  abilities.forEach(ability => {
    ability.base = baseAbilityScores[ability.key];
    ability.final = finalAbilityScores[ability.key];
    ability.change = ability.final - ability.base;
  });

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <TrendingUpIcon sx={{ mr: 1, color: 'success.main' }} />
        <Typography variant="subtitle1" fontWeight="bold">
          Ability Score Growth
        </Typography>
      </Box>

      {/* Bar chart showing growth */}
      <Box sx={{ mb: 3 }}>
        {abilities.map(ability => (
          <Box key={ability.key} sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="body2" fontWeight="bold">
                {ability.name}
              </Typography>
              <Box>
                <Typography component="span" variant="body2" color="text.secondary">
                  {ability.base}
                </Typography>
                {ability.change !== 0 && (
                  <Typography component="span" variant="body2" color={ability.change > 0 ? 'success.main' : 'error.main'} sx={{ ml: 1 }}>
                    {ability.change > 0 ? '+' : ''}{ability.change} → {ability.final}
                  </Typography>
                )}
              </Box>
            </Box>

            <Box sx={{ position: 'relative', height: 24, bgcolor: 'grey.200', borderRadius: 1 }}>
              {/* Base score bar */}
              <Box
                sx={{
                  position: 'absolute',
                  left: 0,
                  width: `${(ability.base / 30) * 100}%`,
                  height: '100%',
                  bgcolor: 'grey.400',
                  borderRadius: 1,
                }}
              />
              {/* Final score bar */}
              <Box
                sx={{
                  position: 'absolute',
                  left: 0,
                  width: `${(ability.final / 30) * 100}%`,
                  height: '100%',
                  bgcolor: ability.change > 0 ? 'success.main' : ability.change < 0 ? 'error.main' : 'grey.400',
                  borderRadius: 1,
                  display: 'flex',
                  alignItems: 'center',
                  paddingLeft: 1,
                }}
              >
                <Typography variant="caption" sx={{ color: 'white', fontWeight: 'bold' }}>
                  {ability.final}
                </Typography>
              </Box>
            </Box>
          </Box>
        ))}
      </Box>

      {/* Ability increases timeline */}
      {increases.length > 0 && (
        <Box>
          <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
            Level-Up Increases ({increases.length} total):
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {increases.map((inc, index) => (
              <Chip
                key={index}
                label={`L${inc.level}: ${inc.ability.toUpperCase()}`}
                size="small"
                color="secondary"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>
      )}
    </Box>
  );
}

export default AbilityGrowthChart;
