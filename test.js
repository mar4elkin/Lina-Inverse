const Database = require('./Database')
let database = new Database()
const OverwatchApi = require('./OverwatchApi')
let overwatchApi = new OverwatchApi('mar4elkin#2842')
//const asddsa = ''
//database.createTable('your_mom_is', 'asd, TEXT', 'dsa, TEXT')
//database.insertValue('UserOverwatch', ['username', 'battle_id'], ['asdasd', 'ra4elkin#123123'])
//database.updateValue('your_mom_is', ['gay, nooooooooo', 'big_gay, hahahahaha'], 'id, 1')
//database.selectViaBattlenet('UserOverwatch', 'mar4elkin#123123', test => (console.log(test)))

function test(x) {
    //console.log(x)
    console.log(x['competitive']['tank']['rank'])
}

//database.selectAllRows('UserOverwatch', test)
overwatchApi.getRanks(test)


// function getCookies(){
//     if (document.querySelector('#upgrade0') != null){
//         document.querySelector('#upgrade0').click()
//     }
//     document.querySelector('#bigCookie').click()
//     for (let i = 0; i < 18; i++) { 
//         if (document.querySelector('#product' + i) != null){
//             document.querySelector('#product' + i).click()
//         }
//     }
//     Game.cookies = Infinity
//     setTimeout(getCookies, 1)
// }

