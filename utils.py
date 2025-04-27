# 使用する変数の整理…グローバルとローカルで使う名前を変える

import unicodedata, json, random

# CPUが使う辞書の読込
worddict_cpu = {} # cpuが単語選択に使う辞書
worddict_used = [] # user, cpuが使った単語を格納するためのリスト
selected_word_cpu = "" # cpuが前回選んだ単語
inputed_word_user = "" # userが前回入力した単語
next_letter = "" # 次の単語の頭文字


def fileOpen(): # cpuの辞書を取得する
    with open('worddict.json', mode="r", encoding="utf-8") as f:
        # worddict_cpu = json.load(f)
        return json.load(f)

# 前回の文字の終わりと今回の文字の頭の比較用の関数。cpuの場合、
def lastletterChecker(prev_word, follow_word):
    prev_letter = prev_word[-1]
    # 最後の文字が伸ばし棒の場合、一つ前の文字をとる
    if prev_letter == "ー":
        prev_letter = prev_word[-2]

    # prev濁点・半濁点で終わる場合、次のプレイヤーが始める言葉は濁点・半濁点を取り除いたものとする
    table = str.maketrans(
        "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ", # 変換元の文字
        "かきくけこさしすせそたちつてとはひふへほはひふへほ" # 変換先の文字
        )
    prev_letter = prev_letter.translate(table)

    follow_letter = follow_word[0] # 次のターンがuserの場合、follow_letterから始まる単語を使わせる
    return prev_letter, follow_letter


# # 前回の文字の終わりと今回の文字の頭の比較を関数化する
# # !CPUは自分が選ぶ単語だけを確定すればいいのでuserチェックと内容を変える
# def lastletterChecker_forCPU(prev):
#     prev_last_letter = prev[-1]
#     # 最後の文字が伸ばし棒の場合、一つ前の文字をとる
#     if prev_last_letter == "ー":
#         prev_last_letter = prev[-2]

#     # 濁点・半濁点で終わる場合、次のプレイヤーが始める言葉は濁点・半濁点を取り除いたものとする
#     table = str.maketrans(
#         "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ", # 変換元の文字
#         "かきくけこさしすせそたちつてとはひふへほはひふへほ" # 変換先の文字
#         )
#     prev_last_letter = prev_last_letter.translate(table)
#     return prev_last_letter

#! userの入力内容をチェックする。
#! 元々Python単体で完結できるようにcontinueを使ったがbreakでerror_messageを返すべきかも
#* 引数について：inputed=userがブラウザでinputした単語, used=worddict_used, cpu=selected_word_cpu
def check_inputed_user(inputed, used, cpu):
    n_count = 0 # 「ん」で終わらせようとするuser向けチェッカー
    # ユーザの入力チェック
    while True:
    #* 未入力チェック...これはブラウザ側でやるから必要ない可能性が高い
        # inputed = input('ひらがなを入力してください：')
        if inputed == "":
            print("空白のままでは送信できません")
            continue

        # 入力された単語はひらがなか？
        all_hiragana = True
        for letter in inputed:
            # print(unicodedata.name(letter))
            if 'HIRAGANA' not in unicodedata.name(letter):
                all_hiragana = False

        if not all_hiragana:
            print('注意：入力は平仮名のみにしてください！')
            continue

        # 入力された単語は使用済みか？
        if inputed in used:
            print('注意：その単語は既に使われています！')
            continue

        # cpuの単語から続く言葉を入力しているか？
        if cpu != "": #userが先行の場合はスキップ
            prev, follow = lastletterChecker(cpu, inputed)
            if prev != follow:
                print("CPUの言葉に続く単語を入力してください！")
                continue

        # 「ん」で終わる単語を入れるuserがいたら必死に止める
        if inputed[-1] == "ん":
            if n_count == 0:
                print("本当に「ん」で終わる単語を入れますか？")
                n_count += 1
                continue
            elif n_count == 1:
                print("後悔しませんね？")
                n_count += 1
                continue
            elif n_count == 2:
                print("本当に後悔しませんね？")
                n_count += 1
                continue
            else:
                print("CPUの勝ちですって言うかCPUに勝たせました")
                inputed = None
                return inputed

        print(f'入力文字：{inputed}')

        used.append(inputed)
        print(f'returnされたinputed: {inputed}')
        print(f'これまでに使われた単語：{used}')

        return inputed, used


def choice_word_cpu(inputed, dict_cpu, dict_used): # CPUが単語を選ぶ時の処理
    if inputed == "": # cpu先攻の場合は辞書からランダムに選ぶ
        letter = random.choice(list(worddict_cpu.keys()))
    else:
        letter = lastletterChecker(inputed, inputed)
        if len(dict_cpu[letter]) == 0:
            print("CPUが出せる単語はもうありません。あなたの勝ちです")
            return None

    selected = dict_cpu[letter][0]
    print(f'CPUが選んだ単語： {selected}')

    # 使用済み辞書への追加と、cpuが使う辞書からの使用した単語の除去
    dict_used.append(selected)
    dict_cpu[selected[0]].remove(selected)

    print(f'returnされたselected: {selected}')
    print(f'これまでに使われた単語：{dict_used}')
    return selected, dict_cpu, dict_used

#! 以下テストプレイ用のコード
gameend_flag = False
while gameend_flag == False:
    game_start = input('先攻でプレイしますか？ y/n: ')
    if game_start.lower() == 'y':
        while True:
            inputed_word_user = check_inputed_user()
            if inputed_word_user == None:
                gameend_flag = True
                break
            selected_word_cpu = choice_word_cpu(inputed_word_user)
            if selected_word_cpu == None:
                gameend_flag = True
                break
    elif game_start.lower() == 'n':
        while True:
            selected_word_cpu = choice_word_cpu(inputed_word_user)
            if selected_word_cpu == None:
                gameend_flag = True
                break
            inputed_word_user = check_inputed_user()
            if inputed_word_user == None:
                gameend_flag = True
                break
    else:
        print('y または n を入力してください')
        continue