import os,sys,discord
from discord.ext import commands
sys.path.append(str(__file__)[:-12])
from components.db import DBaccess
from components.time import Time

class Todo(commands.Cog):
    def __init__(self,ctx):
        self.time = Time()
    
    def genTaskInfo(self,taskID,title):
        self.connect = DBaccess()
        data = self.connect.taskinfo(taskID)
        limit = self.time.limit(data[0][5])
        description = [
                '```',
                'タスク:' + data[0][3] + '\n',
                '状態: ' + ('未' if data[0][2] else '済')  + '\n',
                '余裕/超過: ' + (((str(limit if 0 < limit else (1 if 0==limit else abs(limit)+1)) + (' 日の余裕があります。' if 0<limit else ' 日超過しています。'))) if data[0][2] else (('余裕 ' if 0<limit else '超過 ') + str(limit if 0 < limit else (1 if 0==limit else abs(limit)+1)) + ' 日でこのタスクは消化されました。')),
                '```'
            ]

        return discord.Embed(
            title=title,
            description=''.join(description),
            color=0xff7f1e
            )


    # タスク一覧
    @commands.command()
    async def task(self,ctx):
        self.connect = DBaccess()
        user = str(ctx.author)
        data = self.connect.getUserdata(user)

        # db.getUserdata の返り値↓
        # [[(ユーザー情報)],[未完了のタスク],[完了したタスク(新しい順に20件)]]

        if data==[[],[],[]]:
            self.connect.addUser(user)
            data = self.connect.getUserdata(user)

        embed = discord.Embed(title=data[0][0][0][:-5]+' のタスク一覧',color=0xff7f1e)

        embed.add_field(name='アクティブなタスク',value='`現在進行中のタスクです。`',inline=False)
        
        if len(data[1]):
            stack = ''
            l = ''
            for i in range(len(data[1])):
                tmp = data[1][i][3] if len(data[1][i][3])<=20 else data[1][i][3][:17]+'...'
                limit = self.time.limit(data[1][i][5])
                stack = stack + str(i+1) + '. ' + tmp + '\n'
                l = l + ('超過 ' if limit<1 else '余裕 ') + (str(limit) if 0<limit else ('1' if limit==0 else str(abs(limit)+1))) +' 日\n'
            embed.add_field(name='タスク',value='```' + stack + '```\n')
            embed.add_field(name='ステータス',value='```' + l + '```\n')
        else:
            embed.add_field(name='未完了のタスク',value='```未完了のタスクはありません```',inline=False)
        
        embed.add_field(name='完了済みのタスク',value='`完了したタスクです。タスクの登録順で最新の10件まで表示します。`',inline=False)

        if len(data[2]):
            stack = ''
            l = ''
            for i in range(len(data[2])):
                tmp = data[2][i][3] if len(data[2][i][3])<=20 else data[2][i][3][:17]+'...'
                stack = stack+str(i+1)+'. '+ tmp +'\n'
                limit = data[2][i][6]
                l = l + ('超過 ' if limit<1 else '余裕 ') + (str(limit) if 0<limit else ('1' if limit==0 else str(abs(limit)+1))) + ' 日で完了\n'
            embed.add_field(name='タスク',value='```' + stack + '```\n')
            embed.add_field(name='ステータス',value='```' + l + '```\n')
        else:
            embed.add_field(name='タスク',value='```完了済みのタスクはありません```',inline=False)
        
        embed.add_field(name='累計完了タスク',value= '`' + str(data[0][0][1]) + '` 件',inline=False)
        await ctx.send(embed=embed)

    # タスク登録
    @commands.command()
    async def addtask(self,ctx,*args):
        self.connect = DBaccess()
        user = str(ctx.author)
        data = self.connect.getUserdata(user)
        if data == [[],[],[]]:
            self.connect.addUser(user)
            data = self.connect.getUserdata(user)

        if len(args) == 2:
            self.connect.addtask(user,args[0],args[1])
            data = self.connect.getUserdata(user)
            await ctx.send(embed=self.genTaskInfo(data[1][-1][0],'タスクを登録しました！'))
        else:
            await ctx.send('```[構文エラー] 引数 "task" に不正な値が入力されました「todo:help」でコマンドの詳細を確認する事が出来ます。```')
    
    # タスクを完了する
    @commands.command()
    async def complete(self,ctx,*args):
        self.connect = DBaccess()
        user = str(ctx.author)
        data = self.connect.getUserdata(user)

        if data == [[],[],[]]:
            self.connect.addUser(user)
            data = self.connect.getUserdata(user)

        if len(args) == 1 and 0 < int(args[0]) and int(args[0]) < len(data[1])+1:
            self.connect.completeTask(user,data[1][int(args[0])-1][0])
            await ctx.send(embed=self.genTaskInfo(data[1][int(args[0])-1][0],'タスクを完了しました！:tada:'))
        else:
            await ctx.send('```[構文エラー] 引数 "taskNum" に不正な値が入力されました「todo:help」でコマンドの詳細を確認する事が出来ます。```')

def setup(bot):
    bot.add_cog(Todo(bot))
    print('[cog] todo was loaded!')