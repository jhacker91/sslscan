# sslscan

# Script: Giuseppe Compare\n
# sito web: https://jhackers.it
# pagina youtube: https://www.youtube.com/channel/UCre9ioOuozO7pwJdUN0vvNA
# gruppo telegram: https://t.me/joinchat/H9mGjhSHp-jVV5QPnvtqeg

# Giuseppe Compare 

Script Python creato da Giuseppe Compare - @jhacker91

Il file in formato go è disponibile su gitHub - https://github.com/ssllabs/ssllabs-scan/

Installazione:

sudo pip3 install xlsxwriter

sudo pip3 install openpyxl

sudo pip3 install xlrd

Avvio :

go run ssllabs-scan-v3.go [option] hostname

go run ssllabs-scan-v3.go --hostfile file > output.json

Una volta ottenuto il file è possibile importare i dati in un excel

python3 analisi_certificati.py



Option	Default value	Description
--api	BUILTIN	API entry point, for example https://www.example.com/api/
--verbosity	info	Configure log verbosity: error, info, debug, or trace
--quiet	false	Disable status messages (logging)
--ignore-mismatch	false	Proceed with assessments on certificate mismatch
--json-flat	false	Output results in flattened JSON format
--hostfile	none	File containing hosts to scan (one per line)
--usecache	false	If true, accept cached results (if available), else force live scan
--grade	false	Output only the hostname: grade
--hostcheck	false	If true, host resolution failure will result in a fatal error

