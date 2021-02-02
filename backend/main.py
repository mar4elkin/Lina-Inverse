from flask import Flask, jsonify
from Overwatch import Competitive
from Overwatch import Exceptions

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "To infinity and beyond!" })

@app.route('/profile/<battle_tag>')
def profile(battle_tag):
    competitive = {}
    comp = Competitive(battle_tag)
    page = comp.getPage()
    
    try:
        comp.checkPage(page)
        competitive['player'] = comp.playerInfo(page)
        competitive['ranks'] = comp.getRanks(page)
    except Exceptions.BattleTagError:
        return jsonify({"error": "Check battle tag!" })
    
    competitive['games'] = comp.getGames(page)

    return jsonify(competitive)


if __name__ == '__main__':
    app.run(debug=True)