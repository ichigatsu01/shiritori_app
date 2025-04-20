import unicodedata, json, random

# CPUが使う辞書の読込
worddict_cpu = {}
with open('worddict.json', mode="r", encoding="utf-8") as f:
    worddict_cpu = json.load(f)


worddict_used = [] # user, cpuが使った単語を格納するためのリスト
selected_word_cpu = "" # cpuが前回選んだ単語
inputed_word_user = "" # userが前回入力した単語


# 前回の文字の終わりと今回の文字の頭の比較用の関数
def lastletterChecker(prev, follow):
    prev_last_letter = prev[-1]
    # 最後の文字が伸ばし棒の場合、一つ前の文字をとる
    if prev_last_letter == "ー":
        prev_last_letter = prev[-2]

    # 濁点・半濁点で終わる場合、次のプレイヤーが始める言葉は濁点・半濁点を取り除いたものとする
    # inputed_word_user = "かんじ"
    table = str.maketrans(
        "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ", # 変換元の文字
        "かきくけこさしすせそたちつてとはひふへほはひふへほ" # 変換先の文字
        )
    prev_last_letter = prev_last_letter.translate(table)

    follow_first_letter = follow[0]
    return prev_last_letter, follow_first_letter


# 前回の文字の終わりと今回の文字の頭の比較を関数化する
# !CPUは自分が選ぶ単語だけを確定すればいいのでuserチェックと内容を変える
def lastletterChecker_forCPU(prev):
    prev_last_letter = prev[-1]
    # 最後の文字が伸ばし棒の場合、一つ前の文字をとる
    if prev_last_letter == "ー":
        prev_last_letter = prev[-2]

    # 濁点・半濁点で終わる場合、次のプレイヤーが始める言葉は濁点・半濁点を取り除いたものとする
    table = str.maketrans(
        "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ", # 変換元の文字
        "かきくけこさしすせそたちつてとはひふへほはひふへほ" # 変換先の文字
        )
    prev_last_letter = prev_last_letter.translate(table)
    return prev_last_letter


def check_inputed_user(): #userの入力内容をチェックする
    n_count = 0 # 「ん」で終わらせようとするuser向けチェッカー
    # ユーザの入力チェック
    while True:
    # 未入力チェック
        inputed_word_user = input('ひらがなを入力してください：')
        if inputed_word_user == "":
            print("空白のままでは送信できません")
            continue

        # 入力された単語はひらがなか？
        all_hiragana = True
        for letter in inputed_word_user:
            # print(unicodedata.name(letter))
            if 'HIRAGANA' not in unicodedata.name(letter):
                all_hiragana = False

        if not all_hiragana:
            print('注意：入力は平仮名のみにしてください！')
            continue

        # 入力された単語は使用済みか？
        if inputed_word_user in worddict_used:
            print('注意：その単語は既に使われています！')
            continue

        # cpuの単語から続く言葉を入力しているか？
        if selected_word_cpu != "": #userが先行の場合はスキップ
            prev, follow = lastletterChecker(selected_word_cpu, inputed_word_user)
            if prev != follow:
                print("CPUの言葉に続く単語を入力してください！")
                continue

        # 「ん」で終わる単語を入れるuserがいたら必死に止める
        if inputed_word_user[-1] == "ん":
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
                inputed_word_user = None
                return inputed_word_user
                # break

        print(f'入力文字：{inputed_word_user}')

        worddict_used.append(inputed_word_user)
        print(f'returnされたinputed_word_user: {inputed_word_user}')
        print(f'これまでに使われた単語：{worddict_used}')

        return inputed_word_user


def choice_word_cpu(inputed_word_user):
    # CPUが単語を選ぶ時の処理

    if inputed_word_user == "":
        lastletter_user = random.choice(list(worddict_cpu.keys())) # cpu先攻の場合は辞書からランダムに選ぶ

    else:
        lastletter_user = lastletterChecker_forCPU(inputed_word_user)
        if len(worddict_cpu[lastletter_user]) == 0:
            print("CPUが出せる単語はもうありません。あなたの勝ちです")
            return None
        
    selected_word_cpu = worddict_cpu[lastletter_user][0]

    print(f'CPUが選んだ単語： {selected_word_cpu}')
    worddict_used.append(selected_word_cpu)
    worddict_cpu[selected_word_cpu[0]].remove(selected_word_cpu) # cpuが選んだ単語をリストから除外

    print(f'returnされたselected_word_cpu: {selected_word_cpu}')
    print(f'これまでに使われた単語：{worddict_used}')
    return selected_word_cpu

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