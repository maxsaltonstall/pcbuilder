import { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  RadioGroup,
  FormControlLabel,
  Radio,
  TextField,
  Autocomplete,
} from '@mui/material';
import { useCharacter } from '../context/CharacterContext';
import { FocusType } from '../types/character';
import { ClassSelection, ClassPriority } from '../types/classes';

// Import data
import classesData from '@data/classes.json';
import prestigeClassesData from '@data/prestige-classes.json';
import featsData from '@data/feats.json';
import skillsData from '@data/skills.json';

interface GoalSettingProps {
  onNext: () => void;
  onBack: () => void;
}

function GoalSetting({ onNext, onBack }: GoalSettingProps) {
  const { state, updateGoals } = useCharacter();
  const [selectedClasses, setSelectedClasses] = useState<ClassSelection[]>(state.targetClasses);
  const [selectedFeats, setSelectedFeats] = useState<string[]>(state.desiredFeats);
  const [selectedSkills, setSelectedSkills] = useState<string[]>(state.keySkills);
  const [focus, setFocus] = useState<FocusType>(state.focus);

  const allClasses = [...classesData, ...prestigeClassesData];

  const handleAddClass = () => {
    setSelectedClasses([
      ...selectedClasses,
      { classId: '', className: '', priority: 'medium' },
    ]);
  };

  const handleRemoveClass = (index: number) => {
    setSelectedClasses(selectedClasses.filter((_, i) => i !== index));
  };

  const handleClassChange = (index: number, classId: string) => {
    const cls = allClasses.find((c) => c.id === classId);
    if (cls) {
      const newClasses = [...selectedClasses];
      newClasses[index] = { classId: cls.id, className: cls.name, priority: newClasses[index].priority };
      setSelectedClasses(newClasses);
    }
  };

  const handlePriorityChange = (index: number, priority: ClassPriority) => {
    const newClasses = [...selectedClasses];
    newClasses[index] = { ...newClasses[index], priority };
    setSelectedClasses(newClasses);
  };

  const handleNext = () => {
    updateGoals(selectedClasses, selectedFeats, selectedSkills, focus);
    onNext();
  };

  const isValid =
    selectedClasses.length > 0 &&
    selectedClasses.every((cls) => cls.classId !== '');

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Goal Setting
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Define your character goals: target classes, desired feats, key skills, and combat focus.
      </Typography>

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Target Classes
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Select desired classes and set priorities. The optimizer will distribute {state.totalLevel} levels among them.
      </Typography>

      {selectedClasses.map((cls, index) => (
        <Box key={index} sx={{ display: 'flex', gap: 2, mb: 2, alignItems: 'center' }}>
          <FormControl sx={{ flex: 2 }}>
            <InputLabel>Class</InputLabel>
            <Select
              value={cls.classId}
              label="Class"
              onChange={(e) => handleClassChange(index, e.target.value)}
            >
              {allClasses.map((c) => (
                <MenuItem key={c.id} value={c.id}>
                  {c.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl sx={{ flex: 1 }}>
            <InputLabel>Priority</InputLabel>
            <Select
              value={cls.priority || 'medium'}
              label="Priority"
              onChange={(e) => handlePriorityChange(index, e.target.value as ClassPriority)}
            >
              <MenuItem value="high">High</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="low">Low</MenuItem>
            </Select>
          </FormControl>
          <Button onClick={() => handleRemoveClass(index)} color="error">
            Remove
          </Button>
        </Box>
      ))}

      <Button onClick={handleAddClass} variant="outlined" sx={{ mb: 3 }}>
        Add Class
      </Button>

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Desired Feats
      </Typography>
      <Autocomplete
        multiple
        options={featsData.map((f) => f.id)}
        getOptionLabel={(option) => featsData.find((f) => f.id === option)?.name || option}
        value={selectedFeats}
        onChange={(_, newValue) => setSelectedFeats(newValue)}
        renderInput={(params) => (
          <TextField {...params} label="Select Feats" placeholder="Choose feats..." />
        )}
        sx={{ mb: 3 }}
      />

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Key Skills
      </Typography>
      <Autocomplete
        multiple
        options={skillsData.map((s) => s.id)}
        getOptionLabel={(option) => skillsData.find((s) => s.id === option)?.name || option}
        value={selectedSkills}
        onChange={(_, newValue) => setSelectedSkills(newValue)}
        renderInput={(params) => (
          <TextField {...params} label="Select Skills" placeholder="Choose skills..." />
        )}
        sx={{ mb: 3 }}
      />

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Combat Focus
      </Typography>
      <FormControl component="fieldset" sx={{ mb: 3 }}>
        <RadioGroup value={focus} onChange={(e) => setFocus(e.target.value as FocusType)}>
          <FormControlLabel value="melee" control={<Radio />} label="Melee Combat" />
          <FormControlLabel value="ranged" control={<Radio />} label="Ranged Combat" />
          <FormControlLabel value="spells" control={<Radio />} label="Spellcasting" />
          <FormControlLabel value="healing" control={<Radio />} label="Healing/Support" />
          <FormControlLabel value="hp" control={<Radio />} label="Hit Points/Tanking" />
        </RadioGroup>
      </FormControl>

      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack}>Back</Button>
        <Button variant="contained" onClick={handleNext} disabled={!isValid}>
          Next
        </Button>
      </Box>
    </Box>
  );
}

export default GoalSetting;
