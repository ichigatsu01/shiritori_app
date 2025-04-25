import unicodedata
import json
import random

class ShiritoriGame:
    def __init__(self):
        self.worddict_cpu = {} # cpuがゲーム中に使う辞書
        self.worddict_used = [] # user, cpuが使った単語を格納するためのリスト
        self.selected_word_cpu = "" # cpuが前回選んだ単語
        self.inputed_word_user = "" # userが前回入力した単語
        self.n_count = 0 # 「ん」で終わらせようとするuser向けチェッカー

    def startGame(self): # CPUが使う辞書の読込
        with open('worddict.json', mode="r", encoding="utf-8") as f:
            self.worddict_cpu = json.load(f)

    # 前回の文字の終わりと今回の文字の頭の比較用の関数
    def lastletterChecker(self, prev, follow):
        prev_last = prev[-1]
        # 最後の文字が伸ばし棒の場合、一つ前の文字をとる
        if prev_last == "ー":
            prev_last = prev[-2]

        # 濁点・半濁点で終わる場合、次のプレイヤーが始める言葉は濁点・半濁点を取り除いたものとする
        # inputed_word_user = "かんじ"
        table = str.maketrans(
            "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ", # 変換元の文字
            "かきくけこさしすせそたちつてとはひふへほはひふへほ" # 変換先の文字
            )
        prev_last = prev_last.translate(table)

        # follow_first_letter = follow[0]
        return prev_last, follow[0]
    
    # 前回の文字の終わりと今回の文字の頭の比較を関数化する
    # !CPUは自分が選ぶ単語だけを確定すればいいのでuserチェックと内容を変える
    def lastletterChecker_forCPU(self, prev):
        # prev_last_letter = prev[-1]
        # # 最後の文字が伸ばし棒の場合、一つ前の文字をとる
        # if prev_last_letter == "ー":
        #     prev_last_letter = prev[-2]

        # # 濁点・半濁点で終わる場合、次のプレイヤーが始める言葉は濁点・半濁点を取り除いたものとする
        # table = str.maketrans(
        #     "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ", # 変換元の文字
        #     "かきくけこさしすせそたちつてとはひふへほはひふへほ" # 変換先の文字
        #     )
        # prev_last_letter = prev_last_letter.translate(table)
        # return prev_last_letter
        return self.lastletterChecker(prev, prev)[0]
    
    def check_inputed_user(self): #userの入力内容をチェックする
        # ユーザの入力チェック
        while True:
        # 未入力チェック
            self.inputed_word_user = input('ひらがなを入力してください：')
            if self.inputed_word_user == "":
                print("空白のままでは送信できません")
                continue

            # 入力された単語はひらがなか？
            all_hiragana = True
            for letter in self.inputed_word_user:
                # print(unicodedata.name(letter))
                if 'HIRAGANA' not in unicodedata.name(letter):
                    all_hiragana = False

            if not all_hiragana:
                print('注意：入力は平仮名のみにしてください！')
                continue

            # 入力された単語は使用済みか？
            if self.inputed_word_user in self.worddict_used:
                print('注意：その単語は既に使われています！')
                continue

            # cpuの単語から続く言葉を入力しているか？
            if self.selected_word_cpu != "": #userが先行の場合はスキップ
                prev, follow = self.lastletterChecker(self.selected_word_cpu, self.inputed_word_user)
                if prev != follow:
                    print("CPUの言葉に続く単語を入力してください！")
                    continue

            # 「ん」で終わる単語を入れるuserがいたら必死に止める
            if self.inputed_word_user[-1] == "ん":
                if self.n_count == 0:
                    print("本当に「ん」で終わる単語を入れますか？")
                    self.n_count += 1
                    continue
                elif self.n_count == 1:
                    print("後悔しませんね？")
                    self.n_count += 1
                    continue
                elif self.n_count == 2:
                    print("本当に後悔しませんね？")
                    self.n_count += 1
                    continue
                else:
                    print("CPUの勝ちですって言うかCPUに勝たせました")
                    # self.inputed_word_user = None
                    # return self.inputed_word_user
                    # break
                    return None

            print(f'入力文字：{self.inputed_word_user}')

            self.worddict_used.append(self.inputed_word_user)
            print(f'returnされたinputed_word_user: {self.inputed_word_user}')
            print(f'これまでに使われた単語：{self.worddict_used}')

            return self.inputed_word_user
        
    def choice_word_cpu(self, inputed_word_user):
        # CPUが単語を選ぶ時の処理

        if self.inputed_word_user == "":
            head = random.choice(list(self.worddict_cpu.keys())) # cpu先攻の場合は辞書からランダムに選ぶ

        else:
            head = self.lastletterChecker_forCPU(inputed_word_user)
            if len(self.worddict_cpu[head]) == 0:
                print("CPUが出せる単語はもうありません。あなたの勝ちです")
                return None
            
        self.selected_word_cpu = self.worddict_cpu[head][0]

        print(f'CPUが選んだ単語： {self.selected_word_cpu}')
        self.worddict_used.append(self.selected_word_cpu)
        self.worddict_cpu[head].remove(self.selected_word_cpu) # cpuが選んだ単語をリストから除外

        print(f'returnされたselected_word_cpu: {self.selected_word_cpu}')
        print(f'これまでに使われた単語：{self.worddict_used}')
        return self.selected_word_cpu


# # CPUが使う辞書の読込
# # worddict_cpu = {}
# with open('worddict.json', mode="r", encoding="utf-8") as f:
#     worddict_cpu = json.load(f)


# worddict_used = [] # user, cpuが使った単語を格納するためのリスト
# selected_word_cpu = "" # cpuが前回選んだ単語
# inputed_word_user = "" # userが前回入力した単語













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