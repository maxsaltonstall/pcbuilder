import { useState } from 'react';
import { Box, Stepper, Step, StepLabel, Paper } from '@mui/material';
import InitialSetup from '../../steps/InitialSetup';
import RaceSelection from '../../steps/RaceSelection';
import DeitySelection from '../../steps/DeitySelection';
import AbilityScores from '../../steps/AbilityScores';
import GoalSetting from '../../steps/GoalSetting';
import OptimizationResults from '../../steps/OptimizationResults';
import SpellSelection from '../../steps/SpellSelection';
import CharacterReview from '../../steps/CharacterReview';

const steps = [
  'Initial Setup',
  'Race Selection',
  'Deity & Domains',
  'Ability Scores',
  'Goal Setting',
  'Optimization',
  'Spell Selection',
  'Character Review',
];

function WizardContainer() {
  const [activeStep, setActiveStep] = useState(0);

  const handleNext = () => {
    setActiveStep((prevStep) => Math.min(prevStep + 1, steps.length - 1));
  };

  const handleBack = () => {
    setActiveStep((prevStep) => Math.max(prevStep - 1, 0));
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return <InitialSetup onNext={handleNext} />;
      case 1:
        return <RaceSelection onNext={handleNext} onBack={handleBack} />;
      case 2:
        return <DeitySelection onNext={handleNext} onBack={handleBack} />;
      case 3:
        return <AbilityScores onNext={handleNext} onBack={handleBack} />;
      case 4:
        return <GoalSetting onNext={handleNext} onBack={handleBack} />;
      case 5:
        return <OptimizationResults onNext={handleNext} onBack={handleBack} />;
      case 6:
        return <SpellSelection onNext={handleNext} onBack={handleBack} />;
      case 7:
        return <CharacterReview onBack={handleBack} />;
      default:
        return null;
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <Paper elevation={3} sx={{ p: 4, minHeight: 400 }}>
        {renderStepContent(activeStep)}
      </Paper>
    </Box>
  );
}

export default WizardContainer;
