import { Box, Container, Typography } from '@mui/material';
import { CharacterProvider } from './context/CharacterContext';
import WizardContainer from './components/Wizard/WizardContainer';

function App() {
  return (
    <CharacterProvider>
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            D&D 3.5 Character Builder
          </Typography>
          <Typography variant="subtitle1" gutterBottom align="center" color="text.secondary">
            Create optimized high-level characters with intelligent progression
          </Typography>
          <WizardContainer />
        </Box>
      </Container>
    </CharacterProvider>
  );
}

export default App;
