#!/usr/bin/env python

"""
Frontend module for Clair Obscur: Expedition 33 Configuration.
Contains all UI components and user interaction logic.
"""

import configparser
from core.backend import ClairObscurConfig
from pathlib import Path
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, RadioButton, RadioSet, Select, Static, Switch
from typing import Any


class ConfigOption(Container):
    """A configuration option widget with label and control."""

    def __init__(self, label: str, control_type: str = "select", options: list = None, value: str = "", **kwargs):
        super().__init__(**kwargs)
        self.label_text = label
        self.control_type = control_type
        self.options = options or []
        self.value = value

    def compose(self) -> ComposeResult:
        yield Label(self.label_text)

        if self.control_type == "select" and self.options:
            yield Select([(opt, opt) for opt in self.options], value=self.value, allow_blank=False)
        elif self.control_type == "input":
            yield Input(value=self.value, placeholder="Enter value")
        elif self.control_type == "switch":
            yield Switch(value=self.value == "Enabled")


class GameVersionSection(Container):
    """Game version selection section."""

    def compose(self) -> ComposeResult:
        yield Static("Game Version")
        with RadioSet(id="game-version"):
            yield RadioButton("Steam Version", value=True)
            yield RadioButton("GamePass Version")


class GraphicsSection(Container):
    """Graphics configuration section."""

    def compose(self) -> ComposeResult:
        yield Static("Graphics Configuration")

        # Resolution options
        resolutions = ["1920x1080", "2560x1440", "3840x2160", "4096x4096"]
        yield ConfigOption("Resolution", "select", resolutions, "4096x4096")

        # Anisotropic Filtering
        aniso_options = ["Disabled", "2x", "4x", "8x", "16x"]
        yield ConfigOption("Anisotropic Filtering", "select", aniso_options, "16x")

        # Depth of Field
        quality_options = ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"]
        yield ConfigOption("Depth of Field", "select", quality_options, "Very High")

        # Bloom
        yield ConfigOption("Bloom", "select", quality_options, "Very High")

        # Motion Blur
        yield ConfigOption("Motion Blur", "select", quality_options, "Very High")

        # Lens Flares
        yield ConfigOption("Lens Flares", "select", quality_options, "High")

        # Fog
        yield ConfigOption("Fog", "switch", value="Enabled")

        # Volumetric Fog
        yield ConfigOption("Volumetric Fog", "switch", value="Enabled")

        # Chromatic Aberration
        yield ConfigOption("Chromatic Aberration", "switch", value="Enabled")

        # Disable Distortion Effects
        yield ConfigOption("Disable Distortion Effects", "switch", value="Disabled")


class PresetSection(Container):
    """Preset buttons section."""

    def compose(self) -> ComposeResult:
        yield Static("Performance Presets")

        with Grid():
            yield Button("Low", id="preset-low", classes="preset-low")
            yield Button("Balanced", id="preset-balanced", classes="preset-balanced")
            yield Button("Ultra", id="preset-ultra", classes="preset-ultra")
            yield Button("Sharp & Clear", id="preset-sharp", classes="preset-sharp")
            yield Button("Soft & Ambient", id="preset-soft", classes="preset-soft")
            yield Button("Custom", id="preset-custom", classes="preset-custom")


class AdvancedSection(Container):
    """Advanced options section."""

    def compose(self) -> ComposeResult:
        yield Static("Advanced Options")

        with RadioSet(id="advanced-options"):
            yield RadioButton("Hide Options", value=True)
            yield RadioButton("Show Options")

        # Engine tweaks toggle
        yield ConfigOption("Include Engine Tweaks", "switch", value="Enabled")

        # Read-only mode toggle
        yield ConfigOption("Set Config Read-Only", "switch", value="Disabled")

        # Split advanced settings into two columns
        with Grid():
            with Vertical(classes="advanced-column"):
                yield ConfigOption("Film Grain", "switch", value="Enabled")
                yield ConfigOption("Shadow Quality", "select", ["Low", "Medium", "High", "Ultra"], "Ultra")
                yield ConfigOption("Shadow Resolution", "input", value="4096x4096")
                yield ConfigOption("Tonemapper Quality", "input", value="5")
                yield ConfigOption("Grain Quantization", "switch", value="Disabled")

            with Vertical(classes="advanced-column"):
                yield ConfigOption("Sharpening Strength", "input", value="1.0")
                yield ConfigOption("View Distance", "input", value="2.75")
                yield ConfigOption("Shadow Distance", "input", value="2.75")
                yield ConfigOption("Foliage Distance", "input", value="2.50")


class ClairConfigTUI(App):
    """Main TUI application for Clair Obscur configuration."""

    TITLE = "Clair Obscur: Expedition 33 - Unreal Config v2.0"

    CSS_PATH = "../static/styles.tcss"

    BINDINGS = [
        Binding("ctrl+s", "save_changes", "Save Changes"),
        Binding("ctrl+r", "reload_config", "Reload Config"),
        Binding("ctrl+l", "launch_game", "Launch Game"),
        Binding("ctrl+p", "toggle_palette", "Toggle Palette"),
        Binding("ctrl+q", "save_and_exit", "Save & Exit"),
        Binding("escape", "quit", "Exit"),
    ]

    def __init__(self, config_path: Path | None = None, game_version: str = "steam"):
        super().__init__()
        self.game_version = game_version
        self.custom_config_path = config_path
        self.config_manager = ClairObscurConfig(config_path=config_path, game_version=self.game_version)
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # Preserve case
        self.include_tweaks = True  # Default to including engine tweaks

    def update_game_version(self, version: str) -> None:
        """Update game version and recreate config manager with correct paths."""
        self.game_version = version
        self.config_manager = ClairObscurConfig(config_path=self.custom_config_path, game_version=version)

    def apply_preset_to_ui(self, preset_name: str) -> None:
        """Apply preset values to UI controls."""
        preset_config = self.config_manager.get_performance_preset(preset_name)
        system_settings = preset_config.get("SystemSettings", {})

        # Mapping of config keys to UI control lookups
        ui_mappings = {
            "r.MaxAnisotropy": ("Anisotropic Filtering", lambda x: f"{x}x" if x != "0" else "Disabled"),
            "r.DepthOfFieldQuality": (
                "Depth of Field",
                lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)],
            ),
            "r.BloomQuality": ("Bloom", lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)]),
            "r.MotionBlurQuality": (
                "Motion Blur",
                lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)],
            ),
            "r.LensFlareQuality": (
                "Lens Flares",
                lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)],
            ),
            "r.ShadowQuality": ("Shadow Quality", lambda x: ["Low", "Medium", "High", "Ultra"][min(int(x), 3)]),
            "r.FilmGrain": ("Film Grain", lambda x: "Enabled" if x != "0" else "Disabled"),
            "r.Fog": ("Fog", lambda x: "Enabled" if x.lower() == "true" else "Disabled"),
            "r.VolumetricFog": ("Volumetric Fog", lambda x: "Enabled" if x.lower() == "true" else "Disabled"),
            "r.SceneColorFringeQuality": ("Chromatic Aberration", lambda x: "Enabled" if x != "0" else "Disabled"),
            "r.ViewDistanceScale": ("View Distance", lambda x: x),
            "r.Tonemapper.Sharpen": ("Sharpening Strength", lambda x: x),
        }

        # Apply settings to UI controls
        for config_key, (ui_label, converter) in ui_mappings.items():
            if config_key in system_settings:
                value = system_settings[config_key]
                converted_value = converter(value)
                self.update_ui_control(ui_label, converted_value)

    def update_ui_control(self, label: str, value: str) -> None:
        """Update a specific UI control with a value."""
        try:
            for option in self.query(ConfigOption):
                option_label = option.query_one(Label).renderable
                if str(option_label) == label:
                    if option.control_type == "select":
                        select = option.query_one(Select)
                        select.value = value
                    elif option.control_type == "input":
                        input_widget = option.query_one(Input)
                        input_widget.value = value
                    elif option.control_type == "switch":
                        switch = option.query_one(Switch)
                        switch.value = value == "Enabled"
                    break
        except Exception:
            pass  # Ignore errors for missing controls

    def compose(self) -> ComposeResult:
        """Build the UI."""
        yield Header()

        with Container(id="main-container"):
            # Left column
            with Vertical(id="left-column"):
                yield GameVersionSection()
                yield GraphicsSection()

            # Right column
            with Vertical(id="right-column"):
                yield PresetSection()
                yield AdvancedSection()

        # Bottom button bar
        with Container(id="button-bar"), Grid(id="button-grid"):
            yield Button("Save & Exit", id="exit-btn")
            yield Button("Save Changes", id="save-btn")
            yield Button("Reload Config", id="reload-btn")
            yield Button("Launch Game", id="launch-btn")
            yield Button("Palette", id="palette-btn")

        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""
        self.load_config()
        self.adjust_button_layout()

        # Update UI to reflect initial game version
        if self.game_version == "gamepass":
            try:
                radio_set = self.query_one("#game-version", RadioSet)
                for button in radio_set.query(RadioButton):
                    if button.label == "GamePass Version":
                        button.value = True
                    else:
                        button.value = False
            except Exception:
                pass

    @on(RadioSet.Changed, "#game-version")
    def on_game_version_changed(self, event: RadioSet.Changed) -> None:
        """Handle game version selection change."""
        if event.pressed.label == "GamePass Version":
            self.update_game_version("gamepass")
        else:
            self.update_game_version("steam")
        self.load_config()  # Reload config from new path
        config_path = self.config_manager.engine_ini_path
        self.notify(f"Switched to {event.pressed.label} - Path: {config_path.parent.name}", severity="information")

    def on_resize(self) -> None:
        """Called when terminal is resized."""
        self.adjust_button_layout()

    def adjust_button_layout(self) -> None:
        """Adjust button grid based on terminal width."""
        try:
            button_grid = self.query_one("#button-grid", Grid)
            width = self.size.width

            if width < 60:
                # 2 columns for very narrow terminals
                button_grid.styles.grid_size = (2, 3)
                button_grid.styles.grid_columns = "1fr 1fr"
            elif width < 100:
                # 3 columns for medium terminals
                button_grid.styles.grid_size = (3, 2)
                button_grid.styles.grid_columns = "1fr 1fr 1fr"
            else:
                # 5 columns for wide terminals
                button_grid.styles.grid_size = (5, 1)
                button_grid.styles.grid_columns = "1fr 1fr 1fr 1fr 1fr"
        except Exception:
            pass

    def load_config(self) -> None:
        """Load configuration from Engine.ini."""
        self.config = self.config_manager.read_config()
        self.apply_config_to_ui()

    def apply_config_to_ui(self) -> None:
        """Apply loaded config values to UI controls."""
        # This would map config values to UI controls
        # For brevity, keeping this as a placeholder
        pass

    def gather_ui_values(self) -> dict:
        """Gather all values from UI controls."""
        settings = {
            "SystemSettings": {},
            "/Script/Engine.RendererSettings": {},
        }

        # Gather values from all ConfigOption widgets
        for option in self.query(ConfigOption):
            label = option.query_one(Label).renderable

            # Get value based on control type
            if option.control_type == "select":
                select = option.query_one(Select)
                value = select.value
            elif option.control_type == "input":
                input_widget = option.query_one(Input)
                value = input_widget.value
            elif option.control_type == "switch":
                switch = option.query_one(Switch)
                value = "True" if switch.value else "False"
            else:
                continue

            # Map UI labels to config keys with improved mapping
            config_map = {
                "Resolution": ("SystemSettings", "r.ScreenPercentage"),
                "Anisotropic Filtering": ("SystemSettings", "r.MaxAnisotropy"),
                "Depth of Field": ("SystemSettings", "r.DepthOfFieldQuality"),
                "Bloom": ("SystemSettings", "r.BloomQuality"),
                "Motion Blur": ("SystemSettings", "r.MotionBlurQuality"),
                "Lens Flares": ("SystemSettings", "r.LensFlareQuality"),
                "Fog": ("SystemSettings", "r.Fog"),
                "Volumetric Fog": ("SystemSettings", "r.VolumetricFog"),
                "Chromatic Aberration": ("SystemSettings", "r.SceneColorFringeQuality"),
                "Disable Distortion Effects": ("SystemSettings", "r.DistortionEffects"),
                "Film Grain": ("SystemSettings", "r.FilmGrain"),
                "Shadow Quality": ("SystemSettings", "r.ShadowQuality"),
                "Shadow Resolution": ("SystemSettings", "r.Shadow.MaxResolution"),
                "Tonemapper Quality": ("SystemSettings", "r.Tonemapper.Quality"),
                "Grain Quantization": ("SystemSettings", "r.Tonemapper.GrainQuantization"),
                "Sharpening Strength": ("SystemSettings", "r.Tonemapper.Sharpen"),
                "View Distance": ("SystemSettings", "r.ViewDistanceScale"),
                "Shadow Distance": ("SystemSettings", "r.Shadow.DistanceScale"),
                "Foliage Distance": ("SystemSettings", "r.Foliage.LODDistanceScale"),
            }

            if str(label) in config_map:
                section, key = config_map[str(label)]

                # Convert UI values to config values
                if option.control_type == "select":
                    # Map dropdown values to config values
                    quality_map = {
                        "Disabled": "0",
                        "Low": "1",
                        "Medium": "2",
                        "High": "3",
                        "Very High": "4",
                        "Ultra": "5",
                        "2x": "2",
                        "4x": "4",
                        "8x": "8",
                        "16x": "16",
                    }
                    value = quality_map.get(value, value)
                elif option.control_type == "switch":
                    # Convert switch values to proper config format
                    if str(label) in ["Fog", "Volumetric Fog"]:
                        value = "True" if value == "True" else "False"
                    else:
                        value = "1" if value == "True" else "0"

                settings[section][key] = value

        return settings

    def get_engine_tweaks_setting(self) -> bool:
        """Get the engine tweaks toggle setting from UI."""
        try:
            for option in self.query(ConfigOption):
                label = option.query_one(Label).renderable
                if str(label) == "Include Engine Tweaks":
                    switch = option.query_one(Switch)
                    return switch.value
        except Exception:
            pass
        return True  # Default to enabled

    def get_read_only_setting(self) -> bool:
        """Get the read-only toggle setting from UI."""
        try:
            for option in self.query(ConfigOption):
                label = option.query_one(Label).renderable
                if str(label) == "Set Config Read-Only":
                    switch = option.query_one(Switch)
                    return switch.value
        except Exception:
            pass
        return False  # Default to disabled

    # Preset button handlers
    @on(Button.Pressed, "#preset-low")
    def preset_low(self) -> None:
        """Apply Low preset."""
        self.apply_preset_to_ui("low")
        self.notify("Low preset applied", severity="information")

    @on(Button.Pressed, "#preset-balanced")
    def preset_balanced(self) -> None:
        """Apply Balanced preset."""
        self.apply_preset_to_ui("balanced")
        self.notify("Balanced preset applied", severity="information")

    @on(Button.Pressed, "#preset-ultra")
    def preset_ultra(self) -> None:
        """Apply Ultra preset."""
        self.apply_preset_to_ui("ultra")
        self.notify("Ultra preset applied", severity="information")

    @on(Button.Pressed, "#preset-sharp")
    def preset_sharp(self) -> None:
        """Apply Sharp & Clear preset."""
        self.apply_preset_to_ui("sharp_clear")
        self.notify("Sharp & Clear preset applied", severity="information")

    @on(Button.Pressed, "#preset-soft")
    def preset_soft(self) -> None:
        """Apply Soft & Ambient preset."""
        self.apply_preset_to_ui("soft_ambient")
        self.notify("Soft & Ambient preset applied", severity="information")

    @on(Button.Pressed, "#preset-custom")
    def preset_custom(self) -> None:
        """Reset to custom/default values."""
        self.notify("Custom preset - manually adjust settings", severity="information")

    @on(Button.Pressed, "#save-btn")
    def action_save_changes(self) -> None:
        """Save configuration to Engine.ini."""
        settings = self.gather_ui_values()

        # Check if engine tweaks should be included
        self.include_tweaks = self.get_engine_tweaks_setting()

        # Create backup
        backup_path = self.config_manager.backup_existing_config()
        if backup_path:
            self.notify(f"Backup created: {backup_path.name}", severity="information")

        # Apply settings using the config manager
        self.config_manager.apply_custom_settings(settings)

        # Add engine tweaks if enabled
        if self.include_tweaks:
            tweaks = self.config_manager.get_engine_tweaks()
            self.config_manager.apply_custom_settings(tweaks)

        # Set read-only mode if requested
        read_only = self.get_read_only_setting()
        if read_only:
            self.config_manager.set_read_only(True)
            self.notify("Configuration saved and set to read-only!", severity="information")
        else:
            self.config_manager.set_read_only(False)
            self.notify("Configuration saved successfully!", severity="information")

    @on(Button.Pressed, "#reload-btn")
    def action_reload_config(self) -> None:
        """Reload configuration from disk."""
        self.load_config()
        config_path = self.config_manager.engine_ini_path
        if config_path.exists():
            self.notify(f"Configuration reloaded from {config_path.name}", severity="information")
        else:
            self.notify(f"No config found at {config_path.parent.name}", severity="warning")

    @on(Button.Pressed, "#launch-btn")
    def action_launch_game(self) -> None:
        """Launch the game."""
        self.notify("Launch game functionality not implemented", severity="warning")

    @on(Button.Pressed, "#exit-btn")
    def action_save_and_exit(self) -> None:
        """Save and exit."""
        self.action_save_changes()
        self.exit()

    def action_quit(self) -> None:
        """Exit without saving."""
        self.exit()

    @on(Button.Pressed, "#palette-btn")
    def action_toggle_palette(self) -> None:
        """Toggle dark/light mode."""
        self.app.dark = not self.app.dark
        if self.app.dark:
            self.notify("Switched to dark mode", severity="information")
        else:
            self.notify("Switched to light mode", severity="information")

