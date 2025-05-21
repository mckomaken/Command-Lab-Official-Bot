import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
# from typing import Optional
import random


class CTranslate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ctranslate", description="各言語に翻訳できます")
    @app_commands.describe(text="翻訳したい文章(Text-to-be-translated)", language="翻訳先言語(translation-target-language)")
    # @app_commands.choices(
    #     language=[
    #         app_commands.Choice(value="af", name="afrikaans/アフリカーンス語"),
    #         app_commands.Choice(value="sq", name="albanian/アルバニア語"),
    #         app_commands.Choice(value="am", name="amharic/アムハラ語"),
    #         app_commands.Choice(value="ar", name="arabic/アラビア語"),
    #         app_commands.Choice(value="hy", name="armenian/アルメニア語"),
    #         app_commands.Choice(value="az", name="azerbaijani/アゼルバイジャン語"),
    #         app_commands.Choice(value="eu", name="basque/バスク語"),
    #         app_commands.Choice(value="be", name="belarusian/ベラルーシ語"),
    #         app_commands.Choice(value="bn", name="bengali/ベンガル語"),
    #         app_commands.Choice(value="bs", name="bosnian/ボスニア語"),
    #         app_commands.Choice(value="bg", name="bulgarian/ブルガリア語"),
    #         app_commands.Choice(value="ca", name="catalan/カタロニア語"),
    #         app_commands.Choice(value="ceb", name="cebuano/セブアノ語"),
    #         app_commands.Choice(value="ny", name="chichewa/チチェワ語"),
    #         app_commands.Choice(value="zh-cn", name="chinese-simplified/中国簡体字"),
    #         app_commands.Choice(value="zh-tw", name="chinese-traditional/中国繁体字"),
    #         app_commands.Choice(value="co", name="corsican/コルシカ語"),
    #         app_commands.Choice(value="hr", name="croatian/クロアチア語"),
    #         app_commands.Choice(value="cs", name="czech/チェコ語"),
    #         app_commands.Choice(value="da", name="danish/デンマーク語"),
    #         app_commands.Choice(value="nl", name="dutch/オランダ語"),
    #         app_commands.Choice(value="en", name="english/英語"),
    #         app_commands.Choice(value="eo", name="esperanto/エスペラント語"),
    #         app_commands.Choice(value="et", name="estonian/エストニア語"),
    #         app_commands.Choice(value="tl", name="filipino/フィリピーノ語"),
    #         app_commands.Choice(value="fi", name="finnish/フィンランド語"),
    #         app_commands.Choice(value="fr", name="french/フランス語"),
    #         app_commands.Choice(value="fy", name="frisian/フリジア語"),
    #         app_commands.Choice(value="gl", name="galician/ガリシア語"),
    #         # app_commands.Choice(value="ka", name="georgian/ゲオルギー語"),
    #         # app_commands.Choice(value="de", name="german/ドイツ語"),
    #         # app_commands.Choice(value="el", name="greek/ギリシャ語"),
    #         # app_commands.Choice(value="gu", name="gujarati/グジャラート語"),
    #         # app_commands.Choice(value="ht", name="haitian creole/ハイト・クレオール語"),
    #         # app_commands.Choice(value="ha", name="hausa/ハウサ語"),
    #         # app_commands.Choice(value="haw", name="hawaiian/ハワイ語"),
    #         # app_commands.Choice(value="iw", name="hebrew/ヘブライ語"),
    #         # app_commands.Choice(value="he", name="hebrew/ヘブライ語"),
    #         # app_commands.Choice(value="hi", name="hindi/ヒンディー語"),
    #         # app_commands.Choice(value="hmn", name="hmong/モン語"),
    #         # app_commands.Choice(value="hu", name="hungarian/ハンガリー語"),
    #         # app_commands.Choice(value="is", name="icelandic/アイスランド語"),
    #         # app_commands.Choice(value="ig", name="igbo/イボ語"),
    #         # app_commands.Choice(value="id", name="indonesian/インドネシア語"),
    #         # app_commands.Choice(value="ga", name="irish/アイルランド語"),
    #         # app_commands.Choice(value="it", name="italian/イタリア語"),
    #         # app_commands.Choice(value="ja", name="japanese/日本語"),
    #         # app_commands.Choice(value="jw", name="javanese/ジャワ語"),
    #         # app_commands.Choice(value="kn", name="kannada/カンナダ語"),
    #         # app_commands.Choice(value="kk", name="kazakh/カザフ語"),
    #         # app_commands.Choice(value="km", name="khmer/クメール語"),
    #         # app_commands.Choice(value="ko", name="korean/韓国語"),
    #         # app_commands.Choice(value="ku", name="kurdish(kurmanji)/クルド語"),
    #         # app_commands.Choice(value="ky", name="kyrgyz/キルギス語"),
    #         # app_commands.Choice(value="lo", name="lao/ラオス語"),
    #         # app_commands.Choice(value="la", name="latin/ラテン語"),
    #         # app_commands.Choice(value="lv", name="latvian/ラトビア語"),
    #         # app_commands.Choice(value="lt", name="lithuanian/リトアニア語"),
    #         # app_commands.Choice(value="lb", name="luxembourgish/ルクセンブルク語"),
    #         # app_commands.Choice(value="mk", name="macedonian/マケドニア語"),
    #         # app_commands.Choice(value="mg", name="malagasy/マラガシ語"),
    #         # app_commands.Choice(value="ms", name="malay/マレー語"),
    #         # app_commands.Choice(value="ml", name="malayalam/マラヤーラム語"),
    #         # app_commands.Choice(value="mt", name="maltese/マルタ語"),
    #         # app_commands.Choice(value="mi", name="maori/マオリ語"),
    #         # app_commands.Choice(value="mr", name="marathi/マラーティー語"),
    #         # app_commands.Choice(value="mn", name="mongolian/モンゴル語"),
    #         # app_commands.Choice(value="my", name="myanmar(burmese)/ミャンマー語"),
    #         # app_commands.Choice(value="ne", name="nepali/ネパール語"),
    #         # app_commands.Choice(value="no", name="norwegian/ノルウェー語"),
    #         # app_commands.Choice(value="or", name="odia/オディア語"),
    #         # app_commands.Choice(value="ps", name="pashto/パシュトー語"),
    #         # app_commands.Choice(value="fa", name="persian/ペルシア語"),
    #         # app_commands.Choice(value="pl", name="polish/ポーランド語"),
    #         # app_commands.Choice(value="pt", name="portuguese/ポルトガル語"),
    #         # app_commands.Choice(value="pa", name="punjabi/パンジャブ語"),
    #         # app_commands.Choice(value="ro", name="romanian/ルーマニア語"),
    #         # app_commands.Choice(value="ru", name="russian/ロシア語"),
    #         # app_commands.Choice(value="sm", name="samoan/サモア語"),
    #         # app_commands.Choice(value="gd", name="scotsgaelic/スコットランド・ゲール語"),
    #         # app_commands.Choice(value="sr", name="serbian/セルビア語"),
    #         # app_commands.Choice(value="st", name="sesotho/セソト語"),
    #         # app_commands.Choice(value="sn", name="shona/ショナ語"),
    #         # app_commands.Choice(value="sd", name="sindhi/シンディ語"),
    #         # app_commands.Choice(value="si", name="sinhala/シンハラ語"),
    #         # app_commands.Choice(value="sk", name="slovak/スロバキア語"),
    #         # app_commands.Choice(value="sl", name="slovenian/スロベニア語"),
    #         # app_commands.Choice(value="so", name="somali/ソマリア語"),
    #         # app_commands.Choice(value="es", name="spanish/スペイン語"),
    #         # app_commands.Choice(value="su", name="sundanese/スンダ語"),
    #         # app_commands.Choice(value="sw", name="swahili/スワヒリ語"),
    #         # app_commands.Choice(value="sv", name="swedish/スウェーデン語"),
    #         # app_commands.Choice(value="tg", name="tajik/タジク語"),
    #         # app_commands.Choice(value="ta", name="tamil/タミル語"),
    #         # app_commands.Choice(value="te", name="telugu/テルグ語"),
    #         # app_commands.Choice(value="th", name="thai/タイ語"),
    #         # app_commands.Choice(value="tr", name="turkish/トルコ語"),
    #         # app_commands.Choice(value="uk", name="ukrainian/ウクライナ語"),
    #         # app_commands.Choice(value="ur", name="urdu/ウルドゥー語"),
    #         # app_commands.Choice(value="ug", name="uyghur/ウイグル語"),
    #         # app_commands.Choice(value="uz", name="uzbek/ウズベク語"),
    #         # app_commands.Choice(value="vi", name="vietnamese/ベトナム語"),
    #         # app_commands.Choice(value="cy", name="welsh/ウェールズ語"),
    #         # app_commands.Choice(value="xh", name="xhosa/ホサ語"),
    #         # app_commands.Choice(value="yi", name="yiddish/イディッシュ語"),
    #         # app_commands.Choice(value="yo", name="yoruba/ヨルバ語"),
    #         # app_commands.Choice(value="zu", name="zulu/ズールー語"),
    #     ]
    # )
    async def ctranslate(self, interaction: discord.Interaction, text: str, language: str = None):
        await interaction.response.defer(thinking=True)
        translator = Translator()
        textlang = translator.detect(text)

        try:
            if language is None:
                if textlang == "ja":
                    translationsource = "ja"
                    translationtarget = "en"
                    translated_text = await translator.translate(text, src="ja", dest="en")
                else:
                    translationsource = textlang
                    translationtarget = "ja"
                    translated_text = await translator.translate(text, dest="ja")
            else:
                translationsource = textlang
                translationtarget = language
                translated_text = await translator.translate(text, dest=language)

            translated_embed = discord.Embed(
                title="翻訳結果",
                description=f"【翻訳元(translation source)/{translationsource}】\n```{text}```\n↓\n【翻訳先(translation target)/{translationtarget}】\n```{translated_text.text}```",
                color=0x00ff00
            )
            translated_embed.set_footer(text="Translated by Google Translate")
            translated_embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
            await interaction.followup.send(embed=translated_embed)

        except Exception as e:
            translated_embed = discord.Embed(
                title="翻訳エラー",
                description=f"翻訳に失敗しました\nエラー内容: {e}",
                color=0xff0000
            )
            await interaction.followup.send(embed=translated_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CTranslate(bot))
