# Avataria PVP TR - V2
Avataria PVP pozwala na skonfigurowanie własnego serwera avataria.

# Aktualizacje 08.08.2025
- Dodano funkcję Chat Decor.
- Naprawiono błędy.

# VDS - Instalacja na VPS
- apt-get update
- apt-get upgrade
- apt install python3-pip
- apt-get install redis-server
- systemctl enable redis-server.service
- git clone https://github.com/emirkibar/avatariapvp-tr
- Zaktualizuj „web.ini” w pliku „avatariapvp-tr” zgodnie z własnym serwerem.
- Pobierz wymagania gry pip3 install --user -r requirements.txt.
- Otwórz terminal na swoim komputerze z poziomu połączenia pulpitu zdalnego, wpisz „cd avatariapvp-tr” i wpisz python3 web.py.
- Otwórz nowy terminal, wpisz cd avatariapvp-tr, a następnie wpisz python3 server i uruchom serwer.

# Konfiguracja XRDP (zapewnia dostęp do pulpitu zdalnego)
- sudo apt update
- sudo apt install xfce4 xfce4-goodies xorg dbus-x11 x11-xserver-utils
- sudo apt install xrdp
- sudo systemctl status xrdp
- xrdp.service - demon xrdp
Załadowano: załadowano (/lib/systemd/system/xrdp.service; włączone; ustawienie wstępne dostawcy: włączone)
Aktywne: aktywne (uruchomione) od niedzieli 2019-07-28 22:40:53 UTC; 4 min 21 godz. temu
Dokumentacja: man:xrdp(8)
man:xrdp.ini(5)
- sudo adduser xrdp ssl-cert
- sudo systemctl restart xrdp

# Dostęp do panelu
- Otwórz Putty.
- Zaloguj się.
- cd "folder, w którym znajdują się pliki gry" (np.: cd ava)
- Wpisz redis-server.
- Wpisz redis-cli.
- Możesz wpisać następujące polecenia.
- 
# Udzielanie uprawnień w grze
- Udziel tajnego administratora (R) = set uid:ID:role 5
- Udziel administratora (A) = set uid:ID:role 4
- Udziel głównego moderatora (M) = set uid:ID:role 3
- Udziel moderatora (M) = set uid:ID:role 2
- Udziel uprawnienia ostrzegawczego (M) = set uid:ID:role 1
- Zwykły gracz (P) = set uid:ID:role 0

# Obraz - Komfort - Poziom - Polecenia zmiany nazwy
- Nadawanie obrazu: set uid:ID:crt {kwota}
- Nadawanie komfortu: set uid:ID:hrt {kwota}
- Nadawanie poziomu (exp): set uid:ID:exp {kwota exp}
- Zmiana nazwy: lset uid:ID:appearance 0 „Nazwa do umieszczenia”

# Ustawienia w grze
- Zablokowanie gracza: !ban ID
- Wyciszenie gracza: !mute ID czas trwania (min)
- Odblokowanie: !unban ID
- Resetowanie konta gracza: !reset ID
- Wyciszenie gracza: !mute ID 0 (min)
- Resetowanie konta gracza: !reset ID
  
# Reset Members
- Otwórz Putty.
- cd {nazwa folderu, w którym znajdują się pliki gry} (np.: cd ava)
- Wpisz redis-server.
- Wpisz redis-cli FLUSHDB.



