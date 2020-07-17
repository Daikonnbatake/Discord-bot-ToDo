import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,ctx):
        self.commands=['task','addtask','complete','help','reload']
        self.help=[
            '```todo:task```\n```タスクの一覧を表示します。引数はありません。```',
            '```todo:addtask [引数1] [引数2]```\n```新規のタスクを追加します。\n\n[引数1] にはタスクの内容を256文字以内(20文字以内を推奨)で記入してください。\n[引数2]にはタスクを完了させるまでの目標日数を入力してください。\n\n(例) 5日後までに終わらせるべきタスク「数学の課題」を登録する場合\n\n todo:addtask 数学の課題 5```',
            '```todo:complete [引数1]```\n```登録したタスクが完了した際に完了手続きを行います。\n\n[引数1]に「task」コマンドで表示される「アクティブなタスク」の中から完了したいタスクの番号を入力します。\n\n(例)「アクティブなタスク」の3番目に表示されているタスクを完了する場合\n\ntodo:complete 3```',
            'helpの空きを補填するやつ',
            '```todo:reload```\n```cogファイルをホットリロードします。管理者以外は使用する事が出来ません```'
            ]

    # help埋め込み生成
    def genHelp(self,title,description):
        return discord.Embed(title=title,color=0xff7f1e,description=description)

    @commands.command()
    async def help(self,ctx,*args):
        if len(args) and args[0]!='help':
            if args[0] in self.commands:
                await ctx.send(embed=self.genHelp('ヘルプ:'+args[0],self.help[self.commands.index(args[0])]))
            else:
                await ctx.send(embed=self.genHelp('[エラー]','コマンド`'+args[0]+'`のヘルプは存在しません'))
        else:
            embed = discord.Embed(title='ヘルプ',description='接頭辞「todo:」の後に各コマンドを入力して使用します。\n各コマンドの詳細は「todo:help [コマンド]」で確認する事が出来ます。',color=0xff7f1e)
            embed.add_field(name='todo関連',value='```task \naddtask [タスク]] [日数]\ncomplete [タスク番号]```')
            embed.add_field(name='その他',value='```help [コマンド]\nreload```')
            embed.add_field(name='免責事項',value='```等botのサービスは個人が管理するVPSおよびDBサーバーによって提供されています。\n当botに対し、個人情報その他利用者が持つ機密事項(社内機密等)を登録すると、bot管理者に情報が漏洩する可能性があるためお控えください。\nまたそのような間違った利用によって生じたトラブルについて一切の責任をbot管理者は負いません。ご了承ください。```',inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    print('[cog] help was loaded!')