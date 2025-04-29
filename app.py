from flask import Flask, render_template, request, redirect, url_for
from utils import Game

app = Flask("shiritori")
game = Game() # utils.pyのGame()をインスタンス化

#! 動作確認用
# game.selected_word_cpu = "しりとり"
# game.worddict_used.append("しりとり")


@app.route("/", methods=['GET', 'POST'])
def index():
    msg = "" #cpuに表示させるメッセージ
    if request.method == 'POST':
        turn = request.form.get('turn')
        if turn == "先攻":
            game.is_user_first = True
            msg = "お好きな言葉を入力してください！"
        elif turn == "後攻":
            game.is_user_first = False
            msg = "CPUの番です"
            print(game.is_user_first)
        else:
            print("おかしなことが起きている")
    print(game.is_user_first)
    return render_template(
        'index.html',
        game = game,
        msg = msg
    )


@app.route("/game", methods=['GET', 'POST'])
def main():
    msg = ""
    game.alert_message = ""

    if request.method == 'POST':
        print("POSTだよ")
        # 既にゲームが終了している場合、入力を受け付けない
        if game.flag_gameend == True:
            msg = "もう一度遊ぶ場合は「再スタート」を押してください"
            return render_template(
                'index.html',
                game = game,
                msg = msg,
                lists = game.worddict_used
            )
        # userが後攻を選んだ時の対応
        if game.is_user_first == False:
            print("今/gameの中でis_user_firstの確認中")
            game.inputed_word_user = ""
            print("game.is_user_first == False")
            game.selected_word_cpu, game.worddict_cpu, game.worddict_used = game.choice_word_cpu(inputed, game.worddict_cpu, game.worddict_used)
            return render_template(
                'index.html',
                game = game,
                msg = game.selected_word_cpu,
                lists = game.worddict_used
            )
        else:
            # ゲームを進行する
            inputed = request.form['inputed']
            game.checkInputedUser(inputed, game.worddict_used, game.selected_word_cpu)
            #userの入力文字に不備があった場合：
            if game.alert_message:
                msg = game.alert_message
            else:
                game.selected_word_cpu, game.worddict_cpu, game.worddict_used = game.choice_word_cpu(inputed, game.worddict_cpu, game.worddict_used)
                if not game.selected_word_cpu:
                    msg = game.alert_message
                else:
                    msg = game.selected_word_cpu
            return render_template(
                'index.html',
                game = game,
                msg = msg,
                lists = game.worddict_used
            )
    else:
        return render_template(
            'index.html',
            game = game,
            msg = msg,
            lists = game.worddict_used
        )
    
@app.route("/reset", methods=['POST'])
def reset():
        # 全ての項目をリセットする
        game.allReset()
        return redirect(url_for("index"))   # ← PRGパターン


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')