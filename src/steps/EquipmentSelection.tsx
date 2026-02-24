import { Box, Button, Typography, Alert, Card, CardContent, Chip, Grid } from '@mui/material';
import { useCharacter } from '../context/CharacterContext';
import { generateEquipmentRecommendations } from '../services/equipmentCalculator';

interface EquipmentSelectionProps {
  onNext: () => void;
  onBack: () => void;
}

function EquipmentSelection({ onNext, onBack }: EquipmentSelectionProps) {
  const { state } = useCharacter();

  const recommendations = state.focus
    ? generateEquipmentRecommendations(state.totalLevel, state.focus)
    : null;

  if (!recommendations) {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Equipment Selection
        </Typography>
        <Alert severity="warning" sx={{ mb: 3 }}>
          Unable to generate equipment recommendations. Please complete previous steps.
        </Alert>
        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button variant="outlined" onClick={onBack}>
            Back
          </Button>
          <Button variant="contained" onClick={onNext}>
            Skip
          </Button>
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Equipment & Wealth
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Based on your level and build focus, here are equipment recommendations for your character.
      </Typography>

      <Card sx={{ mb: 3, bgcolor: 'success.50' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            💰 Total Wealth: {recommendations.totalBudget.toLocaleString()} gp
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Level {state.totalLevel} character standard wealth (DMG Table 5-1)
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recommended Budget Allocation
          </Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={6} sm={4}>
              <Chip
                label={`Weapons: ${recommendations.allocations.weapons.toLocaleString()} gp`}
                color="primary"
                sx={{ width: '100%' }}
              />
            </Grid>
            <Grid item xs={6} sm={4}>
              <Chip
                label={`Armor: ${recommendations.allocations.armor.toLocaleString()} gp`}
                color="primary"
                sx={{ width: '100%' }}
              />
            </Grid>
            <Grid item xs={6} sm={4}>
              <Chip
                label={`Ability Items: ${recommendations.allocations.abilityItems.toLocaleString()} gp`}
                color="secondary"
                sx={{ width: '100%' }}
              />
            </Grid>
            <Grid item xs={6} sm={4}>
              <Chip
                label={`Protection: ${recommendations.allocations.protectionItems.toLocaleString()} gp`}
                color="secondary"
                sx={{ width: '100%' }}
              />
            </Grid>
            <Grid item xs={6} sm={4}>
              <Chip
                label={`Utility: ${recommendations.allocations.utilityItems.toLocaleString()} gp`}
                color="default"
                sx={{ width: '100%' }}
              />
            </Grid>
            <Grid item xs={6} sm={4}>
              <Chip
                label={`Consumables: ${recommendations.allocations.consumables.toLocaleString()} gp`}
                color="default"
                sx={{ width: '100%' }}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {recommendations.recommendedItems.length > 0 && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Priority Items
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              These items are highly recommended for your build:
            </Typography>
            {recommendations.recommendedItems.map((item, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <Typography variant="subtitle1" fontWeight="bold">
                  {item.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {item.description}
                </Typography>
                <Chip label={`${item.cost.toLocaleString()} gp`} size="small" sx={{ mt: 0.5 }} />
              </Box>
            ))}
          </CardContent>
        </Card>
      )}

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>
          <strong>Note:</strong> Equipment Selection (Full Version Coming Soon)
        </Typography>
        <Typography variant="body2">
          This shows recommended budget allocation and priority items. A full equipment selection
          interface with detailed item choices will be available in a future update. For now, use
          these recommendations when manually equipping your character.
        </Typography>
      </Alert>

      <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
        <Button variant="outlined" onClick={onBack}>
          Back
        </Button>
        <Button variant="contained" onClick={onNext}>
          Next
        </Button>
      </Box>
    </Box>
  );
}

export default EquipmentSelection;
