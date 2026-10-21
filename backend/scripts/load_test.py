#!/usr/bin/env python3
"""Teste simples de sobrecarga paralela contra a API."""

from __future__ import annotations

import argparse
import concurrent.futures
import time
import urllib.error
import urllib.request


def hit(url: str) -> int:
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://localhost:8000")
    parser.add_argument("--workers", type=int, default=30)
    parser.add_argument("--requests", type=int, default=90)
    args = parser.parse_args()
    url = f"{args.base}/api/servidores?uf=DF&limit=10"
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        codes = list(pool.map(hit, [url] * args.requests))
    elapsed = time.perf_counter() - started
    ok = sum(1 for code in codes if code == 200)
    limited = sum(1 for code in codes if code == 429)
    print(f"elapsed={elapsed:.2f}s ok={ok} limited={limited} other={args.requests - ok - limited}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
