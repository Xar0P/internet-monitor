from subprocess import Popen, PIPE
import json
from win10toast import ToastNotifier
from datetime import datetime
from playsound import playsound
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class MissingArgs(Exception):
    pass


def notify(msg):
    playsound('./sound.mp3')

    notification = ToastNotifier()
    notification.show_toast(
        'Internet baixa', msg, duration=10)


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


def saveToJson(download_speed, upload_speed, ping, date, hour, filename, isLimited=False):
    obj = {
        "download_speed": download_speed, "upload_speed": upload_speed, "ping": ping, "date": date, "hour": hour
    }

    if not os.path.isfile(filename):
        with open(filename, "w") as outfile:
            json.dump([obj], outfile)
    else:
        with open(filename) as outfile:
            jsonObj = json.load(outfile)

        if isLimited:
            print(len(jsonObj))
            if len(jsonObj) == 15:
                jsonObj.pop(0)

        jsonObj.append(obj)

        with open(filename, 'w') as file:
            json.dump(jsonObj, file,
                      indent=4,
                      separators=(',', ': '))


try:
    if os.environ.get("MIN_DOWNLOAD") is None or os.environ.get("MIN_UPLOAD") is None:
        raise MissingArgs

    out, err, errcode = speedtest()

    min_download = float(os.environ.get("MIN_DOWNLOAD"))
    min_upload = float(os.environ.get("MIN_UPLOAD"))

    speed = json.loads(out)  # Transformar em JSON

    # Cálculo para transformar em Mbps
    download_speed = speed['download']['bandwidth'] * 8 / 1_000_000
    upload_speed = speed['upload']['bandwidth'] * 8 / 1_000_000
    ping = speed['ping']['latency']
    full_date = f"{ISOtoHuman(speed['timestamp'])}"

    if download_speed < min_download and upload_speed < min_upload:
        notify('Velocidade de download e upload estão abaixo do esperado.')
    elif download_speed < min_download:
        notify('Velocidade de download está abaixo do esperado.')
    elif upload_speed < min_upload:
        notify('Velocidade de upload está abaixo do esperado.')
    else:
        print('Está tudo OK.')

    date = full_date.split(' ')[0]
    hour = full_date.split(' ')[1]

    saveToJson(download_speed, upload_speed, ping,
               date, hour, f'./reports/{date}.json')
    saveToJson(download_speed, upload_speed, ping, date,
               hour, './reports/limited_report.json', True)
except MissingArgs:
    print('Velocidade mínima de download ou upload não foi definido, execute o script config.bat')
except KeyError:
    print('Ocorreu um erro no speedtest')
