#!/usr/bin/env python3
"""
KuCoin Top 20 Trading Bot
Überwacht die Top 20 Kryptowährungen und gibt Signale für Aufschwünge und Korrekturen
"""
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style

from kucoin_client import KuCoinClient
from technical_analysis import TechnicalAnalyzer
from notifier import Notifier


class KuCoinTop20Bot:
    """Hauptbot-Klasse für KuCoin Top 20 Überwachung"""

    def __init__(self, check_interval=300, notification_method='console'):
        """
        Initialisiert den Bot

        Args:
            check_interval: Zeit zwischen Checks in Sekunden (default: 300 = 5 Minuten)
            notification_method: Benachrichtigungsmethode ('console', 'file', 'both')
        """
        # Lade Umgebungsvariablen
        load_dotenv()

        # Initialisiere Komponenten
        api_key = os.getenv('KUCOIN_API_KEY')
        api_secret = os.getenv('KUCOIN_API_SECRET')
        api_passphrase = os.getenv('KUCOIN_API_PASSPHRASE')

        self.client = KuCoinClient(api_key, api_secret, api_passphrase)
        self.analyzer = TechnicalAnalyzer()
        self.notifier = Notifier(method=notification_method)

        self.check_interval = check_interval
        self.running = False

        # Tracking für Änderungen
        self.previous_trends = {}

    def analyze_coin(self, symbol: str, timeframe: str = '1h') -> dict:
        """
        Analysiert eine einzelne Kryptowährung

        Args:
            symbol: Trading Pair (z.B. 'BTC/USDT')
            timeframe: Zeitrahmen für Analyse

        Returns:
            Dictionary mit Analyse-Ergebnis
        """
        try:
            # Hole OHLCV Daten
            df = self.client.get_ohlcv(symbol, timeframe=timeframe, limit=100)

            if df.empty:
                return None

            # Berechne Indikatoren
            df = self.analyzer.calculate_indicators(df)

            # Analysiere Trend
            analysis = self.analyzer.analyze_trend(df)

            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'analysis': analysis,
                'timestamp': datetime.now()
            }

        except Exception as e:
            print(f"Fehler bei der Analyse von {symbol}: {e}")
            return None

    def check_for_signals(self, result: dict) -> bool:
        """
        Prüft ob ein wichtiges Signal vorliegt

        Args:
            result: Analyse-Ergebnis

        Returns:
            True wenn Signal gesendet werden soll
        """
        if not result or not result.get('analysis'):
            return False

        symbol = result['symbol']
        analysis = result['analysis']
        trend = analysis['trend']

        # Prüfe ob Trend sich geändert hat
        prev_trend = self.previous_trends.get(symbol)

        # Wichtige Änderungen
        important_change = False

        # Starke Trends sind immer wichtig
        if trend in ['STRONG_BULLISH', 'STRONG_BEARISH']:
            important_change = True

        # Trendwechsel sind wichtig
        elif prev_trend and prev_trend != trend:
            # Von Neutral zu Bullish/Bearish
            if prev_trend == 'NEUTRAL' and trend in ['BULLISH', 'BEARISH']:
                important_change = True
            # Richtungswechsel
            elif ('BULLISH' in prev_trend and 'BEARISH' in trend) or \
                 ('BEARISH' in prev_trend and 'BULLISH' in trend):
                important_change = True

        # Überkauft/Überverkauft Situationen
        rsi = analysis.get('rsi', 50)
        if rsi and (rsi < 30 or rsi > 70):
            important_change = True

        # Speichere aktuellen Trend
        self.previous_trends[symbol] = trend

        return important_change

    def run_single_check(self):
        """Führt eine einzelne Überprüfung aller Top 20 Coins durch"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"🔄 Starte Überprüfung der Top 20 Coins...")
        print(f"Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}{Style.RESET_ALL}\n")

        # Hole Top 20 Coins
        top_20 = self.client.get_top_20_by_volume()

        if not top_20:
            print(f"{Fore.RED}❌ Konnte Top 20 Coins nicht abrufen{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}✓ {len(top_20)} Coins gefunden{Style.RESET_ALL}\n")

        # Analysiere jeden Coin
        results = []
        signals = []

        for i, coin in enumerate(top_20, 1):
            symbol = coin['symbol']
            print(f"{Fore.YELLOW}[{i}/20] Analysiere {symbol}...{Style.RESET_ALL}", end=' ')

            result = self.analyze_coin(symbol)

            if result:
                results.append(result)
                print(f"{Fore.GREEN}✓{Style.RESET_ALL}")

                # Prüfe auf wichtige Signale
                if self.check_for_signals(result):
                    signals.append(result)
                    self.notifier.send_signal(
                        symbol,
                        result['analysis'],
                        force=False
                    )

                # Kleine Pause um API nicht zu überlasten
                time.sleep(0.5)
            else:
                print(f"{Fore.RED}✗{Style.RESET_ALL}")

        # Sende Zusammenfassung
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"📊 ZUSAMMENFASSUNG")
        print(f"{'='*80}{Style.RESET_ALL}\n")

        summary_data = [{'symbol': r['symbol'], 'analysis': r['analysis']} for r in results]
        self.notifier.send_summary(summary_data)

        # Zeige Anzahl der Signale
        if signals:
            print(f"\n{Fore.YELLOW}⚠️  {len(signals)} wichtige Signal(e) gefunden!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✓ Keine kritischen Signale{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    def run(self):
        """Startet den Bot im kontinuierlichen Modus"""
        self.running = True

        print(f"{Fore.GREEN}{Style.BRIGHT}")
        print("="*80)
        print("🤖 KUCOIN TOP 20 BOT GESTARTET")
        print("="*80)
        print(f"Check-Intervall: {self.check_interval} Sekunden ({self.check_interval/60:.1f} Minuten)")
        print(f"Benachrichtigung: {self.notifier.method}")
        print("Drücke Ctrl+C zum Beenden")
        print("="*80)
        print(Style.RESET_ALL)

        try:
            while self.running:
                try:
                    self.run_single_check()

                    # Warte bis zum nächsten Check
                    print(f"\n{Fore.CYAN}⏳ Warte {self.check_interval} Sekunden bis zum nächsten Check...{Style.RESET_ALL}\n")
                    time.sleep(self.check_interval)

                    # Lösche Benachrichtigungs-Cache periodisch
                    self.notifier.clear_cache()

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"{Fore.RED}❌ Fehler bei der Ausführung: {e}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Warte 60 Sekunden vor erneutem Versuch...{Style.RESET_ALL}")
                    time.sleep(60)

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}{'='*80}")
            print("🛑 Bot wird beendet...")
            print(f"{'='*80}{Style.RESET_ALL}\n")
            self.running = False

    def stop(self):
        """Stoppt den Bot"""
        self.running = False


def main():
    """Hauptfunktion"""
    # Lade Konfiguration aus Umgebungsvariablen
    check_interval = int(os.getenv('CHECK_INTERVAL', 300))
    notification_method = os.getenv('NOTIFICATION_METHOD', 'console')

    # Erstelle und starte Bot
    bot = KuCoinTop20Bot(
        check_interval=check_interval,
        notification_method=notification_method
    )

    # Wähle Modus
    print(f"{Fore.CYAN}Wähle Modus:{Style.RESET_ALL}")
    print("1. Kontinuierliche Überwachung")
    print("2. Einzelner Check")
    print()

    try:
        choice = input("Eingabe (1 oder 2, Enter für kontinuierlich): ").strip()

        if choice == '2':
            bot.run_single_check()
        else:
            bot.run()

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Abgebrochen{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
