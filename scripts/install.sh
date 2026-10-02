#!/usr/bin/env bash
# Install the technical-writer Claude Code plugin (global or project scope).
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [--global|--project] [--path DIR]

  --global   Symlink this plugin into ~/.claude/skills/technical-writer (default)
  --project  Symlink into ./.claude/skills/technical-writer of DIR (default: cwd)
  --path DIR Content project root when using --project
  --help     Show this help

After install, restart Claude Code (or run /reload-plugins). Prefer starting
Claude from the repo root for project installs.

Try without install:
  claude --plugin-dir /path/to/technical-writer
EOF
}

MODE="global"
PROJECT_ROOT="$(pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) MODE="global"; shift ;;
    --project) MODE="project"; shift ;;
    --path) PROJECT_ROOT="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

link_plugin() {
  local target="$1"
  mkdir -p "$(dirname "$target")"
  if [[ -e "$target" || -L "$target" ]]; then
    if [[ -L "$target" ]]; then
      rm "$target"
    else
      echo "Refusing to overwrite non-symlink: $target" >&2
      exit 1
    fi
  fi
  ln -s "$PLUGIN_ROOT" "$target"
  echo "Linked $PLUGIN_ROOT -> $target"
}

case "$MODE" in
  global)
    link_plugin "$HOME/.claude/skills/technical-writer"
    echo "Scope: user (all projects)."
    ;;
  project)
    PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
    link_plugin "$PROJECT_ROOT/.claude/skills/technical-writer"
    echo "Scope: project ($PROJECT_ROOT)."
    echo "Commit .claude/skills/technical-writer only if your team wants a shared symlink path,"
    echo "or document the clone+install steps in your content repo README."
    ;;
esac

echo
echo "Next:"
echo "  1. Restart Claude Code or /reload-plugins"
echo "  2. In a content project: /technical-writer:writer setup"
echo "  3. Add samples to .writer/samples/ then /technical-writer:writer-style build"
echo "  4. Write: /technical-writer:writer write <topic>"
echo
echo "Note: older personal /blog skills in ~/.claude/skills still work until you remove them."
