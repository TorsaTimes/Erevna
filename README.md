# Passwort-Leak-Checker

Dieses Python-Programm ermöglicht es Benutzern, Passwörter auf bekannte Leaks zu überprüfen. Es verwendet SHA1-Hashes, um die Passwörter zu überprüfen und vergleicht sie mit einer vorgegebenen Liste von geleakten Passwort-Hashes.

![Bildbeschreibung](Pfad/zum/Bild.jpg)

## Features

- Eingabe von Passwörtern zur Überprüfung auf geleakte Passwort-Hashes
- SHA1-Hash-Algorithmus zur sicheren Überprüfung der Passwörter
- Leicht erweiterbare Liste von geleakten Passwort-Hashes
- Einfache Benutzeroberfläche mit einer GUI-Anwendung auf Basis von PyQt5

## Abhängigkeiten

Das Programm verwendet die folgenden Python-Module:

- sys: Für den Zugriff auf Systemfunktionen
- hashlib: Für die Verwendung des SHA1-Hash-Algorithmus
- os: Für den Zugriff auf Dateisystemfunktionen
- PyQt5: Für die Erstellung der GUI-Anwendung
- pdf2image: Für die Konvertierung von PDF-Dateien in Bilder
- read_img: Ein eigenes Modul zur Extraktion von Text aus Bildern
- qtwidgets: Ein benutzerdefiniertes Modul mit erweiterten Widget-Funktionen

## Verwendung

1. Installieren Sie die erforderlichen Abhängigkeiten mit pip: `pip install sys hashlib os PyQt5 pdf2image qtwidgets`
2. Führen Sie das Python-Programm aus: `python passwort_leak_checker.py`
3. Geben Sie die zu überprüfenden Passwörter ein oder verwenden Sie die GUI-Anwendung, um Dateien mit Passwörtern auszuwählen
4. Das Programm gibt aus, ob die Passwörter in der Liste der geleakten Passwort-Hashes enthalten sind oder nicht

## Bekannte Probleme

- Das Programm verwendet den SHA1-Hash-Algorithmus, der als unsicher gilt und nicht mehr für die Sicherung von Passwörtern empfohlen wird. Es wird empfohlen, einen sichereren Hash-Algorithmus wie SHA256 oder bcrypt zu verwenden.
- Die Liste der geleakten Passwort-Hashes ist statisch und kann veraltet sein. Es wird empfohlen, regelmäßig nach Updates für die Liste zu suchen und diese zu aktualisieren, um aktuelle Leaks abzudecken.

## Beitrag

Beiträge zu Verbesserungen oder Fehlerbehebungen sind willkommen! Bitte erstellen Sie ein Pull-Anfrage mit den gewünschten Änderungen.

## Lizenz

Dieses Programm ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der Lizenzdatei.

Bitte beachten Sie, dass dieses Programm nur für Bildungszwecke und zur Überprüfung der eigenen Passwörter verwendet werden sollte. Die Verwendung dieses Programms für illegale Aktivitäten oder das Überprüfen von Passwörtern ohne Erlaubnis des Eigentümers ist nicht zulässig und kann rechtliche Konsequenzen haben.
