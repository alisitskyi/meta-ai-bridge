# meta-ai-bridge 📱

> **Universal Meta (Facebook & Instagram) Ads CLI for AI Coding Assistants**  
> Enables Claude Code, Cursor, Cline, Roo Code, and marketers to audit campaigns, analyze ROAS and CPA, inspect creative performance, and evaluate placement breakdowns (Reels, Stories, Feed) directly from any terminal.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Meta Marketing API: v21.0](https://img.shields.io/badge/Meta%20Graph%20API-v21.0-blue.svg)](https://developers.facebook.com/docs/marketing-apis)

---

## 💡 Why This Exists

Performance marketers and AI coding assistants frequently need to analyze live Meta ad spend, conversion CPA, and creative fatigue without constantly opening Ads Manager in the browser.

With `meta-ai-bridge`:
- 🤖 **Empower AI Assistants:** Give your AI direct access to query live Meta campaign metrics, calculate real CAC, and compare performance against Google Ads and GA4.
- ⚡ **Lightweight & Fast:** Direct calls to Graph API v21.0 using standard requests.
- 📱 **Placement & Demographic Breakdowns:** Instantly see if your budget is performing better on Instagram Reels vs Stories vs Facebook Feed.
- 🔄 **Multiple Profiles:** Switch between personal and client ad accounts seamlessly using `--profile <name>`.

---

## 🚀 Quickstart

### 1. Installation

**Windows (PowerShell):**
```powershell
git clone https://github.com/<your-username>/meta-ai-bridge.git
cd meta-ai-bridge
.\install.ps1
```

**macOS / Linux:**
```bash
git clone https://github.com/<your-username>/meta-ai-bridge.git
cd meta-ai-bridge
chmod +x install.sh
./install.sh
```

---

### 2. Configure Access Token & Account ID

Get your **System User Access Token** (never expires) from Meta Business Manager $\rightarrow$ Business Settings $\rightarrow$ System Users, or from [Meta Developer App](https://developers.facebook.com/):
```powershell
# Set your token (default profile)
meta config --access-token "YOUR_META_ACCESS_TOKEN"

# (Optional) Set your default ad account ID
meta config --account-id "act_123456789"

# Configure a specific profile (e.g. for a client or work account)
meta config --profile work --access-token "WORK_TOKEN" --account-id "act_987654321"
```

---

## 📖 CLI Usage Reference

All commands work interchangeably with `meta`, `fbads`, or `meta-ads`.

### 1. List Accessible Ad Accounts
```bash
meta accounts
```

### 2. Campaign Performance Overview
List campaigns with spend, clicks, impressions, CTR, CPC, leads, and purchases:
```bash
meta campaigns
meta campaigns --days 14
meta campaigns --days 30 --json
meta campaigns --profile work
```

### 3. Ad Sets Breakdown
```bash
meta adsets --days 30
```

### 4. Ads / Creative Performance (Detect Fatigue)
Evaluate individual ads by spend, CTR, and purchases:
```bash
meta ads --days 30
```

### 5. Breakdowns (Placements, Demographics, Countries)
```bash
# Compare Instagram Reels vs Stories vs Feed:
meta breakdowns --by placement --days 30

# Breakdown by Country:
meta breakdowns --by country --days 30

# Breakdown by Age & Gender:
meta breakdowns --by age_gender --days 30
```

---

## 🤖 Connecting to AI Assistants

Add to `.claude/settings.json` or `.cursorrules`:
```json
{
  "allowedTools": [
    "Bash(meta *)",
    "PowerShell(meta *)",
    "Bash(fbads *)",
    "PowerShell(fbads *)",
    "Bash(meta-ads *)",
    "PowerShell(meta-ads *)"
  ]
}
```

---

## 📄 License

MIT License. Free to use and distribute. See [LICENSE](LICENSE) for details.
