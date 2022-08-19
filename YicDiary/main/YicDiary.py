# YICDiary
# tkカレンダー
#
#
'''*1
Belongs : YIC 情報ビジネス専門学校 情報工学科 2年
Name    : 山崎 晃弘 
E-Mail  : B0021028@ib.yic.ac.jp
'''
# tkWindowPlus tkウィンドウの楽々化
# loginWindow  tk gridフレームに login画面作成(座標 1,1)
# YICDiary     カレンダー表示
# sqlscheduler 予定管理
# 
"""v2 からの変更点
    tk のリサイズ系で定義していたメソッドを
    別クラス(tkWindowPlus)に移動

    ログイン画面生成を内部メソッドから
    loginフレーム生成クラスに分離

    カレンダー表示時
    選択されている日が太字になるよう修正
        関連して
        フォント設定の一部をtk.fontで生成

    予定のない日に予定を入れた直後
    その日付に色がつくように修正

    予定表示をTreeViewを使うように修正

    その他不具合修正
"""


import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca

# 追加要素
import tkinter.font as tkFont
from sqlscheduler import sqlscheduler

#曜日用定数
WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']

# sqlscheduler.checklogin = lambda *a, **aa:True # debug書き換え

class tkWindowPlus: # tk便利化クラス
    def __init__(self) -> None:
        # ウィジェットの親ウィンドウを返す
        def personWindow(widget:tk.Widget, Revivaled=False):

            # 自身が root (か toplevel (RevivaledがTrueの時)
            if widget.master is None or (not Revivaled and type(widget) is tk.Toplevel):
                return widget
            # 親が toplevel
            elif type(widget.master) is tk.Toplevel:
                return widget.master
            # その他(再帰)
            else:
                return personWindow(widget.master, True)

        # 親ウィンドウのリサイズ可否を変更(変更の必要があるときのみ)
        # 変更 (したら True |しなかったら False) を返す
        # python and の 前の式が偽なら後の式が判定されない 性質使用
        self.ReSizable = lambda widget, x=False, y=False : bool(( (int(x), int(y)) != personWindow(widget).resizable() ) and personWindow(widget).resizable(x,y) is None)
        # 親ウィンドウのリサイズ
        self.ReSize = lambda widget, xy='520x280': personWindow(widget).after(10, lambda:(personWindow(widget).geometry(xy)))
        self.person = personWindow




#//@a
class LoginWindow(tkWindowPlus): # ログイン画面作成 ログインデータ保存可

    def __init__(self):
        super().__init__()
        # instance データの送り先 .login() と .guestLogin() と .checkLogin()
        self.__loginDate = None
        self.lastfunc = None
        self.resetMissCount()

    def getLoginData(self):
        return self.__loginDate

    def getMissCount(self):
        return self.__count

    def resetMissCount(self):
        self.__count = 0

    def addMissCount(self):
        self.__count += 1

    def checklogin(self):
        if self.instance is not None:
            return self.instance.checkLogin(self.getLoginData())
        return False


    def loginFrame(self, rootFrame, event, lastfunc = lambda:None, guestuser = True, Windowsize ="300x250", padx=0, pady = 50):
        self.__LFrame = tk.Frame(rootFrame)
        self.__LFrame.grid(row=1, column=1, padx=padx, pady=pady)

        self.instance = event
        def lf():
            nonlocal lastfunc, self
            self.lastfunc = None
            lastfunc()
        self.lastfunc = lf
        
        sizeble = self.person(self.__LFrame).resizable()
        self.ReSizable(self.__LFrame, x=False, y=False)
        self.ReSize(self.__LFrame, Windowsize)

        # ラベル
        sb1_frame = tk.Frame(self.__LFrame)
        if sb1_frame.grid(row=0, column=0) or True: # フレームごとにインデントを変えるためだけのif文(プログラム的に必要ない)
            tk.Label(sb1_frame, text='ユーザーログイン', font=('', 12)).grid(row=0, column=0)

        # データ入力ボックス
        sb2_frame = tk.Frame(self.__LFrame)
        if sb2_frame.grid(row=1, column=0) or True: # フレームごとにインデントを変えるためだけのif文(プログラム的に必要ない)

            #ユーザ名入力ボックス
            label_1 = tk.Label(sb2_frame, text='ユーザーID : 　', font=('', 10))
            label_1.grid(row=0, column=0, sticky=tk.W)
            text = tk.Entry(sb2_frame, width=20)
            text.grid(row=0, column=1)

            #パスワード入力ボックス
            label_2 = tk.Label(sb2_frame, text='パスワード : 　', font=('', 10))
            label_2.grid(row=1, column=0, sticky=tk.W)
            text2 = tk.Entry(sb2_frame, width=20, show="a")
            text2.grid(row=1, column=1)


            #パスワード表示切り替え
            def f(entry=text2):entry["show"] = "a"*int(entry["show"] == "")
            tmp = tk.Button(sb2_frame, text='ch', command=f)
            tmp.bind("<Button-1>", lambda e:f())
            tmp.grid(row=1, column=2)
            ##tmp終了


        # ログイン
        sb3_frame = tk.Frame(self.__LFrame)
        if sb3_frame.grid(row=2, column=0, sticky=tk.S) or True: # フレームごとにインデントを変えるためだけのif文(プログラム的に必要ない)
            def login():#text.get("1.0", "end-1c")
                nonlocal self, sizeble, text, text2, label_3
                self.__loginDate = self.instance.login(userid=text.get(), password=text2.get())
                if not self.instance.checklogin(self.__loginDate):
                    self.addMissCount()
                    if self.getMissCount() < 3:
                        label_3["text"] = f"ログインに失敗しました ({self.getMissCount()} 回失敗)"
                        return
                else:
                    self.resetMissCount()

                self.ReSizable(self.__LFrame, x=sizeble[0], y=sizeble[1])
                self.__LFrame.destroy()
                self.lastfunc()
            
            tmp = tk.Button(sb3_frame, text='ログイン', command=login)
            tmp.grid(row=0, column=0,padx=10, pady=10)
            #キーボード操作
            text.focus_set()
            text.bind('<Return>', lambda e:text2.focus_set()) #ユーザ名からenterでパスワードにフォーカス
            text2.bind('<Return>', lambda e:tmp.focus_set()) #パスワードからenterでログイン実行
            tmp.bind('<Return>', lambda e:login())
            ##tmp終了

            #ゲストユーザあり
            if guestuser:
                label_3 = tk.Label(sb3_frame, text='(↓ゲストログインもできます↓)', font=('', 10))
                label_3.grid(row=2,column=0)
                def guest():
                    nonlocal self, sizeble
                    self.__loginDate = self.instance.guestLogin()
                    #for widget in self.mainFrame.winfo_children():widget.destroy()
                    self.ReSizable(self.__LFrame, x=sizeble[0], y=sizeble[1])
                    self.__LFrame.destroy()
                    self.lastfunc()
                a = tk.Button(sb3_frame, text='ゲストログイン', command=guest, relief=tk.FLAT, bg="snow")
                a.grid(row=3, column=0,padx=10, pady=10)


class loginWindowOnscheduler(LoginWindow): # ログイン画面作成 ログインデータ保存可

    def __init__(self):
        super().__init__()
    
    def loginFrame(self, rootFrame, event, lastfunc = lambda:None, guestuser = True, Windowsize ="300x250", padx=0, pady = 50):

        def f(userid, password):
            event(userid, password)

        super().loginFrame(rootFrame, f, lastfunc, guestuser, Windowsize, padx, pady)







class YicDiary(tkWindowPlus):

    def __init__(self, root:tk.Tk):
        super().__init__()
        root.title('予定管理アプリ')

        root.grid_columnconfigure((0, 1), weight=1)
        self.sub_win = None

        # 他クラス読み込み
        #ログイン情報入力管理
        self.loginWindow = LoginWindow()
        #データ呼び出し
        self.scheduler = sqlscheduler()

        self.mainFrame = tk.Frame(root)
        self.mainFrame.pack()

        self.ReSizable(root)
        self.loginFrame()


    #------------------------------#
    # login要求画面生成
    #
    def loginFrame(self, guest=True):
        #ウィンドウ内消去
        for widget in self.mainFrame.winfo_children():widget.destroy()

        self.loginWindow.loginFrame(rootFrame=self.mainFrame, event=self.scheduler, lastfunc=self.executedLogin, guestuser=guest)
        tk.Label(self.mainFrame, text='tk YICDiary Login Window').grid(row=0, column=1)


    # ログイン画面からの遷移
    def executedLogin(self):
        # ログインしているか
        if self.scheduler.checklogin(self.loginWindow.getLoginData()):
            self.__calendar()
        else:
            #ログイン失敗回数によって処理替え
            if self.loginWindow.getMissCount() > 5:
                self.person(self.mainFrame, True).destroy()
            else:
                #　ログイン失敗のメッセージ表示
                pr = self.person(self.mainFrame, True)
                self.ReSize(pr, "200x100")
                tk.Label(self.mainFrame, text='ログイン失敗！', font=('', 20)).grid(row=0, column=1)
                lbl = tk.Label(self.mainFrame)
                lbl.grid(row=2, column=1)

                # クールタイム表示の動的生成
                def f(i):
                    nonlocal self, pr, lbl
                    if i > 0:
                        pr.after(1000, lambda i=i:(f(i-1) or True)and(lbl.configure(text=f'{i} 秒後に入力求む')))
                    elif i == 0:
                        pr.after(1000, lambda:self.loginFrame(False))
                    else:
                        raise ValueError
                # クールタイム表示の生成(旧)
                #for i in range(self.loginWindow.getMissCount()+1):
                #    pr.after(1000*i, lambda i=i:lbl.configure(text=f'{self.loginWindow.getMissCount()-i} 秒後に入力求む'))
                #pr.after(1000*i,lambda : self.loginFrame(False))
                f(self.loginWindow.getMissCount())


    #----------------------------------------------------
    # カレンダーメイン 初期化実行
    #
    def __calendar(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()
        self.ReSizable(self.mainFrame, x=False, y=False)
        self.ReSize(self.mainFrame, '520x280')

        self.year  = da.date.today().year
        self.mon   = da.date.today().month
        self.today = da.date.today().day
        self.title = None

        # 上側の部分row=0, column=0, sticky=tk.N
        topFrame = tk.Frame(self.mainFrame)
        topFrame.grid(row= 0, column= 0, columnspan=2, sticky=tk.N+tk.EW)
        self.topBuild(topFrame)

        # 左側のカレンダー部分row=1, column=0, sticky=tk.NW
        leftFrame = tk.Frame(self.mainFrame)
        leftFrame.grid(row= 1, column= 0, sticky=tk.NE)
        self.leftBuild(leftFrame)

        # 右側の予定管理部分row=1, column=1, sticky=tk.NW
        rightFrame = tk.Frame(self.mainFrame)
        rightFrame.grid(row= 1, column= 1, sticky=tk.NW)
        self.rightBuild(rightFrame)

        # ログインの簡易情報
        self.User()


    #-----------------------------------------------------------------
    # アプリの上側の領域を作成する
    #
    # topFrame: 上側のフレーム
    def topBuild(self, topFrame):
        self.topLabel = tk.Label(topFrame, text="",font=('', 10))
        self.topLabel.grid(row=0, column=0, pady=0, padx=0, sticky=tk.NW)
        tk.Button(topFrame, text='別ユーザでlogin', command=self.loginFrame).grid(row=0, column=1)

    #-----------------------------------------------------------------
    # アプリの左側の領域を作成する
    #
    # leftFrame: 左側のフレーム
    def leftBuild(self, leftFrame):
        self.viewLabel = tk.Label(leftFrame, font=('', 10))
        beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
        nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

        self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
        beforButton.grid(row=0, column=0, pady=10, padx=10)
        nextButton.grid(row=0, column=2, pady=10, padx=10)

        self.calendar = tk.Frame(leftFrame)
        self.calendar.grid(row=1, column=0, columnspan=3, padx=10, sticky=tk.NW)
        self.disp(0)


    #-----------------------------------------------------------------
    # アプリの右側の領域を作成する
    #
    # rightFrame: 右側のフレーム
    def rightBuild(self, rightFrame):
        r1_frame = tk.Frame(rightFrame)
        r1_frame.grid(row=0, column=0, pady=10)

        temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
        self.title = tk.Label(r1_frame, text=temp, font=('', 12))
        self.title.grid(row=0, column=0, padx=0)


        button = tk.Button(r1_frame, text='追加', command=lambda:self.add())
        button.grid(row=0, column=1)


        self.r2_frame = tk.Frame(rightFrame)
        self.r2_frame.grid(row=1, column=0)

        self.schedule()




    #---------------------------------------------------------------
    # 現在のログインネーム
    #
    def User(self):
        tmp1 = ""
        tmp2 = self.scheduler.getUserData(self.loginWindow.getLoginData())
        if tmp2[1] is not None:
            tmp1 += f"{tmp2[1]}\n"
        self.topLabel["text"] = tmp1+ f"{tmp2[0]} 様 こんにちは"
        self.schedule()


    #-----------------------------------------------------------------
    # アプリの右側の領域に予定を表示する
    #
    def schedule(self):
        # ウィジットを廃棄
        for widget in self.r2_frame.winfo_children():
            widget.destroy()
        """
        # データベースに予定の問い合わせを行う
        temp = self.scheduler.fetchOneDayPlanPreview(logincode=self.loginWindow.getLoginData(), year = self.year, mon = self.mon, day = self.today)
        self.plans = tk.Label(self.r2_frame, text=" "*50+"\n"+temp, font=('', 12), justify=tk.LEFT, anchor="e")
        self.plans.grid(row=0, column=0, padx=0, pady=20)
        if temp != "":
            button = tk.Button(self.r2_frame, text='詳細', command=lambda:self.details())
            button.grid(row=1, column=0)
        #else:
        #    tk.Label(self.r2_frame, text="予定なし", font=('', 20), justify=tk.LEFT, anchor="e").grid(row=0, column=0, padx=0, pady=20)
        """

        sb_frame = tk.Frame(self.r2_frame)
        sb_frame.grid(row=0, column=0)


        # 予定表示エリア（スクロール付）
        sb3_frame = tk.Frame(sb_frame)
        sb3_frame.grid(row=2, column=0)
        """
        text = tk.Text(sb3_frame, width=40, height=15,wrap= tk.NONE)
        #text.grid(row=0, column=0)

        temp = self.scheduler.fetchOneDayPlans(logincode= self.loginWindow.getLoginData(), year= self.year, mon= self.mon, day= self.today)
        text.insert("1.0", temp)"""

        # 予定表示
        tree = ttk.Treeview(sb3_frame, columns= ("value"), padding=(0,0,0,0), height=7)
        tree.grid_propagate(False)
        tree.columnconfigure(0, weight=1)
        tree.rowconfigure(0, weight=1)

        #列の幅 名前
        tree.heading("#0",text="ユーザ名 - 種類 - ")
        tree.heading("value", text="内容")
        tree.column("#0", width=80, anchor=tk.NW)
        tree.column("value", width=150, anchor=tk.NW)

        tmp = self.scheduler.fetchOneDayPlans(logincode= self.loginWindow.getLoginData(), year= self.year, mon= self.mon, day= self.today)
        ls = []
        if tmp[0]:
            nid = tree.insert("", "end", text="---", open="True", values= "----")
        for kind, value in tmp[0]:
            if not kind in ls:
                id = tree.insert(nid, "end", text=kind, open="False", values= "----")
                ls.append(kind)
            tree.insert(id, "end", text="|-----" , values= value)
        nsls, ls = [], []
        for name, kind, value in tmp[1]:
            if not name in nsls:
                nid = tree.insert("", "end", text=name, open="False", values= "----")
                nsls.append(name)
            if not kind in ls:
                id = tree.insert(nid, "end", text=kind, open="False", values= "----")
                ls.append(kind)
            tree.insert(id, "end", text="|-----" , values= value)

        tree.grid(row = 0, column=0, sticky = tk.N+tk.S+tk.E+tk.W  )

        def lc(event, *arg, **kw):
            print(tree.selection(), event, arg, kw)
            #.bind("<Double-Button-1>", callback)
            pass
        tree.bind("<<TreeviewSelect>>", lc)

        # 縦スクロールバー作成vy
        # 横スクロールバー作成hx
        scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=tree.yview)
        scroll_h = tk.Scrollbar(sb3_frame, orient=tk.HORIZONTAL, command=tree.xview)
        scroll_v.grid(row=0, column=10, sticky=tk.NS)
        scroll_h.grid(row=10, column=0, sticky=tk.EW)
        tree["yscrollcommand"] = scroll_v.set
        tree["xscrollcommand"] = scroll_h.set










    #-----------------------------------------------------------------
    # カレンダーを表示する
    #
    # argv: -1 = 前月
    #                0 = 今月（起動時のみ）更新時も
    #                1 = 次月
    def disp(self, argv):
        self.mon = self.mon + argv
        if self.mon < 1:
            self.mon, self.year = 12, self.year - 1
        elif self.mon > 12:
            self.mon, self.year = 1, self.year + 1

        self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

        cal = ca.Calendar(firstweekday=6)
        cal = cal.monthdayscalendar(self.year, self.mon)

        # ウィジットを廃棄
        for widget in self.calendar.winfo_children():
            widget.destroy()

        # 見出し行
        r = 0
        for i, x in enumerate(WEEK):
            label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
            label_day.grid(row=r, column=i, pady=1)


        # カレンダー本体
        self.__saveday = None
        #debugprint(da.date(self.year, self.mon, 1))
        tmpdays = self.scheduler.getDaysWithPlans(logincode=self.loginWindow.getLoginData(), year=self.year, month=self.mon) # 色付け用
        r = 1
        self.DefaltFont = tkFont.Font(size=10, weight="normal")
        for week in cal:
            for i, day in enumerate(week):
                if day == 0: day = ' '
                label_day = tk.Label(self.calendar, text=day, font=self.DefaltFont, fg=WEEK_COLOUR[i], borderwidth=1)

 
                if day == 1: # forcusしている日付
                    self.__saveday = label_day
                if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
                    label_day['relief'] = 'solid'
                    label_day['takefocus'] = 1
                    if argv == 0:
                        self.__saveday = label_day


                # クリックしたときのイベント
                label_day.bind('<Button-1>', self.click)
                label_day.grid(row=r, column=i, padx=2, pady=1)

                # 色付け
                if day in tmpdays[0]:
                    label_day['bg'] = '#cf0' if day in tmpdays[1] else '#ff0'
                elif day in tmpdays[1]:
                    label_day['bg'] = '#fc0'

            r = r + 1

        # 画面右側の表示を変更
        if self.title is not None:
            self.today = 1
            self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
            self.schedule()

        # forcusしている日付
        self.__saveday["font"] = tkFont.Font(size=12, weight="bold")

    #-----------------------------------------------------------------
    # 予定を追加したときに呼び出されるメソッド
    #
    def add(self):
        if self.sub_win == None or not self.sub_win.winfo_exists():
            self.sub_win = tk.Toplevel()
            #self.sub_win.geometry("300x300")
            #self.sub_win.resizable(0, 0)
            self.ReSize(self.sub_win, "300x300")
            self.ReSizable(self.sub_win)
            self.sub_win.focus_set()
            self.sub_win.grab_set()

            # ラベル
            sb1_frame = tk.Frame(self.sub_win)
            sb1_frame.grid(row=0, column=0)

            temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
            title = tk.Label(sb1_frame, text=temp, font=('', 12))
            title.grid(row=0, column=0)

            # 予定種別（コンボボックス）
            sb2_frame = tk.Frame(self.sub_win)
            sb2_frame.grid(row=1, column=0)
            label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
            label_1.grid(row=0, column=0, sticky=tk.W)
            actions = self.scheduler.actions(logincode = self.loginWindow.getLoginData())
            self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
            self.combo.current(0)
            self.combo.grid(row=0, column=1)

            # テキストエリア（垂直スクロール付）
            sb3_frame = tk.Frame(self.sub_win)
            sb3_frame.grid(row=2, column=0)
            self.text = tk.Text(sb3_frame, width=40, height=15)
            self.text.grid(row=0, column=0)
            scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
            scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
            self.text["yscrollcommand"] = scroll_v.set

            # 保存ボタン
            sb4_frame = tk.Frame(self.sub_win)
            sb4_frame.grid(row=3, column=0, sticky=tk.NE)
            button = tk.Button(sb4_frame, text='保存', command=self.done)
            button.pack(padx=10, pady=10)
        elif self.sub_win != None and self.sub_win.winfo_exists():
            self.sub_win.lift()


    #-----------------------------------------------------------------
    # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
    #
    def done(self):
        # データベースに新規予定を挿入する

        self.scheduler.setPlan(
                logincode = self.loginWindow.getLoginData(), 
                year = self.year,
                mon = self.mon,
                day = self.today,
                category = self.combo.get(),
                plan = self.text.get("1.0", "end-1c")
                )
        self.sub_win.destroy()
        self.schedule()
        self.__saveday['bg'] = '#ff0' if self.__saveday['bg'] =='#cf0' else '#cf0'

    #------------------------------------------------
    # 詳細を押したときに表示する
    #
    '''
    def details(self):
        if self.sub_win == None or not self.sub_win.winfo_exists():
            self.sub_win = tk.Toplevel()
            self.ReSize(widget=self.sub_win, xy="400x300")
            self.ReSizable(self.sub_win)
            self.sub_win.focus_set()
            self.sub_win.grab_set()

            # ラベル
            sb1_frame = tk.Frame(self.sub_win)
            sb1_frame.grid(row=0, column=0)

            temp = '{}年{}月{}日　予定詳細'.format(self.year, self.mon, self.today)
            title = tk.Label(sb1_frame, text=temp, font=('', 12))
            title.grid(row=0, column=0)

            # 予定表示エリア（スクロール付）
            sb3_frame = tk.Frame(self.sub_win)
            sb3_frame.grid(row=2, column=0)
            """
            text = tk.Text(sb3_frame, width=40, height=15,wrap= tk.NONE)
            #text.grid(row=0, column=0)

            temp = self.scheduler.fetchOneDayPlans(logincode= self.loginWindow.getLoginData(), year= self.year, mon= self.mon, day= self.today)
            text.insert("1.0", temp)"""

            # 予定表示
            tree = ttk.Treeview(sb3_frame, columns= 1, padding=(0,0,0,0))

            #列の幅 名前
            tree.heading("#0",text="種類")
            tree.heading(1, text="内容")
            tree.column("#0", width=100, anchor=tk.NW)
            tree.column(1, width=250, anchor=tk.NW)

            tmp = self.scheduler.fetchOneDayPlans(logincode= self.loginWindow.getLoginData(), year= self.year, mon= self.mon, day= self.today)
            ls = []
            for kind, value in tmp[0]:
                if not kind in ls:
                    id = tree.insert("", "end", text=kind, open="True", values= "----"*16)
                    ls.append(kind)
                tree.insert(id, "end", text="|-----" , values= value)
            nsls, ls = [], []
            for name, kind, value in tmp[1]:
                if not name in nsls:
                    nid = tree.insert("", "end", text=name, open="False", values= "----"*16)
                    nsls.append(name)
                if not kind in ls:
                    id = tree.insert(nid, "end", text=kind, open="True", values= "----"*16)
                    ls.append(kind)
                tree.insert(id, "end", text="|-----" , values= value)

            tree.grid(row = 0, column=0)

            def lc(event, *arg, **kw):
                print(tree.selection(), event, arg, kw)
                #.bind("<Double-Button-1>", callback)
                pass
            tree.bind("<<TreeviewSelect>>", lc)

            # 縦スクロールバー作成
            scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=tree.yview)
            scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
            tree["yscrollcommand"] = scroll_v.set
            # 横スクロールバー作成
            scroll_h = tk.Scrollbar(sb3_frame, orient=tk.HORIZONTAL, command=tree.xview)
            scroll_h.grid(row=10, column=0, sticky=tk.W+tk.E)
            tree["xscrollcommand"] = scroll_h.set

    
            # 閉じるボタン
            sb4_frame = tk.Frame(self.sub_win)
            sb4_frame.grid(row=3, column=0, sticky=tk.NE)
            tk.Button(sb4_frame, text='閉じる', command=lambda:self.sub_win.destroy()).pack(padx=10, pady=10)


        elif self.sub_win != None and self.sub_win.winfo_exists():
            self.sub_win.lift()
    '''

    #-----------------------------------------------------------------
    # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
    #
    # event: 左クリックイベント <Button-1>
    def click(self, event):
        day = event.widget['text']
        if day != ' ':
            # forcusしている日付
            self.__saveday["font"] = self.DefaltFont
            event.widget["font"] = tkFont.Font(size=12, weight="bold")
            self.__saveday = event.widget

            self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
            self.today = day
            self.schedule()




def Main():
    root = tk.Tk()
    YicDiary(root)
    root.mainloop()
if __name__ == '__main__':
    Main()
