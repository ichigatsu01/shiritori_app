# import文は一つずつ書くのがPythonのルールのようだ
import unicodedata
import json
import random

class Game:
    def __init__(self):
        self.worddict_cpu = self.fileOpen() # CPUが使う辞書の読込
        self.worddict_used = [] # user, cpuが使った単語を格納するためのリスト
        self.selected_word_cpu = "" # cpuが前回選んだ単語
        self.inputed_word_user = "" # userが前回入力した単語
        self.next_letter = "" # 次の単語の頭文字
        self.alert_message = "" # エラー時のメッセージ
        self.n_count = 0 # 「ん」で終わろうとするユーザチェック用
        self.flag_gameend = False # ゲームが修了した後の処理用フラグ
        self.is_user_first = None

    def fileOpen(self): # cpuが使う辞書を取得する
        try:
            with open('worddict.json', mode="r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'絶対に起きないはずのエラー、起きたらファイルが消えてる: {e}')
            return {}

    # 前回の文字の終わりと今回の文字の頭の比較用の関数。
    def lastletterChecker(self, prev_word, follow_word):
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

    #* 引数について：inputed=userがブラウザでinputした単語, used=worddict_used, cpu=selected_word_cpu
    def checkInputedUser(self, inputed, used, cpu):
        # ユーザの入力チェック
        while True:
            # 入力された単語はひらがなか？
            all_hiragana = True
            for letter in inputed:
                if 'HIRAGANA' not in unicodedata.name(letter):
                    all_hiragana = False

            if not all_hiragana:
                print('注意：入力は平仮名のみにしてください！')
                self.alert_message = '注意：入力は平仮名のみにしてください！'
                return self.alert_message

            # 入力された単語は使用済みか？
            if inputed in used:
                print('注意：その単語は既に使われています！')
                self.alert_message = '注意：その単語は既に使われています！'
                return self.alert_message

            # cpuの単語から続く言葉を入力しているか？
            if cpu != "": #userが先行の場合はスキップ
                prev, follow = self.lastletterChecker(cpu, inputed)
                if prev != follow:
                    self.alert_message = 'CPUの言葉に続けてください（濁音・半濁音不可）！'
                    return self.alert_message

            # 「ん」で終わる単語を入れるuserがいたら必死に止める
            if inputed[-1] == "ん":
                if self.n_count == 0:
                    self.n_count += 1
                    self.alert_message = "本当に「ん」で終わる単語を入れますか？"
                    return self.n_count, self.alert_message

                elif self.n_count == 1:
                    self.n_count += 1
                    self.alert_message = "後悔しませんね？"
                    return self.n_count, self.alert_message

                else:
                    self.alert_message = "あなたは負けました…"
                    self.flag_gameend = True
                    return inputed, used

            # 使用済み辞書にuserが入力した単語を追加
            used.append(inputed)
            return inputed, used


    def choice_word_cpu(self, inputed, dict_cpu, dict_used): # CPUが単語を選ぶ時の処理
        print("CPUが言葉を選んでいます")
        if inputed == "": # cpu先攻の場合は辞書からランダムに選ぶ
            letter = random.choice(list(dict_cpu.keys()))
        else:
            letter, _ = self.lastletterChecker(inputed, inputed)
            # cpuの返す言葉がなくなっている場合：
            if letter not in dict_cpu:
                self.alert_message = "CPUが出せる単語はもうありません。あなたの勝ちです！"
                selected = None
                self.flag_gameend = True
                return selected, dict_cpu, dict_used

        # 辞書の中からランダムで言葉を選ぶ
        while True:
            selected = random.choice(dict_cpu[letter])
            if selected not in dict_used:
                break

        # 使用済み辞書への追加と、cpuが使う辞書からの使用した単語の除去
        dict_used.append(selected)
        # 辞書の残りが1の場合、辞書から該当インデックスごと削除する
        if len(dict_cpu[selected[0]]) == 1:
            del dict_cpu[selected[0]]
        else:
            dict_cpu[selected[0]].remove(selected)

        return selected, dict_cpu, dict_used

    # *最初からやり直す用関数
    def allReset(self):
        self.worddict_cpu = self.fileOpen() # CPUが使う辞書の読込
        self.worddict_used = [] # user, cpuが使った単語を格納するためのリスト
        self.selected_word_cpu = "" # cpuが前回選んだ単語
        self.inputed_word_user = "" # userが前回入力した単語
        self.next_letter = "" # 次の単語の頭文字
        self.alert_message = "" # エラー時のメッセージ
        self.n_count = 0 # 「ん」で終わろうとするユーザチェック用
        self.flag_gameend = False
        self.is_user_first = None