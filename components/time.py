from datetime import datetime,timedelta
import time

class Time:
    # 今日の 00:00 のUTを取得
    def today(self):
        lt=list(map(int,str(datetime.fromtimestamp(time.time()))[:10].split('-')))
        return int(datetime(lt[0],lt[1],lt[2]).timestamp())
    
    # タスクの猶予+1日後の 00:00 のUTを取得
    def timelimit(self,limit):
        lt=list(map(int,str(datetime.now() + timedelta(days=limit))[:10].split('-')))
        return int(datetime(lt[0],lt[1],lt[2]).timestamp())

    # タイムリミットまでの日数を計算
    def limit(self,timelimit):
        return (timelimit - self.today()) // 86400