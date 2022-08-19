# sqlscheduler
# sqlによる予定管理
#
#
'''*1
Belongs : YIC 情報ビジネス専門学校 情報工学科 2年
Name    : 山崎 晃弘 
E-Mail  : B0021028@ib.yic.ac.jp
'''
#
# 
#
"""v2からの変更点

    checklogin 追加
    actions 完成
    fetchOneDayPlans 出力型変更
    OneDayPlans
"""
"""
    __fetchstr から名前変更 -> __AvoidSqlCtrlChars

"""
"""今後の実装予定

(実装しない可能性あり)
新規ユーザ追加
新規家族追加
アカウントマネージャ作成
暗号化（accountMgr - YICDiary）&sql
 #メモ : ASE鍵長256ビットのとき、ラウンド数は14回である。
"""

from audioop import mul
import string


class accountMgr: # 未完
    def __init__(self):
        self.__logindata = None

    def getLogindata(self):
        return hash(self.__logindata)
    
    def __getLogindata(self):
        return self.__logindata


    def login(self, f, *args, **kwargs) -> bool:
        try:
            self.__logindata = f(*args, **kwargs)
        except:
            self.__logindata = None
        return self.__logindata is not None


 #エラー時でも動くように (目次もかねて)
class sqlscheduler:
    def __init__              (*args, **keywords) -> None  : print (ConnectionError("ReStert This Program"))
    def __getuserid           (*args, **keywords) -> None  : raise  ConnectionError("ReStert This Program")
    def __setuserid           (*args, **keywords) -> None  : raise  ConnectionError("ReStert This Program")
    def getUserID             (*args, **keywords) -> int   : return -1
    def newuser               (*args, **keywords) -> int   : return -1 #未実装
    def guestLogin            (*args, **keywords) -> int   : return -1
    def login                 (*args, **keywords) -> int   : return -1
    def checklogin            (*args, **keywords) -> bool  : return True
    def __checklogin          (*args, **keywords) -> bool  : return False
    def getUserData           (*args, **keywords) -> tuple : return ("OffLine", None)#変更済み d->t #{"NAME":"OffLine","FAMILYNAME":None}
    def setPlan               (*args, **keywords) -> None  : raise  ConnectionError("ReStert This Program")
    def getDaysWithPlans      (*args, **keywords) -> tuple : return (),()
    def getOneDayPlans        (*args, **keywords) -> tuple : return (),()
    def fetchOneDayPlans      (*args, **keywords) -> tuple : return (),()
    def fetchOneDayPlanPreview(*args, **keywords) -> str   : return ""
    def actions               (*args, **keywords) -> tuple : return tuple(" ")
    def __str__(*args, **kwargs) -> str:return "\n[sqlscheduler]\nDon't imported to pyMySQL\nor\nDon't connected to MySQL\n"
    def __repr__(*args, **kwargs) -> str:return "\n[sqlscheduler]\nDon't imported to pyMySQL\nor\nDon't connected to MySQL\n"


try:
    import pymysql
    pymysql.connect(host="127.0.0.1",user='root',password='',db='APR01',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor).close()
except ModuleNotFoundError:
    print("error Don't imported to pyMySQL")
except pymysql.err.OperationalError:
    print("error Don't connected to MySQL")
except:
    print("unknown error")
    exit()
else:
    pass
#if True:
    # クラスの置き換え
    class sqlscheduler:
        # 制御文字の回避 .replace("\\", "\\\\").replace("'", r"\'")
        # Connect to the database でータベースに接続
        @staticmethod
        def __AvoidSqlCtrlChars(*txts):
            return (x.replace("\\", "\\\\").replace("'", r"\'") for x in map(str, txts))

        def __init__(self) -> None:
            self.connection = None
            self.__userid = None
            self.__changeConection(host="127.0.0.1", user='root', password='', db='APR01')

    # 接続先設定 一部未実装
        def changeConection(self, host, user, password, db):
            #self.__changeConection(host, user, password, db)
            pass
        def __changeConection(self, host, user, password, db):
            f = lambda:pymysql.connect(
                                    host=host,
                                    user=user,
                                    password=password,
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
            c = self.connection
            with f() as connect:# コネクトできるか確認
                self.connection = f
                return
            self.connection = c
            return






        # 内部id
        def __getuserid(self):
            return self.__userid
        def __setuserid(self, userid):
            self.__userid = userid


        # 公開セッションid
        def getUserID(self):
            return hash(self.__getuserid())

        # ユーザー追加 未実装
        def newuser(self):
            pass

# sql
        # guestログイン 無くても作る
        def guestLogin(self) -> int:
            with self.connection() as connect:
                with connect.cursor() as cursor:

                    sql = f"SELECT USERID FROM USERS WHERE USERNAME = 'Guest';"
                    cursor.execute(sql)
                    sqlout_userid = cursor.fetchone()
            """
                    if sqlout_userid is None:

                        cursor.execute(f"INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('root', 'Guest', '');")
                        cursor.execute(sql)
                        sqlout_userid = cursor.fetchone()
            """
            self.__setuserid(sqlout_userid['USERID'])

            return self.getUserID()

# sql
        # 通常ログイン
        def login(self, userid="Guest", password="") -> int:#None
            userid, password = self.__AvoidSqlCtrlChars(userid, password)
            if userid == "Guest":
                return -1
                return self.guestLogin()
            else:
                with self.connection() as connect:
                    with connect.cursor() as cursor:
                        sql = f"SELECT USERID FROM USERS WHERE USERID = '{userid}' AND PASSWORD = '{password}'"
                        cursor.execute(sql)
                        _userid = cursor.fetchone()
                        if _userid is None:
                            return hash("fajhuiesfiuhseaifuhesihfiusheiufhsifhuieshifuhsiuhfuisehiufhiushufihae")

                        self.__setuserid(_userid["USERID"])

            return self.getUserID()

        # ログイン確認
        def checklogin(self, data) -> bool:
            return self.__checklogin(data)
        def __checklogin(self, data) -> bool:
            return hash(self.__getuserid()) == data

# sql 訂正予定
        # ユーザーデータ取得
        def getUserData(self, logincode) -> tuple[str, None]:
            if self.__checklogin(logincode):
                with self.connection() as connect:
                    with connect.cursor() as cursor:
                        sql = (
                            "SELECT U.USERNAME AS NAME, F.FAMILYNAME AS FAMILYNAME FROM "+
                                f"(SELECT * FROM USERS WHERE USERID = '{self.__getuserid()}') AS U "+
                                "LEFT OUTER JOIN FRIENDLY AS FY ON U.USERID = FY.USERID "+
                                "LEFT OUTER JOIN FAMILIES AS F ON FY.FAMILYID = F.FAMILYID;"
                            )
                        cursor.execute(sql)
                        sqlout_Name = cursor.fetchone()
                        return (sqlout_Name["NAME"], sqlout_Name["FAMILYNAME"])
            return ("ログイン失敗野郎", "残念")


# sql
    # 予定を保存
        def setPlan(self, logincode, year, mon, day, category, plan) -> None:
            if self.__checklogin(logincode):
                date = f'{int(year)}-{int(mon)}-{int(day)}'
                category, plan = self.__AvoidSqlCtrlChars(category, plan)
                print(date, category, plan)
                with self.connection() as connect:
                    connect.begin()
                    with connect.cursor() as cursor:

                        #カテゴリーID取得
                        sql = f"SELECT CATEGORYID FROM CATEGORY WHERE CATEGORY = '{category}'"
                        cursor.execute(sql)
                        cid = cursor.fetchone()["CATEGORYID"]



                        # PLANS にあるプランか?なかったら作る
                        sql = f"SELECT PLANID FROM PLANS WHERE PLAN = '{plan}';"
                        cursor.execute(sql)
                        sqlout_pid = cursor.fetchone()
                        if sqlout_pid is None:
                            cursor.execute(f"INSERT INTO PLANS (CATEGORYID, PLAN) VALUES ({cid}, '{plan}');")
                            cursor.execute(f"SELECT MAX(PLANID) AS PLANID FROM PLANS") # AUTO_INCREMENT なので MAX を取る 違う場合 変数sqlを使え
                            sqlout_pid = cursor.fetchone()
                        pid = sqlout_pid['PLANID']


                        # まったく同じ予定があるか
                        cursor.execute(
                            "SELECT PLANID FROM SCHEDULE "+
                            f"WHERE PLANID = {pid} AND CALENDARDATE='{date}' AND USERID = '{self.__getuserid()}';"
                            )
                        if cursor.fetchone() is None: # 同じ予定がない

                            # SCHEDULE にインサート
                            cursor.execute(f"INSERT INTO SCHEDULE (PLANID, CALENDARDATE, USERID) VALUES ({pid}, '{date}', '{self.__getuserid()}');")

                            connect.commit()
                            print("success")

                        else:
                            print("おんなじ予定かぶっとる")


            else:
                raise ValueError("Bat Login Code")

# sql
    #予定が入っている日の取得(ひと月のみ)
        def getDaysWithPlans(self, logincode, year, month) -> tuple[tuple[int],tuple[int]]:#tuple(tuple(日),tuple(日))
            year  = int(year + (month // 12))
            month = int(month % 12) if month % 12 != 0 else 12
            if self.__checklogin(logincode):
                with self.connection() as connect:
                    with connect.cursor() as cursor:
                        befordate = (year, month, 1)
                        afterdate = (year + 1, 1, 1) if month == 12 else (year, month + 1, 1)
                        # ユーザーズ取得
                        sql = f"SELECT USERID FROM FRIENDLY AS F1 WHERE EXISTS (SELECT * FROM FRIENDLY F2 WHERE F2.USERID = '{self.__getuserid()}' AND F1.USERID <> F2.USERID AND F1.FAMILYID = F2.FAMILYID)"
                        cursor.execute(sql)

                        #仲間の予定が入っている日付の取得
                        sql = "SELECT CALENDARDATE FROM SCHEDULE WHERE USERID IN ('" + "','".join(map(lambda x:x["USERID"], cursor.fetchall())) + "') GROUP BY CALENDARDATE HAVING CALENDARDATE BETWEEN " + f"'{befordate[0]}-{befordate[1]}-{befordate[2]}' AND '{afterdate[0]}-{afterdate[1]}-{afterdate[2]}'"
                        cursor.execute(sql)
                        multiuser = cursor.fetchall()

                        #自身の予定が入っている日付の取得
                        sql = f"SELECT CALENDARDATE FROM SCHEDULE WHERE USERID = '{self.__getuserid()}' GROUP BY CALENDARDATE HAVING CALENDARDATE BETWEEN " + f"'{befordate[0]}-{befordate[1]}-{befordate[2]}' AND '{afterdate[0]}-{afterdate[1]}-{afterdate[2]}'"
                        cursor.execute(sql)
                        dates = cursor.fetchall()
                        
                        if dates != ():
                            #print(type(dates[0]))
                            dates = tuple(map(lambda x:  x['CALENDARDATE'].day, dates))
                        if multiuser != ():
                            multiuser = tuple(map(lambda x: x['CALENDARDATE'].day, multiuser))



                        return dates, multiuser
            return (), ()

# sql
    #その日の予定を取得
        def getOneDayPlans(self, logincode, year, mon, day) -> tuple[tuple[dict],tuple[dict]]:
            if self.__checklogin(logincode):
                date = f'{int(year)}-{int(mon)}-{int(day)}'
                with self.connection() as connect:
                    with connect.cursor() as cursor:
                        sql = (
                            "SELECT C.CATEGORY AS CATEGORY, P.PLAN AS PLAN " +
                            "FROM ( " +
                                "SELECT * FROM SCHEDULE " +
                                f"WHERE SCHEDULE.CALENDARDATE = '{date}' AND SCHEDULE.USERID = '{self.__getuserid()}'" +
                            ") AS S " +
                            "INNER JOIN PLANS    AS P ON P.PLANID = S.PLANID " +
                            "INNER JOIN CATEGORY AS C ON C.CATEGORYID = P.CATEGORYID " +
                            "ORDER BY C.CATEGORYID "
                            )
                        cursor.execute(sql)
                        cdata = cursor.fetchall()


                        # ユーザーズ取得
                        sql = f"SELECT USERID FROM FRIENDLY AS F1 WHERE EXISTS (SELECT * FROM FRIENDLY F2 WHERE F2.USERID = '{self.__getuserid()}' AND F1.USERID <> F2.USERID AND F1.FAMILYID = F2.FAMILYID)"
                        cursor.execute(sql)

                        #仲間の予定が入っている日付の取得
                        sql = (
                            "SELECT C.CATEGORY AS CATEGORY, P.PLAN AS PLAN, U.USERNAME AS USERNAME"+
                            " FROM ("+
                                " SELECT PLANID, USERID FROM SCHEDULE "+
                                " WHERE USERID IN ('" + "','".join(map(lambda x:x["USERID"], cursor.fetchall())) + f"') AND CALENDARDATE = '{date}'"+
                                ") AS S"+
                            " INNER JOIN PLANS    AS P ON P.PLANID = S.PLANID " +
                            " INNER JOIN CATEGORY AS C ON C.CATEGORYID = P.CATEGORYID " +
                            " INNER JOIN USERS    AS U ON U.USERID = S.USERID " +
                            " ORDER BY U.USERNAME, C.CATEGORYID"
                        )
                        ___sql = (
                            f"""SELECT C.CATEGORY AS CATEGORY, P.PLAN AS PLAN, U.USERNAME AS USERNAME
                            FROM (
                                SELECT PLANID, USERID FROM SCHEDULE WHERE USERID IN (
                                    SELECT USERID FROM FRIENDLY AS F1 WHERE EXISTS (
                                        SELECT * FROM FRIENDLY F2 WHERE F2.USERID = '{self.__getuserid()}' AND F1.USERID <> F2.USERID AND F1.FAMILYID = F2.FAMILYID
                                    )
                                ) AND CALENDARDATE = '{date}'
                            ) AS S
                            INNER JOIN PLANS    AS P ON P.PLANID = S.PLANID
                            INNER JOIN CATEGORY AS C ON C.CATEGORYID = P.CATEGORYID
                            INNER JOIN USERS    AS U ON U.USERID = S.USERID
                            ORDER BY U.USERNAME, C.CATEGORYID;"""
                        )
                        cursor.execute(sql)
                        multicdata = cursor.fetchall()

                        return cdata, multicdata
            return (),()


    #その日の予定を取得カテゴリ別にフェッチ
        def fetchOneDayPlans(self, logincode, year, mon, day) -> tuple[tuple[tuple[str,str]], tuple[tuple[str,str,str]]]:#str:
            tmp = self.getOneDayPlans(logincode, year = year, mon = mon, day = day)
            return tuple(map(lambda x:(x['CATEGORY'],x['PLAN']) , tmp[0])), tuple(map(lambda x:(x['USERNAME'],x['CATEGORY'],x['PLAN']) , tmp[1]))
            return "\n\n".join([f"{x['CATEGORY']} :\n{x['PLAN']}" for x in tmp])



    #その日の予定の概要を取得
        def fetchOneDayPlanPreview(self, logincode, year, mon, day, txtlim = 20, listlim = 5, txtN=True) -> str:
            cdata = self.getOneDayPlans(logincode, year = year, mon = mon, day = day)[0]
            output = []
            category = ""
            for x in cdata:
                y = x["PLAN"]
                if y is not None:
        # categoryが変わったらcategory名を入れる
                    if category != x["CATEGORY"]:
                        category = x["CATEGORY"]
                        output.append(category + " : ")

        # タブの置き換え
                    if "\t" in y:
                        y = y.replace("\t","    ")
        # 長すぎる予定を短くして入れる
                    if len(y) > txtlim:
                        y = y[:txtlim-3] + "..."
        # 改行文字があれば短くする
                    if txtN and ("\n" in y):
                        y = y[:y.index("\n")] + "..."


                    output.append(" ・ " + y)

        # 予定が多いと省略する
            if len(output) > listlim:
                output = output[:listlim] + ["..."]

            return "\n".join(output)


# sql
        def actions(self, logincode) -> tuple[str]:
            #("学校", "試験", "課題", "行事", "就活", "アルバイト", "旅行")
            # sqlで取得する
            if self.__checklogin(logincode):
                with self.connection() as connect:
                    with connect.cursor() as cursor:
                        cursor.execute("SELECT CATEGORY FROM CATEGORY ORDER BY CATEGORYID")
                        kinds = tuple(map(lambda x:x["CATEGORY"], cursor.fetchall()))
                        if kinds : return kinds
            return tuple(" ")

