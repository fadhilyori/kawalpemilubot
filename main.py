import telepot
import time
from telepot.loop import MessageLoop
import requests

bot = telepot.Bot('721772446:AAGm3bJ-IEYUrv0099aXoOfCGGcpmFtt2ME')

members = []

last_update = time.asctime(time.localtime(time.time()))

def getData():
    r = requests.get("https://kawal-c1.appspot.com/api/c/0")
    last_update = time.asctime(time.localtime(time.time()))
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
    text = "*[Kawal Pemilu Bot 2019]*\n";
    text += "Last update " + last_update + "\n"
    text += "Hasil : \n\n"
    text += "--------------------------------------------------\n"
    text += "*Paslon 01*\n*Ir.Joko Widodo & KH.Maruf Amin*\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara\t: {} \n".format(data['total_pas1'])
    text += "Prosentase\t: {0:.2f} %\n".format(data['total_pas1']/(data['total_sah']+data['total_tSah'])*100)
    text += "--------------------------------------------------\n\n"
    text += "--------------------------------------------------\n"
    text += "*Paslon 02*\n*H.Prabowo Subianto & Sandiaga Uno*\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara\t: {} \n".format(data['total_pas2'])
    text += "Prosentase\t: {0:.2f} %\n".format(data['total_pas2']/(data['total_sah']+data['total_tSah'])*100)
    text += "--------------------------------------------------\n\n"
    text += "--------------------------------------------------\n"
    text += "Total Suara Sah\t: {}\n".format(data['total_sah'])
    text += "Total Suara Tidak Sah\t: {}\n".format(data['total_tSah'])
    text += "TPS di Proses\t: {}\n".format(data['tps_proses'])
    text += "Total TPS\t: {}\n".format(data['total_tps'])
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
                found += 1
        if found == 0:
            result = bot.sendMessage(chat_id, tampilData(), parse_mode='Markdown')
            members.append({'chat_id': chat_id, 'message_id': result['message_id']})
        else:
            result = bot.sendMessage(member['chat_id'], tampilData(), parse_mode='Markdown')
            member.update({'message_id': result['message_id']})
    print(members)

MessageLoop(bot, handle).run_as_thread()
print('Bot was ready')

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