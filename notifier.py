"""
Benachrichtigungssystem für Trading Signale
"""
from datetime import datetime
from colorama import Fore, Style, init
from typing import Dict, List

# Initialisiere Colorama für farbige Konsolen-Ausgabe
init(autoreset=True)


class Notifier:
    """Verwaltet Benachrichtigungen für Trading-Signale"""

    def __init__(self, method='console'):
        """
        Initialisiert den Notifier

        Args:
            method: Benachrichtigungsmethode ('console', 'file', 'both')
        """
        self.method = method
        self.log_file = 'trading_signals.log'
        self.last_notifications = {}  # Verhindert Spam

    def send_signal(self, symbol: str, analysis: Dict, force: bool = False):
        """
        Sendet ein Trading-Signal

        Args:
            symbol: Trading Pair
            analysis: Analyse-Ergebnis
            force: Erzwingt Benachrichtigung auch bei Duplikaten
        """
        # Verhindere Duplikate innerhalb kurzer Zeit
        cache_key = f"{symbol}_{analysis['trend']}"
        if not force and cache_key in self.last_notifications:
            return

        self.last_notifications[cache_key] = datetime.now()

        # Formatiere Nachricht
        message = self._format_signal(symbol, analysis)

        # Sende über gewählte Methode
        if self.method in ['console', 'both']:
            self._send_console(message, analysis['trend'])

        if self.method in ['file', 'both']:
            self._send_file(message)

    def send_summary(self, summaries: List[Dict]):
        """
        Sendet eine Zusammenfassung mehrerer Coins

        Args:
            summaries: Liste von Analyse-Ergebnissen
        """
        if not summaries:
            return

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header = f"\n{'='*80}\n🤖 KUCOIN TOP 20 BOT - MARKTÜBERSICHT\n{timestamp}\n{'='*80}\n"

        if self.method in ['console', 'both']:
            print(Fore.CYAN + Style.BRIGHT + header)

        messages = []
        for summary in summaries:
            symbol = summary['symbol']
            analysis = summary['analysis']
            msg = self._format_summary_line(symbol, analysis)
            messages.append(msg)

            if self.method in ['console', 'both']:
                self._print_summary_line(symbol, analysis)

        if self.method in ['file', 'both']:
            full_message = header + '\n'.join(messages) + '\n' + '='*80 + '\n'
            self._send_file(full_message)

    def _format_signal(self, symbol: str, analysis: Dict) -> str:
        """Formatiert ein Trading-Signal"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        trend = analysis['trend']
        price = analysis.get('price', 0)
        rsi = analysis.get('rsi', 0)

        message = f"""
{'='*80}
⚠️  TRADING SIGNAL für {symbol}
{'='*80}
Zeit: {timestamp}
Trend: {trend}
Preis: ${price:.8f}
RSI: {rsi:.2f}
Trend-Stärke: {analysis.get('strength', 0):.2f}
Bullish Score: {analysis.get('bullish_score', 0)}
Bearish Score: {analysis.get('bearish_score', 0)}

📊 Signale:
"""
        for signal in analysis.get('signals', []):
            message += f"  • {signal}\n"

        message += '='*80 + '\n'
        return message

    def _format_summary_line(self, symbol: str, analysis: Dict) -> str:
        """Formatiert eine Zeile für die Zusammenfassung"""
        trend = analysis['trend']
        price = analysis.get('price', 0)
        rsi = analysis.get('rsi', 0)
        net_score = analysis.get('net_score', 0)

        return f"{symbol:15} | Trend: {trend:20} | Preis: ${price:12.8f} | RSI: {rsi:6.2f} | Score: {net_score:+3d}"

    def _print_summary_line(self, symbol: str, analysis: Dict):
        """Druckt eine formatierte Zusammenfassungszeile in Farbe"""
        trend = analysis['trend']
        price = analysis.get('price', 0)
        rsi = analysis.get('rsi', 0)
        net_score = analysis.get('net_score', 0)

        # Farbe basierend auf Trend
        if 'BULLISH' in trend:
            color = Fore.GREEN
            emoji = '📈'
        elif 'BEARISH' in trend:
            color = Fore.RED
            emoji = '📉'
        else:
            color = Fore.YELLOW
            emoji = '➡️'

        symbol_part = f"{symbol:15}"
        trend_part = f"Trend: {trend:20}"
        price_part = f"Preis: ${price:12.8f}"
        rsi_part = f"RSI: {rsi:6.2f}"
        score_part = f"Score: {net_score:+3d}"

        print(f"{emoji} {color}{symbol_part} | {trend_part} | {price_part} | {rsi_part} | {score_part}")

        # Zeige wichtigste Signale
        if analysis.get('signals'):
            for signal in analysis['signals'][:2]:  # Nur erste 2 Signale
                print(f"    {Fore.CYAN}• {signal}")

    def _send_console(self, message: str, trend: str):
        """Sendet Nachricht an Konsole mit Farbe"""
        if 'BULLISH' in trend:
            color = Fore.GREEN
        elif 'BEARISH' in trend:
            color = Fore.RED
        else:
            color = Fore.YELLOW

        print(color + Style.BRIGHT + message)

    def _send_file(self, message: str):
        """Schreibt Nachricht in Log-Datei"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f"Fehler beim Schreiben in Log-Datei: {e}")

    def clear_cache(self):
        """Löscht den Benachrichtigungs-Cache"""
        self.last_notifications.clear()
