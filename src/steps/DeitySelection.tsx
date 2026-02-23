import { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  FormControl,
  FormLabel,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Alert,
} from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import { Deity, Domain } from '../types/deities';
import { useCharacter } from '../context/CharacterContext';
import deitiesData from '@data/deities.json';
import domainsData from '@data/domains.json';

interface DeitySelectionProps {
  onNext: () => void;
  onBack: () => void;
}

function DeitySelection({ onNext, onBack }: DeitySelectionProps) {
  const { updateDeity } = useCharacter();
  const [selectedDeity, setSelectedDeity] = useState<Deity | null>(null);
  const [selectedDomains, setSelectedDomains] = useState<string[]>([]);

  const deities = deitiesData as Deity[];
  const domains = domainsData as Domain[];

  const handleDeitySelect = (deity: Deity) => {
    setSelectedDeity(deity);
    setSelectedDomains([]); // Reset domains when changing deity
  };

  const handleDomainToggle = (domainId: string) => {
    if (selectedDomains.includes(domainId)) {
      setSelectedDomains(selectedDomains.filter(d => d !== domainId));
    } else if (selectedDomains.length < 2) {
      setSelectedDomains([...selectedDomains, domainId]);
    }
  };

  const handleNext = () => {
    if (selectedDeity) {
      updateDeity({
        deityId: selectedDeity.id,
        deityName: selectedDeity.name,
        selectedDomains: selectedDomains,
      });
    }
    onNext();
  };

  const handleSkip = () => {
    updateDeity(undefined);
    setSelectedDeity(null);
    setSelectedDomains([]);
    onNext();
  };

  const isValid = !selectedDeity || selectedDomains.length === 2;

  const getAlignmentColor = (alignment: string): string => {
    if (alignment.includes('G')) return '#4caf50'; // Green for good
    if (alignment.includes('E')) return '#f44336'; // Red for evil
    return '#9e9e9e'; // Gray for neutral
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Deity & Domain Selection
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Choose a deity to worship and select two domains to gain their granted powers.
        This is optional - you can skip if your character doesn't worship a deity.
      </Typography>

      {!selectedDeity ? (
        <>
          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Available Deities
          </Typography>
          <Grid container spacing={2}>
            {deities.map((deity) => (
              <Grid item xs={12} sm={6} md={4} key={deity.id}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 4,
                    },
                  }}
                  onClick={() => handleDeitySelect(deity)}
                >
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {deity.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
                      {deity.title}
                    </Typography>
                    <Chip
                      label={deity.alignment}
                      size="small"
                      sx={{
                        bgcolor: getAlignmentColor(deity.alignment),
                        color: 'white',
                        fontWeight: 'bold',
                        mb: 1
                      }}
                    />
                    <Typography variant="body2" sx={{ mt: 1, mb: 1 }}>
                      {deity.portfolio}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Favored Weapon: {deity.favoredWeapon}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Domains: {deity.domains.length}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button variant="outlined" onClick={onBack}>
              Back
            </Button>
            <Button variant="contained" onClick={handleSkip}>
              Skip (No Deity)
            </Button>
          </Box>
        </>
      ) : (
        <>
          <Card sx={{ mb: 3, bgcolor: 'primary.50' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AutoAwesomeIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">
                  {selectedDeity.name} - {selectedDeity.title}
                </Typography>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2">
                    <strong>Alignment:</strong>{' '}
                    <Chip
                      label={selectedDeity.alignment}
                      size="small"
                      sx={{
                        bgcolor: getAlignmentColor(selectedDeity.alignment),
                        color: 'white',
                        ml: 1
                      }}
                    />
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    <strong>Portfolio:</strong> {selectedDeity.portfolio}
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    <strong>Favored Weapon:</strong> {selectedDeity.favoredWeapon}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2">
                    <strong>Worshipers:</strong> {selectedDeity.worshipers}
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    <strong>Source:</strong> {selectedDeity.source}
                  </Typography>
                </Grid>
              </Grid>
              <Button
                variant="outlined"
                size="small"
                onClick={() => setSelectedDeity(null)}
                sx={{ mt: 2 }}
              >
                Choose Different Deity
              </Button>
            </CardContent>
          </Card>

          <Typography variant="h6" gutterBottom>
            Select Two Domains
          </Typography>
          <Alert severity="info" sx={{ mb: 2 }}>
            Choose 2 domains from your deity's available domains. You'll gain their granted powers and domain spell slots.
          </Alert>

          <FormControl component="fieldset">
            <FormLabel component="legend">Available Domains ({selectedDomains.length}/2 selected)</FormLabel>
            <FormGroup>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                {selectedDeity.domains.map((domainId) => {
                  const domain = domains.find(d => d.id === domainId);
                  if (!domain) return null;

                  const isSelected = selectedDomains.includes(domainId);
                  const isDisabled = !isSelected && selectedDomains.length >= 2;

                  return (
                    <Grid item xs={12} sm={6} key={domainId}>
                      <Card
                        sx={{
                          border: isSelected ? 2 : 1,
                          borderColor: isSelected ? 'primary.main' : 'divider',
                          opacity: isDisabled ? 0.5 : 1,
                          cursor: isDisabled ? 'not-allowed' : 'pointer',
                        }}
                        onClick={() => !isDisabled && handleDomainToggle(domainId)}
                      >
                        <CardContent>
                          <FormControlLabel
                            control={
                              <Checkbox
                                checked={isSelected}
                                disabled={isDisabled}
                                onChange={() => handleDomainToggle(domainId)}
                              />
                            }
                            label={
                              <Typography variant="subtitle1" fontWeight="bold">
                                {domain.name}
                              </Typography>
                            }
                          />
                          <Typography variant="body2" color="text.secondary" sx={{ ml: 4, mb: 1 }}>
                            {domain.description}
                          </Typography>
                          <Typography variant="caption" color="primary.main" sx={{ ml: 4, display: 'block', fontWeight: 'bold' }}>
                            Granted Power:
                          </Typography>
                          <Typography variant="caption" sx={{ ml: 4, display: 'block' }}>
                            {domain.grantedPower}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  );
                })}
              </Grid>
            </FormGroup>
          </FormControl>

          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button variant="outlined" onClick={() => setSelectedDeity(null)}>
              Back to Deities
            </Button>
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={!isValid}
            >
              Next
            </Button>
          </Box>
        </>
      )}
    </Box>
  );
}

export default DeitySelection;
