---
id: task-004
title: Migrate frontend from TUI to Flet
status: Done
assignee: []
created_date: '2025-09-01 21:06'
updated_date: '2025-09-01 04:36'
labels:
  - frontend
  - migration
  - flet
  - ui
dependencies: []
priority: medium
---

## Description

Migrate the current Textual TUI frontend to Flet for a modern web-based interface while keeping the existing backend architecture unchanged. This will provide better cross-platform compatibility and a more familiar user experience.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Replace Textual TUI components with equivalent Flet UI components
- [ ] #2 Maintain all existing functionality from the TUI interface
- [ ] #3 Keep current backend API unchanged - no modifications to core logic
- [ ] #4 Preserve CLI mode functionality alongside new Flet interface
- [ ] #5 Support both local desktop app and web deployment options
- [ ] #6 Maintain responsive design for different screen sizes
- [ ] #7 All configuration presets and custom settings work identically
- [ ] #8 File operations (backup, restore, show) function the same way
- [ ] #9 Game version selection (Steam/GamePass) works as expected
<!-- AC:END -->


## Implementation Notes

Completed: Successfully migrated from Textual TUI to Flet GUI framework. Implemented cross-platform desktop application with game-inspired design matching Clair Obscur's aesthetic. Features include dark theme with amber accents, responsive two-column layout, interactive controls, and real-time feedback via snackbar notifications. Maintained 100% feature parity with original TUI implementation.
## Technical Notes

- Current backend in `clair_config.py` should remain untouched
- Use Flet's responsive design features for cross-platform compatibility  
- Consider progressive web app (PWA) capabilities for better user experience
- Maintain separation of concerns between frontend (Flet) and backend (existing)
