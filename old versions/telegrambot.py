import pandas as pd 
from telegram import (
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

answer = {}
login_data = {  "B171413": {'pwd': '#Sandeep', 'login': 1},
                "B171415": {'pwd':"#matla", 'login': 0},
                "B171452": {'pwd':"#payili", 'login':0}
             }
Sid_chat_data = {}
globals = {}
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
    if(login_data.get(id) == None):
        password = "#Sandeep"
        login_data[id] = {"pwd":password,"login" : 1}

        reply = "This is Your password "+ password +"\n You have to use every time you freshly start the bot with '/start' command "

        update.message.reply_text(reply,parse_mode = ParseMode.HTML)

        print(login_data)
        return ConversationHandler.END
    else:
        reply = "Enter YOur Password ."
        update.message.reply_text(reply,parse_mode = ParseMode.HTML)

        globals["curr_id"] = id
        return Login


    print(id)
    print(login_data)

def Login(update:Update,context : CallbackContext) :
    passwrd = update.message.text
    id = globals.get("curr_id")

    # If user id not fiund in data
    if(passwrd.lower() == "help"):
        print("help")
        help(update,context)
        return ConversationHandler.END
    

    if(id == None):
        reply = "You have not registered.\n\n Enter your ID"
        update.message.reply_text(reply,parse_mode = ParseMode.HTML)

        # Ask him to sign up 
        MessageHandler(Filters.text & ~Filters.command, SignUP)

    # Registered User
    elif(login_data[id]["pwd"] == passwrd):
        reply = "Your Logged in :). "
        login_data[id]["login"] = 1
        print(login_data)
        about = "Now You can tell about what you eat ."
        update.message.reply_text(reply + about,parse_mode = ParseMode.HTML)
    else:
        reply = "Invalid Credentials 😟\n\n"
        action = "Enter Your password again || Enter help to contact Tech SGC "
        update.message.reply_text(reply+action ,parse_mode = ParseMode.HTML)

        return Login
  
def help(update:Update , context : CallbackContext):
    print("In help")
    reply  = "Change Password : /changePwd \n\n Forgot Password: /resetpwd \n\n"
    update.message.reply_text(reply,parse_mode = ParseMode.HTML)

    return ConversationHandler.END

def Feedback(update:Update,context:CallbackContext):
    print("Feedback")
    
    options = ['5','4','3','2','1']

    poll_msg = context.send_poll(update.chat.id,"Rate Your Food :",options,allows_multiple_answers=False)

    payload= {
           poll_msg.poll.id:{
                "options":options,
                "message":poll_msg.message_id,
                "chat_id": update.chat.id,
                "ratings": 0,
            }
        }
    context.bot_data.update(payload)

def Feed_receive(update,context):

    answer = update.poll_answer
    poll_id = answer.poll_id
    try:
        options = context.bot_data[poll_id]["options"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    rating = answer.option_ids
    msg = "Thank You for your Response 🙂."
    context.bot.send_message(context.bot[poll_id]["chat_id"] , text = msg)    




# def main():

print("Running .........")
updater = Updater("5204195525:AAGnKWgsi33FwshRCxPrDRDkwYiMNUJcN-4",use_context = True)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler("start",start),CommandHandler("help",help),CommandHandler("FeedBack",Feedback)],
    states = {
        SignUP : [MessageHandler(Filters.text & ~Filters.command, SignUP)],
        Login  : [MessageHandler(Filters.text & ~Filters.command, Login)],
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