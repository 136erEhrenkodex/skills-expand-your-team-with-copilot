"""
Technische Analyse Module für Kryptowährungen
"""
import pandas as pd
import ta
from typing import Dict


class TechnicalAnalyzer:
    """Führt technische Analyse auf OHLCV Daten durch"""

    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Berechnet alle technischen Indikatoren

        Args:
            df: DataFrame mit OHLCV Daten

        Returns:
            DataFrame mit zusätzlichen Indikator-Spalten
        """
        if df.empty or len(df) < 30:
            return df

        try:
            # RSI (Relative Strength Index)
            df['rsi'] = ta.momentum.RSIIndicator(
                close=df['close'],
                window=14
            ).rsi()

            # MACD (Moving Average Convergence Divergence)
            macd = ta.trend.MACD(
                close=df['close'],
                window_slow=26,
                window_fast=12,
                window_sign=9
            )
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()

            # Moving Averages
            df['ema_9'] = ta.trend.EMAIndicator(
                close=df['close'],
                window=9
            ).ema_indicator()

            df['ema_21'] = ta.trend.EMAIndicator(
                close=df['close'],
                window=21
            ).ema_indicator()

            df['sma_50'] = ta.trend.SMAIndicator(
                close=df['close'],
                window=50
            ).sma_indicator()

            # Bollinger Bands
            bollinger = ta.volatility.BollingerBands(
                close=df['close'],
                window=20,
                window_dev=2
            )
            df['bb_high'] = bollinger.bollinger_hband()
            df['bb_mid'] = bollinger.bollinger_mavg()
            df['bb_low'] = bollinger.bollinger_lband()

            # ADX (Average Directional Index) für Trendstärke
            adx = ta.trend.ADXIndicator(
                high=df['high'],
                low=df['low'],
                close=df['close'],
                window=14
            )
            df['adx'] = adx.adx()

            # Volume Indicator
            df['volume_sma'] = df['volume'].rolling(window=20).mean()

            return df

        except Exception as e:
            print(f"Fehler bei der Berechnung der Indikatoren: {e}")
            return df

    @staticmethod
    def analyze_trend(df: pd.DataFrame) -> Dict:
        """
        Analysiert den aktuellen Trend basierend auf technischen Indikatoren

        Returns:
            Dictionary mit Trend-Analyse
        """
        if df.empty or len(df) < 30:
            return {
                'trend': 'UNKNOWN',
                'strength': 0,
                'signals': []
            }

        try:
            # Neueste Werte
            latest = df.iloc[-1]
            prev = df.iloc[-2]

            signals = []
            bullish_score = 0
            bearish_score = 0

            # RSI Analyse
            if 'rsi' in df.columns and pd.notna(latest['rsi']):
                if latest['rsi'] < 30:
                    signals.append("RSI überverkauft (<30) - Potentieller Aufschwung")
                    bullish_score += 2
                elif latest['rsi'] > 70:
                    signals.append("RSI überkauft (>70) - Mögliche Korrektur")
                    bearish_score += 2
                elif latest['rsi'] > 50 and prev['rsi'] <= 50:
                    signals.append("RSI steigt über 50 - Bullish Signal")
                    bullish_score += 1
                elif latest['rsi'] < 50 and prev['rsi'] >= 50:
                    signals.append("RSI fällt unter 50 - Bearish Signal")
                    bearish_score += 1

            # MACD Analyse
            if 'macd_diff' in df.columns and pd.notna(latest['macd_diff']):
                if latest['macd_diff'] > 0 and prev['macd_diff'] <= 0:
                    signals.append("MACD Bullish Crossover - Kaufsignal")
                    bullish_score += 3
                elif latest['macd_diff'] < 0 and prev['macd_diff'] >= 0:
                    signals.append("MACD Bearish Crossover - Verkaufssignal")
                    bearish_score += 3
                elif latest['macd_diff'] > 0:
                    bullish_score += 1
                else:
                    bearish_score += 1

            # EMA Crossover
            if 'ema_9' in df.columns and 'ema_21' in df.columns:
                if pd.notna(latest['ema_9']) and pd.notna(latest['ema_21']):
                    if latest['ema_9'] > latest['ema_21'] and prev['ema_9'] <= prev['ema_21']:
                        signals.append("EMA9 kreuzt EMA21 nach oben - Bullish")
                        bullish_score += 2
                    elif latest['ema_9'] < latest['ema_21'] and prev['ema_9'] >= prev['ema_21']:
                        signals.append("EMA9 kreuzt EMA21 nach unten - Bearish")
                        bearish_score += 2
                    elif latest['ema_9'] > latest['ema_21']:
                        bullish_score += 1
                    else:
                        bearish_score += 1

            # Bollinger Bands
            if all(x in df.columns for x in ['bb_high', 'bb_low']):
                if pd.notna(latest['bb_high']) and pd.notna(latest['bb_low']):
                    if latest['close'] >= latest['bb_high']:
                        signals.append("Preis am oberen Bollinger Band - Überkauft")
                        bearish_score += 1
                    elif latest['close'] <= latest['bb_low']:
                        signals.append("Preis am unteren Bollinger Band - Überverkauft")
                        bullish_score += 1

            # ADX für Trendstärke
            trend_strength = 0
            if 'adx' in df.columns and pd.notna(latest['adx']):
                trend_strength = min(100, max(0, latest['adx']))

            # Volumen Analyse
            if 'volume_sma' in df.columns and pd.notna(latest['volume_sma']):
                if latest['volume'] > latest['volume_sma'] * 1.5:
                    signals.append("Hohes Volumen - Starke Bewegung erwartet")

            # Trend bestimmen
            net_score = bullish_score - bearish_score

            if net_score > 3:
                trend = 'STRONG_BULLISH'
            elif net_score > 0:
                trend = 'BULLISH'
            elif net_score < -3:
                trend = 'STRONG_BEARISH'
            elif net_score < 0:
                trend = 'BEARISH'
            else:
                trend = 'NEUTRAL'

            return {
                'trend': trend,
                'strength': trend_strength,
                'bullish_score': bullish_score,
                'bearish_score': bearish_score,
                'net_score': net_score,
                'signals': signals,
                'rsi': latest.get('rsi'),
                'macd_diff': latest.get('macd_diff'),
                'price': latest['close']
            }

        except Exception as e:
            print(f"Fehler bei der Trend-Analyse: {e}")
            return {
                'trend': 'ERROR',
                'strength': 0,
                'signals': [f'Fehler: {str(e)}']
            }
