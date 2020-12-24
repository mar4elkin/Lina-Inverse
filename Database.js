const sqlite3 = require('sqlite3').verbose();

class Database {
    
    constructor(pathToDb = '') {
        if (pathToDb != '') {
            this.db = new sqlite3.Database(pathToDb);
        } else {
            this.db = new sqlite3.Database('./database.db');
        }
    }

    createTable(tableName, ...params) {
        //database.createTable('your_mom_is', 'asd, TEXT', 'dsa, TEXT')

        var sql = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' (id INTEGER PRIMARY KEY, '
        params.forEach((el, index) => {
            if (params.length == index + 1) {
                sql = sql + el.split(',')[0] + el.split(',')[1] + ')'
            } else {
                sql = sql + el.split(',')[0] + el.split(',')[1] + ', '
            }
        })
        this.db.run(sql)
    }

    insertValue(tableName, params, values) {
        //database.insertValue('your_mom_is', ['asd', 'dsa'], ['keks', 'no keks'])

        var sql = 'INSERT INTO ' + tableName + ' ('
        params.forEach((el, index) => {
            if (params.length == index + 1) {
                sql = sql + el + ')'
            } else {
                sql = sql + el + ', '
            }
        })

        sql = sql + ' VALUES ('

        values.forEach((el, index) => {
            if (values.length == index + 1) {
                sql = sql + '?)'
            } else {
                sql = sql + '?, '
            }
        })
        this.db.run(sql, values)
    }

    updateValue(tableName, setValues, whereValue) {
        //database.updateValue('your_mom_is', ['asd, nooooooooo'], 'id, 1')
        //database.updateValue('your_mom_is', ['asd, nooooooooo', 'dsa, hahahahaha'], 'id, 1')

        var sql = 'UPDATE ' + tableName + ' SET '
        let setValuesData = []
        setValues.forEach((el, index) => {
            if (setValues.length == index + 1) {
                sql = sql + el.split(',')[0].trim() + '= ? '
                setValuesData.push(el.split(',')[1].trim())
            } else {
                sql = sql + el.split(',')[0].trim() + '= ?, '
                setValuesData.push(el.split(',')[1].trim())
            }
        })
        sql = sql + 'WHERE ' + whereValue.split(',')[0].trim() + ' = ' + whereValue.split(',')[1].trim()
        this.db.run(sql, setValuesData)
    }

    updateViaBattleTag(tableName, dict, games, battle) {
        let sql = `UPDATE ${tableName} SET last_rank = ?, games = ? WHERE battle_id = ?`
        let data = [dict, games, battle]
        this.db.run(sql, data)
    }

    select(tableName, id, callback) {
        //database.select('your_mom_is', 1, callback)

        var sql = 'SELECT * FROM ' + tableName + ' WHERE id = ?'
        this.db.get(sql, [id], (err, row) => {
            callback(row)
        })
    }

    selectViaDiscord(tableName, discord_id, callback) {
        var sql = 'SELECT * FROM ' + tableName + ' WHERE discord_id = ?'
        this.db.get(sql, [discord_id], (err, row) => {
            callback(row)
        })
    }

    selectViaBattlenet(tableName, battle_id, callback) {
        var sql = 'SELECT * FROM ' + tableName + ' WHERE battle_id = ?'
        this.db.get(sql, [battle_id], (err, row) => {
            callback(row)
        })
    }
    
    selectAllRows(tableName, callback) {
        var sql = 'SELECT * FROM ' + tableName
        this.db.all(sql, [], (err, rows ) => {
            callback(rows)
        })
    }
}

module.exports = Database