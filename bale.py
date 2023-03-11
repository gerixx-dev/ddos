#LydiaTeam


from telebot import types
import telebot, os, random
import requests
from ast import literal_eval

admin = [5129249246]
btoken =  "6076861700:AAHeeiykww5n3NhnLhAhCWP6pQeWMEbHyig"
#url = "https://web.bale.ai/login"

bot = telebot.TeleBot(btoken)

request_headers = {

    'authority': 'next-api.bale.ai',
    'method': 'POST',
    'accept': 'application/grpc-web-text',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '152',
    'content-type': 'application/grpc-web-text',
    'cookie': '_ga=GA1.1.1530819521.1676153465; _ga_M7ZV898665=GS1.1.1676195727.2.1.1676196141.60.0.0',
    'origin': 'https://web.bale.ai',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-grpc-web': '1',
    'x-user-agent': 'grpc-web-javascript/0.1',

}

def perform_headers(token, path):
    perform_header = {

    'authority': 'next-api.bale.ai',
    'method': 'POST',
    'scheme': 'https',
    'path': f'{path}',
    'accept': 'application/grpc-web-text',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '36',
    'content-type': 'application/grpc-web-text',
    'cookie': f'access_token={token};',
    'origin': 'https://web.bale.ai',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'ec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-grpc-web': '1',
    'x-user-agent': 'grpc-web-javascript/0.1',

    }

    return perform_header

def login(message, res):
    auth = message.text
    rphone = open('./data/number.txt', 'r').read()
    chatid = message.chat.id
    response_decode = decode_grpc(res)
    result = response_decode['1:2']

    verify_encode = encode_grpc({'1:2': f'{result}', '2:2': f'{auth}', '3:2': {'1:0': 1}})
    sendcode = requests.post('https://next-api.bale.ai/bale.auth.v1.Auth/ValidateCode', data=verify_encode, headers=request_headers)

    if sendcode.status_code == 200:
        res_decode = decode_grpc(sendcode.text)
        resresult = res_decode['2:2']['2:0']
        resresult2 = res_decode['4:2']['1:2']

        sid = open('./data/sid.txt', 'w')
        sid.write(f"{resresult}")
        sid.close

        accesstoken = open('./data/token.txt', 'w')
        accesstoken.write(f"{resresult2}")
        accesstoken.close
        print(resresult)
        bot.send_message(chatid, f"✅ You have successfully logged in.\n📞 Phone : {rphone}")
    else:
        bot.send_message(chatid, f"❌ Somthing wrong :/")

def makeKeyboard(number=None):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="👤 PhoneNumber :",
                                            callback_data="phone"),
        types.InlineKeyboardButton(text=f"{number}",
                                callback_data="jyjytyjyj")),
    
    markup.add(types.InlineKeyboardButton(text="📝 Set Text ",
                                            callback_data="settext"),
        types.InlineKeyboardButton(text=f"🔎 Login",
                                callback_data="login")),
    
    markup.add(types.InlineKeyboardButton(text="Edit Name",
                                            callback_data="ename"),
        types.InlineKeyboardButton(text="Edit Bio",
                                callback_data="ebio")),

    markup.add(types.InlineKeyboardButton(text="🪜 Send",
                                        callback_data="sender")) 
                      
    return markup

def setphonenumber(message):
    number = message.text
    lnumber = list(message.text)

    if len(lnumber) == 12:
        psaver = open('./data/number.txt', 'w', encoding='utf-8')
        psaver.write(number)
        psaver.close()
        bot.send_message(message.chat.id, "✅ Your PHONENUMBER changed successfully.")

    else:
        bot.send_message(message.chat.id, "❌ Please send me a valid PHONENUMBER .")

def settext(message):
    text = message.text

    psaver = open('./data/message.txt', 'w', encoding='utf-8')
    psaver.write(text)
    psaver.close()
    bot.send_message(message.chat.id, "✅ Your Text Changed successfully.")

def editname(message):
    text = message.text.encode("utf-8").decode('unicode-escape')
    raccesstoken = open('./data/token.txt', 'r').read()
    ename_encode = encode_grpc({'1:2': f'{text}'})
    ename = requests.post('https://next-api.bale.ai/bale.users.v1.Users/EditName', data=ename_encode, headers=perform_headers(raccesstoken, '/bale.users.v1.Users/EditName'))
    if ename.status_code == 200:
        bot.send_message(message.chat.id, "✅ Your name Changed successfully.")

def editbio(message):
    text = message.text.encode("utf-8").decode('unicode-escape')
    raccesstoken = open('./data/token.txt', 'r').read()
    ebio_encode = encode_grpc({'1:2': {'1:2': f'{text}'}})
    ebio = requests.post('https://next-api.bale.ai/bale.users.v1.Users/EditAbout', data=ebio_encode, headers=perform_headers(raccesstoken, '/bale.users.v1.Users/EditAbout'))
    if ebio.status_code == 200:
        bot.send_message(message.chat.id, "✅ Your biography changed successfully.")


def decode_grpc(string):
    result = requests.post('http://zocaoe.com/decode', data={"string": f"{string}"})
    if result.status_code == 200:
        return eval(result.text)

def encode_grpc(string):
    result = requests.post('http://zocaoe.com/encode', data={"string": f"{string}"})
    if result.status_code == 200:
        return result.text

def checknumbers(num):
    phonelist = num.splitlines()

    for number in phonelist:
        listnumber = list(number)

        if not number.isdigit():
            result = False
            break

        elif not number.startswith("98"):
            result = False
            break

        elif not len(listnumber) == 12:
            result = False
            break

        elif number.isdigit():
            result = True
    
    return result
        
def sender(message):
    #text = message.text.splitlines()
    chatid = message.chat.id
    readmessage = open('./data/message.txt', 'r', encoding='utf-8').read().encode("utf-8").decode('unicode-escape')
    raccesstoken = open('./data/token.txt', 'r').read()

    rsid = open('./data/sid.txt', 'r').read()
    phone_list = message.text.splitlines()
    if checknumbers(message.text):

        for number in phone_list:
            #randomname maker
            listname = ["turk", "jungle", "mmd", "arash", "ahmad", "mobina", "sara", "nahid", "mojtaba", "alex", "kordkolbar"]
            rndrange = random.randrange(00000, 99999)
            rndname = random.choice(listname)
            fullname = f"{rndname}{rndrange}"
            
            #hunt for Contact
            #also u can hunt for contact to check it exist or not

            #Import Contact 
            grcpencode = encode_grpc({'1:2': {'1:0': int(number), '2:2': {'1:2': f'{fullname}'}}})
            importco = requests.post('https://next-api.bale.ai/bale.users.v1.Users/ImportContacts', data=grcpencode, headers=perform_headers(raccesstoken, '/bale.users.v1.Users/ImportContacts'))
            importco_response = decode_grpc(importco.text) #response import contact
            if importco.status_code == 200 and "4:2" in importco_response:
                #Sendmessage
                user_id = importco_response['4:2']['1:0']
                grcpmsg = encode_grpc({'1:2': {'1:0': 1, '2:0': int(user_id)}, '2:0': int(rsid), '3:2': {'15:2': {'1:2': f'{readmessage}'}}})
                print(grcpmsg)
                sendmsg = requests.post('https://next-api.bale.ai/bale.messaging.v2.Messaging/SendMessage', data=grcpmsg, headers=perform_headers(raccesstoken, '/bale.messaging.v2.Messaging/SendMessage'))
                if sendmsg.status_code == 200:
                    bot.send_message(chatid, f"sent to {number} ✅")
                else:
                    bot.send_message(chatid, "message could not be sent ❌")
            else:
                bot.send_message(chatid, "Probably user_id does not exist. ❌")
    else:
        bot.send_message(chatid, "Please send me valid number boy :/")



@bot.message_handler(commands=['start'])
def handle_command_adminwindow(message): 
    user_id = message.chat.id
    if os.path.isfile('./data/number.txt'):
        rphone = open('./data/number.txt', 'r').read()
        bot.send_message(chat_id=message.chat.id,
                text=f"Welcome to bale sender .",
                reply_markup=makeKeyboard(rphone),
                parse_mode='HTML')
    else:

        bot.send_message(chat_id=message.chat.id,
            text=f"Welcome to bale sender .",
            reply_markup=makeKeyboard(),
            parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    if chat_id in admin:
        if (call.data.startswith("phone")):
            input_text = bot.send_message(chat_id, '📞 Send me your PhoneNumber for Login (989121478259) :')
            bot.register_next_step_handler(input_text, setphonenumber)

        elif (call.data.startswith("settext")):
            input_text = bot.send_message(chat_id, '✏️ Send me your textmessaeg :')
            bot.register_next_step_handler(input_text, settext)
            
        elif (call.data.startswith("sender")):
            input_text = bot.send_message(chat_id, '✏️ Send me your PhoneNumbers for send message (989121478259) :')
            bot.register_next_step_handler(input_text, sender)


        elif (call.data.startswith("ename")):
            input_text = bot.send_message(chat_id, '✏️ Send me your name :')
            bot.register_next_step_handler(input_text, editname)
            
        elif (call.data.startswith("ebio")):
            input_text = bot.send_message(chat_id, '✏️ Send me your biography :')
            bot.register_next_step_handler(input_text, editbio)

        elif (call.data.startswith("login")):
            if os.path.isfile('./data/number.txt'):
                bot.send_message(chat_id, "🕔Please wait ...")
                rphone = open('./data/number.txt', 'r').read()
                
                grcpencode = encode_grpc({'1:0': int(rphone), '2:0': 4, '3:2': 'C28D46DC4C3A7A26564BFCC48B929086A95C93C98E789A19847BEE8627DE4E7D', '4:2': 'Chrome, Windows', '5:2': 'Chrome, Windows'})
                loginn = requests.post('https://next-api.bale.ai/bale.auth.v1.Auth/StartPhoneAuth', data=grcpencode, headers=request_headers)
                if loginn.status_code == 200:
                    input_text = bot.send_message(chat_id, '✏️ Send me your AUTH Code (i will send it to your PHONENUMBER) :')
                    bot.register_next_step_handler(input_text, login, loginn.text)
                else:
                    bot.send_message(chat_id, "❌ There is problem :/")

bot.infinity_polling()
#u can use while loop .

#LydiaTeam