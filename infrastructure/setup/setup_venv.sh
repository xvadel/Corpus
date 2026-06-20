#!/bin/bash
# =============================================================================
# Corpus — macOS & Linux Setup & Virtual Environment Initializer
# =============================================================================
# This script automates creating, activating, and installing dependencies
# into an isolated local Python virtual environment (venv) on macOS/Linux.
#
# Usage:
#   chmod +x infrastructure/setup/setup_venv.sh
#   ./infrastructure/setup/setup_venv.sh
# =============================================================================

set -e

# Colors
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0;37m' # No Color

echo -e "${CYAN}==========================================================${NC}"
echo -e "${CYAN}  Corpus — Local Development Environment Initializer${NC}"
echo -e "${CYAN}==========================================================${NC}"

# Navigate to project root (2 directories up from this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"
echo -e "Project root located at: $PROJECT_ROOT"

# 1. Check Python Version
echo -e "\n${YELLOW}[1/4] Checking Python installation...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python 3 is not installed or not in your PATH. Please install Python 3.10+.${NC}"
    exit 1
fi
echo -e "Found Python: $($PYTHON_CMD --version)"

# 2. Create Virtual Environment
echo -e "\n${YELLOW}[2/4] Initializing isolated virtual environment...${NC}"
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo -e "Virtual environment folder already exists at: $PROJECT_ROOT/venv"
else
    echo -e "Creating venv..."
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓ Virtual environment successfully created.${NC}"
fi

# 3. Upgrade pip & Install Requirements in the Virtual Environment
echo -e "\n${YELLOW}[3/4] Installing backend dependencies from requirements.txt...${NC}"
PIP_BIN="$PROJECT_ROOT/venv/bin/pip"
if [ ! -f "$PIP_BIN" ]; then
    echo -e "${RED}Error: Failed to locate pip binary inside venv. Make sure venv is configured correctly.${NC}"
    exit 1
fi

echo -e "Upgrading pip..."
"$PIP_BIN" install --upgrade pip

echo -e "Installing requirements..."
"$PIP_BIN" install -r "$PROJECT_ROOT/requirements.txt"
echo -e "${GREEN}✓ Backend dependencies successfully installed.${NC}"

# 4. Success Instructions
echo -e "\n${GREEN}[4/4] Setup completed successfully! 🎉${NC}"
echo -e "${CYAN}==========================================================${NC}"
echo -e "${CYAN}HOW TO ACTIVATE AND USE:${NC}"
echo -e "${YELLOW}1. Activate in Bash/Zsh:${NC}"
echo -e "   source venv/bin/activate"
echo -e "${YELLOW}2. Run development backend:${NC}"
echo -e "   uvicorn backend.main:app --reload"
echo -e "${YELLOW}3. To select this environment in VS Code / Cursor:${NC}"
echo -e "   - Press 'Cmd + Shift + P'"
echo -e "   - Type 'Python: Select Interpreter'"
echo -e "   - Click 'Enter interpreter path...' and select:"
echo -e "     $PROJECT_ROOT/venv/bin/python"
echo -e "${CYAN}==========================================================${NC}"
