#!/usr/bin/env python3
"""
Test-Skript für den KuCoin Bot
Zeigt die Funktionalität ohne kontinuierliche Überwachung
"""
from kucoin_client import KuCoinClient
from technical_analysis import TechnicalAnalyzer
from colorama import Fore, Style, init

init(autoreset=True)


def test_top_20():
    """Testet das Abrufen der Top 20 Coins"""
    print(f"{Fore.CYAN}{'='*80}")
    print("TEST 1: Top 20 Kryptowährungen abrufen")
    print(f"{'='*80}{Style.RESET_ALL}\n")

    client = KuCoinClient()
    top_20 = client.get_top_20_by_volume()

    if top_20:
        print(f"{Fore.GREEN}✓ Erfolgreich {len(top_20)} Coins abgerufen{Style.RESET_ALL}\n")
        print(f"{'Symbol':<15} {'Preis (USDT)':<20} {'24h Änderung':<15} {'Volumen (USDT)':<20}")
        print("-" * 80)
        for coin in top_20[:5]:  # Zeige nur Top 5
            symbol = coin['symbol']
            price = coin['price']
            change = coin['change_24h']
            volume = coin['volume']

            color = Fore.GREEN if change > 0 else Fore.RED
            print(f"{symbol:<15} ${price:<19.8f} {color}{change:>6.2f}%{Style.RESET_ALL}        ${volume:>15,.2f}")
        print(f"\n... und {len(top_20) - 5} weitere Coins\n")
        return True
    else:
        print(f"{Fore.RED}✗ Fehler beim Abrufen der Top 20{Style.RESET_ALL}\n")
        return False


def test_technical_analysis():
    """Testet die technische Analyse"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print("TEST 2: Technische Analyse")
    print(f"{'='*80}{Style.RESET_ALL}\n")

    client = KuCoinClient()
    analyzer = TechnicalAnalyzer()

    # Teste mit BTC/USDT
    symbol = 'BTC/USDT'
    print(f"Analysiere {symbol}...\n")

    df = client.get_ohlcv(symbol, timeframe='1h', limit=100)

    if df.empty:
        print(f"{Fore.RED}✗ Konnte keine Daten für {symbol} abrufen{Style.RESET_ALL}\n")
        return False

    # Berechne Indikatoren
    df = analyzer.calculate_indicators(df)
    analysis = analyzer.analyze_trend(df)

    # Zeige Ergebnisse
    print(f"{Fore.GREEN}✓ Analyse abgeschlossen{Style.RESET_ALL}\n")
    print(f"{'='*80}")
    print(f"Symbol: {symbol}")
    print(f"Trend: {analysis['trend']}")
    print(f"Preis: ${analysis.get('price', 0):.2f}")
    print(f"RSI: {analysis.get('rsi', 0):.2f}")
    print(f"MACD Diff: {analysis.get('macd_diff', 0):.4f}")
    print(f"Trend-Stärke: {analysis.get('strength', 0):.2f}")
    print(f"Bullish Score: {analysis.get('bullish_score', 0)}")
    print(f"Bearish Score: {analysis.get('bearish_score', 0)}")
    print(f"\nSignale:")
    for signal in analysis.get('signals', []):
        print(f"  • {signal}")
    print(f"{'='*80}\n")

    return True


def main():
    """Hauptfunktion"""
    print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*80}")
    print("🧪 KUCOIN BOT - TEST SUITE")
    print(f"{'='*80}{Style.RESET_ALL}\n")

    # Test 1: Top 20 abrufen
    success1 = test_top_20()

    # Test 2: Technische Analyse
    success2 = test_technical_analysis()

    # Zusammenfassung
    print(f"{Fore.CYAN}{'='*80}")
    print("ZUSAMMENFASSUNG")
    print(f"{'='*80}{Style.RESET_ALL}\n")

    if success1 and success2:
        print(f"{Fore.GREEN}✓ Alle Tests erfolgreich!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Der Bot ist bereit!")
        print(f"Starte ihn mit: python kucoin_bot.py{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}✗ Einige Tests fehlgeschlagen{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Prüfe deine Internetverbindung und stelle sicher, dass alle Abhängigkeiten installiert sind:{Style.RESET_ALL}")
        print(f"pip install -r requirements.txt\n")


if __name__ == '__main__':
    main()
