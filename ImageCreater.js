const { createCanvas, loadImage } = require('canvas')
const fs = require('fs')
const fetch = require('node-fetch');

class ImageCreater {
    constructor(type='', data) {
        this.data = data
        if(type == 'overwatch') {
            this.width = 300
            this.height = 370
            this.backgroundColor = '#2c3959'
        }
        if(type == 'osu') {
            this.width = 300
            this.height = 290
            this.backgroundColor = '#4a2c59' //'#3D2932'
        }
    }

    getOverwatchPtsColor(str) { 
        let green = '#008000'
        let red = '#ff0000'
        
        if (str.split('→')[1].match(/\+/gm) == '+') {
            return [green, str.split('+')[0].trim(), '+', str.split('+')[1].trim()]
        } else {
            if (str.split('→')[1].match(/\+/gm) == '-'){
                console.log(str)
                return [red, str.split('-')[0].trim(), '-', str.split('-')[1].trim()]
            } else {
                return ['#fff', str, '', '']
            }
        }
    }

    async getImage(url, name, callback) {
        let response = await fetch(url);
        let buffer = await response.buffer();
        fs.writeFile(`./tmp/overwatch/${name}.jpg`, buffer, callback)
    }
    
    async createImage() {
        //console.log(this.data)
        
        let canvas = createCanvas(this.width, this.height)
        let context = canvas.getContext('2d')
        
        context.fillStyle = this.backgroundColor
        context.fillRect(0, 0, this.width, this.height)

        context.fillStyle = '#fff'
        context.font = 'bold 20pt Sans'
        context.fillText(this.data['username'], 105, 60)

        // context.fillStyle = '#fff'
        // context.font = 'bold 25pt Sans'
        // context.fillText('Рейтинг', 20, 140)

        await this.getImage(this.data['support_img'], 'support_img', () => {
            loadImage('./tmp/overwatch/support_img.jpg').then(image => {

                context.fillStyle = '#fff'
                context.font = 'bold 15pt Sans'
                context.fillText('Support', 5, 120)
                
                let arr = this.getOverwatchPtsColor(this.data['support'])
                
                context.fillStyle = '#fff'
                context.font = 'bold 13pt Sans'
                context.fillText(arr[1], 50, 145)

                context.fillStyle = arr[0]
                context.font = 'bold 13pt Sans'
                context.fillText(arr[2] + ' ' + arr[3], 180, 145)

                context.drawImage(image, 0, 120, 45, 45)
            })
        })

        await this.getImage(this.data['tank_img'], 'tank_img', () => {
            loadImage('./tmp/overwatch/tank_img.jpg').then(image => {

                context.fillStyle = '#fff'
                context.font = 'bold 15pt Sans'
                context.fillText('Tank', 5, 220)

                let arr = this.getOverwatchPtsColor(this.data['tank'])
                
                context.fillStyle = '#fff'
                context.font = 'bold 13pt Sans'
                context.fillText(arr[1], 50, 245)

                context.fillStyle = arr[0]
                context.font = 'bold 13pt Sans'
                context.fillText(arr[2] + ' ' + arr[3], 180, 245)

                context.drawImage(image, 0, 220, 45, 45)
            })
        })

        await this.getImage(this.data['damage_img'], 'damage_img', () => {
            loadImage('./tmp/overwatch/damage_img.jpg').then(image => {

                context.fillStyle = '#fff'
                context.font = 'bold 15pt Sans'
                context.fillText('Damage', 5, 320)

                let arr = this.getOverwatchPtsColor(this.data['damage'])
                
                context.fillStyle = '#fff'
                context.font = 'bold 13pt Sans'
                context.fillText(arr[1], 50, 345)

                context.fillStyle = arr[0]
                context.font = 'bold 13pt Sans'
                context.fillText(arr[2] + ' ' + arr[3], 180, 345)

                context.drawImage(image, 0, 320, 45, 45)
            })
        })

        await this.getImage(this.data['avatar'], 'userImage', () => {
            loadImage('./tmp/overwatch/userImage.jpg').then(image => {
                context.drawImage(image, 20, 20, 70, 70)
                let buffer = canvas.toBuffer('image/png')
                fs.writeFileSync('./tmp/overwatch/overwatchImage.png', buffer)
            })
        })
    }

}

module.exports = ImageCreater