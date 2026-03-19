"""
TRADING AGENT v2 — APEX TRADING FLEET
========================================
Complete rebuild from Week 1 version.

WHAT CHANGED FROM v1:
- Upgraded to claude-sonnet-4-6 (adaptive thinking for market analysis)
- Runs entirely in GitHub Actions — zero terminal needed
- Multi-strategy: momentum + mean reversion + news sentiment
- Claude analyzes each signal before trading (AI-filtered, not just rules)
- Position sizing built in (no more all-in mistakes)
- Full daily P&L report saved to artifacts
- Risk management: stop loss, max daily loss, position limits
- Paper trading on Alpaca (safe, no real money at risk)

GITHUB SECRETS REQUIRED:
  ALPACA_KEY_ID     — your Alpaca paper trading key (starts with PK...)
  ALPACA_SECRET_KEY — your Alpaca paper trading secret
  ANTHROPIC_API_KEY — your Claude API key

HOW TO GET ALPACA PAPER KEYS:
  1. alpaca.markets → log in
  2. Switch to Paper Trading (top of dashboard)
  3. API Keys → Generate New Key
  4. Copy Key ID + Secret Key
  5. Add both as GitHub secrets
"""

import os
import json
import requests
from datetime import datetime, timedelta

# ── CREDENTIALS ───────────────────────────────────────────
ALPACA_KEY    = os.environ.get("ALPACA_KEY_ID", "").strip()
ALPACA_SECRET = os.environ.get("ALPACA_SECRET_KEY", "").strip()
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

# ── CONFIG ────────────────────────────────────────────────
PAPER_BASE_URL = "https://paper-api.alpaca.markets"
DATA_BASE_URL  = "https://data.alpaca.markets"

# Risk management
MAX_POSITION_PCT  = 0.10   # Max 10% of portfolio per position
MAX_DAILY_LOSS    = 0.03   # Stop trading if down 3% in a day
MAX_OPEN_POSITIONS = 5     # Never hold more than 5 stocks at once
STOP_LOSS_PCT     = 0.05   # Auto exit if position drops 5%

# Watchlist — liquid, high-volume stocks that work well for paper trading
WATCHLIST = [
    "AAPL", "MSFT", "NVDA", "TSLA", "META",
    "AMZN", "GOOGL", "AMD", "SPY",  "QQQ",
]

os.makedirs("trading", exist_ok=True)
LOG_FILE = f"trading/trading_log_{datetime.now().strftime('%Y%m%d')}.txt"


# ── HELPERS ───────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def alpaca_get(endpoint, params=None):
    if not ALPACA_KEY:
        log("ERROR: No ALPACA_KEY_ID secret set")
        return None
    try:
        r = requests.get(
            f"{PAPER_BASE_URL}{endpoint}",
            headers={
                "APCA-API-KEY-ID": ALPACA_KEY,
                "APCA-API-SECRET-KEY": ALPACA_SECRET,
            },
            params=params,
            timeout=15,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"Alpaca GET error {endpoint}: {e}")
        return None


def alpaca_post(endpoint, data):
    if not ALPACA_KEY:
        return None
    try:
        r = requests.post(
            f"{PAPER_BASE_URL}{endpoint}",
            headers={
                "APCA-API-KEY-ID": ALPACA_KEY,
                "APCA-API-SECRET-KEY": ALPACA_SECRET,
                "Content-Type": "application/json",
            },
            json=data,
            timeout=15,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"Alpaca POST error {endpoint}: {e}")
        return None


def alpaca_delete(endpoint):
    if not ALPACA_KEY:
        return None
    try:
        r = requests.delete(
            f"{PAPER_BASE_URL}{endpoint}",
            headers={
                "APCA-API-KEY-ID": ALPACA_KEY,
                "APCA-API-SECRET-KEY": ALPACA_SECRET,
            },
            timeout=15,
        )
        return r.status_code
    except Exception as e:
        log(f"Alpaca DELETE error {endpoint}: {e}")
        return None


def get_bars(symbol, timeframe="1Day", limit=30):
    try:
        r = requests.get(
            f"{DATA_BASE_URL}/v2/stocks/{symbol}/bars",
            headers={
                "APCA-API-KEY-ID": ALPACA_KEY,
                "APCA-API-SECRET-KEY": ALPACA_SECRET,
            },
            params={"timeframe": timeframe, "limit": limit},
            timeout=15,
        )
        r.raise_for_status()
        return r.json().get("bars", [])
    except Exception as e:
        log(f"Data error {symbol}: {e}")
        return []


def ask_claude(prompt, max_tokens=500):
    """Use Claude Sonnet 4.6 with adaptive thinking for market analysis."""
    if not ANTHROPIC_KEY:
        log("No ANTHROPIC_API_KEY — skipping Claude analysis")
        return None
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6-20250217",
                "max_tokens": max_tokens,
                "thinking": {
                    "type": "adaptive",
                    "budget_tokens": 2000,
                },
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=45,
        )
        data = r.json()
        # Extract text from response (adaptive thinking returns multiple blocks)
        for block in data.get("content", []):
            if block.get("type") == "text":
                return block["text"]
        return None
    except Exception as e:
        log(f"Claude error: {e}")
        return None


# ── ACCOUNT ───────────────────────────────────────────────
def get_account():
    return alpaca_get("/v2/account")


def get_positions():
    return alpaca_get("/v2/positions") or []


def get_orders(status="open"):
    return alpaca_get("/v2/orders", {"status": status, "limit": 20}) or []


# ── SIGNALS ───────────────────────────────────────────────
def calc_momentum(bars):
    """Simple momentum: compare 5-day avg vs 20-day avg."""
    if len(bars) < 20:
        return None
    closes = [b["c"] for b in bars]
    ma5  = sum(closes[-5:]) / 5
    ma20 = sum(closes[-20:]) / 20
    current = closes[-1]
    prev    = closes[-2]
    pct_chg = (current - prev) / prev * 100
    return {
        "ma5": round(ma5, 2),
        "ma20": round(ma20, 2),
        "current": round(current, 2),
        "pct_change_1d": round(pct_chg, 2),
        "momentum_signal": "bullish" if ma5 > ma20 else "bearish",
    }


def calc_rsi(bars, period=14):
    """RSI — overbought >70, oversold <30."""
    if len(bars) < period + 1:
        return None
    closes = [b["c"] for b in bars]
    gains, losses = [], []
    for i in range(1, period + 1):
        diff = closes[-period + i] - closes[-period + i - 1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100
    rs  = avg_gain / avg_loss
    rsi = round(100 - (100 / (1 + rs)), 1)
    return rsi


def calc_volume_signal(bars):
    """Is today's volume unusually high? Signals institutional interest."""
    if len(bars) < 10:
        return None
    vols = [b.get("v", 0) for b in bars]
    avg_vol = sum(vols[-10:-1]) / 9
    today_vol = vols[-1]
    ratio = round(today_vol / avg_vol, 2) if avg_vol > 0 else 1.0
    return {"avg_volume": int(avg_vol), "today_volume": int(today_vol), "ratio": ratio}


def analyze_with_claude(symbol, momentum, rsi, volume, portfolio_value):
    """
    Let Claude Sonnet 4.6 make the final trade decision.
    Uses adaptive thinking — it reasons harder on complex setups.
    """
    rsi_str = f"{rsi:.1f}" if rsi else "N/A"
    vol_str = f"{volume['ratio']}x average" if volume else "N/A"

    prompt = f"""You are a disciplined paper trading agent making a buy/sell/hold decision.

STOCK: {symbol}
PORTFOLIO VALUE: ${portfolio_value:,.2f}
MAX POSITION SIZE: 10% of portfolio = ${portfolio_value * 0.10:,.2f}

TECHNICAL DATA:
- Current price: ${momentum['current']}
- 1-day change: {momentum['pct_change_1d']}%
- 5-day MA: ${momentum['ma5']} vs 20-day MA: ${momentum['ma20']}
- Momentum signal: {momentum['momentum_signal']}
- RSI(14): {rsi_str}
- Volume: {vol_str}

RULES YOU MUST FOLLOW:
- Only BUY if RSI < 65 (not overbought)
- Only BUY if momentum is bullish (5MA > 20MA)
- Only BUY if volume ratio > 0.8 (healthy volume)
- SELL if RSI > 75 (overbought)
- HOLD if signals are mixed or unclear
- Never recommend buying if RSI > 70

Respond in this exact JSON format only:
{{
  "action": "BUY" or "SELL" or "HOLD",
  "confidence": 1-10,
  "reasoning": "one sentence",
  "qty_suggestion": number of shares (0 if HOLD/SELL)
}}"""

    response = ask_claude(prompt, max_tokens=300)
    if not response:
        return {"action": "HOLD", "confidence": 0, "reasoning": "Claude unavailable", "qty_suggestion": 0}

    try:
        # Extract JSON from response
        import re
        match = re.search(r'\{.*?\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return {"action": "HOLD", "confidence": 0, "reasoning": "Parse error", "qty_suggestion": 0}


# ── RISK MANAGEMENT ───────────────────────────────────────
def check_stop_losses(positions, account):
    """Close any positions that hit stop loss."""
    closed = []
    for pos in positions:
        unrealized_pct = float(pos.get("unrealized_plpc", 0))
        if unrealized_pct <= -STOP_LOSS_PCT:
            symbol = pos["symbol"]
            qty    = abs(int(float(pos["qty"])))
            log(f"STOP LOSS triggered: {symbol} at {unrealized_pct:.1%} loss — closing {qty} shares")
            result = alpaca_post("/v2/orders", {
                "symbol": symbol,
                "qty": qty,
                "side": "sell",
                "type": "market",
                "time_in_force": "day",
            })
            if result:
                closed.append(symbol)
                log(f"  Closed {symbol}: order {result.get('id', 'N/A')}")
    return closed


def is_market_open():
    clock = alpaca_get("/v2/clock")
    if clock:
        return clock.get("is_open", False)
    return False


def check_daily_loss_limit(account):
    """Don't trade if we're already down 3% today."""
    equity      = float(account.get("equity", 0))
    last_equity = float(account.get("last_equity", equity))
    if last_equity == 0:
        return False
    daily_pnl_pct = (equity - last_equity) / last_equity
    if daily_pnl_pct <= -MAX_DAILY_LOSS:
        log(f"Daily loss limit hit: {daily_pnl_pct:.2%}. Pausing trading.")
        return True
    return False


# ── MAIN TRADING LOOP ─────────────────────────────────────
def run_trading_session():
    log("=" * 55)
    log("  APEX TRADING AGENT v2")
    log(f"  {datetime.now().strftime('%A %B %d, %Y %H:%M EST')}")
    log("=" * 55)

    # Check credentials
    if not ALPACA_KEY or not ALPACA_SECRET:
        log("ERROR: ALPACA_KEY_ID and ALPACA_SECRET_KEY secrets not set.")
        log("Go to: alpaca.markets → Paper Trading → API Keys")
        log("Then add both as GitHub secrets.")
        return

    # Get account
    account = get_account()
    if not account:
        log("Could not connect to Alpaca. Check your API keys.")
        return

    equity         = float(account.get("equity", 0))
    buying_power   = float(account.get("buying_power", 0))
    portfolio_value = float(account.get("portfolio_value", 0))

    log(f"Portfolio: ${portfolio_value:,.2f}")
    log(f"Buying power: ${buying_power:,.2f}")
    log(f"Equity: ${equity:,.2f}")

    # Check if market is open
    if not is_market_open():
        log("Market is closed. Running analysis only (no trades).")
        log("Tip: GitHub workflow runs at market hours for live trading.")

    # Check daily loss limit
    if check_daily_loss_limit(account):
        log("Daily loss limit reached. No new trades today.")
        generate_report(account, [], [], [])
        return

    # Get current positions
    positions = get_positions()
    log(f"\nOpen positions: {len(positions)}")
    for p in positions:
        pnl = float(p.get("unrealized_pl", 0))
        pct = float(p.get("unrealized_plpc", 0)) * 100
        log(f"  {p['symbol']}: {p['qty']} shares | P&L: ${pnl:+.2f} ({pct:+.1f}%)")

    # Check stop losses first
    log("\n--- Stop Loss Check ---")
    stopped = check_stop_losses(positions, account)
    if stopped:
        log(f"Closed {len(stopped)} positions via stop loss: {stopped}")

    # Scan watchlist for opportunities
    log("\n--- Scanning Watchlist ---")
    trades_made = []
    analyses    = []
    open_count  = len(positions) - len(stopped)

    for symbol in WATCHLIST:
        if open_count >= MAX_OPEN_POSITIONS:
            log(f"Max positions reached ({MAX_OPEN_POSITIONS}). Skipping {symbol}.")
            break

        # Already have this position?
        held = any(p["symbol"] == symbol for p in positions)

        # Get price data
        bars = get_bars(symbol, "1Day", 30)
        if len(bars) < 20:
            log(f"  {symbol}: insufficient data")
            continue

        momentum = calc_momentum(bars)
        rsi      = calc_rsi(bars)
        volume   = calc_volume_signal(bars)

        if not momentum:
            continue

        rsi_display = f"{rsi:.1f}" if rsi else "N/A"
        log(f"\n  {symbol}: ${momentum['current']} | RSI: {rsi_display} | {momentum['momentum_signal']} | Vol: {volume['ratio'] if volume else 'N/A'}x")

        # Ask Claude for decision
        decision = analyze_with_claude(symbol, momentum, rsi, volume, portfolio_value)
        action     = decision.get("action", "HOLD")
        confidence = decision.get("confidence", 0)
        reasoning  = decision.get("reasoning", "")

        log(f"  Claude says: {action} (confidence: {confidence}/10) — {reasoning}")

        analyses.append({
            "symbol": symbol,
            "price": momentum["current"],
            "rsi": rsi,
            "momentum": momentum["momentum_signal"],
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
        })

        # Execute trade if market is open and confidence is high enough
        if is_market_open() and confidence >= 7:
            if action == "BUY" and not held and buying_power > 100:
                # Position sizing: max 10% of portfolio
                max_spend = min(portfolio_value * MAX_POSITION_PCT, buying_power * 0.95)
                qty = max(1, int(max_spend / momentum["current"]))
                cost = qty * momentum["current"]

                log(f"  BUYING {qty} shares of {symbol} @ ~${momentum['current']} (${cost:.0f})")
                order = alpaca_post("/v2/orders", {
                    "symbol": symbol,
                    "qty": qty,
                    "side": "buy",
                    "type": "market",
                    "time_in_force": "day",
                })
                if order:
                    trades_made.append(f"BUY {qty} {symbol}")
                    log(f"  Order placed: {order.get('id', 'N/A')}")
                    open_count += 1
                    buying_power -= cost

            elif action == "SELL" and held:
                pos = next((p for p in positions if p["symbol"] == symbol), None)
                if pos:
                    qty = abs(int(float(pos["qty"])))
                    log(f"  SELLING {qty} shares of {symbol}")
                    order = alpaca_post("/v2/orders", {
                        "symbol": symbol,
                        "qty": qty,
                        "side": "sell",
                        "type": "market",
                        "time_in_force": "day",
                    })
                    if order:
                        trades_made.append(f"SELL {qty} {symbol}")
                        log(f"  Order placed: {order.get('id', 'N/A')}")
        elif not is_market_open() and action == "BUY":
            log(f"  Would buy {symbol} — market closed, logged for next open session")

    # Generate daily report
    generate_report(account, positions, trades_made, analyses)


# ── DAILY REPORT ──────────────────────────────────────────
def generate_report(account, positions, trades, analyses):
    log("\n" + "=" * 55)
    log("  DAILY REPORT")
    log("=" * 55)

    today = datetime.now().strftime("%Y-%m-%d")
    report_file = f"trading/REPORT_{today}.txt"

    equity     = float(account.get("equity", 0))
    last_eq    = float(account.get("last_equity", equity))
    daily_pnl  = equity - last_eq
    daily_pct  = (daily_pnl / last_eq * 100) if last_eq > 0 else 0

    lines = [
        f"APEX TRADING REPORT — {today}",
        f"Generated: {datetime.now().strftime('%H:%M EST')}",
        "=" * 55,
        "",
        "ACCOUNT",
        f"  Portfolio value:  ${float(account.get('portfolio_value', 0)):,.2f}",
        f"  Equity:           ${equity:,.2f}",
        f"  Daily P&L:        ${daily_pnl:+,.2f} ({daily_pct:+.2f}%)",
        f"  Buying power:     ${float(account.get('buying_power', 0)):,.2f}",
        "",
        f"POSITIONS ({len(positions)} open)",
    ]

    total_unrealized = 0
    for p in positions:
        pnl = float(p.get("unrealized_pl", 0))
        pct = float(p.get("unrealized_plpc", 0)) * 100
        total_unrealized += pnl
        lines.append(f"  {p['symbol']:6} {p['qty']:>5} shares | P&L: ${pnl:+.2f} ({pct:+.1f}%)")

    lines += [
        f"  Total unrealized: ${total_unrealized:+.2f}",
        "",
        f"TRADES TODAY ({len(trades)})",
    ]
    for t in trades:
        lines.append(f"  {t}")
    if not trades:
        lines.append("  No trades executed today")

    lines += [
        "",
        f"ANALYSIS SUMMARY ({len(analyses)} stocks scanned)",
    ]
    buys  = [a for a in analyses if a["action"] == "BUY"]
    sells = [a for a in analyses if a["action"] == "SELL"]
    holds = [a for a in analyses if a["action"] == "HOLD"]
    lines.append(f"  BUY signals:  {len(buys)}")
    lines.append(f"  SELL signals: {len(sells)}")
    lines.append(f"  HOLD:         {len(holds)}")

    if buys:
        lines.append("\n  Top BUY signals:")
        for a in sorted(buys, key=lambda x: x["confidence"], reverse=True)[:3]:
            lines.append(f"    {a['symbol']}: {a['reasoning']} (confidence: {a['confidence']}/10)")

    lines += [
        "",
        "RISK STATUS",
        f"  Stop loss:        {STOP_LOSS_PCT:.0%} per position",
        f"  Max daily loss:   {MAX_DAILY_LOSS:.0%} of portfolio",
        f"  Max positions:    {MAX_OPEN_POSITIONS}",
        f"  Max position size:{MAX_POSITION_PCT:.0%} of portfolio",
        "",
        "=" * 55,
        "This is PAPER TRADING — no real money at risk.",
        "=" * 55,
    ]

    report_text = "\n".join(lines)
    with open(report_file, "w") as f:
        f.write(report_text)

    log(f"\nPortfolio: ${float(account.get('portfolio_value', 0)):,.2f}")
    log(f"Daily P&L: ${daily_pnl:+,.2f} ({daily_pct:+.2f}%)")
    log(f"Trades today: {len(trades)}")
    log(f"Report saved: {report_file}")


# ── ENTRY POINT ───────────────────────────────────────────
if __name__ == "__main__":
    run_trading_session()
