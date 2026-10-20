#!/usr/bin/env bash
# macOS / Linux Installer for meta-ai-bridge
set -e

echo "=========================================="
echo "  Installing meta-ai-bridge (Unix)        "
echo "=========================================="

PYTHON_CMD=$(which python3 || which python || true)
if [ -z "$PYTHON_CMD" ]; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    exit 1
fi
echo "[+] Found Python: $PYTHON_CMD"

echo "[*] Installing Python dependencies..."
$PYTHON_CMD -m pip install -r "$(dirname "$0")/requirements.txt" --quiet
echo "[+] Dependencies installed successfully."

META_HOME="$HOME/.meta_ads"
META_BIN="$META_HOME/bin"
mkdir -p "$META_BIN"

cp "$(dirname "$0")/src/meta_ai/cli.py" "$META_HOME/meta_tool.py"

cat << 'EOF' > "$META_BIN/meta"
#!/usr/bin/env bash
python3 "$HOME/.meta_ads/meta_tool.py" "$@"
EOF
chmod +x "$META_BIN/meta"

ln -sf "$META_BIN/meta" "$META_BIN/fbads"
ln -sf "$META_BIN/meta" "$META_BIN/meta-ads"

SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "$META_BIN" "$SHELL_RC"; then
        echo "export PATH=\"\$PATH:$META_BIN\"" >> "$SHELL_RC"
        echo "[+] Added $META_BIN to $SHELL_RC"
    fi
fi

echo ""
echo "[+] Installation complete!"
echo "1. Set access token: meta config --access-token <YOUR_TOKEN>"
echo "2. Run: meta accounts"
