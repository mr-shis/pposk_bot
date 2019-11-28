
import qrcode
import PIL
from PIL import Image, ImageFilter,ImageFont, ImageDraw
import datetime
import sqlite3
import  requests 

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update





def card(fname,sname,tname,inst,p_numb):
    sp_num=len(p_numb)
    t=""
    for i in range(6-sp_num):
        t+="0"
    p_numb=t+p_numb
    allh=125
    try:  
        original = Image.open("bg.png")  
    except FileNotFoundError:  
        print("Файл не найден")
   
    W,H=(500,800)
    print("The size of the Image is: ")  
    print(original.format, original.size, original.mode)
    draw = ImageDraw.Draw(original)
    font = ImageFont.truetype("fonts/3952.ttf",40)
    
    text=fname
    w,h=draw.textsize(text,font)
    draw.text(((W-w)/2,allh), text,font=font,fill="#123f8d")
    allh+=h+5
    text=sname
    w,h=draw.textsize(text,font)
    draw.text(((W-w)/2,allh), text,font=font,fill="#123f8d")
    allh+=h+5
    text=tname
    w,h=draw.textsize(text,font)
    draw.text(((W-w)/2,allh), text,font=font,fill="#123f8d")
    allh+=h+5
    text=inst
    w,h=draw.textsize(text,font)
    draw.text(((W-w)/2,allh), text,font=font,fill="#123f8d")
    allh+=h+5
    text="Номер билета: "+p_numb
    font = ImageFont.truetype("fonts/3952.ttf",40)
    w,h=draw.textsize(text,font)
    draw.text(((W-w)/2,allh), text,font=font,fill="#123f8d")
    allh+=h+5
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
        )

    now = datetime.datetime.now()
    qr_str="Подтверждение: "+p_numb+" "+fname+" "+sname+" от "+str(now.date())
    qr.add_data(qr_str)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('qr.png')
    try:  
        img = Image.open("qr.png")
        img=img.convert('RGB')
    except FileNotFoundError:  
        print("Файл не найден")
    print(img.format, img.size, img.mode)
    img=img.resize((400,400))
    iw,ih=img.size[0],img.size[1]
    original.paste(img,(int((W-iw)/2),H-ih-10))
    original.show()
    original.save("1.png")
def serch(nm):
    conn = sqlite3.connect("pposk_sql_db.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM chlen WHERE num=?"
    cursor.execute(sql, [(str(nm))])
    arr=cursor.fetchall()
    nb,p_numb,name,inst,ee=arr[0]
    ar_name=name.split()
    print(arr[0])
    fname= ar_name[0] if (len(ar_name)>=1) else " "
    sname= ar_name[1] if (len(ar_name)>=2) else " "
    tname= ar_name[2] if (len(ar_name)>=3) else " "
    if(inst=="Институт Международного транспортного менеджмента"): inst="ИМТМ"
    if(inst=="Институт Водного Транспорта"): inst="ИВТ"
    if(inst=="Институт Морская Академия"): inst="ИМА"
    card(fname,sname,tname,inst,p_numb)

#nm=input("Введите номер")
#serch(nm)
#input("Жмякни")
token="994898066:AAHQ_Rxca1U6fx8qH8Y4xalXAQ_PkaSDxts"
greet_bot = BotHandler(token)  
greetings = ('здравствуй', 'привет', 'ку', 'здорово')  
now = datetime.datetime.now()


def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()