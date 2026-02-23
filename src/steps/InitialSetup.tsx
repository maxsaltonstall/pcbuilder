import { useState, useMemo } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  OutlinedInput,
  SelectChangeEvent,
  ListSubheader,
} from '@mui/material';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import { useCharacter } from '../context/CharacterContext';
import { getGroupedSources } from '../utils/extractSources';
import { loadCharacterFromFile } from '../services/characterStorage';

interface InitialSetupProps {
  onNext: () => void;
}

function InitialSetup({ onNext }: InitialSetupProps) {
  const { state, updateInitialSetup, loadCharacter } = useCharacter();
  const [level, setLevel] = useState(state.totalLevel);
  const [concept, setConcept] = useState(state.concept);
  const [sources, setSources] = useState<string[]>(state.rulesSources);

  // Dynamically extract available sources from data files, organized by category
  const groupedSources = useMemo(() => getGroupedSources(), []);

  // Flatten all sources for "Select All" functionality
  const allSources = useMemo(
    () => groupedSources.flatMap(group => group.sources),
    [groupedSources]
  );

  const handleSourcesChange = (event: SelectChangeEvent<string[]>) => {
    const value = event.target.value;
    const selectedValues = typeof value === 'string' ? value.split(',') : value;

    // Handle special "Select All" and "Clear All" options
    if (selectedValues.includes('__SELECT_ALL__')) {
      setSources(allSources);
      return;
    }
    if (selectedValues.includes('__CLEAR_ALL__')) {
      setSources([]);
      return;
    }

    setSources(selectedValues);
  };

  const handleNext = () => {
    updateInitialSetup(level, concept, sources);
    onNext();
  };

  const handleLoad = async () => {
    if (concept && !window.confirm('Load a character? This will replace your current progress.')) {
      return;
    }

    try {
      const savedCharacter = await loadCharacterFromFile();
      loadCharacter(savedCharacter);

      // Update local state to reflect loaded character
      setLevel(savedCharacter.totalLevel);
      setConcept(savedCharacter.concept);
      setSources(savedCharacter.rulesSources);

      alert(`Character "${savedCharacter.characterName || savedCharacter.concept}" loaded successfully!`);
    } catch (error) {
      console.error('Error loading character:', error);
      alert('Failed to load character. Please check the file and try again.');
    }
  };

  const isValid = concept.trim() !== '' && sources.length > 0;

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Initial Setup
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Let's start by defining your character's total level and concept.
      </Typography>

      <Box sx={{ mb: 4 }}>
        <Typography gutterBottom>Character Level: {level}</Typography>
        <Slider
          value={level}
          onChange={(_, value) => setLevel(value as number)}
          min={1}
          max={30}
          step={1}
          marks={[
            { value: 1, label: '1' },
            { value: 10, label: '10' },
            { value: 20, label: '20' },
            { value: 30, label: '30' },
          ]}
          valueLabelDisplay="auto"
        />
        {level > 20 && (
          <Typography variant="caption" color="warning.main" sx={{ mt: 1, display: 'block' }}>
            Epic Level (21+) - Some features may be limited
          </Typography>
        )}
      </Box>

      <TextField
        fullWidth
        label="Character Concept"
        placeholder="e.g., Archer-mage who focuses on ranged combat and battlefield control"
        value={concept}
        onChange={(e) => setConcept(e.target.value)}
        multiline
        rows={3}
        sx={{ mb: 3 }}
        helperText="Describe what you want your character to do or be"
      />

      <FormControl fullWidth sx={{ mb: 4 }}>
        <InputLabel>Rules Sources</InputLabel>
        <Select
          multiple
          value={sources}
          onChange={handleSourcesChange}
          input={<OutlinedInput label="Rules Sources" />}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} size="small" />
              ))}
            </Box>
          )}
          MenuProps={{
            PaperProps: {
              style: {
                maxHeight: 400,
              },
            },
          }}
        >
          {/* Quick selection options */}
          <MenuItem
            value="__SELECT_ALL__"
            sx={{
              fontWeight: 'bold',
              color: 'success.main',
              borderBottom: '1px solid',
              borderColor: 'divider'
            }}
          >
            ✓ Select All Sources ({allSources.length})
          </MenuItem>
          <MenuItem
            value="__CLEAR_ALL__"
            sx={{
              fontWeight: 'bold',
              color: 'error.main',
              borderBottom: '2px solid',
              borderColor: 'divider',
              mb: 1
            }}
          >
            ✗ Clear All
          </MenuItem>

          {/* Grouped sources */}
          {groupedSources.map((group) => [
            <ListSubheader key={`header-${group.category}`} sx={{ fontWeight: 'bold', color: 'primary.main' }}>
              {group.category}
            </ListSubheader>,
            ...group.sources.map((source) => (
              <MenuItem key={source} value={source} sx={{ pl: 4 }}>
                {source}
              </MenuItem>
            )),
          ])}
        </Select>
      </FormControl>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
        <Button
          startIcon={<FolderOpenIcon />}
          onClick={handleLoad}
          variant="outlined"
        >
          Load Character
        </Button>
        <Button variant="contained" onClick={handleNext} disabled={!isValid}>
          Next
        </Button>
      </Box>
    </Box>
  );
}

export default InitialSetup;
