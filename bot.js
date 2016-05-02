#!/bin/env node
var TelegramBot = require('node-telegram-bot-api');
var monster = require('./monster');


// Bot setup
var token = 'YOUR_TOKEN';

// Setup webhook
var bot = new TelegramBot(token);
bot.setWebHook('YOUR_WEBHOOK' + bot.token);


console.log('bot server started...');
// End bot setup

//Callback for wrapping bot.sendMessage
function sendMessageBack(id, message, options) {
    //console.log(id,message,options); //debug purposes
    bot.sendMessage(id, message, options);
}

// Matches /debilidades monster]
bot.onText(/\/debilidades ([a-zA-Z\s*]+)/, function (msg, match) {

    monster.find_weakness(msg, sendMessageBack);
});

// Matches /recompensa monster
bot.onText(/\/recompensa ([a-zA-Z\s*]+)/, function (msg, match) { 
    monster.find_reward(msg, sendMessageBack);
});


module.exports = bot;