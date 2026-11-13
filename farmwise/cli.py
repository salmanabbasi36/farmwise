"""Command line: ask | chat | serve | weather"""

from __future__ import annotations

import argparse

from . import weather
from .advisor import Advisor


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="farmwise", description="Maize advisory demo for smallholder farmers")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("ask", help="ask one question")
    a.add_argument("question")
    a.add_argument("--sms", action="store_true", help="short SMS-style answer")

    sub.add_parser("chat", help="interactive chat in the terminal")

    s = sub.add_parser("serve", help="start the local web chat")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8000)
    s.add_argument("--no-log", action="store_true", help="do not write queries.jsonl")

    w = sub.add_parser("weather", help="planting signal from the 7-day rain forecast (needs internet)")
    w.add_argument("--lat", type=float, required=True)
    w.add_argument("--lon", type=float, required=True)

    args = p.parse_args(argv)

    if args.cmd == "ask":
        adv = Advisor()
        ans = adv.ask(args.question)
        print(Advisor.format_sms(ans) if args.sms else ans.text)
    elif args.cmd == "chat":
        adv = Advisor()
        print("FarmWise maize advisor (draft guidance). Type 'quit' to exit.\n")
        while True:
            try:
                q = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if q.lower() in {"quit", "exit"}:
                break
            print("\n" + adv.ask(q).text + "\n")
    elif args.cmd == "serve":
        from .web import serve

        serve(args.host, args.port, None if args.no_log else "queries.jsonl")
    elif args.cmd == "weather":
        rain = weather.fetch_daily_rain(args.lat, args.lon)
        if rain is None:
            print("Forecast unavailable (no internet or service down).")
            return 1
        sig = weather.planting_signal(rain)
        print(f"Next 7 days: {sig['total_mm']} mm over {sig['wet_days']} wet days -> {sig['level'].upper()}\n{sig['message']}")
    return 0
