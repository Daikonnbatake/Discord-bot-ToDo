from mysql import connector as db
import json,sys
sys.path.append(str(__file__)[:-16])
from components import time

# 個人的なメモ
#
# mysql.connectorは.commit()しないとINSERT文が反映されないから気をつけよう！
# 使い方を忘れたらaddUserメソッドなどを確認すべし。
#
# メモ終わり。

class DBaccess:
    # 初期化
    def __init__(self):
        c=__file__
        with open(c[0:-16]+'meta/db.json','r',encoding='utf-8') as f:
            d=json.load(f)
            self.connect=db.connect(host=d['host'],port=d['port'],user=d['user'],password=d['passwd'],database=d['db'])
            self.user_mst=d['user_mst']
            self.todo_mst=d['todo_mst']
            self.time=time.Time()

    # 接続確認
    def is_connected(self):
        return self.connect.is_connected()
    
    # ユーザー追加
    def addUser(self,userName):
        cur = self.connect.cursor(prepared=True)
        cur.execute('INSERT INTO ' + self.user_mst + ' (userID) VALUES (?)',(userName,))
        self.connect.commit()
    
    # タスク追加
    def addtask(self,userName,task,limit):
        cur = self.connect.cursor(prepared=True)
        now = self.time.today()
        timeLimit = self.time.timelimit(int(limit))
        cur.execute('INSERT INTO ' + self.todo_mst + ' (userID,task,`set`,`limit`) VALUES (?,?,?,?)',(userName,task,str(now),str(timeLimit)))
        self.connect.commit()
    
    # テスト用取得
    def getTest(self):
        cur=self.connect.cursor(prepared=True)
        cur.execute('SELECT * FROM ' + self.user_mst)
        print(cur.fetchall())
        cur.execute('SELECT * FROM ' + self.todo_mst)
        print(cur.fetchall())

    # ユーザー情報取得
    # [[ユーザー情報],[未完了のタスク],[完了したタスク(新しい順に20件)]]
    def getUserdata(self,userName):
        cur=self.connect.cursor(prepared=True)
        cur.execute('SELECT * FROM ' + self.user_mst + ' WHERE userID = ?',(userName,))
        r=[cur.fetchall()]
        cur.execute('SELECT * FROM ' + self.todo_mst + ' WHERE userID = ? AND enable = 1',(userName,))
        r.append(cur.fetchall())
        cur.execute('SELECT * FROM ' + self.todo_mst + ' WHERE userID = ? AND enable = 0 ORDER BY taskID DESC limit 10',(userName,))
        r.append(cur.fetchall())
        return r
    
    # タスクを終了
    def completeTask(self,userName,taskID):
        cur=self.connect.cursor(prepared=True)
        cur.execute('SELECT * FROM ' + self.todo_mst + ' WHERE taskID = ?',(str(taskID),))
        data=cur.fetchall()
        cur.execute('UPDATE ' + self.todo_mst + ' SET enable = 0 WHERE taskID = ?',(str(taskID),))
        cur.execute('UPDATE ' + self.todo_mst + ' SET status = ? WHERE taskID = ?',(self.time.limit(data[0][5]),str(taskID)))
        cur.execute('UPDATE ' + self.user_mst + ' SET count = count  + 1 WHERE userID = ?',(userName,))
        self.connect.commit()
    
    # タスクIDを指定してタスクをピンポイントに取得
    def taskinfo(self,taskID):
        cur=self.connect.cursor(prepared=True)
        cur.execute('SELECT * FROM ' + self.todo_mst + ' WHERE taskID = ?',(str(taskID),))
        return cur.fetchall()