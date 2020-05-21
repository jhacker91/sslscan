import json
from datetime import datetime
import xlsxwriter
from pip._vendor.distlib.compat import raw_input
import requests
import time



# SCANSIONE O ANALISI FILE
scelta = 0

while scelta == 0:
    valore_iniziale = input("\nVuoi effettuare una scansione o hai già un file json da analizzare? (1 -Scansione) (2 - file json)? : ")
    output = raw_input("\nInserisci il nome del file excel da creare (senza specificare l'estensione) : ")
    if valore_iniziale == '1':
        scelta=1
        # SCANSIONE CERTIFICATI
        err = 0
        while err == 0:
            scanner = input("\nVuoi scansionare uno o piu host? (1 - un solo host) (2 - piu' host) : ")
            # SCANSIONE SINGOLO HOST
            if scanner == '1':
                data = []
                host_singolo = input("\nInserisci l'host da scansionare : ")
                file_da_analizzare = input("\nInserisci il nome del file json da creare (.json) : ")
                o = open(file_da_analizzare, "a")
                params = (
                    ('host', host_singolo),
                    ('all', 'done'),
                )
                response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=params)
                print("\nAnalisi in corso di : " + host_singolo + " in 190 secondi ")
                time.sleep(190)
                print("Analisi Terminata !! ")
                data.append(response.json())
                json.dump(data, o)
                o.close()
                err = 1

            # SCANSIONE FILE HOST
            elif scanner == '2':

                nome_doc = input("\nInserisci nome del documento da analizzare (.txt) : ")
                data = []
                f = open(nome_doc, "r")
                righe_file = f.readlines()
                file_da_analizzare = input("\nInserisci il nome del file json da creare (.json) : ")
                o = open(file_da_analizzare, "a")

                for linea in righe_file:
                    params = (
                        ('host', linea),
                        ('all', 'done'),
                    )
                    response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=params)
                    print("\nAnalisi in corso di : " + linea + " in 190 secondi")
                    time.sleep(190)
                    print("Analisi Terminata !!")
                    data.append(response.json())

                json.dump(data, o)
                err = 1
                o.close()
                f.close()
                err = 1

            # SINTASSI NON VALIDA
            else:
                print("I valori validi sono solo 1 e 2\n")


    #ANALISI FILE
    elif valore_iniziale == '2':
        file_da_analizzare = raw_input("Inserisci il file da analizzare (.json): ")
        scelta=1

    #ERROR
    else:
        print("Valore inserito non valido \n I Valori ammessi sono 1 e 2 !! \n")



# creazione file di excel

controllo = (output + ".xlsx")
workbook = xlsxwriter.Workbook(output + ".xlsx")
worksheet = workbook.add_worksheet('Generale')
worksheet.write('A1', 'IP')
worksheet.write('B1', 'HOSTNAME')
worksheet.write('C1', 'NOME COMUNE')
worksheet.write('D1', 'SCADENZA CERTIFICATO PRINCIPALE')
worksheet.write('E1', 'GRADO')
worksheet.write('F1', 'ALGORITMO CHIAVE')
worksheet.write('G1', 'LUNGHEZZA CHIAVE')
worksheet.write('H1', 'TLS 1.0')
worksheet.write('I1', 'TLS 1.1')
worksheet.write('J1', 'TLS 1.2')
worksheet.write('K1', 'TLS 1.3')

# altri certificati

worksheet2 = workbook.add_worksheet('Certificati Aggiuntivi')
worksheet2.write('A1', 'CERTIFICATO')
worksheet2.write('B1', 'NOME')
worksheet2.write('C1', 'DATA SCADENZA')
worksheet2.write('D1', 'ALGORITMO CHIAVE')
worksheet2.write('E1', 'LUNGHEZZA CHIAVE')
worksheet2.write('F1', 'HOST')
worksheet2.write('G1', 'IP')

# weak key
worksheet3 = workbook.add_worksheet('Weak Key')
worksheet3.write('A1', 'NUMERO PROTOCOLLO')
worksheet3.write('B1', 'ID')
worksheet3.write('C1', 'TLS')
worksheet3.write('D1', 'NOME')
worksheet3.write('E1', 'CIPHER STRENGHT')
worksheet3.write('F1', 'HOST')
worksheet3.write('G1', 'IP')
worksheet3.write('H1', 'Weak/Insecure')

with open(file_da_analizzare, 'r') as json_file:
    data = json.load(json_file)
    ip_analizzati = 0
    conta_excel = 2
    riga_exc = 1
    enumcer = 2
    conta_we = 2
    while ip_analizzati < len(data):
        if 'errors' in data[ip_analizzati]:
            print("\nErrore : "+data[ip_analizzati]['errors'][0]['message']+" \n")

        elif data[ip_analizzati]['status'] != "READY":
            print("\nErrore - Host non analizzato \n")

        elif data[ip_analizzati]['endpoints'][0]['statusMessage'] != "Ready":
            print("Errore : " + data[ip_analizzati]['endpoints'][0]['statusMessage'])

        elif data[ip_analizzati]['status'] == 'READY':
            print("---------------------------------------------------------------------")
            print("-----------------------------" + data[ip_analizzati]['endpoints'][0]['ipAddress'] + "-----------------------------")
            print("---------------------------------------------------------------------")
            print("Informazioni in dettaglio per l'ip " + data[ip_analizzati]['endpoints'][0][
                'ipAddress'] + " con hostname : " + data[ip_analizzati]['host'])
            timestamp = str(data[ip_analizzati]['startTime'])
            time = int(timestamp[:10])
            dt_object = datetime.fromtimestamp(time)
            print("data inizio scansione (+GMT 2h) =", dt_object)
            print("certificato primario: " + data[ip_analizzati]['certs'][0]['subject'])
            print("nome comune : " + data[ip_analizzati]['certs'][0]['commonNames'][0])
            print("host: " + data[ip_analizzati]['host'])
            print("port: " + str(data[ip_analizzati]['port']))
            print("protocollo: " + data[ip_analizzati]['protocol'])
            print("grado: " + data[ip_analizzati]['endpoints'][0]['grade'])
            if 'serverSignature' in data[ip_analizzati]['endpoints'][0]['details']:
                print("server signature: " + data[ip_analizzati]['endpoints'][0]['details']['serverSignature'])
            if 'httpForwarding' in data[ip_analizzati]['endpoints'][0]['details']:
                print("server signature: " + data[ip_analizzati]['endpoints'][0]['details']['httpForwarding'])
            print("algoritmo chiave: " + data[ip_analizzati]['certs'][0]['keyAlg'])
            lun_key = data[ip_analizzati]['certs'][0]['keySize']
            print("lunghezza chiave: " + str(lun_key))
            # timestamp
            timestamp = str(data[ip_analizzati]['certs'][0]['notAfter'])
            time = int(timestamp[:10])
            dt_object = datetime.fromtimestamp(time)
            print("data scadenza certificato (+GMT 2h) =", dt_object)

            # EXCEL
            worksheet.write('A' + str(conta_excel), data[ip_analizzati]['endpoints'][0]['ipAddress'])
            worksheet.write('B' + str(conta_excel), data[ip_analizzati]['host'])
            worksheet.write('C' + str(conta_excel), data[ip_analizzati]['certs'][0]['commonNames'][0])
            worksheet.write('D' + str(conta_excel), str(dt_object))
            worksheet.write('E' + str(conta_excel), data[ip_analizzati]['endpoints'][0]['grade'])
            worksheet.write('F' + str(conta_excel), data[ip_analizzati]['certs'][0]['keyAlg'])
            worksheet.write_number('G' + str(conta_excel), lun_key)
            conta_excel = conta_excel + 1

            # protocolli TLS
            print("\n")
            worksheet.write(riga_exc, 7, "No")
            worksheet.write(riga_exc, 8, "No")
            worksheet.write(riga_exc, 9, "No")
            worksheet.write(riga_exc, 10, "No")
            print("----PROTOCOLLI TLS----")
            version_tls = 0
            while version_tls < len(data[ip_analizzati]['endpoints'][0]['details']['protocols']):
                if data[ip_analizzati]['endpoints'][0]['details']['protocols'][version_tls]['version'] == "1.0":
                    print("TLS 1.0")
                    worksheet.write(riga_exc, 7, "Si")

                if data[ip_analizzati]['endpoints'][0]['details']['protocols'][version_tls]['version'] == "1.1":
                    print("TLS 1.1")
                    worksheet.write(riga_exc, 8, "Si")

                if data[ip_analizzati]['endpoints'][0]['details']['protocols'][version_tls]['version'] == "1.2":
                    print("TLS 1.2")
                    worksheet.write(riga_exc, 9, "Si")

                if data[ip_analizzati]['endpoints'][0]['details']['protocols'][version_tls]['version'] == "1.3":
                    print("TLS 1.3")
                    worksheet.write(riga_exc, 10, "Si")

                version_tls = version_tls + 1

            print("\n")
            riga_exc = riga_exc + 1

            # altri certificati

            print("----ALTRI CERTIFICATI----")
            certificati = 1
            while certificati < len(data[ip_analizzati]['certs']):
                print("certificato aggiuntivo: " + data[ip_analizzati]['certs'][certificati]['subject'])
                worksheet2.write('A' + str(enumcer), data[ip_analizzati]['certs'][certificati]['subject'])
                print("nome comune : " + data[ip_analizzati]['certs'][certificati]['commonNames'][0])
                worksheet2.write('B' + str(enumcer), data[ip_analizzati]['certs'][certificati]['commonNames'][0])
                timestamp = str(data[ip_analizzati]['certs'][certificati]['notAfter'])
                time = int(timestamp[:10])
                dt_object = datetime.fromtimestamp(time)
                print("data scadenza certificato (+GMT 2h) =", dt_object)
                worksheet2.write('C' + str(enumcer), str(dt_object))
                print("algoritmo chiave: " + data[ip_analizzati]['certs'][certificati]['keyAlg'])
                worksheet2.write('D' + str(enumcer), data[ip_analizzati]['certs'][certificati]['keyAlg'])
                lun_key = data[ip_analizzati]['certs'][certificati]['keySize']
                print("lunghezza chiave: " + str(lun_key))
                worksheet2.write_number('E' + str(enumcer), lun_key)
                worksheet2.write("F" + str(enumcer), data[ip_analizzati]['host'])
                worksheet2.write("G" + str(enumcer), data[ip_analizzati]['endpoints'][0]['ipAddress'])
                certificati = certificati + 1
                enumcer = enumcer + 1
                print("\n")

            print("\n")

            # weak key
            print("----WEAK KEY----\n")
            s = 0
            while s < len(data[ip_analizzati]['endpoints'][0]['details']['suites']):
                v = 0
                while v < len(data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list']):
                    if 'q' in data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v]:
                        if data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 769:
                            print("-----------")
                            print("| TLS 1.0 |")
                            print("-----------\n")
                            protocollo = data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol']
                            print("protocol : " + str(protocollo))
                        elif data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 770:
                            print("-----------")
                            print("| TLS 1.1 |")
                            print("-----------\n")
                            protocollo = data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol']
                            print("protocol : " + str(protocollo))
                        elif data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 771:
                            print("-----------")
                            print("| TLS 1.2 |")
                            print("-----------\n")
                            protocollo = data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol']
                            print("protocol : " + str(protocollo))
                        elif data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 772:
                            print("-----------")
                            print("| TLS 1.3 |")
                            print("-----------\n")
                            protocollo = data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol']
                            print("protocol : " + str(protocollo))

                        preferenza = data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['preference']
                        print("preferenza : " + str(preferenza))
                        print("\n")
                        print("protocollo numero : " + str(protocollo) + " - " + str(v))
                        worksheet3.write('A' + str(conta_we), str(protocollo) + " - " + str(v))
                        print(
                            "id : " + str(data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v]['id']))
                        worksheet3.write('B' + str(conta_we), str(
                            data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v]['id']))
                        if data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 769:
                            print("TLS 1.0")
                            worksheet3.write('C' + str(conta_we), "TLS 1.0")
                        elif data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 770:
                            print("TLS 1.1")
                            worksheet3.write('C' + str(conta_we), "TLS 1.1")
                        elif data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 771:
                            print("TLS 1.2")
                            worksheet3.write('C' + str(conta_we), "TLS 1.2")
                        elif data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['protocol'] == 772:
                            print("TLS 1.3")
                            worksheet3.write('C' + str(conta_we), "TLS 1.3")
                        print(
                            "nome : " + data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v]['name'])
                        worksheet3.write('D' + str(conta_we),
                                         data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v]['name'])
                        print("cipher strenght : " + str(
                            data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v]['cipherStrength']))
                        print("\n")
                        worksheet3.write_number('E' + str(conta_we),
                                                data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v][
                                                    'cipherStrength'])
                        worksheet3.write("F" + str(conta_we), data[ip_analizzati]['host'])
                        worksheet3.write("G" + str(conta_we), data[ip_analizzati]['endpoints'][0]['ipAddress'])
                        if data[ip_analizzati]['endpoints'][0]['details']['suites'][s]['list'][v]['q'] == 1:
                            worksheet3.write('H' + str(conta_we), "Weak")
                        else:
                            worksheet3.write('H' + str(conta_we), "Insecure")
                        conta_we = conta_we + 1

                    v = v + 1
                s = s + 1

        else:
            print("Analisi non completa")

        ip_analizzati = ip_analizzati + 1


workbook.close()
