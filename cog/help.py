import discord,json
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,ctx):
        with open(str(__file__)[:-11]+'meta/help.json',encoding='utf-8') as f:
            self.help=json.load(f)
        with open(str(__file__)[:-11]+'meta/disclaimer.txt',encoding='utf-8') as f:
            self.disclaimer=f.read()

    # help埋め込み生成
    def genHelp(self,title,description):
        return discord.Embed(title=title,color=0xff7f1e,description=description)
        
    @commands.command()
    async def help(self,ctx,*args):
        if len(args) and args[0]!='help':
            if args[0] in self.help.keys():
                await ctx.send(embed=self.genHelp('ヘルプ:'+args[0],self.help[args[0]]))
            else:
                await ctx.send(embed=self.genHelp('[エラー]','コマンド`'+args[0]+'`のヘルプは存在しません'))
        else:
            embed = discord.Embed(title='ヘルプ',description='接頭辞「todo:」の後に各コマンドを入力して使用します。\n各コマンドの詳細は「todo:help [コマンド]」で確認する事が出来ます。',color=0xff7f1e)
            embed.add_field(name='todo関連',value='```task \naddtask [タスク] [日数]\ncomplete [タスク番号]```')
            embed.add_field(name='その他',value='```help [コマンド]\nreload```')
            embed.add_field(name='免責事項',value=self.disclaimer,inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    print('[cog] help was loaded!')