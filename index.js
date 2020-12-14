const Discord = require('discord.js')
const client = new Discord.Client()
const Database = require('./Database')
const database = new Database()
const OverwatchApi = require('./OverwatchApi')

const prefix = "`"
const commands = {
	"help": {
		"description": "Shows that message",
		"name": prefix + "help"
	},
	"ping": {
		"description": "Test command",
		"name": prefix + "ping"
	},
	"ov_start": {
		"description": "Start overwatch stats. `ov_start user#1234",
		"name": prefix + "ov_start"
	}
}

client.on('ready', () => {
	console.log('I am ready! motherfucker')
	client.user.setActivity("`help");
	database.createTable(
		'UserOverwatch', 
		'discord_id, TEXT',
		'battle_id, TEXT',
		'last_rank, TEXT'
	) 
	setInterval(checkUser, 5000);
})

client.on('message', message => {
	if (message.content.startsWith(getCommand('help'))) {
		message.channel.send(helpMessage())
	}
	if (message.content.startsWith(getCommand('ping'))) {
		//sendDm(message.author.id, 'ping')
		message.channel.send('bong!')
	}
	if (message.content.startsWith(getCommand('ov_start'))) {
		//message.channel.send("```" + message.content.split(' ') + "```")
		if (message.content.split(' ')[1] == undefined) {
			sendDm(message.author.id, "Battle id не может быть пустым")
		} else {
			battle_id = message.content.split(' ')[1]
			ovStart(message.author.id, battle_id)
		}
	}
})

function helpMessage() {
	msg = ''
	for( let el in commands){
		msg = msg + commands[el]['name'] + ' : ' + commands[el]["description"] + "\n" 
	}
	return "```" + msg + "```"
}

function getCommand(command) {
	return commands[command]["name"]
}

function sendDm(id, message) {
	client.users.cache.get(id).send(message)
}

function checkUser() {
	database.selectAllRows('UserOverwatch', checkUserCallback)
}

function checkUserCallback(rows) {
	rows.forEach(el => {
		overwatchApi = new OverwatchApi(el['battle_id'])
		overwatchApi.getRanks(value => {
			overwatchApiStatsCallback(value, el)
		})
	})
}

function overwatchApiStatsCallback(ranks, el) {
	// console.log(ranks['competitive']['tank'])
	// console.log(ranks['competitive']['damage'])
	// console.log(ranks['competitive']['support'])

	//console.log(el[])

	// if (ranks['competitive']['tank'] != el['last_rank']['tank'] || ranks['competitive']['damage'] != el['last_rank']['damage'] || ranks['competitive']['support'] != el['last_rank']['support']) {
	// 	database.insertValue('UserOverwatch', ['discord_id', 'battle_id, last_rank'], [el['discord_id'], el['battle_id'], ranks['competitive']])
	// 	client.users.cache.get(el['discord_id']).send('asdasdasd')//.send(ranks['competitive'])
	// }
}

function ovStart(discord_id, battle_id) {
	if (battle_id.split('#').length == 2) {
		database.selectViaBattlenet('UserOverwatch', battle_id, value => (
			ovStartCallback(value, discord_id, battle_id)
		))
	} else {
		sendDm(discord_id, "Проверьте свой battle id")
	}
}

function ovStartCallback(value, discord_id, battle_id) {
	if (value == undefined) {
		overwatchApi = new OverwatchApi(battle_id)
		overwatchApi.getRanks(value => {
			ovStartDbInsert(value, discord_id, battle_id)
		})
	} else {
		sendDm(discord_id, "Данный аккаунт уже есть в базе")
	}
}

function ovStartDbInsert(ranks, discord_id, battle_id) {
	database.insertValue('UserOverwatch', ['discord_id', 'battle_id, last_rank'], [discord_id, battle_id, JSON.stringify(ranks['competitive'])])
	sendDm(discord_id, "Аккаунт добавлен")
}


