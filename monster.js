var request = require('request');
var cheerio = require('cheerio');

var monster = (function() {

    var url = 'http://kiranico.com/es/mh4u/monstruo/';

    function parse_weakness(monster_json) {
        var parts = monster_json.monster.monsterbodyparts;
        var result = '';

        var weakness_json = {
            'Fire':0,
            'Ice':0,
            'Thunder':0,
            'Water':0,
            'Dragon':0
        }

        var usedparts=[];
        
        parts.map(function(i) {
            if (usedparts.indexOf(parseInt(i.pivot.monsterbodypart_id)) == -1) {
                
                weakness_json['Fire']+= parseInt(i['pivot']['res_fire']);
                weakness_json['Ice']+= parseInt(i['pivot']['res_ice']);
                weakness_json['Thunder']+= parseInt(i['pivot']['res_thunder']);
                weakness_json['Water']+= parseInt(i['pivot']['res_water']);
                weakness_json['Dragon']+= parseInt(i['pivot']['res_dragon']);

                usedparts.push( parseInt(i['pivot']['monsterbodypart_id']));
            }
        });

        Object.keys(weakness_json).map(function(a_weakness) {
            result += a_weakness + ' : ' + weakness_json[a_weakness] + '\n';
        });

        result += '\n';
        
        return result;        
    }


    function parse_reward(monster_json)
    {
        //On the original version we did a message
        //with multiple answers
        var message = {
            bajo : '',
            alto : '',
            g : ''
        };

        parts = monster_json.monster.monsterbodyparts;
        
        message.bajo = 'RANGO BAJO\n';
        message.alto = 'RANGO ALTO\n';
        message.g = 'RANGO G\n';
        
        parts = monster_json['monster']['items'];
        var firstime = true;
        var jold='';

        parts.map(function(i){
            jnew = i['pivot']['monsteritemmethod']['local_name']

            if (i['pivot']['rank']['local_name'] == 'Bajo') {
                if (jnew != jold && !firstime)
                   message.bajo += '======================================='
                                    + '===========\n';

               message.bajo += (i['local_name'] + ' ' 
                + i['pivot']['monsteritemmethod']['local_name'] 
                + ' ' + i['pivot']['percentage'] + '%');

               message.bajo += '\n';
            }

            else if (i['pivot']['rank']['local_name'] == 'Alto') {
                if (jnew != jold && !firstime)
                    message.alto += '====================================='
                                        + '=============\n';

                message.alto += (i['local_name']+ ' ' 
                    + i['pivot']['monsteritemmethod']['local_name'] + ' ' 
                    + i['pivot']['percentage'] + '%');

                message.alto += '\n';
            }

            else {
                if (jnew != jold && !firstime)
                    message.g += '========================================'
                                    + '==========\n';

                message.g += (i['local_name'] + ' ' 
                    + i['pivot']['monsteritemmethod']['local_name'] 
                    + ' ' + i['pivot']['percentage'] + '%');

                message.g += '\n';
            }

            firstime=false;

            jold = i['pivot']['monsteritemmethod']['local_name'];            
        });

        return message;
    }

    function get_monster_json (msg, rank_filter, parse_function, sender_function,
                              error, response, body)
    {

        if(!error && response.statusCode==200) {
            var $ = cheerio.load(body);

            //Parse JSON from inline script on the webpage
            var monster_json = $('script')[5].children[0].data;

            monster_json = monster_json.split('window.js_vars = ');
            monster_json = monster_json[1].split(';')[0];

            var message = parse_function(JSON.parse(monster_json));

        } else {
            var message = 'No he encontrado a ese monstruo :C';
        }

        //Message back
        var fromId = msg.chat.id;
        var options = {
            parse_mode : 'Markdown'
        };

        if(typeof(message) == "object") {
            if(rank_filter != null) {
                 sender_function(fromId, message[rank_filter], options);
            } else {

                Object.keys(message).map(function(rank) {
                    sender_function(fromId, message[rank], options);    
                });
            }

        } else {
            sender_function(fromId, message, options);  
        }
        
    }

    function find_weakness(msg, sender_function)
    {
        
        //Buscamos al monstruo 
        var message_args = msg.text.split(' ');
        var message_args_length = msg.text.split(' ').length;
        
        var my_url = url;

        if (message_args_length > 2) {
           message_args.shift();
           
           var sanitized_monster_name = message_args.map(function(i) {    
               return i.toLowerCase();                          
           });

           var monster_name_compound = sanitized_monster_name.join('-');
           my_url += monster_name_compound;   
        }

        else if (message_args_length == 2) {
            my_url += message_args[1].toLowerCase();
        }
        
        if (my_url != url)
            request(my_url,get_monster_json.bind(null,msg,null,parse_weakness,
                                            sender_function));
        else
            sender_function(msg.chat.id, 'No he encontrado a ese monstruo :C');
    }

    function find_reward(msg, sender_function)
    {
        //Function for getting the rewards
        var message_args = msg.text.split(' ');
        var message_args_length = msg.text.split(' ').length;

        var rank = message_args[message_args_length - 1].toLowerCase();
        
        var my_url = url;

        if (rank == 'alto' || rank == 'bajo' || rank == 'g')
            message_args.pop();
        else
            rank = null;
        
        if (message_args_length > 2) {
           message_args.shift();
           
           var monster_name_compound = message_args.map(function(i) {    
               return i = i.toLowerCase();                          
           }).join('-');

           my_url += monster_name_compound;   
        }

        else if (message_args_length == 2) {
            my_url += message_args[1].toLowerCase();
        }

        if (my_url != url) {
            request(my_url, get_monster_json.bind(null,msg,rank,parse_reward,
                                            sender_function));
        }
        else
            sender_function(msg.chat.id, 'No he encontrado a ese monstruo :C');

    }

    return {
        find_reward : find_reward,
        find_weakness : find_weakness
    }

})();

module.exports = monster;


