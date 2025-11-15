# 🤖 KuCoin Top 20 Trading Bot

Ein vollautomatischer Bot, der die Top 20 Kryptowährungen auf KuCoin überwacht und technische Analyse durchführt, um potenzielle Aufschwünge und Korrekturen zu erkennen.

## 🎯 Features

- **Automatische Top 20 Erkennung**: Identifiziert automatisch die Top 20 Coins nach Handelsvolumen
- **Technische Analyse**: Verwendet multiple Indikatoren:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - EMA/SMA (Exponential/Simple Moving Averages)
  - Bollinger Bands
  - ADX (Average Directional Index)
  - Volumen-Analyse
- **Intelligente Signale**: Erkennt Aufschwünge und Korrekturen basierend auf mehreren Faktoren
- **Echtzeit-Benachrichtigungen**: Farbcodierte Konsolen-Ausgabe und optionale Log-Dateien
- **Kontinuierliche Überwachung**: Läuft 24/7 mit konfigurierbarem Intervall
- **Keine API Keys erforderlich**: Funktioniert mit öffentlichen Daten (API Keys optional für erweiterte Features)

## 📋 Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

## 🚀 Installation

1. **Repository klonen oder Dateien herunterladen**

2. **Virtuelle Umgebung erstellen (empfohlen)**:
```bash
python3 -m venv venv
source venv/bin/activate  # Auf Linux/Mac
# oder
venv\Scripts\activate  # Auf Windows
```

3. **Abhängigkeiten installieren**:
```bash
pip install -r requirements.txt
```

4. **Konfiguration (optional)**:
```bash
cp .env.example .env
# Bearbeite .env mit deinen Einstellungen (optional)
```

## ⚙️ Konfiguration

### Umgebungsvariablen (.env)

Erstelle eine `.env` Datei basierend auf `.env.example`:

```bash
# KuCoin API Credentials (OPTIONAL - nur für private Daten nötig)
KUCOIN_API_KEY=your_api_key_here
KUCOIN_API_SECRET=your_api_secret_here
KUCOIN_API_PASSPHRASE=your_api_passphrase_here

# Bot Konfiguration
CHECK_INTERVAL=300                # Sekunden zwischen Checks (300 = 5 Minuten)
NOTIFICATION_METHOD=console       # console, file, oder both
```

**Hinweis**: API Keys sind NICHT erforderlich für die Grundfunktionalität. Der Bot funktioniert mit öffentlichen Marktdaten.

## 🎮 Verwendung

### Modus 1: Kontinuierliche Überwachung (Empfohlen)

```bash
python kucoin_bot.py
```

Wähle Option `1` oder drücke einfach Enter für kontinuierliche Überwachung.

Der Bot wird:
- Alle 5 Minuten (konfigurierbar) die Top 20 Coins analysieren
- Wichtige Signale in Farbe anzeigen
- Eine Zusammenfassung aller Coins ausgeben
- Kontinuierlich laufen bis du Ctrl+C drückst

### Modus 2: Einzelner Check

```bash
python kucoin_bot.py
```

Wähle Option `2` für einen einmaligen Scan.

## 📊 Signal-Interpretation

### Trend-Kategorien

- **STRONG_BULLISH** 📈: Starker Aufwärtstrend - Gute Kaufgelegenheit
- **BULLISH** 📈: Aufwärtstrend - Potentieller Aufschwung
- **NEUTRAL** ➡️: Seitwärtsbewegung - Abwarten
- **BEARISH** 📉: Abwärtstrend - Vorsicht
- **STRONG_BEARISH** 📉: Starker Abwärtstrend - Mögliche Korrektur

### Wichtige Signale

Der Bot benachrichtigt dich bei:

- **RSI < 30**: Überverkauft - Potentieller Aufschwung
- **RSI > 70**: Überkauft - Mögliche Korrektur
- **MACD Crossover**: Bullish/Bearish Trendwechsel
- **EMA Crossover**: Kurzfristiger Trendwechsel
- **Bollinger Bands**: Überkauft/Überverkauft Zonen
- **Hohem Volumen**: Starke Bewegung erwartet

## 📁 Projektstruktur

```
.
├── kucoin_bot.py           # Hauptbot-Anwendung
├── kucoin_client.py        # KuCoin API Client
├── technical_analysis.py   # Technische Analyse Module
├── notifier.py             # Benachrichtigungssystem
├── requirements.txt        # Python Abhängigkeiten
├── .env.example           # Beispiel-Konfiguration
├── .env                   # Deine Konfiguration (nicht in Git)
├── trading_signals.log    # Log-Datei (wird erstellt)
└── README.md              # Diese Datei
```

## 🔧 Erweiterte Nutzung

### Intervall anpassen

In `.env` die Variable `CHECK_INTERVAL` ändern:
```bash
CHECK_INTERVAL=180  # 3 Minuten
CHECK_INTERVAL=600  # 10 Minuten
```

### Log-Dateien aktivieren

```bash
NOTIFICATION_METHOD=both  # Konsole + Datei
```

Signale werden dann auch in `trading_signals.log` gespeichert.

### Als Hintergrund-Prozess (Linux/Mac)

```bash
nohup python kucoin_bot.py > bot_output.log 2>&1 &
```

### Mit systemd (Linux)

Erstelle `/etc/systemd/system/kucoin-bot.service`:

```ini
[Unit]
Description=KuCoin Top 20 Trading Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/bot
ExecStart=/path/to/venv/bin/python kucoin_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Dann:
```bash
sudo systemctl enable kucoin-bot
sudo systemctl start kucoin-bot
```

## 📈 Verwendete Indikatoren

### RSI (Relative Strength Index)
- Periode: 14
- Überverkauft: < 30
- Überkauft: > 70

### MACD
- Fast: 12
- Slow: 26
- Signal: 9

### Moving Averages
- EMA 9 (Kurzfristig)
- EMA 21 (Mittelfristig)
- SMA 50 (Langfristig)

### Bollinger Bands
- Periode: 20
- Standard-Abweichungen: 2

### ADX (Trend Strength)
- Periode: 14

## ⚠️ Wichtige Hinweise

1. **Keine Finanzberatung**: Dieser Bot dient nur zu Informationszwecken. Keine Trading-Signale sollten als Finanzberatung verstanden werden.

2. **Eigene Recherche**: Führe immer deine eigene Analyse durch bevor du handelst.

3. **Risiko**: Kryptowährungen sind hochvolatil. Investiere nur, was du dir leisten kannst zu verlieren.

4. **API Limits**: KuCoin hat Rate Limits. Der Bot respektiert diese durch Pausen zwischen Anfragen.

5. **Keine Garantien**: Technische Analyse garantiert keine zukünftigen Ergebnisse.

## 🐛 Fehlerbehebung

### "ccxt.errors.ExchangeError"
- KuCoin API könnte vorübergehend nicht verfügbar sein
- Der Bot wartet automatisch und versucht es erneut

### "Connection refused" oder Netzwerkfehler
- Prüfe deine Internetverbindung
- Möglicherweise blockiert eine Firewall die Anfragen

### "ModuleNotFoundError"
- Stelle sicher, dass alle Abhängigkeiten installiert sind: `pip install -r requirements.txt`

### Bot zeigt keine Signale
- Das ist normal wenn keine signifikanten Bewegungen erkannt werden
- Die Zusammenfassung zeigt trotzdem alle Top 20 Coins

## 📝 Lizenz

Dieses Projekt ist Open Source und frei verwendbar.

## 🤝 Beitragen

Verbesserungen und Bug-Fixes sind willkommen! Erstelle einfach einen Pull Request.

## 📧 Support

Bei Fragen oder Problemen erstelle bitte ein Issue im Repository.

---

**Happy Trading! 🚀**

*Denk dran: Dies ist ein Tool zur Information, keine Finanzberatung. Handle verantwortungsvoll!*
