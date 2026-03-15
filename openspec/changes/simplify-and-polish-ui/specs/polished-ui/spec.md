## ADDED Requirements

### Requirement: Font hierarchy uses proportional and monospace fonts

The theme module SHALL define two font families: a proportional font (`TkDefaultFont`) for UI labels, headings, and button text, and a monospace font (`Courier New`) for numeric values and command display.

#### Scenario: Section headers use proportional font
- **WHEN** the app renders section headers ("PRESETS", "MANUAL CONTROL", "GENERATED COMMAND")
- **THEN** they SHALL use the proportional font family at size 9

#### Scenario: Numeric values use monospace font
- **WHEN** the app renders RGB slider values or the xrandr command
- **THEN** they SHALL use the monospace font family

#### Scenario: App title uses proportional bold
- **WHEN** the app renders the "BLUE LIGHT FILTER" header
- **THEN** it SHALL use the proportional font family at a larger bold size

### Requirement: Increased spacing and padding

The UI SHALL use consistent, generous padding across all sections for visual breathing room.

#### Scenario: Card inner padding
- **WHEN** a card container renders its content
- **THEN** the inner padding SHALL be at least 18px on all sides

#### Scenario: Section vertical spacing
- **WHEN** sections are separated by dividers
- **THEN** the vertical gap SHALL be at least 10px above and below the divider

#### Scenario: Window edge padding
- **WHEN** content is placed against the window edge
- **THEN** horizontal padding SHALL be at least 24px

### Requirement: Button hover effects

Buttons SHALL provide visual feedback on mouse hover by changing their background color.

#### Scenario: Mouse enters button
- **WHEN** the mouse pointer enters a non-primary button
- **THEN** the button background SHALL change to the border color to indicate hover

#### Scenario: Mouse leaves button
- **WHEN** the mouse pointer leaves a button
- **THEN** the button background SHALL return to its original color

#### Scenario: Primary button hover
- **WHEN** the mouse pointer enters the primary "Apply Now" button
- **THEN** the button background SHALL change to the secondary accent color

### Requirement: Larger preview swatch

The color preview swatch SHALL be larger to provide a more prominent color indicator.

#### Scenario: Swatch dimensions
- **WHEN** the preview card renders
- **THEN** the swatch canvas SHALL be at least 64x64 pixels
