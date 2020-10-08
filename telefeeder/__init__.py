import telegram
import feedparser
from telegram import ParseMode
import html2text
import random
import schedule
import time
import ast

def autoposting(rss_file_path,TELEGRAM):
    with open('{}'.format(rss_file_path)) as file: # Opening the rss feed list
        list = file.readlines()

    feedlist = [list[i].rstrip() for i in range(len(list))]
    Feed = feedparser.parse(random.choice(feedlist))
    rands = random.randint(0, len(Feed.entries)-1)
    print(len(Feed.entries), rands)
    entry = Feed.entries[rands]
    print(entry.link)
    bot = telegram.Bot(token=TELEGRAM['bot_token'])
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.images_to_alt = True
    h.ignore_emphasis = True
    text = h.handle(entry.summary)
    msg = "\n\n"
    msg += '<b> {} </b>'.format(entry.title) + '\n\n' + '{}'.format(text)
    msg += "Read More:" + ' [<a href="'+ entry.link +'"> Source </a>]'
    msg += ' \n\n' + '#articles' + '\n\n' + 'Follow: {}'.format(TELEGRAM['channel_1'])
    status = bot.send_message(chat_id=TELEGRAM['channel_1'], text = msg ,caption=msg, parse_mode=ParseMode.HTML)
    print('Posted!')

# Opening the token information:
f = open('token_info.txt', "r")
contents = f.read()
TELEGRAM = ast.literal_eval(contents)
f.close()


autoposting(rss_file_path='rss_feeds.txt', TELEGRAM = TELEGRAM['channel_1'])
schedule.every(15).minutes.do(autoposting)


# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
   schedule.run_pending()
   time.sleep(1)
