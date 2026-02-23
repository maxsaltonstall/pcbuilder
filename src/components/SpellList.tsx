import { useState } from 'react';
import {
  Box,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Grid,
  TextField,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Spell } from '../types/spells';
import spellsData from '@data/spells.json';

interface SpellListProps {
  casterClass: string;
  casterLevel: number;
  highestSpellLevel: number;
}

export function SpellList({ casterClass, casterLevel: _casterLevel, highestSpellLevel }: SpellListProps) {
  const [searchTerm, setSearchTerm] = useState('');

  // Filter spells by class and level
  const availableSpells = (spellsData as Spell[]).filter(spell => {
    // Check if spell is available to this class
    const spellLevel = spell.level[casterClass] || spell.level[casterClass.toLowerCase()];
    if (spellLevel === null || spellLevel === undefined) return false;

    const level = typeof spellLevel === 'string' ? parseInt(spellLevel) : spellLevel;
    if (isNaN(level) || level > highestSpellLevel) return false;

    // Apply search filter
    if (searchTerm && !spell.name.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }

    return true;
  });

  // Group spells by level
  const spellsByLevel: Record<number, Spell[]> = {};
  availableSpells.forEach(spell => {
    const spellLevel = spell.level[casterClass] || spell.level[casterClass.toLowerCase()];
    if (spellLevel === null || spellLevel === undefined) return;
    const level = typeof spellLevel === 'string' ? parseInt(spellLevel) : spellLevel;
    if (!spellsByLevel[level]) spellsByLevel[level] = [];
    spellsByLevel[level].push(spell);
  });

  // Sort spells within each level by name
  Object.values(spellsByLevel).forEach(spells => {
    spells.sort((a, b) => a.name.localeCompare(b.name));
  });

  return (
    <Box>
      <TextField
        fullWidth
        size="small"
        placeholder="Search spells..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        sx={{ mb: 2 }}
      />

      {Object.entries(spellsByLevel)
        .sort(([a], [b]) => Number(a) - Number(b))
        .map(([level, spells]) => (
          <Accordion key={level} sx={{ mb: 1 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle2">
                <strong>Level {level === '0' ? '0 (Cantrips)' : level}</strong> — {spells.length} spells
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={1}>
                {spells.map((spell, index) => (
                  <Grid item xs={12} sm={6} md={4} key={spell.id || `${spell.name}-${index}`}>
                    <Box
                      sx={{
                        p: 1,
                        border: '1px solid',
                        borderColor: 'divider',
                        borderRadius: 1,
                        '&:hover': { bgcolor: 'action.hover' },
                      }}
                    >
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {spell.name}
                      </Typography>
                      {spell.school && (
                        <Chip label={spell.school} size="small" sx={{ mt: 0.5 }} />
                      )}
                      {spell.description && (
                        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                          {spell.description.length > 100
                            ? `${spell.description.substring(0, 100)}...`
                            : spell.description}
                        </Typography>
                      )}
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </AccordionDetails>
          </Accordion>
        ))}

      {availableSpells.length === 0 && (
        <Typography variant="body2" color="text.secondary" align="center" sx={{ py: 2 }}>
          {searchTerm ? 'No spells found matching your search.' : 'No spells available.'}
        </Typography>
      )}
    </Box>
  );
}
