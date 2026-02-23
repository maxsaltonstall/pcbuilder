import { Box, Typography, Paper } from '@mui/material';
import { LevelProgression } from '../types/classes';

interface ClassDistributionProps {
  progression: LevelProgression[];
}

function ClassDistribution({ progression }: ClassDistributionProps) {
  // Calculate class distribution
  const distribution: Record<string, number> = {};
  progression.forEach(level => {
    const className = level.class.name;
    distribution[className] = (distribution[className] || 0) + 1;
  });

  const totalLevels = progression.length;
  const classes = Object.entries(distribution);

  const colors = [
    '#3f51b5', '#f50057', '#4caf50', '#ff9800', '#9c27b0',
    '#00bcd4', '#8bc34a', '#ffc107', '#e91e63', '#009688'
  ];

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom fontWeight="bold">
        Class Distribution
      </Typography>

      {/* Simple bar chart */}
      <Box sx={{ mt: 2 }}>
        {classes.map(([className, levels], index) => {
          const percentage = (levels / totalLevels) * 100;

          return (
            <Box key={className} sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                <Typography variant="body2">{className}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {levels} {levels === 1 ? 'level' : 'levels'} ({percentage.toFixed(0)}%)
                </Typography>
              </Box>
              <Box
                sx={{
                  width: '100%',
                  height: 24,
                  bgcolor: 'grey.200',
                  borderRadius: 1,
                  overflow: 'hidden',
                }}
              >
                <Box
                  sx={{
                    width: `${percentage}%`,
                    height: '100%',
                    bgcolor: colors[index % colors.length],
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'width 0.3s ease',
                  }}
                >
                  {percentage > 15 && (
                    <Typography variant="caption" sx={{ color: 'white', fontWeight: 'bold' }}>
                      {percentage.toFixed(0)}%
                    </Typography>
                  )}
                </Box>
              </Box>
            </Box>
          );
        })}
      </Box>

      {/* Summary stats */}
      <Paper variant="outlined" sx={{ p: 2, mt: 2, bgcolor: 'grey.50' }}>
        <Typography variant="caption" color="text.secondary" display="block">
          Total Classes: {classes.length}
        </Typography>
        <Typography variant="caption" color="text.secondary" display="block">
          Total Levels: {totalLevels}
        </Typography>
        <Typography variant="caption" color="text.secondary" display="block">
          Average Levels per Class: {(totalLevels / classes.length).toFixed(1)}
        </Typography>
      </Paper>
    </Box>
  );
}

export default ClassDistribution;
