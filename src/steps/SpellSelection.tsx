import { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Alert,
  Card,
  CardContent,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useCharacter } from '../context/CharacterContext';
import { calculateSpellcasting } from '../services/spellcastingCalculator';
import { SpellList } from '../components/SpellList';

interface SpellSelectionProps {
  onNext: () => void;
  onBack: () => void;
}

function SpellSelection({ onNext, onBack }: SpellSelectionProps) {
  const { state } = useCharacter();
  const [selectedSpells] = useState<string[]>([]);

  // Calculate spellcasting info from current progression
  const spellcastingInfo = state.optimizedProgression.length > 0 && state.abilityScores
    ? calculateSpellcasting(state.optimizedProgression, state.abilityScores)
    : undefined;

  const hasSpellcasting = spellcastingInfo && spellcastingInfo.spellcastingClasses.length > 0;

  const handleNext = () => {
    // TODO: Save selected spells to character state
    onNext();
  };

  const handleSkip = () => {
    onNext();
  };

  if (!hasSpellcasting) {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Spell Selection
        </Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          Your character does not have any spellcasting classes. You can skip this step.
        </Alert>
        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button variant="outlined" onClick={onBack}>
            Back
          </Button>
          <Button variant="contained" onClick={handleSkip}>
            Skip
          </Button>
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Spell Selection
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Select spells for your spellcasting classes. Your available spells are determined by your
        class levels and spellcasting ability scores.
      </Typography>

      {spellcastingInfo.spellcastingClasses.map((casterInfo, index) => (
        <Card key={index} sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ textTransform: 'capitalize' }}>
              {casterInfo.className} (Caster Level {casterInfo.casterLevel})
            </Typography>

            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Spells Per Day:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {Object.entries(casterInfo.spellsPerDayByLevel).map(([level, count]) => (
                  <Chip
                    key={level}
                    label={`${level}${level === '0' ? ' (cantrips)' : getOrdinalSuffix(level)}: ${
                      count === Infinity ? '∞' : count
                    }/day`}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                ))}
              </Box>
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Spells Known:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {Object.entries(casterInfo.spellsKnownByLevel).map(([level, count]) => (
                  <Chip
                    key={level}
                    label={`${level}${level === '0' ? ' (cantrips)' : getOrdinalSuffix(level)}: ${
                      count === Infinity ? 'All' : count
                    }`}
                    size="small"
                    color="secondary"
                    variant="outlined"
                  />
                ))}
              </Box>
            </Box>

            {casterInfo.spellsKnownByLevel[0] !== Infinity && (
              <Alert severity="info" sx={{ mt: 2 }}>
                As a spontaneous caster ({casterInfo.className}), you have a limited number of
                spells known. Choose wisely!
              </Alert>
            )}
          </CardContent>
        </Card>
      ))}

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Available Spells
      </Typography>
      <Alert severity="info" sx={{ mb: 2 }}>
        <strong>Note:</strong> For this version, spell selection is informational. Your character
        will have access to appropriate spells based on their class and level. Full spell selection
        and preparation will be available in a future update.
      </Alert>

      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1">
            Browse Spells ({selectedSpells.length} selected)
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          {spellcastingInfo.spellcastingClasses.map((casterInfo, index) => (
            <Box key={index} sx={{ mb: 3 }}>
              <Typography variant="subtitle2" gutterBottom sx={{ textTransform: 'capitalize' }}>
                {casterInfo.className} Spells
              </Typography>
              <SpellList
                casterClass={casterInfo.className}
                casterLevel={casterInfo.casterLevel}
                highestSpellLevel={casterInfo.highestSpellLevel}
              />
            </Box>
          ))}
        </AccordionDetails>
      </Accordion>

      <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
        <Button variant="outlined" onClick={onBack}>
          Back
        </Button>
        <Button variant="contained" onClick={handleNext}>
          Next
        </Button>
      </Box>
    </Box>
  );
}

function getOrdinalSuffix(num: string | number): string {
  const n = typeof num === 'string' ? parseInt(num) : num;
  const s = ['th', 'st', 'nd', 'rd'];
  const v = n % 100;
  return s[(v - 20) % 10] || s[v] || s[0];
}

export default SpellSelection;
