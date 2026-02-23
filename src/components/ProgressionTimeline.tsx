import { Box, Typography, Chip, Tooltip } from '@mui/material';
import { LevelProgression } from '../types/classes';

interface ProgressionTimelineProps {
  progression: LevelProgression[];
}

function ProgressionTimeline({ progression }: ProgressionTimelineProps) {
  // Group levels by class for visualization
  const classGroups: { className: string; startLevel: number; endLevel: number; color: string }[] = [];
  const colors = [
    '#3f51b5', '#f50057', '#4caf50', '#ff9800', '#9c27b0',
    '#00bcd4', '#8bc34a', '#ffc107', '#e91e63', '#009688'
  ];

  let currentClass = progression[0]?.class.name;
  let startLevel = 1;
  let colorIndex = 0;

  progression.forEach((_level, index) => {
    const isLastLevel = index === progression.length - 1;
    const classChanged = !isLastLevel && progression[index + 1]?.class.name !== currentClass;

    if (classChanged || isLastLevel) {
      classGroups.push({
        className: currentClass,
        startLevel,
        endLevel: index + 1,
        color: colors[colorIndex % colors.length],
      });

      if (classChanged) {
        currentClass = progression[index + 1].class.name;
        startLevel = index + 2;
        colorIndex++;
      }
    }
  });

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom fontWeight="bold">
        Level Progression Timeline
      </Typography>

      {/* Timeline visualization */}
      <Box sx={{ position: 'relative', height: 60, mb: 2 }}>
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: 0,
            right: 0,
            height: 4,
            bgcolor: 'grey.300',
            borderRadius: 2,
          }}
        />

        {classGroups.map((group, index) => {
          const startPercent = ((group.startLevel - 1) / progression.length) * 100;
          const widthPercent = ((group.endLevel - group.startLevel + 1) / progression.length) * 100;

          return (
            <Tooltip
              key={index}
              title={`${group.className}: Levels ${group.startLevel}-${group.endLevel}`}
            >
              <Box
                sx={{
                  position: 'absolute',
                  top: '50%',
                  left: `${startPercent}%`,
                  width: `${widthPercent}%`,
                  height: 20,
                  bgcolor: group.color,
                  borderRadius: 1,
                  transform: 'translateY(-50%)',
                  cursor: 'pointer',
                  '&:hover': {
                    height: 24,
                    zIndex: 1,
                  },
                  transition: 'height 0.2s',
                }}
              />
            </Tooltip>
          );
        })}
      </Box>

      {/* Legend */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 2 }}>
        {classGroups.map((group, index) => (
          <Chip
            key={index}
            label={`${group.className} (${group.startLevel}-${group.endLevel})`}
            sx={{ bgcolor: group.color, color: 'white' }}
            size="small"
          />
        ))}
      </Box>

      {/* Key milestones */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
          Key Milestones:
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {progression
            .filter(l => l.featGained || l.abilityIncrease)
            .map((level, index) => (
              <Chip
                key={index}
                label={
                  level.featGained
                    ? `L${level.levelNumber}: Feat`
                    : `L${level.levelNumber}: +1 ${level.abilityIncrease?.toUpperCase()}`
                }
                size="small"
                variant="outlined"
                color={level.featGained ? 'primary' : 'secondary'}
              />
            ))}
        </Box>
      </Box>
    </Box>
  );
}

export default ProgressionTimeline;
