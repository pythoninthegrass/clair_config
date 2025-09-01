#!/usr/bin/env python

"""
Backend module for Clair Obscur: Expedition 33 Configuration.
Handles all configuration management logic independently of UI.
"""

import configparser
import shutil
import tomllib
from pathlib import Path
from typing import Any, Optional


class ClairObscurConfig:
    """Manage Engine.ini configurations for Clair Obscur: Expedition 33."""

    def __init__(self, config_path: Path | None = None, game_version: str = "steam"):
        """Initialize with game version specific config path or custom path."""
        # Load configuration from TOML file
        with open(Path(__file__).parent.parent / "config.toml", "rb") as f:
            self.toml_config = tomllib.load(f)

        if config_path:
            self.config_path = Path(config_path)
        else:
            home = Path.home()
            if game_version == "gamepass":
                # GamePass path
                self.config_path = home / self.toml_config["paths"]["gamepass_path"]
            else:
                # Default Steam Proton path
                self.config_path = home / self.toml_config["paths"]["steam_path"]

        self.engine_ini_path = self.config_path / "Engine.ini"

        # Ensure config directory exists
        self.config_path.mkdir(parents=True, exist_ok=True)

    def get_performance_preset(self, preset: str = "balanced") -> dict[str, dict[str, Any]]:
        """Get predefined performance presets from TOML config."""
        return self.toml_config["presets"].get(preset, self.toml_config["presets"]["balanced"])

    def get_engine_tweaks(self) -> dict[str, dict[str, Any]]:
        """Additional engine tweaks for better performance from TOML config."""
        return self.toml_config["engine_tweaks"]

    def backup_existing_config(self) -> Path | None:
        """Create a backup of existing Engine.ini if it exists."""
        if self.engine_ini_path.exists():
            backup_path = self.engine_ini_path.with_suffix(".ini.backup")
            shutil.copy2(self.engine_ini_path, backup_path)
            return backup_path
        return None

    def create_engine_ini(self, preset: str = "balanced", include_tweaks: bool = True) -> None:
        """Create Engine.ini with specified preset and tweaks."""
        config = configparser.ConfigParser()
        config.optionxform = str  # Preserve case sensitivity

        # Add preset settings
        preset_config = self.get_performance_preset(preset)
        for section, settings in preset_config.items():
            config[section] = {}
            for key, value in settings.items():
                config[section][key] = str(value)

        # Add engine tweaks if requested
        if include_tweaks:
            tweak_config = self.get_engine_tweaks()
            for section, settings in tweak_config.items():
                if section not in config:
                    config[section] = {}
                for key, value in settings.items():
                    config[section][key] = str(value)

        # Write config file
        with open(self.engine_ini_path, 'w') as f:
            config.write(f)

    def apply_custom_settings(self, custom_settings: dict[str, dict[str, Any]]) -> None:
        """Apply custom settings to existing Engine.ini."""
        config = configparser.ConfigParser()
        config.optionxform = str

        # Read existing config if it exists
        if self.engine_ini_path.exists():
            config.read(self.engine_ini_path)

        # Apply custom settings
        for section, settings in custom_settings.items():
            if section not in config:
                config[section] = {}
            for key, value in settings.items():
                config[section][key] = str(value)

        # Write updated config
        with open(self.engine_ini_path, 'w') as f:
            config.write(f)

    def set_read_only(self, read_only: bool = True) -> None:
        """Set Engine.ini as read-only to prevent game from overwriting."""
        if self.engine_ini_path.exists():
            current_stat = self.engine_ini_path.stat()
            if read_only:
                # Remove write permissions
                self.engine_ini_path.chmod(current_stat.st_mode & ~0o200)
            else:
                # Add write permissions
                self.engine_ini_path.chmod(current_stat.st_mode | 0o200)

    def read_config(self) -> configparser.ConfigParser:
        """Read and return current Engine.ini configuration."""
        config = configparser.ConfigParser()
        config.optionxform = str
        if self.engine_ini_path.exists():
            config.read(self.engine_ini_path)
        return config

    def show_current_config(self) -> None:
        """Display current Engine.ini configuration."""
        if not self.engine_ini_path.exists():
            print("Engine.ini does not exist")
            return

        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(self.engine_ini_path)

        print(f"Current Engine.ini configuration ({self.engine_ini_path}):")
        print("=" * 60)

        for section in config.sections():
            print(f"\n[{section}]")
            for key, value in config[section].items():
                print(f"{key}={value}")

