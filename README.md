#Monster Hunter Bot
This bot is designed to extract info from kiranico and print into a telegram
chat.

#Scraping
Scraping is the art of reading some web content and parse it to extract 
information. 

Kiranico stores the data in a json variable, so I parsed it and I just navigated
throught it in order to extract the needed data.

#Telegram Bot
A telegram bot is a powerful option. This bot was initially done on Python,
but Javascript is cooler.

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
