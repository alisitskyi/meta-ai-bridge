# Claude Code Guide for Meta (Facebook & Instagram) Ads

You have access to a global command-line utility `fbads` (or `meta-ads`) to query Meta Ads performance, campaigns, ad sets, and creative breakdowns.

## Quick Reference
- **List accessible ad accounts:**
  ```bash
  fbads accounts [--profile work]
  ```
- **Campaigns overview (Spend, Clicks, CTR, CPC, Leads, Purchases):**
  ```bash
  fbads campaigns [--account-id act_XXXXX] [--days 30] [--profile work]
  ```
- **Ad Sets breakdown:**
  ```bash
  fbads adsets [--account-id act_XXXXX] [--days 14]
  ```
- **Ads / Creative performance:**
  ```bash
  fbads ads [--account-id act_XXXXX] [--days 30]
  ```
- **Breakdown reports (Placements / Country / Age & Gender):**
  ```bash
  # See performance across Instagram Reels vs Stories vs Feed:
  fbads breakdowns --by placement [--days 30]
  # By country:
  fbads breakdowns --by country
  # By demographics:
  fbads breakdowns --by age_gender
  ```
