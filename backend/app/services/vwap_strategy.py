from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd


def calculate_vwap(price_data: List[Dict], volume_data: List[Dict]) -> float:
    """
    VWAP (Volume Weighted Average Price)를 계산합니다.
    
    Args:
        price_data: 가격 데이터 리스트 [{"price": float, "timestamp": datetime}, ...]
        volume_data: 거래량 데이터 리스트 [{"volume": int, "timestamp": datetime}, ...]
    
    Returns:
        VWAP 값
    """
    if not price_data or not volume_data:
        return 0.0
    
    # 데이터를 DataFrame으로 변환
    price_df = pd.DataFrame(price_data)
    volume_df = pd.DataFrame(volume_data)
    
    # 타임스탬프를 기준으로 병합
    df = pd.merge(price_df, volume_df, on='timestamp', how='inner')
    
    if len(df) == 0:
        return 0.0
    
    # VWAP 계산: (가격 * 거래량)의 합 / 거래량의 합
    total_price_volume = (df['price'] * df['volume']).sum()
    total_volume = df['volume'].sum()
    
    if total_volume == 0:
        return 0.0
    
    vwap = total_price_volume / total_volume
    return float(vwap)


def calculate_vwap_bands(vwap: float, price_data: List[Dict], volume_data: List[Dict], 
                        std_dev: float = 2.0) -> Dict[str, float]:
    """
    VWAP 밴드를 계산합니다 (상단/하단).
    
    Args:
        vwap: VWAP 값
        price_data: 가격 데이터
        volume_data: 거래량 데이터
        std_dev: 표준편차 배수 (기본값: 2.0)
    
    Returns:
        {"upper": float, "lower": float, "vwap": float}
    """
    if not price_data or not volume_data:
        return {"upper": vwap, "lower": vwap, "vwap": vwap}
    
    # 가격과 거래량 데이터 병합
    price_df = pd.DataFrame(price_data)
    volume_df = pd.DataFrame(volume_data)
    df = pd.merge(price_df, volume_df, on='timestamp', how='inner')
    
    if len(df) == 0:
        return {"upper": vwap, "lower": vwap, "vwap": vwap}
    
    # 가격의 표준편차 계산
    price_std = df['price'].std()
    
    upper_band = vwap + (std_dev * price_std)
    lower_band = vwap - (std_dev * price_std)
    
    return {
        "upper": float(upper_band),
        "lower": float(lower_band),
        "vwap": vwap
    }


def generate_trading_signal(
    current_price: float,
    vwap: float,
    entry_threshold: float = 0.5,
    exit_threshold: float = 1.0
) -> Dict[str, Any]:
    """
    VWAP 기반 매매 신호를 생성합니다.
    
    Args:
        current_price: 현재 가격
        vwap: VWAP 값
        entry_threshold: 진입 임계값 (%)
        exit_threshold: 청산 임계값 (%)
    
    Returns:
        {
            "signal": "BUY" | "SELL" | "HOLD",
            "price_diff_percent": float,
            "reason": str
        }
    """
    price_diff = current_price - vwap
    price_diff_percent = (price_diff / vwap) * 100
    
    # 매수 신호: 가격이 VWAP 아래에서 VWAP로 상승 돌파
    if price_diff_percent < -entry_threshold and price_diff_percent > -exit_threshold:
        return {
            "signal": "BUY",
            "price_diff_percent": price_diff_percent,
            "reason": f"가격이 VWAP 아래 {abs(price_diff_percent):.2f}% 위치, 상승 돌파 대기"
        }
    
    # 매도 신호: 가격이 VWAP 위에서 VWAP로 하락 이탈
    if price_diff_percent > entry_threshold and price_diff_percent < exit_threshold:
        return {
            "signal": "SELL",
            "price_diff_percent": price_diff_percent,
            "reason": f"가격이 VWAP 위 {price_diff_percent:.2f}% 위치, 하락 이탈 대기"
        }
    
    # Mean Reversion: 가격이 VWAP에서 크게 벗어난 경우
    if abs(price_diff_percent) > exit_threshold:
        if price_diff_percent > 0:
            return {
                "signal": "SELL",
                "price_diff_percent": price_diff_percent,
                "reason": f"가격이 VWAP 위 {price_diff_percent:.2f}% 벗어남, Mean Reversion 매도"
            }
        else:
            return {
                "signal": "BUY",
                "price_diff_percent": price_diff_percent,
                "reason": f"가격이 VWAP 아래 {abs(price_diff_percent):.2f}% 벗어남, Mean Reversion 매수"
            }
    
    return {
        "signal": "HOLD",
        "price_diff_percent": price_diff_percent,
        "reason": "신호 없음"
    }


def check_stop_loss_take_profit(
    entry_price: float,
    current_price: float,
    stop_loss_percent: float = 2.0,
    take_profit_percent: float = 3.0
) -> Dict[str, Any]:
    """
    손절매/익절매 조건을 확인합니다.
    
    Args:
        entry_price: 진입 가격
        current_price: 현재 가격
        stop_loss_percent: 손절매 비율 (%)
        take_profit_percent: 익절매 비율 (%)
    
    Returns:
        {
            "action": "STOP_LOSS" | "TAKE_PROFIT" | "HOLD",
            "profit_loss_percent": float,
            "reason": str
        }
    """
    profit_loss_percent = ((current_price - entry_price) / entry_price) * 100
    
    if profit_loss_percent <= -stop_loss_percent:
        return {
            "action": "STOP_LOSS",
            "profit_loss_percent": profit_loss_percent,
            "reason": f"손절매 조건 달성: {profit_loss_percent:.2f}%"
        }
    
    if profit_loss_percent >= take_profit_percent:
        return {
            "action": "TAKE_PROFIT",
            "profit_loss_percent": profit_loss_percent,
            "reason": f"익절매 조건 달성: {profit_loss_percent:.2f}%"
        }
    
    return {
        "action": "HOLD",
        "profit_loss_percent": profit_loss_percent,
        "reason": "보유 중"
    }

