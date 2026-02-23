# D&D 3.5 Character Builder

A desktop application for creating optimized high-level D&D 3.5 characters through an intelligent wizard interface.

## Features

- **Intelligent Wizard Interface**: Step-by-step character creation
- **Class Progression Optimization**: Automatically suggests optimal level progression
- **Skill Point Maximization**: Front-loads high skill-point classes
- **Prerequisite Validation**: Ensures feat and prestige class requirements are met
- **Character Sheet Export**: Export to PDF or JSON

## Technology Stack

- **Electron**: Desktop application framework
- **React + TypeScript**: Modern UI framework
- **Material-UI**: Component library
- **Vite**: Build tool

## Project Structure

```
pcbuilder/
├── electron/              # Electron main process
├── src/                   # React renderer
│   ├── components/        # UI components
│   ├── steps/            # Wizard step screens
│   ├── context/          # State management
│   ├── services/         # Business logic
│   ├── types/            # TypeScript definitions
│   └── utils/
├── data/                 # D&D 3.5 rules data (JSON)
└── scripts/              # Utilities
```

## Getting Started

### Install Dependencies

```bash
npm install
```

### Development

```bash
# Start both React and Electron in dev mode
npm run dev

# Or start separately
npm run dev:react      # Start Vite dev server only
npm run dev:electron   # Start Electron only
```

### Building

```bash
npm run build          # Build both React and Electron
npm run package        # Create distributable (DMG/NSIS/AppImage)
```

### Testing

```bash
npm test               # Run unit tests
npm run type-check     # TypeScript type checking
npm run lint           # ESLint
```

## Implementation Status

### Phase 1: Foundation ✅
- [x] Project initialization
- [x] Type definitions
- [x] Sample data files
- [x] Basic UI shell

### Phase 2: Core Features (In Progress)
- [ ] Prerequisite validator
- [ ] Skill calculator
- [ ] Optimization engine

### Phase 3: Character Generation
- [ ] Character sheet display
- [ ] HTML/PDF export
- [ ] Validation and error handling

### Phase 4: Polish
- [ ] Enhanced optimization
- [ ] More data (classes, feats, prestige classes)
- [ ] UI improvements

## License

MIT
