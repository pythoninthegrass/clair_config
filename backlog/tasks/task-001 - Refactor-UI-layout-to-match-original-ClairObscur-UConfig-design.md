---
id: task-001
title: Refactor UI layout to match original ClairObscur-UConfig design
status: Done
assignee: []
created_date: '2025-08-31 06:32'
updated_date: '2025-09-01 04:36'
labels:
  - ui
  - refactor
  - layout
dependencies: []
priority: high
---

## Description

Redesign the current TUI layout to match the compact, functional design from the original ClairObscur-UConfig repository, optimizing for 1080p viewports and improving space efficiency while retaining all existing functionality

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 UI layout matches the compact design shown in original ClairObscur-UConfig screenshots,Interface is properly sized for 1080p viewports without oversized elements,Layout is less cluttered with improved space efficiency compared to current implementation,All existing TUI and CLI functionality is preserved for Linux OSes,Advanced options are visible without scrolling on 1080p screens
<!-- AC:END -->

## Implementation Notes

Completed: Implemented attrs-based theme configuration with decouple integration, centered banner text horizontally, updated resolution for nearest neighbor scaling (1280x720), aligned columns vertically, centered 'Sharp & Clear' and 'Soft & Ambient' button text, moved version info to bottom right aligned with buttons, fixed banner/main content alignment overlap, and fixed non-responsive bottom buttons by restructuring layout.
