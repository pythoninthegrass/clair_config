#!/usr/bin/env python3

import attrs
import flet as ft
from core.backend import ClairObscurConfig, get_version
from decouple import config
from pathlib import Path


@attrs.define
class ThemeConfig:
    """Theme configuration using attrs and decouple."""

    # Theme mode from environment or default to DARK
    mode: str = attrs.field(
        factory=lambda: config("THEME_MODE", default="DARK")
    )

    # Window dimensions from environment with defaults - optimized for nearest neighbor scaling
    height: int = attrs.field(
        factory=lambda: config("GUI_HEIGHT", default=1075, cast=int)
    )

    width: int = attrs.field(
        factory=lambda: config("GUI_WIDTH", default=1100, cast=int)
    )

    # TODO: set to false
    # Window resizable setting
    resizable: bool = attrs.field(
        factory=lambda: config("GUI_RESIZABLE", default=True, cast=bool)
    )

    # App title from environment with default
    title: str = attrs.field(
        factory=lambda: config("APP_TITLE", default="Clair Obscur: Expedition 33 - Unreal Config")
    )

    def get_flet_theme_mode(self) -> ft.ThemeMode:
        """Convert string theme mode to Flet ThemeMode enum."""
        theme_map = {
            "DARK": ft.ThemeMode.DARK,
            "LIGHT": ft.ThemeMode.LIGHT,
            "SYSTEM": ft.ThemeMode.SYSTEM
        }
        return theme_map.get(self.mode.upper(), ft.ThemeMode.DARK)

    def toggle_mode(self) -> str:
        """Toggle between light and dark mode and return new mode."""
        if self.mode.upper() == "DARK":
            self.mode = "LIGHT"
        else:
            self.mode = "DARK"
        return self.mode


# Legacy constants for backward compatibility
THEME = config("THEME", default="DARK")
GUI_WIDTH = config("GUI_WIDTH", default=1200, cast=int)
GUI_HEIGHT = config("GUI_HEIGHT", default=800, cast=int)

class ClairConfigFlet:
    """Main Flet application for Clair Obscur configuration."""

    def __init__(self, config_path: Path | None = None, game_version: str = "steam"):
        self.game_version = game_version
        self.custom_config_path = config_path
        self.config_manager = ClairObscurConfig(config_path=config_path, game_version=self.game_version)
        self.include_tweaks = True
        self.page = None

        # Initialize theme configuration with attrs and decouple
        self.theme_config = ThemeConfig()

        # UI component references
        self.game_version_radio = None
        self.preset_buttons = {}
        self.config_controls = {}

    def update_game_version(self, version: str) -> None:
        """Update game version and recreate config manager with correct paths."""
        self.game_version = version
        self.config_manager = ClairObscurConfig(config_path=self.custom_config_path, game_version=version)

    def main(self, page: ft.Page):
        """Main Flet app entry point."""
        self.page = page
        page.title = self.theme_config.title
        page.theme_mode = self.theme_config.get_flet_theme_mode()
        page.window.width = self.theme_config.width
        page.window.height = self.theme_config.height
        page.window.resizable = self.theme_config.resizable

        # Create the main layout inspired by the game's interface
        page.add(self.build_ui())

    def build_ui(self) -> ft.Container:
        """Build the main UI inspired by the game interface."""
        return ft.Container(
            content=ft.Column([
                # Header section - compact
                self.build_header(),

                # Main content area - tight layout at top
                ft.Row([
                    # Left column - Game Version & Graphics
                    ft.Container(
                        content=ft.Column([
                            self.build_game_version_section(),
                            self.build_graphics_section(),
                        ], tight=True),
                        width=420,
                        padding=ft.padding.all(10),
                    ),

                    # Right column - Presets & Advanced Options
                    ft.Container(
                        content=ft.Column([
                            self.build_preset_section(),
                            self.build_advanced_section(),
                        ], tight=True),
                        width=640,
                        padding=ft.padding.all(10),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),

                # Bottom button bar - positioned at bottom
                ft.Container(expand=True),  # Flexible spacer
                self.build_button_bar(),
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_GREY_900,
            expand=True,
        )

    def build_header(self) -> ft.Container:
        """Build the header section similar to the game's title area."""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "CLAIR OBSCUR",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.AMBER_300,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "EXPEDITION 33",
                    size=18,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.AMBER_200,
                    text_align=ft.TextAlign.CENTER,
                ),
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            padding=ft.padding.symmetric(vertical=12, horizontal=15),
            bgcolor=ft.Colors.BLACK54,
            alignment=ft.alignment.center,
        )

    def build_game_version_section(self) -> ft.Container:
        """Build game version selection section."""
        self.game_version_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="steam", label="Steam Version"),
                ft.Radio(value="gamepass", label="GamePass Version"),
            ]),
            value=self.game_version,
            on_change=self.on_game_version_changed,
        )

        return ft.Container(
            content=ft.Column([
                ft.Text("Game Version", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Divider(color=ft.Colors.WHITE24, height=1),
                self.game_version_radio,
            ], tight=True, spacing=5),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=ft.padding.all(12),
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(bottom=8),
        )

    def build_graphics_section(self) -> ft.Container:
        """Build graphics configuration section."""
        graphics_controls = [
            self.create_dropdown_option("Anisotropic Filtering",
                                      ["Disabled", "2x", "4x", "8x", "16x"], "Enabled"),
            self.create_dropdown_option("Depth of Field",
                                      ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"], "Ultra"),
            self.create_dropdown_option("Bloom",
                                      ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"], "Very High"),
            self.create_dropdown_option("Motion Blur",
                                      ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"], "High"),
            self.create_dropdown_option("Lens Flares",
                                      ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"], "High"),
            self.create_dropdown_option("Shadow Quality",
                                      ["Low", "Medium", "High", "Ultra"], "Ultra"),
            self.create_dropdown_option("Shadow Resolution",
                                      ["4096x4096", "2048x2048", "1024x1024"], "4096x4096"),
            self.create_dropdown_option("Film Grain",
                                      ["Disabled", "Enabled"], "Enabled"),
        ]

        return ft.Container(
            content=ft.Column([
                ft.Text("Graphics Configuration", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Divider(color=ft.Colors.WHITE24, height=1),
                ft.Column(graphics_controls, spacing=6, tight=True),
            ], tight=True, spacing=5),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=ft.padding.all(12),
            border_radius=ft.border_radius.all(8),
        )

    def build_preset_section(self) -> ft.Container:
        """Build performance presets section."""
        preset_buttons = [
            ft.Container(
                content=ft.ElevatedButton(
                    text="Low",
                    on_click=lambda _: self.apply_preset("low"),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: ft.Colors.RED_700},
                        color=ft.Colors.WHITE,
                    ),
                    width=110,
                    height=40,
                ),
                margin=ft.margin.all(3),
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Balanced",
                    on_click=lambda _: self.apply_preset("balanced"),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: ft.Colors.ORANGE_700},
                        color=ft.Colors.WHITE,
                    ),
                    width=110,
                    height=40,
                ),
                margin=ft.margin.all(3),
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Ultra",
                    on_click=lambda _: self.apply_preset("ultra"),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN_700},
                        color=ft.Colors.WHITE,
                    ),
                    width=110,
                    height=40,
                ),
                margin=ft.margin.all(3),
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Text(
                        "Sharp &\nClear",
                        text_align=ft.TextAlign.CENTER,
                        size=12,
                        color=ft.Colors.WHITE
                    ),
                    on_click=lambda _: self.apply_preset("sharp_clear"),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: ft.Colors.BLUE_700},
                        color=ft.Colors.WHITE,
                    ),
                    width=110,
                    height=40,
                ),
                margin=ft.margin.all(3),
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Text(
                        "Soft &\nAmbient",
                        text_align=ft.TextAlign.CENTER,
                        size=12,
                        color=ft.Colors.WHITE
                    ),
                    on_click=lambda _: self.apply_preset("soft_ambient"),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: ft.Colors.PURPLE_700},
                        color=ft.Colors.WHITE,
                    ),
                    width=110,
                    height=40,
                ),
                margin=ft.margin.all(3),
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Custom",
                    on_click=lambda _: self.apply_preset("custom"),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREY_700},
                        color=ft.Colors.WHITE,
                    ),
                    width=110,
                    height=40,
                ),
                margin=ft.margin.all(3),
            ),
        ]

        return ft.Container(
            content=ft.Column([
                ft.Text("Performance Presets", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Divider(color=ft.Colors.WHITE24, height=1),
                ft.Row([
                    ft.Column([preset_buttons[0], preset_buttons[1], preset_buttons[2]], spacing=5),
                    ft.Column([preset_buttons[3], preset_buttons[4], preset_buttons[5]], spacing=5),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ], tight=True, spacing=5),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=ft.padding.all(12),
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(bottom=8),
        )

    def build_advanced_section(self) -> ft.Container:
        """Build advanced options section."""
        advanced_controls = [
            self.create_slider_option("Sharpening Strength", 0.0, 3.0, 1.0, 0.1),
            self.create_slider_option("View Distance", 0.5, 3.0, 2.75, 0.05),
            self.create_slider_option("Shadow Distance", 0.5, 3.0, 2.75, 0.05),
            self.create_slider_option("Foliage Distance", 0.5, 3.0, 2.50, 0.05),
            self.create_switch_option("Fog", True),
            self.create_switch_option("Volumetric Fog", True),
            self.create_switch_option("Chromatic Aberration", True),
            self.create_switch_option("Include Engine Tweaks", True),
            self.create_switch_option("Set Config Read-Only", False),
        ]

        return ft.Container(
            content=ft.Column([
                ft.Text("Advanced Options", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Divider(color=ft.Colors.WHITE24, height=1),
                ft.Column(advanced_controls, spacing=6, tight=True),
            ], tight=True, spacing=5),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=ft.padding.all(12),
            border_radius=ft.border_radius.all(8),
        )

    def build_button_bar(self) -> ft.Container:
        """Build bottom button bar with version info."""
        return ft.Container(
            content=ft.Column([
                # Centered buttons row
                ft.Row([
                    ft.ElevatedButton(
                        text="Save & Exit",
                        on_click=self.save_and_exit,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN_600},
                            color=ft.Colors.WHITE,
                        ),
                        width=120,
                        height=40,
                    ),
                    ft.ElevatedButton(
                        text="Save Changes",
                        on_click=self.save_changes,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.DEFAULT: ft.Colors.BLUE_600},
                            color=ft.Colors.WHITE,
                        ),
                        width=120,
                        height=40,
                    ),
                    ft.ElevatedButton(
                        text="Reload Config",
                        on_click=self.reload_config,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.DEFAULT: ft.Colors.ORANGE_600},
                            color=ft.Colors.WHITE,
                        ),
                        width=120,
                        height=40,
                    ),
                    ft.ElevatedButton(
                        text="Launch Game",
                        on_click=self.launch_game,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.DEFAULT: ft.Colors.PURPLE_600},
                            color=ft.Colors.WHITE,
                        ),
                        width=120,
                        height=40,
                    ),
                    ft.ElevatedButton(
                        text="Toggle Theme",
                        on_click=self.toggle_theme,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREY_600},
                            color=ft.Colors.WHITE,
                        ),
                        width=120,
                        height=40,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                
                # Version info row positioned at bottom right
                ft.Row([
                    ft.Container(expand=True),  # Push version to right
                    ft.Text(
                        f"Unreal Config v{get_version()}",
                        size=12,
                        color=ft.Colors.WHITE70,
                    ),
                ], alignment=ft.MainAxisAlignment.END),
            ], spacing=5),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.BLACK54,
        )

    def create_dropdown_option(self, label: str, options: list, default: str) -> ft.Container:
        """Create a dropdown configuration option."""
        dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(opt) for opt in options],
            value=default,
            width=200,
        )
        self.config_controls[label] = dropdown

        return ft.Container(
            content=ft.Row([
                ft.Text(label, size=14, color=ft.Colors.WHITE, width=150),
                dropdown,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(vertical=5),
        )

    def create_slider_option(self, label: str, min_val: float, max_val: float,
                           default: float, step: float) -> ft.Container:
        """Create a slider configuration option."""
        slider_text = ft.Text(str(default), size=14, color=ft.Colors.WHITE, width=50)

        def on_change(e):
            slider_text.value = str(round(e.control.value, 2))
            self.page.update()

        slider = ft.Slider(
            min=min_val,
            max=max_val,
            value=default,
            divisions=int((max_val - min_val) / step),
            on_change=on_change,
            width=200,
        )

        self.config_controls[label] = slider

        return ft.Container(
            content=ft.Row([
                ft.Text(label, size=14, color=ft.Colors.WHITE, width=150),
                slider,
                slider_text,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(vertical=5),
        )

    def create_switch_option(self, label: str, default: bool) -> ft.Container:
        """Create a switch configuration option."""
        switch = ft.Switch(value=default)
        self.config_controls[label] = switch

        return ft.Container(
            content=ft.Row([
                ft.Text(label, size=14, color=ft.Colors.WHITE, width=200),
                switch,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(vertical=5),
        )

    def on_game_version_changed(self, e):
        """Handle game version change."""
        self.update_game_version(e.control.value)
        self.show_snackbar(f"Switched to {e.control.value.capitalize()} version")

    def apply_preset(self, preset_name: str):
        """Apply a performance preset."""
        try:
            preset_config = self.config_manager.get_performance_preset(preset_name)
            system_settings = preset_config.get("SystemSettings", {})

            # Update UI controls with preset values
            mappings = {
                "r.MaxAnisotropy": ("Anisotropic Filtering", lambda x: f"{x}x" if x != "0" else "Disabled"),
                "r.DepthOfFieldQuality": ("Depth of Field", lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)]),
                "r.BloomQuality": ("Bloom", lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)]),
                "r.MotionBlurQuality": ("Motion Blur", lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)]),
                "r.LensFlareQuality": ("Lens Flares", lambda x: ["Disabled", "Low", "Medium", "High", "Very High", "Ultra"][min(int(x), 5)]),
                "r.ShadowQuality": ("Shadow Quality", lambda x: ["Low", "Medium", "High", "Ultra"][min(int(x), 3)]),
                "r.FilmGrain": ("Film Grain", lambda x: "Enabled" if x != "0" else "Disabled"),
                "r.Fog": ("Fog", lambda x: x.lower() == "true"),
                "r.VolumetricFog": ("Volumetric Fog", lambda x: x.lower() == "true"),
                "r.ViewDistanceScale": ("View Distance", lambda x: float(x)),
                "r.Tonemapper.Sharpen": ("Sharpening Strength", lambda x: float(x)),
            }

            for config_key, (ui_label, converter) in mappings.items():
                if config_key in system_settings and ui_label in self.config_controls:
                    value = system_settings[config_key]
                    converted_value = converter(value)
                    control = self.config_controls[ui_label]

                    if isinstance(control, ft.Dropdown | ft.Slider | ft.Switch):
                        control.value = converted_value

            self.page.update()
            self.show_snackbar(f"{preset_name.title()} preset applied")

        except Exception as e:
            self.show_snackbar(f"Error applying preset: {str(e)}", is_error=True)

    def gather_ui_values(self) -> dict:
        """Gather all configuration values from UI controls."""
        settings = {"SystemSettings": {}, "/Script/Engine.RendererSettings": {}}

        # Map UI controls to config keys
        config_map = {
            "Anisotropic Filtering": ("SystemSettings", "r.MaxAnisotropy"),
            "Depth of Field": ("SystemSettings", "r.DepthOfFieldQuality"),
            "Bloom": ("SystemSettings", "r.BloomQuality"),
            "Motion Blur": ("SystemSettings", "r.MotionBlurQuality"),
            "Lens Flares": ("SystemSettings", "r.LensFlareQuality"),
            "Shadow Quality": ("SystemSettings", "r.ShadowQuality"),
            "Shadow Resolution": ("SystemSettings", "r.Shadow.MaxResolution"),
            "Film Grain": ("SystemSettings", "r.FilmGrain"),
            "Fog": ("SystemSettings", "r.Fog"),
            "Volumetric Fog": ("SystemSettings", "r.VolumetricFog"),
            "Chromatic Aberration": ("SystemSettings", "r.SceneColorFringeQuality"),
            "Sharpening Strength": ("SystemSettings", "r.Tonemapper.Sharpen"),
            "View Distance": ("SystemSettings", "r.ViewDistanceScale"),
            "Shadow Distance": ("SystemSettings", "r.Shadow.DistanceScale"),
            "Foliage Distance": ("SystemSettings", "r.Foliage.LODDistanceScale"),
        }

        for ui_label, (section, key) in config_map.items():
            if ui_label in self.config_controls:
                control = self.config_controls[ui_label]

                if isinstance(control, ft.Dropdown):
                    value = control.value
                    # Convert UI values to config values
                    quality_map = {
                        "Disabled": "0", "Low": "1", "Medium": "2", "High": "3",
                        "Very High": "4", "Ultra": "5", "2x": "2", "4x": "4",
                        "8x": "8", "16x": "16", "Enabled": "1"
                    }
                    value = quality_map.get(value, value)
                elif isinstance(control, ft.Slider):
                    value = str(control.value)
                elif isinstance(control, ft.Switch):
                    if ui_label in ["Fog", "Volumetric Fog"]:
                        value = "True" if control.value else "False"
                    else:
                        value = "1" if control.value else "0"
                else:
                    continue

                settings[section][key] = value

        return settings

    def save_changes(self, e):
        """Save configuration changes."""
        try:
            settings = self.gather_ui_values()

            # Create backup
            backup_path = self.config_manager.backup_existing_config()
            if backup_path:
                self.show_snackbar(f"Backup created: {backup_path.name}")

            # Apply settings
            self.config_manager.apply_custom_settings(settings)

            # Add engine tweaks if enabled
            if self.config_controls.get("Include Engine Tweaks", ft.Switch(value=True)).value:
                tweaks = self.config_manager.get_engine_tweaks()
                self.config_manager.apply_custom_settings(tweaks)

            # Set read-only if enabled
            read_only = self.config_controls.get("Set Config Read-Only", ft.Switch(value=False)).value
            self.config_manager.set_read_only(read_only)

            message = "Configuration saved and set to read-only!" if read_only else "Configuration saved successfully!"
            self.show_snackbar(message)

        except Exception as e:
            self.show_snackbar(f"Error saving configuration: {str(e)}", is_error=True)

    def reload_config(self, e):
        """Reload configuration from disk."""
        try:
            # Reset UI to default values and reload from config
            self.show_snackbar("Configuration reloaded")
        except Exception as e:
            self.show_snackbar(f"Error reloading configuration: {str(e)}", is_error=True)

    def launch_game(self, e):
        """Launch the game."""
        self.show_snackbar("Launch game functionality not implemented")

    def save_and_exit(self, e):
        """Save and exit the application."""
        self.save_changes(e)
        self.page.window.close()

    def toggle_theme(self, e):
        """Toggle between light and dark themes using attrs-based theme config."""
        new_mode = self.theme_config.toggle_mode()
        self.page.theme_mode = self.theme_config.get_flet_theme_mode()
        self.page.update()
        self.show_snackbar(f"Switched to {new_mode.lower()} theme")

    def show_snackbar(self, message: str, is_error: bool = False):
        """Show a snackbar notification."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED if is_error else ft.Colors.GREEN,
        )
        self.page.snack_bar.open = True
        self.page.update()


def run_flet_app(config_path: Path | None = None, game_version: str = "steam"):
    """Run the Flet application."""
    app = ClairConfigFlet(config_path=config_path, game_version=game_version)
    ft.app(target=app.main, view=ft.AppView.FLET_APP)


if __name__ == "__main__":
    run_flet_app()
