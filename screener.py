import pandas as pd

from config import VOLUME_RATIO


def check_strategy(day_df: pd.DataFrame, month_df: pd.DataFrame):

    # 日K至少要有足夠資料才能計算MACD
    if len(day_df) < 35:
        return None

    # 月K至少需要三個月才能比較前一個月與前前一個月
    if len(month_df) < 3:
        return None

    # ---------- 日K ----------
    today = day_df.iloc[-1]
    yesterday = day_df.iloc[-2]

    close_today = float(today["Close"])
    close_yesterday = float(yesterday["Close"])
    high_yesterday = float(yesterday["High"])

    osc_today = float(today["OSC"])
    osc_yesterday = float(yesterday["OSC"])

    # 新增：成交量
    volume_today = float(today["Volume"])
    volume_yesterday = float(yesterday["Volume"])

    # ---------- 月K ----------
    # 前一個已完成月份
    month_prev = month_df.iloc[-2]

    # 前前一個月份
    month_prev2 = month_df.iloc[-3]

    month_osc = float(month_prev["OSC"])
    month_osc_prev = float(month_prev2["OSC"])

    # ---------- 漲跌幅 ----------
    change_percent = round(
        (close_today - close_yesterday)
        / close_yesterday * 100,
        2
    )

    # ---------- 選股條件 ----------

    # 1. 收盤突破昨日最高價(包含上影線)
    condition1 = close_today > high_yesterday

    # 2. 日MACD OSC持續走強
    condition2 = osc_today >= osc_yesterday

    # 3. 月MACD OSC判斷
    if month_osc >= 0:
        # 0軸以上不得轉弱
        condition3 = month_osc >= month_osc_prev
    else:
        # 0軸以下必須向0軸收斂
        condition3 = abs(month_osc) <= abs(month_osc_prev)

    # 4. 成交量放大1.5倍
    condition4 = (
        volume_yesterday > 0
        and volume_today >= volume_yesterday * VOLUME_RATIO
    )

    passed = (
        condition1
        and condition2
        and condition3
        and condition4
    )

    return {
        "pass": passed,

        "close": round(close_today, 2),
        "high": round(high_yesterday, 2),

        "osc": round(osc_today, 4),
        "osc_prev": round(osc_yesterday, 4),

        "month_osc": round(month_osc, 4),
        "month_osc_prev": round(month_osc_prev, 4),

        "change_percent": change_percent,

        "condition1": condition1,
        "condition2": condition2,
        "condition3": condition3,
        "condition4": condition4,

        # 新增：方便前端顯示
        "volume": int(volume_today),
        "volume_prev": int(volume_yesterday),
        "volume_ratio": round(
            volume_today / volume_yesterday,
            2
        ) if volume_yesterday > 0 else 0,
    }