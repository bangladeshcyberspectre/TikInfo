#!/bin/bash
# ╔══════════════════════════════════════════╗
# ║  TikInfo Pro — Auto Setup               ║
# ║  Bangladesh Cyber Spectre               ║
# ║  CEO: Ochena Gamer                      ║
# ╚══════════════════════════════════════════╝

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo ""
echo -e "${RED}████████╗██╗██╗  ██╗    ██╗███╗   ██╗███████╗ ██████╗${NC}"
echo -e "${YELLOW}   ██║   ██║█████╔╝     ██║██╔██╗ ██║█████╗  ██║   ██║${NC}"
echo -e "${RED}   ╚═╝   ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝${NC}"
echo ""
echo -e "${CYAN}  Bangladesh Cyber Spectre — CEO: Ochena Gamer${NC}"
echo -e "${CYAN}  Auto Setup Script${NC}"
echo ""

# Step 1: Update
echo -e "${YELLOW}[1/4] Updating packages...${NC}"
pkg update -y 2>/dev/null && pkg upgrade -y 2>/dev/null
echo -e "${GREEN}[✓] Done${NC}"

# Step 2: Python
echo -e "${YELLOW}[2/4] Installing Python...${NC}"
pkg install python -y 2>/dev/null
python --version 2>/dev/null && echo -e "${GREEN}[✓] Python ready${NC}" || {
    echo -e "${RED}[✗] Python install failed${NC}"
    exit 1
}

# Step 3: pip dependencies
echo -e "${YELLOW}[3/4] Installing Python packages...${NC}"
pip install --upgrade pip 2>/dev/null
pip install cloudscraper requests colorama 2>/dev/null
echo -e "${GREEN}[✓] Packages installed${NC}"

# Step 4: Verify
echo -e "${YELLOW}[4/4] Verifying installation...${NC}"
python -c "import cloudscraper, requests, colorama; print('[✓] All OK')" 2>/dev/null || {
    echo -e "${RED}[✗] Verification failed${NC}"
    echo -e "${YELLOW}Try manually: pip install cloudscraper requests colorama${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Setup Complete! Ready to run.      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Run with:${NC}"
echo -e "${WHITE}  python tikinfo_v3.py${NC}"
echo ""
