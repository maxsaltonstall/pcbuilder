import { Box, Typography, Chip, Tooltip, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import { Skill } from '../types/skills';
import { getSkillSynergies } from '../services/skillCalculator';
import skillsData from '@data/skills.json';

interface SkillsDisplayProps {
  skillRanks: Record<string, number>;
  classSkills: string[];
}

export function SkillsDisplay({ skillRanks, classSkills }: SkillsDisplayProps) {
  const skills = skillsData as Skill[];

  // Separate skills into those with ranks and those without
  const skillsWithRanks = skills.filter(skill => (skillRanks[skill.id] || 0) > 0);
  const skillsWithoutRanks = skills.filter(skill => (skillRanks[skill.id] || 0) === 0);

  const renderSkill = (skill: Skill) => {
    const ranks = skillRanks[skill.id] || 0;
    const isClassSkill = classSkills.includes(skill.id);
    const synergies = getSkillSynergies(skill.id, skillRanks);
    const activeSynergies = synergies.filter(s => s.active);

    return (
      <Accordion key={skill.id} sx={{ mb: 1 }}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', gap: 2 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', minWidth: 180 }}>
              {skill.name}
            </Typography>
            {ranks > 0 && (
              <Chip
                label={`${ranks} ranks`}
                size="small"
                color="primary"
                sx={{ minWidth: 80 }}
              />
            )}
            {isClassSkill && (
              <Chip
                label="Class Skill"
                size="small"
                variant="outlined"
                sx={{ minWidth: 100 }}
              />
            )}
            {activeSynergies.length > 0 && (
              <Chip
                label={`+${activeSynergies.reduce((sum, s) => sum + s.bonus, 0)} synergy`}
                size="small"
                color="success"
                sx={{ minWidth: 100 }}
              />
            )}
            <Typography variant="caption" color="text.secondary" sx={{ ml: 'auto' }}>
              {skill.keyAbility.toUpperCase()}
            </Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box>
            <Typography variant="body2" paragraph>
              {skill.description}
            </Typography>

            {skill.trainedOnly && (
              <Chip label="Trained Only" size="small" color="warning" sx={{ mr: 1, mb: 1 }} />
            )}
            {skill.armorCheckPenalty && (
              <Chip label="Armor Check Penalty" size="small" color="error" sx={{ mr: 1, mb: 1 }} />
            )}

            {synergies.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="caption" fontWeight="bold" display="block" gutterBottom>
                  Synergy Bonuses:
                </Typography>
                {synergies.map((synergy, index) => (
                  <Tooltip
                    key={index}
                    title={`Have ${skillRanks[synergy.sourceSkillId] || 0}/${synergy.minimumRanks} ranks`}
                  >
                    <Chip
                      icon={synergy.active ? <CheckCircleIcon /> : <RadioButtonUncheckedIcon />}
                      label={`${synergy.sourceSkillName} ${synergy.minimumRanks}+ → +${synergy.bonus}${synergy.condition ? ` (${synergy.condition})` : ''}`}
                      size="small"
                      color={synergy.active ? 'success' : 'default'}
                      variant={synergy.active ? 'filled' : 'outlined'}
                      sx={{ mr: 1, mb: 1 }}
                    />
                  </Tooltip>
                ))}
              </Box>
            )}

            {skill.examples && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="caption" fontWeight="bold" display="block" gutterBottom>
                  Examples:
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {skill.examples}
                </Typography>
              </Box>
            )}

            <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 2 }}>
              Source: {skill.source}
            </Typography>
          </Box>
        </AccordionDetails>
      </Accordion>
    );
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Skills
      </Typography>

      {skillsWithRanks.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom fontWeight="bold" color="primary.main">
            Skills with Ranks ({skillsWithRanks.length})
          </Typography>
          {skillsWithRanks.map(renderSkill)}
        </Box>
      )}

      {skillsWithoutRanks.length > 0 && (
        <Box>
          <Typography variant="subtitle2" gutterBottom fontWeight="bold" color="text.secondary">
            Other Skills ({skillsWithoutRanks.length})
          </Typography>
          {skillsWithoutRanks.map(renderSkill)}
        </Box>
      )}
    </Box>
  );
}

export default SkillsDisplay;
