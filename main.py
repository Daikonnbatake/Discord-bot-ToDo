from discord.ext import commands
import discord
import os,sys

bot = commands.Bot(command_prefix='todo:',help_command=None)
CWD = str(__file__)[:-8]
with open(CWD+'/meta/bot.txt') as f:
    TOKEN = f.read()
with open(CWD+'/meta/admin.txt') as f:
    ADMINS = f.read().split('\n')

cogs = os.listdir(CWD + '/cog')
for cog in cogs:
    if(cog[len(cog)-3:] == '.py'):
        bot.load_extension('cog.' + str(cog[:-3]))

@bot.event
async def on_ready():
    print('起動しました')
    print('current dir: '+CWD)

@bot.command()
async def reload(ctx):
    if ctx.author in ADMINS:
        cogs = os.listdir(CWD + '/cog')
        allcogs = ''
        for cog in cogs:
            if(cog[len(cog)-3:] == '.py'):
                bot.reload_extension('cog.' + str(cog[:-3]))
                allcogs = allcogs + ( 'cog.' + str(cog[:-3]) + '\n')
        em = discord.Embed(color=0xff7f1e)
        em.add_field(name='再読込されたコグ一覧',value=allcogs)
        await ctx.send(embed=em)
    else:
        '```[権限エラー] todo:reload を実行する権限が有りません```'

bot.run(TOKEN)