# sslscan / sslscan-multithread

Script: Giuseppe Compare

sito web: https://jhackers.it

pagina youtube: https://www.youtube.com/channel/UCre9ioOuozO7pwJdUN0vvNA

gruppo telegram: https://t.me/joinchat/H9mGjhSHp-jVV5QPnvtqeg

Script Python creato da Giuseppe Compare - @jhacker91

# PREREQUISITI

Python 3

PHP

sudo

# INSTALLAZIONE:

sudo pip3 install requests

sudo pip3 install datetime

sudo pip3 install xlsxwriter

sudo pip3 install openpyxl

sudo pip3 install xlrd

# AVVIO :

python3 sslscan.py

python3 sslscan-multithread.py


C'è la possibilità di scansionare un host oppure una lista di host ( in un file txt ). La procedura è completamente guidata.
Alla fine verranno prodotti 2 file: un file json (consultabile da Firefox) ed un file excel per l'analisi dei certificati ottenuti.


# NB : EVITARE DI SOVRACCARICARE IL SERVER CON UN NUMERO TROPPO ALTO DI RICHIESTE ( IN VERSIONE MULTITHREAD )
