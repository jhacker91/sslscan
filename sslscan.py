aimport json
from datetime import datetime
from queue import Queue
import xlsxwriter
from pip._vendor.distlib.compat import raw_input
import requests
import threading
import time
import random

print("##########################")
print("##########################")
print("Script: Giuseppe Compare\n")
print("sito web: https://jhackers.it")
print("pagina youtube: https://www.youtube.com/channel/UCre9ioOuozO7pwJdUN0vvNA")
print("gruppo telegram: https://t.me/joinchat/H9mGjhSHp-jVV5QPnvtqeg")
print("##########################")
print("##########################\n\n")

print("QUESTO SCRIPT UTILIZZA IL MULTITHREAD SCANSIONANDO FINO A 10 HOST IN CONTEMPORANEA\n\n")

global cont
cont=0
global lista_err
global lista_det
lista_err=[]
lista_det=[]

class ThreadScanner(threading.Thread):
    def __init__(self, nome, linea):
        threading.Thread.__init__(self)
        self.nome = nome
        self.linea = linea
        self.o = o

    def run(self):
        time.sleep(2)
        params = (
            ('host', linea),
            ('all', 'done'),
        )
        response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=params)
        print("\nAnalisi in corso di : " + self.linea)
        time.sleep(15)
        time_to_fail=0

        while True:
            if 'errors' not in response.json():
                break
            elif 'errors' in response.json():
                if response.json()['errors'][0]['message']== 'Running at full capacity. Please try again later.':
                    print("\nCapacità di scansione elevata. La scansione dell'host " + self.linea + " verra' riprovata in seguito")
                    print("\nIl processo potrebbe rallentare")
                    ran= random.randint(1,40)
                    time_to_sleep=130+ran
                    time.sleep(time_to_sleep)
                    time_to_fail=time_to_fail+1
                    if time_to_fail > 6:
                        break
                else:
                    break

        if 'errors' not in response.json():
            while response.json()['status'] != 'READY':
                if response.json()['status'] == "ERROR":
                    print("\nL'host " + self.linea + " non e' stato scansionato ")

                    break
                else:
                    time.sleep(20)
                    response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=params)
        else:
            print("\nHost " + self.linea + " non scansionabile ")
            lista_det.append(response.json()['errors'][0]['message'])
            lista_err.append(self.linea)



        print("\nAnalisi di " + self.linea + " terminata !!")
        global cont
        cont = cont -1
        print("response : " + str(response.json()))
        data.append(response.json())


# SCANSIONE O ANALISI FILE
scelta = 0

while scelta == 0:
    valore_iniziale = input(
        "\nVuoi effettuare una scansione o hai già un file json da analizzare? (1 -Scansione) (2 - file json)? : ")
    output = raw_input("\nInserisci il nome del file excel da creare (senza specificare l'estensione) : ")
    if valore_iniziale == '1':
        scelta = 1
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
                print("\nAnalisi in corso di : " + host_singolo)
                time.sleep(15)

                if 'errors' not in response.json():
                    while response.json()['status'] != 'READY':
                        if 'errors' in response.json():
                            break
                        elif response.json()['status'] == "ERROR":
                            break
                        else:
                            time.sleep(20)
                            response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=params)
                else:
                    print("\nHost non scansionabile ")

                print("\nAnalisi di " + host_singolo + " terminata !!")
                data.append(response.json())
                json.dump(data, o)
                o.close()
                err = 1

            # SCANSIONE FILE HOST
            elif scanner == '2':
                n_thre = input("\nInserisci il numero di thread (Scansioni contemporanee - default 5): ")
                if n_thre == '':
                    n_thre = 5
                elif int(n_thre) > 10:
                    n_thre = 10
                    print("\n Il valore e' stato limitato a 10 per non compromettere le performance della scansione")
                else:
                    n_thre = int(n_thre)

                #threadLimiter = threading.BoundedSemaphore(n_thre)
                nome_doc = input("\nInserisci nome del documento da analizzare (.txt) : ")
                data = []
                f = open(nome_doc, "r")
                righe_file = f.readlines()
                file_da_analizzare = input("\nInserisci il nome del file json da creare (.json) : ")
                o = open(file_da_analizzare, "a")
                q = Queue()
                x_t = 0
                lista_thread=[]


                for e in righe_file:
                    q.put(e)


                while x_t < len(righe_file):
                    if cont < n_thre:
                        time.sleep(6)
                        linea = q.get()
                        cont = cont + 1
                        x_t = x_t + 1
                        thread1 = ThreadScanner("Thread#1", linea)
                        lista_thread.append(thread1)
                        thread1.start()

                    else:
                        time.sleep(5)

                for x in lista_thread:
                    x.join()

                if len(lista_err) > 0:
                    workbook_err = xlsxwriter.Workbook("errore.xlsx")
                    worksheet_err = workbook_err.add_worksheet('Host non scansionati')
                    worksheet_err.write('A1', 'Host')
                    worksheet_err.write('B1', 'Errore')
                    n = 2
                    m = 0
                    for l in lista_err:
                        worksheet_err.write('A' + str(n), l)
                        worksheet_err.write('B' + str(n), lista_det[m])
                        n = n + 1
                        m = m + 1
                    workbook_err.close()

                json.dump(data, o)

                err = 1
                o.close()
                f.close()
                err = 1

            # SINTASSI NON VALIDA
            else:
                print("I valori validi sono solo 1 e 2\n")


    # ANALISI FILE
    elif valore_iniziale == '2':
        file_da_analizzare = raw_input("Inserisci il file da analizzare (.json): ")
        scelta = 1

    # ERROR
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
        oth_ip = 0
        if 'errors' in data[ip_analizzati]:
            print("\nErrore : " + data[ip_analizzati]['errors'][oth_ip]['message'] + " \n")
        elif data[ip_analizzati]['status'] != "READY":
            print("\nErrore - Host non analizzato \n")
        elif data[ip_analizzati]['endpoints'][oth_ip]['statusMessage'] != "Ready":
            print("Errore : " + data[ip_analizzati]['endpoints'][oth_ip]['statusMessage'])
        elif data[ip_analizzati]['status'] == 'READY':
            while oth_ip < len(data[ip_analizzati]['endpoints']):
                if 'errors' in data[ip_analizzati]:
                    print("\nErrore : " + data[ip_analizzati]['errors'][oth_ip]['message'] + " \n")
                elif data[ip_analizzati]['status'] != "READY":
                    print("\nErrore - Host non analizzato \n")
                elif data[ip_analizzati]['endpoints'][oth_ip]['statusMessage'] != "Ready":
                    print("Errore : " + data[ip_analizzati]['endpoints'][oth_ip]['statusMessage'])
                elif data[ip_analizzati]['status'] == 'READY':
                    print("---------------------------------------------------------------------")
                    print("-----------------------------" + data[ip_analizzati]['endpoints'][oth_ip][
                        'ipAddress'] + "-----------------------------")
                    print("---------------------------------------------------------------------")
                    print("Informazioni in dettaglio per l'ip " + data[ip_analizzati]['endpoints'][oth_ip][
                        'ipAddress'] + " con hostname : " + data[ip_analizzati]['host'])
                    timestamp = str(data[ip_analizzati]['startTime'])
                    time = int(timestamp[:10])
                    dt_object = datetime.fromtimestamp(time)
                    print("data inizio scansione (+GMT 2h) =", dt_object)
                    if 'subject' in data[ip_analizzati]['certs'][0]:
                        print("certificato primario: " + data[ip_analizzati]['certs'][0]['subject'])
                    else:
                        print("")
                    print("nome comune : " + data[ip_analizzati]['certs'][0]['commonNames'][0])
                    print("host: " + data[ip_analizzati]['host'])
                    print("port: " + str(data[ip_analizzati]['port']))
                    print("protocollo: " + data[ip_analizzati]['protocol'])
                    print("grado: " + data[ip_analizzati]['endpoints'][oth_ip]['grade'])
                    if 'serverSignature' in data[ip_analizzati]['endpoints'][oth_ip]['details']:
                        print("server signature: " + data[ip_analizzati]['endpoints'][oth_ip]['details']['serverSignature'])
                    if 'httpForwarding' in data[ip_analizzati]['endpoints'][oth_ip]['details']:
                        print("server signature: " + data[ip_analizzati]['endpoints'][oth_ip]['details']['httpForwarding'])
                    print("algoritmo chiave: " + data[ip_analizzati]['certs'][0]['keyAlg'])
                    lun_key = data[ip_analizzati]['certs'][0]['keySize']
                    print("lunghezza chiave: " + str(lun_key))
                    # timestamp
                    timestamp = str(data[ip_analizzati]['certs'][0]['notAfter'])
                    time = int(timestamp[:10])
                    dt_object = datetime.fromtimestamp(time)
                    print("data scadenza certificato (+GMT 2h) =", dt_object)

                    # EXCEL
                    worksheet.write('A' + str(conta_excel), data[ip_analizzati]['endpoints'][oth_ip]['ipAddress'])
                    worksheet.write('B' + str(conta_excel), data[ip_analizzati]['host'])
                    worksheet.write('C' + str(conta_excel), data[ip_analizzati]['certs'][0]['commonNames'][0])
                    worksheet.write('D' + str(conta_excel), str(dt_object))
                    worksheet.write('E' + str(conta_excel), data[ip_analizzati]['endpoints'][oth_ip]['grade'])
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
                    while version_tls < len(data[ip_analizzati]['endpoints'][oth_ip]['details']['protocols']):
                        if data[ip_analizzati]['endpoints'][oth_ip]['details']['protocols'][version_tls]['version'] == "1.0":
                            print("TLS 1.0")
                            worksheet.write(riga_exc, 7, "Si")

                        if data[ip_analizzati]['endpoints'][oth_ip]['details']['protocols'][version_tls]['version'] == "1.1":
                            print("TLS 1.1")
                            worksheet.write(riga_exc, 8, "Si")

                        if data[ip_analizzati]['endpoints'][oth_ip]['details']['protocols'][version_tls]['version'] == "1.2":
                            print("TLS 1.2")
                            worksheet.write(riga_exc, 9, "Si")

                        if data[ip_analizzati]['endpoints'][oth_ip]['details']['protocols'][version_tls]['version'] == "1.3":
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
                        worksheet2.write("G" + str(enumcer), data[ip_analizzati]['endpoints'][oth_ip]['ipAddress'])
                        certificati = certificati + 1
                        enumcer = enumcer + 1
                        print("\n")

                    print("\n")

                    # weak key
                    print("----WEAK KEY----\n")
                    s = 0
                    while s < len(data[ip_analizzati]['endpoints'][oth_ip]['details']['suites']):
                        v = 0
                        while v < len(data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list']):
                            if 'q' in data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v]:
                                if data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 769:
                                    print("-----------")
                                    print("| TLS 1.0 |")
                                    print("-----------\n")
                                    protocollo = data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol']
                                    print("protocol : " + str(protocollo))
                                elif data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 770:
                                    print("-----------")
                                    print("| TLS 1.1 |")
                                    print("-----------\n")
                                    protocollo = data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol']
                                    print("protocol : " + str(protocollo))
                                elif data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 771:
                                    print("-----------")
                                    print("| TLS 1.2 |")
                                    print("-----------\n")
                                    protocollo = data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol']
                                    print("protocol : " + str(protocollo))
                                elif data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 772:
                                    print("-----------")
                                    print("| TLS 1.3 |")
                                    print("-----------\n")
                                    protocollo = data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol']
                                    print("protocol : " + str(protocollo))

                                #preference
                                if 'preference' in data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]:
                                    preferenza = data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['preference']
                                    print("preferenza : " + str(preferenza))
                                    print("\n")

                                print("protocollo numero : " + str(protocollo) + " - " + str(v))
                                worksheet3.write('A' + str(conta_we), str(protocollo) + " - " + str(v))
                                print(
                                    "id : " + str(data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v]['id']))
                                worksheet3.write('B' + str(conta_we), str(
                                    data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v]['id']))
                                if data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 769:
                                    print("TLS 1.0")
                                    worksheet3.write('C' + str(conta_we), "TLS 1.0")
                                elif data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 770:
                                    print("TLS 1.1")
                                    worksheet3.write('C' + str(conta_we), "TLS 1.1")
                                elif data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 771:
                                    print("TLS 1.2")
                                    worksheet3.write('C' + str(conta_we), "TLS 1.2")
                                elif data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['protocol'] == 772:
                                    print("TLS 1.3")
                                    worksheet3.write('C' + str(conta_we), "TLS 1.3")
                                print(
                                    "nome : " + data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v]['name'])
                                worksheet3.write('D' + str(conta_we),
                                                 data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v]['name'])
                                print("cipher strenght : " + str(
                                    data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v]['cipherStrength']))
                                print("\n")
                                worksheet3.write_number('E' + str(conta_we),
                                                        data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v][
                                                            'cipherStrength'])
                                worksheet3.write("F" + str(conta_we), data[ip_analizzati]['host'])
                                worksheet3.write("G" + str(conta_we), data[ip_analizzati]['endpoints'][oth_ip]['ipAddress'])
                                if data[ip_analizzati]['endpoints'][oth_ip]['details']['suites'][s]['list'][v]['q'] == 1:
                                    worksheet3.write('H' + str(conta_we), "Weak")
                                else:
                                    worksheet3.write('H' + str(conta_we), "Insecure")
                                conta_we = conta_we + 1

                            v = v + 1
                        s = s + 1
                oth_ip = oth_ip + 1
        else:
            print("Analisi non completa")


        ip_analizzati = ip_analizzati + 1

workbook.close()
