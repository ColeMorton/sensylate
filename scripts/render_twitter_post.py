#!/usr/bin/env python3
import json
import sys

from jinja2 import Environment, FileSystemLoader


def render_twitter_post(ticker, date):
    """Render Twitter post using Jinja2 template with DOCU data"""

    # Load data from metadata
    metadata_file = f"data/outputs/twitter/post_strategy/{ticker}_{date}_metadata.json"
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    # Set up Jinja2 environment with autoescape for security
    env = Environment(
        loader=FileSystemLoader("scripts/templates/twitter/"), autoescape=True
    )

    # Prepare context for template
    context = {
        "ticker": metadata["ticker"],
        "timestamp": metadata["timestamp"],
        "data": {
            "strategy_type": metadata["strategy_details"]["type"],
            "short_window": metadata["strategy_details"]["short_window"],
            "long_window": metadata["strategy_details"]["long_window"],
            "period": metadata["strategy_details"]["period"],
            "net_performance": metadata["performance_metrics"]["net_performance"],
            "win_rate": metadata["performance_metrics"]["win_rate"],
            "total_trades": metadata["performance_metrics"]["total_trades"],
            "avg_win": metadata["performance_metrics"]["avg_win"],
            "avg_loss": metadata["performance_metrics"]["avg_loss"],
            "reward_risk": metadata["performance_metrics"]["reward_risk_ratio"],
            "max_drawdown": metadata["performance_metrics"]["max_drawdown"],
            "buy_hold_drawdown": metadata["performance_metrics"]["buy_hold_drawdown"],
            "sharpe": metadata["performance_metrics"]["sharpe"],
            "sortino": metadata["performance_metrics"]["sortino"],
            "exposure": metadata["performance_metrics"]["exposure"],
            "avg_trade_length": metadata["performance_metrics"]["avg_trade_length"],
            "expectancy": metadata["performance_metrics"]["expectancy"],
            "current_month": metadata["seasonality"]["current_month"],
            "current_month_performance": metadata["seasonality"][
                "current_month_performance"
            ],
            "best_months": metadata["seasonality"]["best_months"],
            "worst_months": metadata["seasonality"]["worst_months"],
            "current_price": metadata["market_data"]["current_price"],
            "target_price": metadata["market_data"]["target_price"],
            "pe_ratio": metadata["market_data"]["pe_ratio"],
            "sector": metadata["market_data"]["sector"],
            "signal_triggered": metadata["live_signal"],
            "technical_setup": "SMA (52/54) crossover confirmed with momentum alignment",
            "fundamental_catalyst": "Strong profitability turnaround with $1.07B net income",
            "market_context": "analyst targets range $85-$105 (current $77.62)",
            "risk_management": "2.1 reward/risk ratio, 52.5% time in market",
            "fundamentals": "A- financial health grade, 31% FCF margin, $920M free cash flow",
            "key_insight": "exceptional operational leverage driving profitability",
            "conviction_level": "high",
            "date": metadata["date"],
        },
    }

    # Create inline template to avoid import issues
    template_content = """📈 ${{ ticker }} dual {{ data.strategy_type }} ({{ data.short_window }}/{{ data.long_window }}) delivered {{ data.net_performance }}% returns with {{ data.win_rate }}% win rate - {{ data.key_insight }}

Here's why this signal matters. 👇

✅ Strategy Performance (${{ ticker }}, dual {{ data.strategy_type }} ({{ data.short_window }}/{{ data.long_window }}) cross, {{ data.period }} years)
• Win Rate: {{ data.win_rate }}% ({{ data.total_trades }} trades)
• Net Performance: +{{ data.net_performance }}%
• Avg Win/Loss: +{{ data.avg_win }}% / -{{ data.avg_loss }}%
• Reward/Risk Ratio: {{ data.reward_risk }}
• Max Drawdown: -{{ data.max_drawdown }}% (vs B&H: -{{ data.buy_hold_drawdown }}%)
• Sharpe: {{ data.sharpe }} | Sortino: {{ data.sortino }}
• Exposure: {{ data.exposure }}% | Avg Trade: {{ data.avg_trade_length }} days
• Expectancy: ${{ data.expectancy }} per $1 risked

📅 Seasonality Edge ({{ data.period }} years)
{%- set timing_assessment = "Strong" if data.current_month_performance > 65 else "Neutral" if data.current_month_performance > 35 else "Weak" -%}
{{ data.current_month }} timing: {{ timing_assessment }} ({{ data.current_month_performance }}% positive periods)
• {{ data.best_months }}: Strong seasonal performance
• {{ data.worst_months }}: Weaker seasonal periods
• Current month ({{ data.current_month }}): {{ timing_assessment }} timing window

🔍 Why This Signal Triggered TODAY
• Entry Condition: {{ data.strategy_type }} ({{ data.short_window }}/{{ data.long_window }}) crossover signal confirmed
• Technical Setup: {{ data.technical_setup }}
• Fundamental Catalyst: {{ data.fundamental_catalyst }}
• Market Context: Current price ${{ data.current_price }} vs {{ data.market_context }}
• Risk Management: {{ data.risk_management }}

📊 ${{ ticker }} Fundamentals
{{ data.fundamentals }}

📌 Bottom Line
Strategy with {{ data.net_performance }}% historical returns just triggered entry signal. {{ timing_assessment }} seasonality + {{ data.technical_setup }} + {{ data.fundamental_catalyst }} align for {{ data.conviction_level }} opportunity.

Time to act on this live signal. 🎯

📋 Full analysis: https://www.colemorton.com/blog/{{ ticker.lower() }}-trading-strategy-{{ data.date }}/

Not financial advice. Historical performance doesn't guarantee future results. Trade at your own risk.

#TradingSignals #TradingStrategy #TradingOpportunity #investment"""

    # Create template from string
    template = env.from_string(template_content)
    rendered_content = template.render(**context)

    return rendered_content


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python render_twitter_post.py <ticker> <date>")
        sys.exit(1)

    ticker = sys.argv[1]
    date = sys.argv[2]

    try:
        content = render_twitter_post(ticker, date)
        print(content)
    except Exception as e:
        print("Error rendering Twitter post: {e}")
        sys.exit(1)
