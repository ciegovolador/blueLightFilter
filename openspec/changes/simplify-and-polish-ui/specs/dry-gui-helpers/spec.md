## MODIFIED Requirements

### Requirement: Button helper supports hover states

The `_btn` helper method SHALL accept hover color parameters and bind `<Enter>`/`<Leave>` events to provide visual hover feedback.

#### Scenario: Non-primary button hover
- **WHEN** a standard button is created via `_btn(parent, text, command)`
- **THEN** it SHALL bind mouse enter/leave to toggle background between `CARD` and `BORDER`

#### Scenario: Primary button hover
- **WHEN** a primary button is created via `_btn(parent, text, command, primary=True)`
- **THEN** it SHALL bind mouse enter/leave to toggle background between `ACCENT` and `ACC2`
