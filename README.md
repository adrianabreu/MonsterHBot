#Monster Hunter Bot
This is a bot designed to extract info from kiranico and print into a telegram chat.

#Scraper
Scraping is the art of reading some web content and parse it to extract information. My python just test
the kiranico web where I extract the whole information.

Kiranico stores the data in a json variable, so I parsed it on python and I extrac the info I need.

#Telegram Bot
A telegram bot is a powerful option. This was initalli based on telebot library and now on telegram api.
If you want to use it add it to a group on @MonsterHBot 

#Usage 
Type /debilidades monstername
It will print the weakness of that monster
If you want to look for rewards type /recompensa monstername
It will send you the rewards of the monster
Now you can filter information passing the rank to if, for example:
/recompensa kirin g
And it will only show you the reward that kirin in g rank gives.

If no given name or bad name it will show error.
If kiranico goes down the bot will announce it.

##To Do:
  1. Look for armor sets
  2. More control errors
  3. When md is ready, use it to format output
