const overwatch = require('overwatch-api');

class OverwatchApi {
    constructor(tag) {
        this.tag = tag.replace('#', '-')
    }
    
    getRanks(callback) {
        overwatch.getProfile('pc', 'global', this.tag, (err, json) => {
            if (err) {
                console.log(err)
            } else {
                callback(json)
            }
        })
    }
}

module.exports = OverwatchApi