#!/usr/bin/env python3
"""
Global Meta (Facebook & Instagram) Ads CLI Tool (fbads / meta-ads)
Enables any AI assistant or developer in VS Code across all projects to:
- Configure once globally with multiple account profiles (--profile)
- Pull ad account metrics, campaigns, adsets, and ads
- Evaluate ROAS, CPA, conversions, and creative performance
- Run breakdown reports (by placement: Reels/Stories/Feed, country, age/gender)
- Output in formatted tables, CSV, or JSON for AI processing
"""

import os
import re
import sys
import csv
import json
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

META_DIR = Path.home() / '.meta_ads'
GRAPH_API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def find_config_file(profile: str = "default") -> Path:
    """Find config file for specific profile."""
    META_DIR.mkdir(parents=True, exist_ok=True)
    if profile and profile != "default":
        return META_DIR / f"config_{profile}.json"
    return META_DIR / "config.json"


def load_config(profile: str = "default") -> Dict[str, Any]:
    """Load configuration (access token, ad account id, etc.)."""
    cfg_file = find_config_file(profile)
    if cfg_file.exists():
        try:
            with open(cfg_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    if profile != "default":
        def_cfg = META_DIR / "config.json"
        if def_cfg.exists():
            try:
                with open(def_cfg, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
    return {}


def save_config(data: Dict[str, Any], profile: str = "default"):
    """Save configuration."""
    META_DIR.mkdir(parents=True, exist_ok=True)
    cfg_file = find_config_file(profile)
    with open(cfg_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def clean_act_id(act_id: str) -> str:
    """Ensure account ID has 'act_' prefix."""
    if not act_id:
        return ""
    act_id = str(act_id).strip()
    if act_id.startswith("act_"):
        return act_id
    # remove any non-digits
    digits = re.sub(r'[^0-9]', '', act_id)
    return f"act_{digits}"


def get_token(profile: str = "default") -> str:
    """Get access token from config or environment variable."""
    cfg = load_config(profile)
    token = cfg.get("access_token") or os.environ.get("META_ACCESS_TOKEN")
    if not token:
        print("[ERROR] Meta Access Token is required.", file=sys.stderr)
        print("Set it using: meta config --access-token <TOKEN>", file=sys.stderr)
        sys.exit(1)
    return token.strip()


def api_get(endpoint: str, params: Dict[str, Any] = None, profile: str = "default") -> Dict[str, Any]:
    """Execute a GET request to Meta Graph API."""
    token = get_token(profile)
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    p = params.copy() if params else {}
    p["access_token"] = token

    resp = requests.get(url, params=p)
    if resp.status_code != 200:
        print(f"[!] Meta API Error ({resp.status_code}):", file=sys.stderr)
        try:
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False), file=sys.stderr)
        except Exception:
            print(resp.text, file=sys.stderr)
        sys.exit(1)

    return resp.json()


def parse_action_val(actions: List[Dict[str, Any]], action_type: str) -> str:
    """Extract action value (e.g. purchase, lead)."""
    if not actions:
        return "0"
    for a in actions:
        if a.get("action_type") == action_type:
            return str(a.get("value", 0))
    return "0"


def print_table(headers: List[str], rows: List[List[str]], out_json: bool = False, out_csv: bool = False):
    """Format and print tabular data to stdout."""
    if out_json:
        result = [dict(zip(headers, row)) for row in rows]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if out_csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        return

    if not rows:
        print("[!] No data returned for this query.", file=sys.stderr)
        return

    widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            widths[idx] = max(widths[idx], len(str(val)))

    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join("-" * widths[i] for i in range(len(headers)))
    print(header_line)
    print(separator)
    for row in rows:
        print(" | ".join(str(val).ljust(widths[i]) for i, val in enumerate(row)))


# ==================== COMMANDS ====================

def cmd_config(args):
    prof = getattr(args, 'profile', 'default')
    cfg = load_config(prof)
    updated = False

    if args.access_token:
        cfg["access_token"] = args.access_token.strip()
        updated = True
    if args.account_id:
        cfg["account_id"] = clean_act_id(args.account_id)
        updated = True

    if updated:
        save_config(cfg, prof)
        print(f"[+] Meta Ads configuration updated for profile '{prof}'!")

    token_preview = cfg.get("access_token", "")
    masked_token = f"{token_preview[:8]}...{token_preview[-6:]}" if len(token_preview) > 14 else "<NOT SET>"

    print(f"=== Meta Ads Config (Profile: '{prof}') ===")
    print(f"Access Token:       {masked_token}")
    print(f"Default Account ID: {cfg.get('account_id', '<NOT SET>')}")


def cmd_status(args):
    prof = getattr(args, 'profile', 'default')
    cfg = load_config(prof)
    token = cfg.get("access_token")

    print(f"=== Meta Ads Status (Profile: '{prof}') ===")
    if not token:
        print("[-] Status: Missing access token. Run 'meta config --access-token <TOKEN>'")
        return

    try:
        user_info = api_get("me", {"fields": "id,name"}, prof)
        print(f"[+] Authenticated as: {user_info.get('name')} (ID: {user_info.get('id')})")
    except Exception as e:
        print(f"[-] Status: Error connecting to Meta API: {e}")
        return

    act_id = cfg.get("account_id")
    if act_id:
        try:
            act_info = api_get(act_id, {"fields": "name,account_status,currency,timezone_name"}, prof)
            print(f"[+] Default Ad Account: {act_info.get('name')} ({act_id})")
            print(f"    Currency: {act_info.get('currency')} | Timezone: {act_info.get('timezone_name')}")
            print(f"    Status: {'ACTIVE' if act_info.get('account_status') == 1 else 'DISABLED'}")
        except Exception:
            pass


def cmd_accounts(args):
    prof = getattr(args, 'profile', 'default')
    res = api_get("me/adaccounts", {"fields": "name,account_id,account_status,currency,amount_spent"}, prof)
    data = res.get("data", [])

    headers = ["Account Name", "Act ID", "Currency", "Spent Total", "Status"]
    rows = []
    for a in data:
        status_num = a.get("account_status", 1)
        status_str = "ACTIVE" if status_num == 1 else "DISABLED"
        spent = round(float(a.get("amount_spent", 0)) / 100, 2)
        rows.append([
            a.get("name", "Unknown"),
            f"act_{a.get('account_id')}",
            a.get("currency", ""),
            f"${spent}",
            status_str
        ])

    print_table(headers, rows, args.json, args.csv)


def get_date_preset(days: int) -> str:
    """Return valid Meta Graph API date_preset string."""
    if days in [3, 7, 14, 28, 30, 90]:
        return f"last_{days}d"
    return "last_30d"


def get_target_account(args, prof: str) -> str:
    if getattr(args, 'account_id', None):
        return clean_act_id(args.account_id)
    cfg = load_config(prof)
    act_id = cfg.get("account_id")
    if not act_id:
        print("[ERROR] Account ID is required (--account-id act_123456789 or set via 'meta config --account-id <ID>')", file=sys.stderr)
        sys.exit(1)
    return clean_act_id(act_id)


def cmd_campaigns(args):
    prof = getattr(args, 'profile', 'default')
    act_id = get_target_account(args, prof)
    days = args.days or 30

    params = {
        "level": "campaign",
        "date_preset": get_date_preset(days),
        "fields": "campaign_name,objective,spend,impressions,clicks,cpc,ctr,cpm,actions,cost_per_action_type",
        "limit": 100
    }

    res = api_get(f"{act_id}/insights", params, prof)
    data = res.get("data", [])

    headers = ["Campaign Name", "Spend", "Clicks", "Impressions", "CTR", "CPC", "Leads", "Purchases"]
    rows = []
    for r in data:
        actions = r.get("actions", [])
        leads = parse_action_val(actions, "lead")
        purchases = parse_action_val(actions, "purchase")

        rows.append([
            r.get("campaign_name", "Unknown"),
            f"${round(float(r.get('spend', 0)), 2)}",
            str(r.get("clicks", 0)),
            str(r.get("impressions", 0)),
            f"{round(float(r.get('ctr', 0)), 2)}%",
            f"${round(float(r.get('cpc', 0)), 2)}",
            leads,
            purchases
        ])

    print_table(headers, rows, args.json, args.csv)


def cmd_adsets(args):
    prof = getattr(args, 'profile', 'default')
    act_id = get_target_account(args, prof)
    days = args.days or 30

    params = {
        "level": "adset",
        "date_preset": get_date_preset(days),
        "fields": "adset_name,campaign_name,spend,impressions,clicks,cpc,ctr,actions",
        "limit": 100
    }

    res = api_get(f"{act_id}/insights", params, prof)
    data = res.get("data", [])

    headers = ["Ad Set Name", "Campaign", "Spend", "Clicks", "CTR", "CPC", "Leads", "Purchases"]
    rows = []
    for r in data:
        actions = r.get("actions", [])
        leads = parse_action_val(actions, "lead")
        purchases = parse_action_val(actions, "purchase")

        rows.append([
            r.get("adset_name", "Unknown"),
            r.get("campaign_name", "Unknown"),
            f"${round(float(r.get('spend', 0)), 2)}",
            str(r.get("clicks", 0)),
            f"{round(float(r.get('ctr', 0)), 2)}%",
            f"${round(float(r.get('cpc', 0)), 2)}",
            leads,
            purchases
        ])

    print_table(headers, rows, args.json, args.csv)


def cmd_ads(args):
    prof = getattr(args, 'profile', 'default')
    act_id = get_target_account(args, prof)
    days = args.days or 30

    params = {
        "level": "ad",
        "date_preset": get_date_preset(days),
        "fields": "ad_name,adset_name,campaign_name,spend,impressions,clicks,ctr,cpc,actions",
        "limit": args.limit or 100
    }

    res = api_get(f"{act_id}/insights", params, prof)
    data = res.get("data", [])

    headers = ["Ad / Creative Name", "Ad Set", "Spend", "Clicks", "CTR", "CPC", "Purchases"]
    rows = []
    for r in data:
        actions = r.get("actions", [])
        purchases = parse_action_val(actions, "purchase")

        rows.append([
            r.get("ad_name", "Unknown"),
            r.get("adset_name", "Unknown"),
            f"${round(float(r.get('spend', 0)), 2)}",
            str(r.get("clicks", 0)),
            f"{round(float(r.get('ctr', 0)), 2)}%",
            f"${round(float(r.get('cpc', 0)), 2)}",
            purchases
        ])

    print_table(headers, rows, args.json, args.csv)


def cmd_breakdowns(args):
    prof = getattr(args, 'profile', 'default')
    act_id = get_target_account(args, prof)
    days = args.days or 30

    breakdown_map = {
        "placement": "publisher_platform,platform_position",
        "country": "country",
        "age_gender": "age,gender"
    }
    bd_param = breakdown_map.get(args.by, args.by)

    params = {
        "date_preset": get_date_preset(days),
        "breakdowns": bd_param,
        "fields": "spend,impressions,clicks,ctr,cpc,actions",
        "limit": 100
    }

    res = api_get(f"{act_id}/insights", params, prof)
    data = res.get("data", [])

    headers = [args.by, "Spend", "Clicks", "Impressions", "CTR", "CPC"]
    rows = []
    for r in data:
        if args.by == "placement":
            label = f"{r.get('publisher_platform')} - {r.get('platform_position')}"
        elif args.by == "age_gender":
            label = f"{r.get('gender')} ({r.get('age')})"
        else:
            label = r.get(args.by, "Unknown")

        rows.append([
            label,
            f"${round(float(r.get('spend', 0)), 2)}",
            str(r.get("clicks", 0)),
            str(r.get("impressions", 0)),
            f"{round(float(r.get('ctr', 0)), 2)}%",
            f"${round(float(r.get('cpc', 0)), 2)}"
        ])

    print_table(headers, rows, args.json, args.csv)


def cmd_query(args):
    prof = getattr(args, 'profile', 'default')
    params = json.loads(args.params) if args.params else {}
    res = api_get(args.endpoint, params, prof)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(res, ensure_ascii=False))


def main():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--profile", default="default", help="Meta Ads account profile name (e.g. 'work', 'client')")

    # Use executed command name if available, default to meta
    invoked_name = Path(sys.argv[0]).stem if sys.argv and sys.argv[0] else "meta"
    if invoked_name in ("cli", "meta_tool"):
        invoked_name = "meta"

    parser = argparse.ArgumentParser(
        prog=invoked_name,
        description="Global Meta (Facebook & Instagram) Ads CLI for AI assistants and marketers.",
        parents=[common_parser]
    )
    sub = parser.add_subparsers(dest="subcommand", help="Command to run")

    # Common
    sub.add_parser("status", help="Check Meta Ads credentials & account status", parents=[common_parser])
    p_cfg = sub.add_parser("config", help="Set or view Meta Ads configuration", parents=[common_parser])
    p_cfg.add_argument("--access-token", help="Set Meta User or System User Access Token")
    p_cfg.add_argument("--account-id", help="Set default Ad Account ID (e.g. act_123456789)")

    # Accounts
    sub.add_parser("accounts", help="List all ad accounts accessible with this token", parents=[common_parser])

    # Campaigns
    p_camp = sub.add_parser("campaigns", help="List campaigns with spend, clicks, conversions", parents=[common_parser])
    p_camp.add_argument("--account-id", help="Ad Account ID (act_xxxxxxxx)")
    p_camp.add_argument("--days", type=int, default=30, help="Days back (7, 14, 30, 90)")
    p_camp.add_argument("--json", action="store_true", help="Output JSON")
    p_camp.add_argument("--csv", action="store_true", help="Output CSV")

    # Adsets
    p_as = sub.add_parser("adsets", help="List ad sets performance", parents=[common_parser])
    p_as.add_argument("--account-id", help="Ad Account ID")
    p_as.add_argument("--days", type=int, default=30, help="Days back")
    p_as.add_argument("--json", action="store_true", help="Output JSON")
    p_as.add_argument("--csv", action="store_true", help="Output CSV")

    # Ads
    p_ad = sub.add_parser("ads", help="List individual ads/creatives performance", parents=[common_parser])
    p_ad.add_argument("--account-id", help="Ad Account ID")
    p_ad.add_argument("--days", type=int, default=30, help="Days back")
    p_ad.add_argument("--limit", type=int, default=100, help="Max rows")
    p_ad.add_argument("--json", action="store_true", help="Output JSON")
    p_ad.add_argument("--csv", action="store_true", help="Output CSV")

    # Breakdowns
    p_bd = sub.add_parser("breakdowns", help="Breakdown by placement, country, age_gender", parents=[common_parser])
    p_bd.add_argument("--account-id", help="Ad Account ID")
    p_bd.add_argument("--by", choices=["placement", "country", "age_gender"], default="placement", help="Breakdown dimension")
    p_bd.add_argument("--days", type=int, default=30, help="Days back")
    p_bd.add_argument("--json", action="store_true", help="Output JSON")
    p_bd.add_argument("--csv", action="store_true", help="Output CSV")

    # Raw Query
    p_q = sub.add_parser("query", help="Execute raw Graph API GET request", parents=[common_parser])
    p_q.add_argument("--endpoint", required=True, help="Graph API endpoint (e.g. 'act_12345/campaigns')")
    p_q.add_argument("--params", help="JSON string of query parameters")
    p_q.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    try:
        if args.subcommand == "config":
            cmd_config(args)
        elif args.subcommand == "status":
            cmd_status(args)
        elif args.subcommand == "accounts":
            cmd_accounts(args)
        elif args.subcommand == "campaigns":
            cmd_campaigns(args)
        elif args.subcommand == "adsets":
            cmd_adsets(args)
        elif args.subcommand == "ads":
            cmd_ads(args)
        elif args.subcommand == "breakdowns":
            cmd_breakdowns(args)
        elif args.subcommand == "query":
            cmd_query(args)
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
