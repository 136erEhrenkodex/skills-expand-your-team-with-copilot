"""
KuCoin API Client für Marktdaten
"""
import ccxt
import pandas as pd
from typing import List, Dict
import time


class KuCoinClient:
    def __init__(self, api_key=None, api_secret=None, api_passphrase=None):
        """
        Initialisiert den KuCoin Client

        Args:
            api_key: KuCoin API Key (optional für öffentliche Daten)
            api_secret: KuCoin API Secret (optional)
            api_passphrase: KuCoin API Passphrase (optional)
        """
        config = {}
        if api_key and api_secret and api_passphrase:
            config = {
                'apiKey': api_key,
                'secret': api_secret,
                'password': api_passphrase,
            }

        self.exchange = ccxt.kucoin(config)
        self.exchange.load_markets()

    def get_top_20_by_volume(self) -> List[Dict]:
        """
        Holt die Top 20 Kryptowährungen nach Handelsvolumen auf KuCoin

        Returns:
            Liste von Dictionaries mit Symbol und Volumen
        """
        try:
            tickers = self.exchange.fetch_tickers()

            # Filtere nur USDT Paare
            usdt_pairs = {
                symbol: ticker for symbol, ticker in tickers.items()
                if '/USDT' in symbol and ticker.get('quoteVolume')
            }

            # Sortiere nach Quote Volume (Volumen in USDT)
            sorted_pairs = sorted(
                usdt_pairs.items(),
                key=lambda x: x[1]['quoteVolume'],
                reverse=True
            )

            # Nimm Top 20
            top_20 = []
            for symbol, ticker in sorted_pairs[:20]:
                top_20.append({
                    'symbol': symbol,
                    'volume': ticker['quoteVolume'],
                    'price': ticker['last'],
                    'change_24h': ticker.get('percentage', 0)
                })

            return top_20

        except Exception as e:
            print(f"Fehler beim Abrufen der Top 20: {e}")
            return []

    def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        """
        Holt OHLCV (Open, High, Low, Close, Volume) Daten

        Args:
            symbol: Trading Pair (z.B. 'BTC/USDT')
            timeframe: Zeitrahmen ('1m', '5m', '15m', '1h', '4h', '1d')
            limit: Anzahl der Kerzen

        Returns:
            DataFrame mit OHLCV Daten
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )

            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            return df

        except Exception as e:
            print(f"Fehler beim Abrufen von OHLCV für {symbol}: {e}")
            return pd.DataFrame()

    def get_ticker_info(self, symbol: str) -> Dict:
        """
        Holt aktuelle Ticker Informationen

        Args:
            symbol: Trading Pair (z.B. 'BTC/USDT')

        Returns:
            Dictionary mit Ticker Informationen
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'high_24h': ticker['high'],
                'low_24h': ticker['low'],
                'volume_24h': ticker['quoteVolume'],
                'change_24h': ticker.get('percentage', 0),
                'bid': ticker['bid'],
                'ask': ticker['ask']
            }
        except Exception as e:
            print(f"Fehler beim Abrufen von Ticker Info für {symbol}: {e}")
            return {}
