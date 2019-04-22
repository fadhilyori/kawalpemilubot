import os
import telepot
import pytz, time
from datetime import datetime
from telepot.loop import MessageLoop
import requests

bot = telepot.Bot(os.getenv("TOKEN"))

members = []

tz = pytz.timezone('Asia/Jakarta')
last_update = datetime.now(tz).strftime('%d %B %Y %H:%M:%S WIB')

def getData():
    r = requests.get("https://kawal-c1.appspot.com/api/c/0")
    last_update = datetime.now(tz).strftime('%d %B %Y %H:%M:%S WIB')
    return r.json()

def update():
    data = getData()
    dataChild = data['children']
    currentChild = []
    for i in range(0,len(dataChild)):
        currentChild.append({
            'id': dataChild[i][0],
            'nama_provinsi': dataChild[i][1],
            'jumlah_tps': dataChild[i][2]
        })
    totalSuaraPaslon1 = 0
    totalSuaraPaslon2 = 0
    totalSah = 0
    totalTidakSah = 0
    dataPerolehan = data['data']
    totalTps = 0
    tpsProses = 0
    currentDataPerolehan = []
    for item in dataPerolehan:
        for val in currentChild:
            if int(item) == val['id']:
                currentDataPerolehan.append({
                    'nama_provinsi': val['nama_provinsi'],
                    'pas1': dataPerolehan[item]['sum']['pas1'],
                    'pas2': dataPerolehan[item]['sum']['pas2'],
                    'sah': dataPerolehan[item]['sum']['sah'],
                    'tSah': dataPerolehan[item]['sum']['tSah'],
                    'tpsmasuk': dataPerolehan[item]['sum']['cakupan'],
                    'total_tps': val['jumlah_tps']
                })
                totalSuaraPaslon1 += int(dataPerolehan[item]['sum']['pas1'])
                totalSuaraPaslon2 += int(dataPerolehan[item]['sum']['pas2'])
                totalSah += int(dataPerolehan[item]['sum']['sah'])
                totalTidakSah += int(dataPerolehan[item]['sum']['tSah'])
                totalTps += int(val['jumlah_tps'])
                tpsProses += int(dataPerolehan[item]['sum']['cakupan'])
    return {
        'total_pas1': totalSuaraPaslon1,
        'total_pas2': totalSuaraPaslon2,
        'total_sah': totalSah,
        'total_tSah': totalTidakSah,
        'total_tps': totalTps,
        'tps_proses': tpsProses
    }

def tampilData():
    data = update()
    text = "*[Kawal Pemilu Bot 2019]*\n"
    text += "Last update " + last_update + "\n"
    text += "Hasil : \n\n"
    text += "--------------------------------------------------\n"
    text += "*Paslon 01*\n*Ir.Joko Widodo & KH.Maruf Amin*\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara\t: " + format_number(data['total_pas1']) + " \n"
    text += "Prosentase\t: {0:.2f} %\n".format(data['total_pas1']/data['total_sah']*100)
    text += "--------------------------------------------------\n\n"
    text += "--------------------------------------------------\n"
    text += "*Paslon 02*\n*H.Prabowo Subianto & Sandiaga Uno*\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara\t: " + format_number(data['total_pas2']) + " \n"
    text += "Prosentase\t: {0:.2f} %\n".format(data['total_pas2']/data['total_sah']*100)
    text += "--------------------------------------------------\n\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara Sah\t: " + format_number(data['total_sah']) + "\n"
    text += "Total Suara Tidak Sah\t: " + format_number(data['total_tSah']) + "\n"
    text += "TPS di Proses\t: " + format_number(data['tps_proses']) + "\n"
    text += "Total TPS\t: " + format_number(data['total_tps']) + "\n"
    text += "--------------------------------------------------\n"
    text += "Note\t: Prosentase lebih dari 100% karena ada data jumlah suara sah dari kedua paslon di beberapa daerah tidak sama dengan total suara sah didaerah tersebut\n"
    text += "Sumber data\t: kawalpemilu.org\n\n"
    text += "by MitraAnakNegeri and @fadhilyori"
    return text

def get_data_from_province(province=None):
    if province == None:
        return "Silahkan sebutkan nama provinsi"
    else:
        data = getData()
        dataChild = data['children']
        province_id = 0
        nama_provinsi = ""
        total_tps = 0
        for i in range(0,len(dataChild)):
            if dataChild[i][1] == province.upper():
                province_id = dataChild[i][0]
                nama_provinsi = dataChild[i][1]
                total_tps = dataChild[i][2]
        totalSuaraPaslon1 = 0
        totalSuaraPaslon2 = 0
        totalSah = 0
        totalTidakSah = 0
        dataPerolehan = data['data']
        totalTps = 0
        tpsProses = 0
        for item in dataPerolehan:
            if int(item) == province_id:
                return {
                    'nama_provinsi': nama_provinsi,
                    'pas1': dataPerolehan[item]['sum']['pas1'],
                    'pas2': dataPerolehan[item]['sum']['pas2'],
                    'sah': dataPerolehan[item]['sum']['sah'],
                    'tSah': dataPerolehan[item]['sum']['tSah'],
                    'tpsmasuk': dataPerolehan[item]['sum']['cakupan'],
                    'total_tps': total_tps
                }
        return "Provinsi tidak terdaftar"

def tampilDataProvince(province):
    data = get_data_from_province(province)
    if data == "Provinsi tidak terdaftar":
        return data
    text = "*[Kawal Pemilu Bot 2019]*\n"
    text += "Last update " + last_update + "\n"
    text += "Hasil Provinsi : *" + data["nama_provinsi"] + "*\n\n"
    text += "--------------------------------------------------\n"
    text += "*Paslon 01*\n*Ir.Joko Widodo & KH.Maruf Amin*\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara\t: " + format_number(data['pas1']) + " \n"
    text += "Prosentase\t: {0:.2f} %\n".format(data['pas1']/data['sah']*100)
    text += "--------------------------------------------------\n\n"
    text += "--------------------------------------------------\n"
    text += "*Paslon 02*\n*H.Prabowo Subianto & Sandiaga Uno*\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara\t: " + format_number(data['pas2']) + " \n"
    text += "Prosentase\t: {0:.2f} %\n".format(data['pas2']/data['sah']*100)
    text += "--------------------------------------------------\n\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara Sah\t: " + format_number(data['sah']) + "\n"
    text += "Total Suara Tidak Sah\t: " + format_number(data['tSah']) + "\n"
    text += "TPS di Proses\t: " + format_number(data['tpsmasuk']) + "\n"
    text += "Total TPS\t: " + format_number(data['total_tps']) + "\n"
    text += "--------------------------------------------------\n"
    text += "Note\t: Prosentase lebih dari 100% karena ada data jumlah suara sah dari kedua paslon di beberapa daerah tidak sama dengan total suara sah didaerah tersebut\n"
    text += "Sumber data\t: kawalpemilu.org\n\n"
    text += "by MitraAnakNegeri and @fadhilyori"
    return text

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg['text']
    if text == "/request":
        found = 0
        for member in members:
            if member['chat_id'] == chat_id:
                result = bot.sendMessage(member['chat_id'], tampilData(), parse_mode='Markdown')
                member.update({'message_id': result['message_id']})
                found += 1
                break
        if found == 0:
            result = bot.sendMessage(chat_id, tampilData(), parse_mode='Markdown')
            members.append({'chat_id': chat_id, 'message_id': result['message_id']})
        print(members)
    else:
        print({'chat_id': chat_id, 'sender': msg['from']['first_name']})
        bot.sendMessage(chat_id, tampilDataProvince(text), parse_mode='Markdown')

MessageLoop(bot, handle).run_as_thread()
print('Bot was ready')


def format_number(number):
    y = str(number)
    if len(y) <= 3:
        return y
    else:
        p = y[-3:]
        q = y[:-3]
        return format_number(q) + ',' + p


while True:
    for member in members:
        if member['message_id'] == 'Null':
            result = bot.sendMessage(member['chat_id'], tampilData(), parse_mode='Markdown')
            member.update({'message_id': result['message_id']})
        else:
            try:
                bot.editMessageText((member['chat_id'], member['message_id']), tampilData(), parse_mode='Markdown')
            except Exception as e:
                pass
    time.sleep(10)
