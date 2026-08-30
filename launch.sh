#!/bin/bash
# Microduck WSLg & Linux Simulation Launcher
export XCURSOR_THEME=Adwaita
export XCURSOR_SIZE=24
export XCURSOR_PATH=/usr/share/icons

# Force X11 root window cursor shape in WSLg
xsetroot -cursor_name left_ptr 2>/dev/null || true

uv run python launch_viewer.py "$@"
