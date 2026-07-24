import time

from stock_list import get_stock_list
from data_loader import download_stock_history
from indicators import calculate_macd, calculate_month_macd
from screener import check_strategy


def scan_market(limit=None):
    """
    掃描股票
    limit=None 表示掃描全部股票
    """

    start_time = time.time()

    stocks = get_stock_list()

    if limit:
        stocks = stocks.head(limit)

    results = []

    total = len(stocks)

    for index, row in stocks.iterrows():

        code = row["code"]
        name = row["name"]
        market = row["market"]
        industry = row["industry"]

        progress = f"[{index + 1:4d}/{total}]"

        print(f"{progress} {code} {name} ({market})")

        try:

            df = download_stock_history(code, market)

            # 日K MACD
            day_df = calculate_macd(df)

            # 月K MACD
            month_df = calculate_month_macd(df)

            result = check_strategy(day_df, month_df)

            if result and result["pass"]:

                results.append({
                    "code": code,
                    "name": name,
                    "market": market,
                    "industry": industry,

                    "close": result["close"],
                    "high": result["high"],

                    "change_percent": result["change_percent"],

                    "osc": result["osc"],
                    "osc_prev": result["osc_prev"],

                    # ===== 成交量資訊 =====
                    "today_volume": result["volume"],
                    "prev_volume": result["volume_prev"],
                    "volume_ratio": result["volume_ratio"],
                })

                print("    ✅ 符合")

            elif result:

                print(
                    f"    ❌ 不符合 "
                    f"(C1={result['condition1']}, "
                    f"C2={result['condition2']}, "
                    f"C3={result['condition3']}, "
                    f"C4={result['condition4']})"
                )

            else:

                print("    ⚠️ 無法判斷")

        except Exception as e:

            print(f"    ⚠️ {e}")

    elapsed = time.time() - start_time

    print("\n==============================")
    print("掃描完成")
    print("==============================")
    print(f"掃描股票：{total} 檔")
    print(f"符合條件：{len(results)} 檔")
    print(f"耗時：{elapsed:.1f} 秒")
    print("==============================")

    return {
        "scan_count": total,
        "results": results
    }