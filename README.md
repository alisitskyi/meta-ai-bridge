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
- 🔄 **Multi-Account & Multi-Profile:** Query multiple ad accounts on the fly with `--account-id` or configure distinct profiles using `--profile <name>`.
- ⏳ **Flexible Date Ranges & Presets:** Query last 7/14/30/90 days or all-time history with `--preset maximum`.

---

## 🚀 Quickstart

### 1. Installation

**Windows (PowerShell):**
```powershell
git clone https://github.com/alisitskyi/meta-ai-bridge.git
cd meta-ai-bridge
.\install.ps1
```

**macOS / Linux:**
```bash
git clone https://github.com/alisitskyi/meta-ai-bridge.git
cd meta-ai-bridge
chmod +x install.sh
./install.sh
```

---

### 2. Configure Access Token & Account ID

#### Getting a Token:
1. **60-Day Token (Fastest):**
   - Go to [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/).
   - Select your App, click **Get Token** $\rightarrow$ **Get User Access Token**, check **`ads_read`**, and click **Generate Access Token**.
   - Open [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/), paste the token, click **Debug**, and click **Extend Access Token** at the bottom to get a 60-day token.
2. **Never-Expiring Token (System User):**
   - Meta Business Settings $\rightarrow$ Users $\rightarrow$ System Users $\rightarrow$ Add Admin $\rightarrow$ Assign Ad Accounts $\rightarrow$ Generate Token (`ads_read`, Expiration: Never).

#### Saving the Configuration:
```powershell
# Set your token and default account
meta config --access-token "YOUR_META_ACCESS_TOKEN" --account-id "1308426748018713"

# (Optional) Add named profiles for other accounts/clients:
meta config --profile helpcrunch --account-id "1740528223248437"
meta config --profile bib --account-id "708855853851186"
```

---

## 📖 CLI Usage Reference

All commands work interchangeably with `meta`, `fbads`, or `meta-ads`.

### 1. List All Accessible Ad Accounts
See every ad account, currency, total spend, and status accessible by your token:
```bash
meta accounts
```

### 2. Campaign Performance Overview
List campaigns with spend, clicks, impressions, CTR, CPC, leads, and purchases:
```bash
# Default account (last 30 days)
meta campaigns

# Specific timeframe
meta campaigns --days 7
meta campaigns --days 14

# All-time / Historical data
meta campaigns --preset maximum
meta campaigns --preset this_year

# Target another account on the fly
meta campaigns --account-id 1740528223248437
meta campaigns --profile helpcrunch
```

### 3. Ad Sets Breakdown
```bash
meta adsets --days 30
meta adsets --account-id 1740528223248437
```

### 4. Ads / Creative Performance (Detect Fatigue)
Evaluate individual creatives by spend, CTR, and conversions:
```bash
meta ads --days 30
meta ads --limit 50
```

### 5. Breakdowns (Placements, Demographics, Countries)
```bash
# Compare Instagram Reels vs Stories vs Facebook Feed:
meta breakdowns --by placement --days 7
meta breakdowns --by placement --days 30

# Breakdown by Country:
meta breakdowns --by country --days 30

# Breakdown by Age & Gender:
meta breakdowns --by age_gender --days 30
```

### 6. Raw Graph API Query
```bash
meta query --endpoint "me/adaccounts" --params '{"fields":"name,currency"}' --json
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

Prompt examples for AI assistants:
- *"Show Meta campaign spend and CTR for the last 14 days using `meta campaigns --days 14`."*
- *"Compare Instagram Reels vs Feed performance with `meta breakdowns --by placement`."*
- *"Audit creative performance for account HelpCrunch EN using `meta ads --profile helpcrunch`."*

---

## 📄 License

MIT License. Free to use and distribute. See [LICENSE](LICENSE) for details.
