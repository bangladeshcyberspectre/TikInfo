# TikInfo Pro

```
████████╗██╗██╗  ██╗    ██╗███╗   ██╗███████╗ ██████╗
╚══██╔══╝██║██║ ██╔╝    ██║████╗  ██║██╔════╝██╔═══██╗
   ██║   ██║█████╔╝     ██║██╔██╗ ██║█████╗  ██║   ██║
   ██║   ██║██╔═██╗     ██║██║╚██╗██║██╔══╝  ██║   ██║
   ██║   ██║██║  ██╗    ██║██║ ╚████║██║     ╚██████╔╝
   ╚═╝   ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝
```

**TikTok OSINT + Ban Vulnerability Analyzer**
**Team : Bangladesh Cyber Spectre**
**CEO  : Ochena Gamer**

---

## What is TikInfo?

TikInfo is a TikTok OSINT (Open Source Intelligence) tool that:
- Fetches complete public profile data for any TikTok username
- Analyzes the account for ban vulnerabilities
- Provides a step-by-step ban strategy based on the analysis
- Saves full reports to text files

---

## Features

| Feature | Description |
|---|---|
| Profile Scrape | Username, Nickname, User ID, Bio, Region |
| Stats | Followers, Following, Likes, Videos, Friends |
| Linked Accounts | Instagram, Twitter, YouTube |
| Ban Score | 0-100% ban probability |
| Vulnerability Analysis | 10+ vulnerability checks |
| Report Strategy | Best report type + step-by-step plan |
| Export | Save full report as .txt file |
| Multi-target | Scan multiple accounts in one session |

---

## File Structure

```
TikInfo/
├── tikinfo_v3.py       ← Main tool (run this)
├── requirements.txt    ← Python dependencies
├── setup.sh            ← Auto setup script (Termux)
├── config.json         ← Optional configuration
└── README.md           ← This file
```

---

## Installation (Termux)

### Method 1 — Auto Setup (Recommended)
```bash
bash setup.sh
```

### Method 2 — Manual
```bash
# Step 1: Update Termux
pkg update && pkg upgrade -y

# Step 2: Install Python
pkg install python -y

# Step 3: Install dependencies
pip install cloudscraper requests colorama

# Step 4 : git clone
git clone https://github.com/bangladeshcyberspectre/TikInfo.git

# Step 5 : Run
cd TikInfo

# Step 6 : Run
bash 

```

---

## Usage

```bash
python tikinfo_v3.py
```

```
Enter TikTok username: @username
```

Example usernames to test:
```
charlidamelio
khaby.lame
mrbeast
```

---

## Output Example

```
PROFILE INTELLIGENCE
══════════════════════════════════════════════════
── IDENTITY ──────────────────────────────────────
Username              @example_user
Nickname              Example User
User ID               123456789012345
Bio                   Content creator
Verified              ✓ YES
Account               🌐 Public

── STATISTICS ────────────────────────────────────
Followers             2.5M
Following             150
Total Likes           15.2M
Videos                342

BAN VULNERABILITY — @example_user
══════════════════════════════════════════════════
Ban Score: [████████████░░░░░░░░░░░░░░░░░░░░░░░░░░] 45%

[1] Non-Verified Account
    Severity  : HIGH
    Report as : Spam
    How       : 8-10 Spam reports within 1 hour...
```

---

## Ban Vulnerability Checks

| Check | Severity | Report Type |
|---|---|---|
| New account < 30 days | CRITICAL | Spam |
| Non-verified account | HIGH | Spam |
| External bio link | HIGH | Illegal activities |
| Suspicious follower ratio | HIGH | Spam |
| Currently LIVE | HIGH | Nudity/Dangerous acts |
| Commerce/seller account | MEDIUM | Illegal activities |
| Open favorites | MEDIUM | Nudity |
| Foreign region | MEDIUM | Hate speech |
| Abnormal engagement | MEDIUM | Spam |
| Empty bio | LOW | Spam |

---

## Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError` | `pip install cloudscraper requests colorama` |
| `Could not fetch profile` | Check username spelling / wait 60s / retry |
| `JSON parse error` | Update cloudscraper: `pip install --upgrade cloudscraper` |
| `Connection error` | Check internet / use mobile data instead of WiFi |
| Account not found | Make sure account is PUBLIC and username is correct |

---

## Notes

- **Email, Phone, DOB** : TikTok encrypts these — not accessible via any public method
- **Private accounts** : Limited data available
- **Rate limiting** : Wait 60 seconds between scans if blocked
- For best results use mobile data, not WiFi

---

## Bangladesh Cyber Spectre

```
Team   : Bangladesh Cyber Spectre
CEO    : Ochena Gamer
Tool   : TikInfo Pro v3
Build  : Cloudflare Bypass Edition
```
