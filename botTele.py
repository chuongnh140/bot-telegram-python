from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from botFunction import *
import os
from dotenv import load_dotenv


load_dotenv()
API_TOKEN_BOT_TELE = os.getenv("API_TOKEN")
updater = Updater(API_TOKEN_BOT_TELE, use_context=True)


def start(update: Update, context: CallbackContext):
    username = update.message.from_user.first_name
    update.message.reply_text("Hi {0}, Welcome to the ITNW-Bot. Please write /help to see the commands available.".format(username))
    
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands:
    /start - Start the bot
    /passwdgen - To gen strong random password
    /quotes - To get a random quote
    /cve - To get information about a CVE number
    /latest_cve - To get the 5 latest CVEs
    /check - Fast ping (ping 1 times)
    /ping - ping 5 times
    /trace - to tracert ip
    /port - Check open port
    /help - To get help""")
    
    
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
    
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
    
    

def passwdgen(update: Update, context: CallbackContext):
    passwd = genpass()
    update.message.reply_text("`{0}`".format(passwd),parse_mode='MarkdownV2')
    

def quotes(update: Update, context: CallbackContext):
    quo = quotes_bot()
    update.message.reply_text('<i>"{0}"</i> - <b>{1}</b>'.format(quo[0]["q"],quo[0]["a"]),parse_mode='HTML')



def cve_func(update: Update, context: CallbackContext):
    try:
        cve = str(context.args[0])
        result = cve_search(cve)
        if str(result) != "None":            
            id_cve = result["id"]
            assigner = result["assigner"]
            cvss = result["cvss"]
            summary = result["summary"]
            refer = result["references"]
            publish = result["Published"]
            update.message.reply_text("""Available information about <b>{0}</b>:
<b>ID</b>: {1}
<b>CVSS</b>: <strong>{2}</strong>
<b>Assigner</b>: {3}
<b>Published</b>: {4}
<b>Summary</b>: {5}
<b>References</b>: {6}""".format(id_cve, id_cve, cvss, assigner, publish, summary, refer[0:5]),parse_mode='HTML')
        else:
            update.message.reply_text("""<b>CVE not found</b>!!!
<i>Please check the ID of the CVE.</i>""",parse_mode='HTML')
    except (IndexError, ValueError):
        update.message.reply_text("""<b>Please enter a valid CVE number</b>.
<i>Example: /cve CVE-2022-1040</i>""",parse_mode='HTML')
        
        


def cve_latest_func(update: Update, context: CallbackContext):
    cve = cve_latest()
    top_5_latest_cve = [25, 26, 27, 28, 29]
    for i in top_5_latest_cve:
        id_cve = cve[i]["id"]
        publish = cve[i]["Published"]
        summary = cve[i]["summary"]
        update.message.reply_text("""
<b>ID</b>: {0}
<b>Published</b>: {1}
<b>Summary</b>: {2}""".format(id_cve, publish, summary),parse_mode='HTML')
    



def checkServerOnline(update: Update, context: CallbackContext):
    try:
        ip = str(context.args[0])
        result = checkOnline(ip)
        if result == 0:
            update.message.reply_text("""Server {0} <b>ONLINE</b> !!!""".format(ip),parse_mode='HTML')
        else:
            update.message.reply_text("""<b>Server {0} <b>OFFLINE</b> !!!""".format(ip),parse_mode='HTML')
    except (IndexError, ValueError):
        update.message.reply_text("""<b>Please check syntax</b>.
<i>Example: /check 10.18.200.101</i>""",parse_mode='HTML')
        


def ping_server_func(update: Update, context: CallbackContext):
    try:
        count_package = 5
        ip = str(context.args[0])
        cmd = 'ping -c 1 {0} > /dev/null 2>&1'.format(ip)
        for i in range(count_package):
            result = os.system(cmd)
            if result == 0:
                update.message.reply_text("<b>Ping {0} SUCCEEDED</b>, icmp_seq={1}".format(ip, i),parse_mode='HTML')
            else:
                update.message.reply_text("<b>Ping {0} FAILED</b>, icmp_seq={1}".format(ip, i),parse_mode='HTML')
    except (IndexError, ValueError):
        update.message.reply_text("""<b>Please check syntax</b>.
<i>Example: /ping 10.18.200.101</i>""",parse_mode='HTML')
        


def tracert_func(update: Update, context: CallbackContext):
    try:
        ip = str(context.args[0])
        result = trace(ip)
        update.message.reply_text(result)
    except(IndexError, ValueError):
        update.message.reply_text("""<b>Please check syntax</b>.
<i>Example: /trace 10.18.200.101</i>""",parse_mode='HTML')
        
        
def port_func(update: Update, context: CallbackContext):
    try:
        ip = str(context.args[0])
        port_number = str(context.args[1])
        result = port(ip, port_number)
        update.message.reply_text(result)
    except(IndexError, ValueError):
        update.message.reply_text("""<b>Please check syntax</b>.
<i>Example: /port 10.100.10.250 3389</i>""",parse_mode='HTML')





updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('passwdgen', passwdgen))
updater.dispatcher.add_handler(CommandHandler('quotes', quotes))
updater.dispatcher.add_handler(CommandHandler('cve', cve_func))
updater.dispatcher.add_handler(CommandHandler('latest_cve', cve_latest_func))
updater.dispatcher.add_handler(CommandHandler('check', checkServerOnline))
updater.dispatcher.add_handler(CommandHandler('ping', ping_server_func))
updater.dispatcher.add_handler(CommandHandler('trace', tracert_func))
updater.dispatcher.add_handler(CommandHandler('port', port_func))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
