#!/usr/bin/env python

"""
Clair Obscur: Expedition 33 - Configuration

Main orchestration layer for the terminal user interface / command line tool.
"""

import argparse
import sys
from core.backend import ClairObscurConfig
from core.frontend import ClairConfigTUI
from pathlib import Path


def main():
    """Main CLI interface with TUI and CLI modes."""
    parser = argparse.ArgumentParser(description="Clair Obscur: Expedition 33 Configuration Tool")

    parser.add_argument(
        "--config-path", type=Path, help="Custom path to config directory (default: auto-detected based on game version)"
    )

    parser.add_argument("--game-version", choices=["steam", "gamepass"], default="steam", help="Game version (steam or gamepass)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create new Engine.ini")
    create_parser.add_argument(
        "--preset",
        choices=["low", "balanced", "ultra", "sharp_clear", "soft_ambient"],
        default="balanced",
        help="Performance preset to apply",
    )
    create_parser.add_argument("--no-tweaks", action="store_true", help="Don't include additional engine tweaks")
    create_parser.add_argument("--read-only", action="store_true", help="Set Engine.ini as read-only after creation")

    # Show command
    subparsers.add_parser("show", help="Show current Engine.ini configuration")

    # Backup command
    subparsers.add_parser("backup", help="Create backup of current Engine.ini")

    # Custom command
    custom_parser = subparsers.add_parser("custom", help="Apply custom settings")
    custom_parser.add_argument("--section", required=True, help="Config section name")
    custom_parser.add_argument(
        "--setting",
        action="append",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Custom setting key-value pair (can be used multiple times)",
    )

    # Read-only command
    readonly_parser = subparsers.add_parser("readonly", help="Set read-only status")
    readonly_parser.add_argument("status", choices=["on", "off"], help="Enable or disable read-only mode")

    args = parser.parse_args()

    try:
        # If no command is specified, launch TUI
        if not args.command:
            app = ClairConfigTUI(config_path=args.config_path, game_version=args.game_version)
            app.run()
        else:
            # CLI mode - execute command directly
            config_manager = ClairObscurConfig(config_path=args.config_path, game_version=args.game_version)

            if args.command == "create":
                backup_path = config_manager.backup_existing_config()
                if backup_path:
                    print(f"Backup created: {backup_path}")

                config_manager.create_engine_ini(preset=args.preset, include_tweaks=not args.no_tweaks)
                print(f"Engine.ini created: {config_manager.engine_ini_path}")
                print(f"Applied preset: {args.preset}")

                if args.read_only:
                    config_manager.set_read_only(True)
                    print("Engine.ini set to read-only")

            elif args.command == "show":
                config_manager.show_current_config()

            elif args.command == "backup":
                backup_path = config_manager.backup_existing_config()
                if backup_path:
                    print(f"Backup created: {backup_path}")
                else:
                    print("No Engine.ini found to backup")

            elif args.command == "custom":
                if not args.setting:
                    print("Error: --setting is required for custom command")
                    return

                custom_settings = {args.section: dict(args.setting)}
                config_manager.apply_custom_settings(custom_settings)
                print(f"Custom settings applied to: {config_manager.engine_ini_path}")

            elif args.command == "readonly":
                config_manager.set_read_only(args.status == "on")
                if args.status == "on":
                    print("Engine.ini set to read-only")
                else:
                    print("Engine.ini write permissions restored")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
