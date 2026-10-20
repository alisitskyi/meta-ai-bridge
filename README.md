# meta-ads-ai-bridge 📱

> **Universal Meta (Facebook & Instagram) Ads CLI for AI Coding Assistants**  
> Enables Claude Code, Cursor, Cline, Roo Code, and marketers to audit campaigns, analyze ROAS and CPA, inspect creative performance, and evaluate placement breakdowns (Reels, Stories, Feed) directly from any terminal.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Meta Marketing API: v21.0](https://img.shields.io/badge/Meta%20Graph%20API-v21.0-blue.svg)](https://developers.facebook.com/docs/marketing-apis)

---

## 💡 Why This Exists

Performance marketers and AI coding assistants frequently need to analyze live Meta ad spend, conversion CPA, and creative fatigue without constantly opening Ads Manager in the browser.

With `meta-ads-ai-bridge`:
- 🤖 **Empower AI Assistants:** Give your AI direct access to query live Meta campaign metrics, calculate real CAC, and compare performance against Google Ads and GA4.
- ⚡ **Lightweight & Fast:** Direct calls to Graph API v21.0 using standard requests.
- 📱 **Placement & Demographic Breakdowns:** Instantly see if your budget is performing better on Instagram Reels vs Stories vs Facebook Feed.

---

## 🚀 Quickstart

### 1. Installation

**Windows (PowerShell):**
```powershell
git clone https://github.com/<your-username>/meta-ads-ai-bridge.git
cd meta-ads-ai-bridge
.\install.ps1
```

**macOS / Linux:**
```bash
git clone https://github.com/<your-username>/meta-ads-ai-bridge.git
cd meta-ads-ai-bridge
chmod +x install.sh
./install.sh
```

---

### 2. Configure Access Token & Account ID

Get your **System User Access Token** (never expires) from Meta Business Manager $\rightarrow$ Business Settings $\rightarrow$ System Users, or from [Meta Developer App](https://developers.facebook.com/):
```powershell
# Set your token
fbads config --access-token "YOUR_META_ACCESS_TOKEN"

# (Optional) Set your default ad account ID
fbads config --account-id "act_123456789"
```

---

## 📖 CLI Usage Reference

Commands work identically using either `fbads` or `meta-ads`.

### 1. List Accessible Ad Accounts
```bash
fbads accounts
```

### 2. Campaign Performance Overview
List campaigns with spend, clicks, impressions, CTR, CPC, leads, and purchases:
```bash
fbads campaigns
fbads campaigns --days 14
fbads campaigns --days 30 --json
```

### 3. Ad Sets Breakdown
```bash
fbads adsets --days 30
```

### 4. Ads / Creative Performance (Detect Fatigue)
Evaluate individual ads by spend, CTR, and purchases:
```bash
fbads ads --days 30
```

### 5. Breakdowns (Placements, Demographics, Countries)
```bash
# Compare Instagram Reels vs Stories vs Feed:
fbads breakdowns --by placement --days 30

# Breakdown by Country:
fbads breakdowns --by country --days 30

# Breakdown by Age & Gender:
fbads breakdowns --by age_gender --days 30
```

---

## 🤖 Connecting to AI Assistants

Add to `.claude/settings.json` or `.cursorrules`:
```json
{
  "allowedTools": [
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
