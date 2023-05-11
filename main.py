from subprocess import Popen, PIPE
import json
import sys
from win10toast import ToastNotifier
from datetime import datetime
import pandas as pd


class MissingArgs(Exception):
    "Está faltando argumentos para a execução do script"
    pass


class LowSpeed(Exception):
    "Velocidade abaixo do esperado"
    pass


def show_toast(msg):
    notification = ToastNotifier()

    notification.show_toast(
        'Internet baixa', msg, duration=10)


try:
    if len(sys.argv) < 3:
        raise MissingArgs

    min_download = float(sys.argv[1])
    min_upload = float(sys.argv[2])

    process = Popen('speedtest --format json --progress no',
                    shell=True, stdout=PIPE, stderr=PIPE)  # Executar comando CMD

    out, err = process.communicate()  # Receber resposta
    errcode = process.returncode  # Receber erro

    speedtest = json.loads(out)  # Transformar em JSON

    download_speed = speedtest['download']['bandwidth'] * \
        8 / 1_000_000  # Cálculo para transformar em Mbps
    upload_speed = speedtest['upload']['bandwidth'] * 8 / 1_000_000
    ping = speedtest['ping']['latency']

    # DateISO to Human
    dateISO = speedtest['timestamp']
    dt_obj = datetime.fromisoformat(dateISO.replace('Z', '+00:00'))
    timestamp = dt_obj.timestamp()
    date = datetime.fromtimestamp(timestamp)
    ####

    print(f'Download: {download_speed:.2f}\nUpload: {upload_speed:.2f}')

    if download_speed < min_download and upload_speed < min_upload:
        show_toast('Velocidade de download e upload estão abaixo do esperado.')
    elif download_speed < min_download:
        show_toast('Velocidade de download está abaixo do esperado.')
    elif upload_speed < min_upload:
        show_toast('Velocidade de upload está abaixo do esperado.')
    else:
        print('Está tudo OK.')

    df = pd.DataFrame({'DOWNLOAD_SPEED': [f'{download_speed:.2f}Mbps'], 'UPLOAD_SPEED': [
                      f'{upload_speed:.2f}Mbps'], 'PING': [f'{ping:.2f}ms'], 'DATE': [date]})

    df.to_csv('report.csv', mode='a', index=False, header=False)
except MissingArgs:
    print('Necessário mínimo de internet de download e upload aceitável.')