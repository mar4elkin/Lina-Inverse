const Discord = require('discord.js')
const client = new Discord.Client()
const Database = require('./Database')
const database = new Database()
const OverwatchApi = require('./OverwatchApi')
const ImageCreater = require('./ImageCreater')
const fs = require('fs')

const prefix = "`"
const commands = {
	"help": {
		"description": "Справка по командам",
		"name": prefix + "help"
	},
	"ping": {
		"description": "Тестовая команда",
		"name": prefix + "ping"
	},
	"ov.add": {
		"description": "Добавление отслеживаемых профилей",
		"name": prefix + "ov.add"
	},
	"bot.settings": {
		"description": "Настройка бота",
		"name": prefix + "bot.settings"
	}
}

client.on('ready', () => {
	console.log('I am ready! motherfucker')
	client.user.setActivity("`help")

	database.createTable(
		'Discord', 
		'server_id, TEXT',
		'channel_id, TEXT'
	)

	database.createTable(
		'UserOverwatch', 
		'discord_id, TEXT',
		'battle_id, TEXT',
		'last_rank, TEXT',
		'games, TEXT'
	)
	
	//console.log(client.guilds.forEach(el => el.id))
	database.selectAllRows('Discord', rows => {
		if (rows != undefined) {
			if (rows != []) {
				rows.forEach(row => {
					client.guilds.cache.find(guild_el => {
						if (row['server_id'] == guild_el.id) {
							client.channels.cache.get(row['channel_id']).send("Перезагружен и готов убивать!")
						}
					})
				})
			}
		}
	})
})

client.on('message', message => {
	setInterval(checkUser, 3600000)
	//checkUser()

	if (message.content == (getCommand('bot.settings'))) {
		message.channel.send(
			'```Доступные настройки:\n' +
			'1) Канал для бота (`bot.settings.channel "название канала")\n' +
			'Для выбора используйте цифру нужного варианта.\n'+
			'Чтобы выйти `bot.settings.exit ```'
		)
		botSettings(message)
	}
	if (message.content == (getCommand('help'))) {
		message.channel.send(helpMessage())
	}
	if (message.content == (getCommand('ping'))) {
		//sendDm(message.author.id, 'ping')
		message.channel.send('bong!')
	}
	if (message.content.startsWith(getCommand('ov.add'))) {
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
	dbGames = JSON.parse(el['games'])
	dbRanks = JSON.parse(el['last_rank'])
	apiRanks = ranks['competitive']
	
	if (dbGames != ranks['games']['competitive']['played']) {
		
		overwatchImage = {
			"username" : ranks['mar4elkin'],
			"avatar": ranks['portrait'],
			"tank_img": ranks['competitive']['tank']['rank_img'],
			"damage_img": ranks['competitive']['damage']['rank_img'],
			"support_img": ranks['competitive']['support']['rank_img']
		}

		function moreOrLessPts(oldvalue, newvalue) {
			let value = ''
			if (oldvalue > newvalue) {	
				finalValue = oldvalue - newvalue
				value = ' - ' + finalValue
			}
			if (oldvalue < newvalue) {
				finalValue = newvalue - oldvalue
				value = ' + ' + finalValue
			}
			return value
		}

		if (dbRanks['tank']['rank'] != apiRanks['tank']['rank']) {
			overwatchImage.tank = dbRanks['tank']['rank'] + " → " + apiRanks['tank']['rank'] + moreOrLessPts(dbRanks['tank']['rank'], apiRanks['tank']['rank'])
		} else {
			overwatchImage.tank = dbRanks['tank']['rank'] + " → " + dbRanks['tank']['rank']
		}
		if (dbRanks['damage']['rank'] != apiRanks['damage']['rank']) {
			overwatchImage.damage = dbRanks['damage']['rank'] + " → " + apiRanks['damage']['rank'] + moreOrLessPts(dbRanks['tank']['rank'], apiRanks['tank']['rank'])
		} else {
			overwatchImage.damage = dbRanks['damage']['rank'] + " → " + dbRanks['damage']['rank']
		}
		if (dbRanks['support']['rank'] != apiRanks['support']['rank']) {
			overwatchImage.support = dbRanks['support']['rank'] + " → " + apiRanks['support']['rank'] + moreOrLessPts(dbRanks['tank']['rank'], apiRanks['tank']['rank'])
		} else {
			overwatchImage.support = dbRanks['support']['rank'] + " → " + dbRanks['support']['rank']
		}

		let imageCreater = new ImageCreater('overwatch', overwatchImage)
		imageCreater.createImage()
		
		apiRanksString = JSON.stringify(apiRanks)
		database.updateViaBattleTag('UserOverwatch', JSON.stringify(apiRanks), ranks['games']['competitive']['played'], el['battle_id'])
		database.selectAllRows('Discord', rows => {
			if (rows != undefined || rows != []) {
				rows.forEach(row => {
					client.guilds.cache.find(guild_el => {
						if (row['server_id'] == guild_el.id) {
							client.channels.cache.get(row['channel_id']).send("<@" + el['discord_id'] + ">", {files: ["./tmp/overwatch/overwatchImage.png"]})
						}
					})
				})
			}
		})
	}
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
	database.insertValue('UserOverwatch', ['discord_id', 'battle_id, last_rank', 'games'], [discord_id, battle_id, JSON.stringify(ranks['competitive']), ranks['games']['competitive']['played']])
	sendDm(discord_id, "Аккаунт добавлен")
}

function botSettings(message) {
	const collector = new Discord.MessageCollector(message.channel, m => m.author.id === message.author.id, { time: 30000 })
	collector.on('collect', message => {
		if (message.content.startsWith("1")) {
			if (message.content.split(' ')[1] != undefined) {
				var channelsArr = []
				message.guild.channels.cache.find(ch => {
					channelsArr.push(ch.name) 
					//console.log(ch.name)
				})

				if(channelsArr.indexOf(message.content.split(' ')[1]) != -1) {
					message.channel.send('Я теперь буду писать в канал #' + message.content.split(' ')[1])
					message.guild.channels.cache.find(ch => {
						if (ch.name === message.content.split(' ')[1]) {
							//message.guild.id
							//ch.id
							//todo: add channel to db
							database.insertValue('Discord', ['server_id', 'channel_id'], [message.guild.id, ch.id])
						}	
					})
				
				channelsArr = []

				} else {
					message.channel.send('Такого канала нету')
				}

			} else {
				message.channel.send('Ты ракушка!')
				message.channel.send('`bot.settings')
			}
		} else if (message.content == "`bot.settings.exit") {
			message.channel.send("Ага ну и пиздуй")
		}
	})
}

fs.readFile('./api.key.txt', 'utf8', function(err, contents) {
    client.login(contents)
})


