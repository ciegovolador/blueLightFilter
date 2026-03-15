## MODIFIED Requirements

### Requirement: UI appearance and theme

The application SHALL use a dark theme with improved visual hierarchy. Font choices SHALL distinguish between UI chrome (proportional) and data display (monospace). The theme module SHALL export font constants for both families.

#### Scenario: Theme fonts are available
- **WHEN** the theme module is imported
- **THEN** it SHALL export proportional font constants (`FONT`, `FONT_B`, `FONT_S`, `FONT_LG`) and monospace constants (`MONO`, `MONO_B`, `MONO_S`)

#### Scenario: Window renders with polished appearance
- **WHEN** the application starts
- **THEN** the window SHALL display with increased padding, hover-state buttons, and a larger preview swatch compared to the original layout
