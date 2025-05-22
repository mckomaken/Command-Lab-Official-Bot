import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
# from typing import Optional
import random

LANGUAGES = [
    "af : afrikaans / アフリカーンス語",
    "sq : albanian / アルバニア語",
    "am : amharic / アムハラ語",
    "ar : arabic / アラビア語",
    "hy : armenian / アルメニア語",
    "az : azerbaijani / アゼルバイジャン語",
    "eu : basque / バスク語",
    "be : belarusian / ベラルーシ語",
    "bn : bengali / ベンガル語",
    "bs : bosnian / ボスニア語",
    "bg : bulgarian / ブルガリア語",
    "ca : catalan / カタロニア語",
    "ceb : cebuano / セブアノ語",
    "ny : chichewa / チチェワ語",
    "zh-cn : chinese(simplified) / 中国語(簡体字)",
    "zh-tw : chinese(traditional) / 中国語(繁体字)",
    "co : corsican / コルシカ語",
    "hr : croatian / クロアチア語",
    "cs : czech / チェコ語",
    "da : danish / デンマーク語",
    "nl : dutch / オランダ語",
    "en : english / 英語",
    "eo : esperanto / エスペラント語",
    "et : estonian / エストニア語",
    "tl : filipino / フィリピーノ語",
    "fi : finnish / フィンランド語",
    "fr : french / フランス語",
    "fy : frisian / フリジア語",
    "gl : galician / ガリシア語",
    "ka : georgian / ゲオルギー語",
    "de : german / ドイツ語",
    "el : greek / ギリシャ語",
    "gu : gujarati / グジャラート語",
    "ht : haitian creole / ハイト・クレオール語",
    "ha : hausa / ハウサ語",
    "haw : hawaiian / ハワイ語",
    "iw : hebrew / ヘブライ語",
    "he : hebrew / ヘブライ語",
    "hi : hindi / ヒンディー語",
    "hmn : hmong / モン語",
    "hu : hungarian / ハンガリー語",
    "is : icelandic / アイスランド語",
    "ig : igbo / イボ語",
    "id : indonesian / インドネシア語",
    "ga : irish / アイルランド語",
    "it : italian / イタリア語",
    "ja : japanese / 日本語",
    "jw : javanese / ジャワ語",
    "kn : kannada / カンナダ語",
    "kk : kazakh / カザフ語",
    "km : khmer / クメール語",
    "ko : korean / 韓国語",
    "ku : kurdish(kurmanji) / クルド語(クルマンジ)",
    "ky : kyrgyz / キルギス語",
    "lo : lao / ラオス語",
    "la : latin / ラテン語",
    "lv : latvian / ラトビア語",
    "lt : lithuanian / リトアニア語",
    "lb : luxembourgish / ルクセンブルク語",
    "mk : macedonian / マケドニア語",
    "mg : malagasy / マラガシ語",
    "ms : malay / マレー語",
    "ml : malayalam / マラヤーラム語",
    "mt : maltese / マルタ語",
    "mi : maori / マオリ語",
    "mr : marathi / マラーティー語",
    "mn : mongolian / モンゴル語",
    "my : myanmar(burmese) / ミャンマー語",
    "ne : nepali / ネパール語",
    "no : norwegian / ノルウェー語",
    "or : odia / オディア語",
    "ps : pashto / パシュトー語",
    "fa : persian / ペルシア語",
    "pl : polish / ポーランド語",
    "pt : portuguese / ポルトガル語",
    "pa : punjabi / パンジャブ語",
    "ro : romanian / ルーマニア語",
    "ru : russian / ロシア語",
    "sm : samoan / サモア語",
    "gd : scotsgaelic / スコットランド・ゲール語",
    "sr : serbian / セルビア語",
    "st : sesotho / セソト語",
    "sn : shona / ショナ語",
    "sd : sindhi / シンディ語",
    "si : sinhala / シンハラ語",
    "sk : slovak / スロバキア語",
    "sl : slovenian / スロベニア語",
    "so : somali / ソマリア語",
    "es : spanish / スペイン語",
    "su : sundanese / スンダ語",
    "sw : swahili / スワヒリ語",
    "sv : swedish / スウェーデン語",
    "tg : tajik / タジク語",
    "ta : tamil / タミル語",
    "te : telugu / テルグ語",
    "th : thai / タイ語",
    "tr : turkish / トルコ語",
    "uk : ukrainian / ウクライナ語",
    "ur : urdu / ウルドゥー語",
    "ug : uyghur / ウイグル語",
    "uz : uzbek / ウズベク語",
    "vi : vietnamese / ベトナム語",
    "cy : welsh / ウェールズ語",
    "xh : xhosa / ホサ語",
    "yi : yiddish / イディッシュ語",
    "yo : yoruba / ヨルバ語",
    "zu : zulu / ズールー語",
]


class CTranslate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ctranslate", description="各言語に翻訳できます(Can be translated into any language)")
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
        textlang = await translator.detect(text)

        try:
            if language is None:
                if textlang.lang == "ja":
                    translationsource = "ja"
                    translationtarget = "en"
                    translated_text = await translator.translate(text, src="ja", dest="en")
                else:
                    translationsource = textlang.lang
                    translationtarget = "ja"
                    translated_text = await translator.translate(text, dest="ja")
            else:
                langcode = str(language(" ")[0])
                translationsource = textlang.lang
                translationtarget = langcode
                translated_text = await translator.translate(text, dest=langcode)

            translated_embed = discord.Embed(
                title="翻訳結果",
                description=f"【翻訳元(translation source)/{translationsource}】\n```{text}```\n【翻訳先(translation target)/{translationtarget}】\n```{translated_text.text}```",
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

    @ctranslate.autocomplete("language")
    async def translate_language(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=n, value=n) for n in LANGUAGES[:25]]


async def setup(bot: commands.Bot):
    await bot.add_cog(CTranslate(bot))
