from email import message
from datetime import datetime
import time
import pandas as pd 
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
    Update,
    ParseMode,
    bot,
    Poll
)
from telegram.ext import (
     Updater,
     MessageHandler,
     CommandHandler,
     ConversationHandler,
     CallbackContext,
     Filters,
)

# data

chat_data = {}
# login_data = {  "B171413": {'pwd': '#Sandeep', 'login': 1},
#                 "B171415": {'pwd':"#matla", 'login': 0},
#                 "B171452": {'pwd':"#payili", 'login':0}
#              }

login_data = {}

Reviews = {     
                "review_date":None,
                "B171413": {'breakfast':{'flag':0,'rating':None} , 'lunch':{'flag':0,'rating':None}, 'dinner':{'flag':0,'rating':None}},
                "B171415": {'breakfast':{'flag':0,'rating':None} , 'lunch':{'flag':0,'rating':None} ,'dinner':{'flag':0,'rating':None}},
                "B171452": {'breakfast':{'flag':0,'rating':None} , 'lunch':{'flag':0,'rating':None} ,'dinner':{'flag':0,'rating':None}}
}
Top_comments = {}
globals = {}

def load_data():
    global login_data

    log = open('logins.csv','r')
    for user in log.readlines():
        user = user.split(',')
        data = {'pwd': user[1], 'login': int(user[2])}
        login_data[user[0]] = data
    log.close()

    chat = open('chat.csv','r')
    for user in chat.readlines():
        user = user.split(',')
        chat_data[user[0]] = int(user[1])
    chat.close()
def show_data():
    print()
    # printing data
    for id,data in login_data.items():
        print(id ," : ", data)
    print()
    for id,chat_id in chat_data.items():
        print(id ," : ", chat_id)
    print()

def store_data():
    #login_data
    f = open('logins.csv','w')
    for id,data in login_data.items():
        row = id
        for val in data.values():
            row += ','+str(val)
        f.write(row+'\n')
    f.close()

    f = open('chat.csv','w')
    for id,chat_id in chat_data.items():
        f.write(id + ',' +str(chat_id)+'\n')
    f.close()
def print_reviews():
    print('ID Number\t'+'breakfast\t'+'lunch\t'+'Dinner')
    for id,feed in Reviews.items():
        if(id == 'review_date'):
            continue
        if(feed['breakfast']['rating'] == None and feed['lunch']['rating'] == None and feed['dinner']['rating'] == None):
            continue
        rate = str(feed['breakfast']['rating']) +'\t'+ str(feed['lunch']['rating']) +'\t'+str(feed['dinner']['rating'])

        # rate.replace('None',' ')
        print(id+'\t\t'+rate+'\n')
def store_feedback():

    ctime = datetime.now()
    cdate = ctime.isoformat()
    cdate = cdate[0:10]
    reviews_file = cdate+'.csv'
    f = open( reviews_file,'w')
    f.write(cdate + '\n')
    f.write('ID Number,'+'breakfast,'+'lunch,'+'Dinner')
    for id,feed in Reviews.items():
        if(id == 'review_date'):
            continue
        rate = str(feed['breakfast']['rating']) +','+ str(feed['lunch']['rating']) +','+str(feed['dinner']['rating'])
        # rate.replace('None',' ')
        f.write(id + ','+ rate +'\n')
    
    f.close()
    

def Reset_reviews():
    for id in login_data.keys():
    
        reset= {'breakfast':{'flag':0,'rating':None} , 'lunch':{'flag':0,'rating':None}, 'dinner':{'flag':0,'rating':None}}
        Reviews[id] = reset

def update_logins(update,id,data_dict):
    try:
        # logging in
        login_data[id] = data_dict
        
        chat_data[id] = update.message.chat.id
        print("⚠ Alert! chat id of ",id,"has changed ")
        store_data()
    except KeyError:
        # registering
        print('Registered ☺')
        login_data[id] = data_dict

        Reviews[id] = {'breakfast':{'flag':0,'rating':None} , 'lunch':{'flag':0,'rating':None} ,'dinner':{'flag':0,'rating':None}}
        store_data()

    print("Data Altered :\n")
    
    show_data()

def get_key(dict,val):

    # using inddexing
    try:
        val_ind = list(dict.values()).index(val)
    except ValueError:
        return ValueError

    key = list(dict.keys())[val_ind]

    return key

#________________________________________
# _________ commands & states ___________
#________________________________________


def start(update:Update , context : CallbackContext):

    #" Ask to login "
    greet = " Welcome to Mess Feedback Bot. \n \t-By Tech SGC\n\n"
    login_msg = "Enter Student Id to login \n"
    msg = greet+login_msg
    update.message.reply_text(msg,parse_mode = ParseMode.HTML)

    return SignUP

def SignUP(update:Update,context:CallbackContext):

    user = update.message.from_user
    id = update.message.text
    chat_id = update.message.chat_id
    if(chat_id in chat_data.values() and get_key(chat_data,chat_id) != id):
        msg = 'Another ID is currently logged in in this device.\n\n please logout by /logout. before logging in with another id .'
        context.bot.send_message(chat_id,msg)

    if(login_data.get(id) == None):
        password = "#Sandeep"

        update_logins(update,id,{'pwd':password, 'login': 0})
        reset= {'breakfast':{'flag':0,'rating':None} , 'lunch':{'flag':0,'rating':None}, 'dinner':{'flag':0,'rating':None}}
        Reviews[id] = reset

        reply = "This is Your password "+ password +"\n You have to use every time login with '/start' command "

        update.message.reply_text(reply,parse_mode = ParseMode.HTML)

        store_data()
        print(login_data)
        return ConversationHandler.END
    else:
        # if user have already logged in another acc
        if(login_data[id]['login'] == 1):
            if(chat_data[id] == update.message.chat.id):
                context.bot.send_message(update.message.chat.id,'You\'ve already logged in. Give your /Feedback\n or refer /help.')
            else:
                context.bot.send_message(update.message.chat.id,'Sorry!😞. You\'r currently logged in another account. You Can\'t give feedback.')
            return ConversationHandler.END
        reply = "Enter YOur Password ."
        update.message.reply_text(reply,parse_mode = ParseMode.HTML)

        globals["curr_id"] = id
        return Login


    print(id)
    print(login_data)

def Login(update:Update,context : CallbackContext) :
    passwrd = update.message.text
    id = globals.get("curr_id")
    
    if(passwrd.lower() == "help"):
        print("help")
        help(update,context)
        return ConversationHandler.END
    
    # If user id not found in data
    if(id == None):
        reply = "You have not registered.\n\n Enter your ID"
        update.message.reply_text(reply,parse_mode = ParseMode.HTML)

        # Ask him to sign up 
        MessageHandler(Filters.text & ~Filters.command, SignUP)

    # Registered User
    elif(login_data[id]["pwd"] == passwrd):
        reply = "Your Logged in :). "
        login_data[id]["login"] = 1
        chat_data[id] = update.message.chat.id

        store_data()
        show_data()
        about = "Now You can tell about what you eat by giving /Feedback."
        update.message.reply_text(reply + about,parse_mode = ParseMode.HTML)

        return ConversationHandler.END
    else:
        reply = "Invalid Credentials 😟\n\n"
        action = "Enter Your password again || Enter /help to contact Tech SGC "
        update.message.reply_text(reply+action ,parse_mode = ParseMode.HTML)

        return Login
  
def help(update:Update , context : CallbackContext):
    print("In help")
    reply  = "Change Password : /changePwd \n\n Forgot Password: /resetpwd \n\n for other help contact sgc.tech@rgukt.ac.in"
    update.message.reply_text(reply,parse_mode = ParseMode.HTML)

    return ConversationHandler.END

def Feedback(update:Update, context : CallbackContext):
    print("Feedback :")
    chat_id = update.message.chat.id
    print(chat_id)
    try:
        id = get_key(chat_data,chat_id)
    except ValueError:
        print("Chat id of this account not present in chat_data \n Your not logged in ")
        msg  = 'You\'r not logged in login using \start command'
        update.message.reply_text(msg)
    
    ctime = datetime.now()
    print('time : {}:{}:{}'.format(ctime.hour,ctime.minute,ctime.second))
    print('Feedback by "',id,'"')

    # if reviwes dict contains a data of previous day -- have to refresh it.
    if(Reviews['review_date']== None):
        Reset_reviews()
    elif( Reviews['review_date'].day != ctime.day): # or (Reviews['review_date']-ctime).days != 0): 
        Reset_reviews()
    
    Reviews['review_date'] = ctime
    
    msg = "Choose Session 👇"
    session_board = []
    rev_todo = []
    if(Reviews[id]['breakfast']['flag'] == 0 and ctime.hour>6): # breakfast review starts from 6:00 am
        session_board += [[KeyboardButton('breakfast')]]
        rev_todo.append('breakfast')
    if(Reviews[id]['lunch']['flag'] == 0 and ctime.hour>12 ):   # lunch review starts from 12:00 pm 
        session_board += [[KeyboardButton('lunch')]]
        rev_todo.append('lunch')
    if(Reviews[id]['dinner']['flag'] == 0 and ctime.hour>18 ):  # Dinner review starts from 6:00 pm
        session_board += [[KeyboardButton('dinner')]]
        rev_todo.append('dinner')
    
    # No feedback is due
    if(session_board == []):
        msg = 'Your Feedback is Already Concerned . Thank You and Come again 😊'
    session_board = ReplyKeyboardMarkup(session_board,resize_keyboard = False,one_time_keyboard = True)
    context.user_data['review_todo'] = rev_todo
    context.bot.send_message(chat_id,msg,reply_markup = session_board)

    return Session_review

def Session_review(update,context):
    chat_id = update.message.chat.id
    id = get_key(chat_data,chat_id)
    
    session = update.message.text
    try:
        if(Reviews[id][session]['flag'] == 1):
            msg = 'Your Feedback is already Concerned'
            context.bot.send_message(chat_id,msg,reply_markup = ReplyKeyboardRemove())
            return ConversationHandler.END
    except KeyError:
        msg = 'Please choose valid Session.'
        context.bot.send_message(chat_id,msg,reply_markup = ReplyKeyboardRemove())
        return Feedback(update,context)
        
    context.user_data ["session"] = session # storing session to pass into store_review state

    msg = "Enter your Feedback : "
    rating_board = [[KeyboardButton('Delicious 😋')],
            [KeyboardButton('Good 😊')],
            [KeyboardButton('Average 😐')],
            [KeyboardButton('Worst 😫')],
            [KeyboardButton('Medicore 🤢')],
            [KeyboardButton('Mess la thinani batch')]
        ]
    reply_keyboard = ReplyKeyboardMarkup(rating_board,resize_keyboard= False,one_time_keyboard= True)
    context.bot.send_message(update.message.chat.id,text = msg,reply_markup = reply_keyboard)
    return store_review

def store_review(update,context):
    # state : reads the revie given by session_review and stores into data base.
    chat_id = update.message.chat.id
    id = get_key(chat_data,chat_id)
    ratings = {'Delicious':5,
                'Good':4,
                'Average':3,
                'Worst':2,
                'Medicore':1
                }
    
    rating_msg  = update.message.text[0:-2] # removing emojies
    if(rating_msg == 'Mess la thinani bat'):
        msg = "Hope you had great 🙂."
        context.bot.send_message(update.message.chat.id,msg,reply_markup = ReplyKeyboardRemove())

        return ConversationHandler.END

    #stroring review
    session = context.user_data['session']
    try:
        Reviews[id][session]['rating'] = ratings[rating_msg]
        Reviews[id][session]['flag'] = 1
    except KeyError:
        print('rating msg not found')
        msg = 'Rating msg not found. Please try again.\n/Feedback'
        context.bot.send_message(update.message.chat.id,msg)
    # print(Reviews)

    print_reviews()
    store_feedback()
    todo = context.user_data['review_todo']
    todo.remove(session)
    todo_msg = ''
    msg  = 'Your Feedback recieved 😊.\nThank you for your feed back\n\n'
    if(len(todo)!=0):
        todo_msg = ' Continue giving feedback for your\n\n'
        for session in todo:
            todo_msg +=  session.upper()+str('\n')
        todo_msg += '\n\nhere /Feedback'
    
    context.bot.send_message(update.message.chat.id,msg + todo_msg,reply_markup = ReplyKeyboardRemove())
    
    if(len(todo)!=0):
        msg = 'Continue chating with me by \n\n'
        commands = ' /Feedback \n /help'

    # comment_board = [
    #                     [KeyboardButton('')]]

    return ConversationHandler.END



    

# def main():

print("Running .........")

load_data()
show_data()
updater = Updater("5204195525:AAGnKWgsi33FwshRCxPrDRDkwYiMNUJcN-4",use_context = True)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler("start",start),CommandHandler("help",help),CommandHandler("FeedBack",Feedback)],
    states = {
        SignUP : [MessageHandler(Filters.text & ~Filters.command, SignUP)],
        Login  : [MessageHandler(Filters.text & ~Filters.command, Login)],
        store_review : [MessageHandler(Filters.text & ~Filters.command , store_review)],
        Session_review : [MessageHandler(Filters.text & ~Filters.command , Session_review)],
       # Feed_receive : [PollAnswerdfbHandler()] 
        
        },
    fallbacks = []
    
)

updater.dispatcher.add_handler(conv_handler)

# Start the Bot
updater.start_polling()
updater.idle()

# if __name__ == "main":
#     main()