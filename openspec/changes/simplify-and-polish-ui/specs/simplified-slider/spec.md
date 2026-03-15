## ADDED Requirements

### Requirement: Slider uses native Scale widget for interaction

The Slider widget SHALL use tkinter's Scale widget for all user interaction (click, drag, keyboard).

#### Scenario: User drags slider
- **WHEN** the user drags the Scale thumb
- **THEN** the slider value SHALL update and the on_change callback SHALL fire

#### Scenario: Slider value is set programmatically
- **WHEN** `slider.set(value)` is called
- **THEN** both the Scale position and the colored fill SHALL update

### Requirement: Slider displays colored fill via Canvas

The Slider widget SHALL display a colored fill bar using a Canvas widget layered with the Scale.

#### Scenario: Fill reflects current value
- **WHEN** the slider value changes
- **THEN** the Canvas fill rectangle width SHALL be proportional to `(value - from_) / (to - from_)`

#### Scenario: Fill uses thumb color
- **WHEN** the slider renders its fill bar
- **THEN** the fill rectangle SHALL use the `thumb_color` parameter

### Requirement: Slider is a Frame containing Canvas and Scale

The Slider class SHALL extend `tk.Frame` (not `tk.Canvas`) and contain both child widgets.

#### Scenario: Widget hierarchy
- **WHEN** a Slider is instantiated
- **THEN** it SHALL be a `tk.Frame` containing a Canvas and a Scale packed vertically
