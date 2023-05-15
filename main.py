from subprocess import Popen, PIPE
import json
import sys
from win10toast import ToastNotifier
from datetime import datetime
import pandas as pd
from playsound import playsound


class MissingArgs(Exception):
    "Está faltando argumentos para a execução do script"
    pass


class LowSpeed(Exception):
    "Velocidade abaixo do esperado"
    pass


def notify(msg):
    playsound('./sound.mp3')

    notification = ToastNotifier()
    notification.show_toast(
        'Internet baixa', msg, duration=10)


def validate():
    if len(sys.argv) < 3:
        raise MissingArgs


def speedtest():
    process = Popen('speedtest --format json --progress no',
                    shell=True, stdout=PIPE, stderr=PIPE)  # Executar comando CMD

    out, err = process.communicate()  # Receber resposta
    errcode = process.returncode  # Receber erro

    return out, err, errcode


def ISOtoHuman(dateISO):
    dt_obj = datetime.fromisoformat(dateISO.replace('Z', '+00:00'))
    timestamp = dt_obj.timestamp()
    return datetime.fromtimestamp(timestamp)


def saveToCSV(download_speed, upload_speed, ping, date):
    df = pd.DataFrame({'DOWNLOAD_SPEED': [f'{download_speed:.2f}Mbps'], 'UPLOAD_SPEED': [
                      f'{upload_speed:.2f}Mbps'], 'PING': [f'{ping:.2f}ms'], 'DATE': [date]})

    df.to_csv('report.csv', mode='a', index=False, header=False)


try:
    validate()
    out, err, errcode = speedtest()

    min_download = float(sys.argv[1])
    min_upload = float(sys.argv[2])

    speed = json.loads(out)  # Transformar em JSON

    # Cálculo para transformar em Mbps
    download_speed = speed['download']['bandwidth'] * 8 / 1_000_000
    upload_speed = speed['upload']['bandwidth'] * 8 / 1_000_000
    ping = speed['ping']['latency']
    date = ISOtoHuman(speed['timestamp'])

    if download_speed < min_download and upload_speed < min_upload:
        notify('Velocidade de download e upload estão abaixo do esperado.')
    elif download_speed < min_download:
        notify('Velocidade de download está abaixo do esperado.')
    elif upload_speed < min_upload:
        notify('Velocidade de upload está abaixo do esperado.')
    else:
        print('Está tudo OK.')

    saveToCSV(download_speed, upload_speed, ping, date)
except MissingArgs:
    print('Necessário mínimo de internet de download e upload aceitável.')
