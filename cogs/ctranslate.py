import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
from typing import Optional
import random


class CTranslate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ctranslate", description="各言語に翻訳できます")
    @app_commands.describe(text="翻訳したい文章(Text-to-be-translated)", language="翻訳先言語-2文字(Language-to-be-translated-2-alphabets)")
    @app_commands.choices(
        language=[
            app_commands.Choice(value="af", name="af : afrikaans / アフリカーンス語"),
            app_commands.Choice(value="sq", name="sq : albanian / アルバニア語"),
            app_commands.Choice(value="am", name="am : amharic / アムハラ語"),
            app_commands.Choice(value="ar", name="ar : arabic / アラビア語"),
            app_commands.Choice(value="hy", name="hy : armenian / アルメニア語"),
            app_commands.Choice(value="az", name="az : azerbaijani / アゼルバイジャン語"),
            app_commands.Choice(value="eu", name="eu : basque / バスク語"),
            app_commands.Choice(value="be", name="be : belarusian / ベラルーシ語"),
            app_commands.Choice(value="bn", name="bn : bengali / ベンガル語"),
            app_commands.Choice(value="bs", name="bs : bosnian / ボスニア語"),
            app_commands.Choice(value="bg", name="bg : bulgarian / ブルガリア語"),
            app_commands.Choice(value="ca", name="ca : catalan / カタロニア語"),
            app_commands.Choice(value="ceb", name="ceb : cebuano / セブアノ語"),
            app_commands.Choice(value="ny", name="ny : chichewa / チチェワ語"),
            app_commands.Choice(value="zh-cn", name="zh-cn : chinese(simplified) / 中国語(簡体字)"),
            app_commands.Choice(value="zh-tw", name="zh-tw : chinese(traditional) / 中国語(繁体字)"),
            app_commands.Choice(value="co", name="co : corsican / コルシカ語"),
            app_commands.Choice(value="hr", name="hr : croatian / クロアチア語"),
            app_commands.Choice(value="cs", name="cs : czech / チェコ語"),
            app_commands.Choice(value="da", name="da : danish / デンマーク語"),
            app_commands.Choice(value="nl", name="nl : dutch / オランダ語"),
            app_commands.Choice(value="en", name="en : english / 英語"),
            app_commands.Choice(value="eo", name="eo : esperanto / エスペラント語"),
            app_commands.Choice(value="et", name="et : estonian / エストニア語"),
            app_commands.Choice(value="tl", name="tl : filipino / フィリピーノ語"),
            app_commands.Choice(value="fi", name="fi : finnish / フィンランド語"),
            app_commands.Choice(value="fr", name="fr : french / フランス語"),
            app_commands.Choice(value="fy", name="fy : frisian / フリジア語"),
            app_commands.Choice(value="gl", name="gl : galician / ガリシア語"),
            app_commands.Choice(value="ka", name="ka : georgian / ゲオルギー語"),
            app_commands.Choice(value="de", name="de : german / ドイツ語"),
            app_commands.Choice(value="el", name="el : greek / ギリシャ語"),
            app_commands.Choice(value="gu", name="gu : gujarati / グジャラート語"),
            app_commands.Choice(value="ht", name="ht : haitian creole / ハイト・クレオール語"),
            app_commands.Choice(value="ha", name="ha : hausa / ハウサ語"),
            app_commands.Choice(value="haw", name="haw : hawaiian / ハワイ語"),
            app_commands.Choice(value="iw", name="iw : hebrew / ヘブライ語"),
            app_commands.Choice(value="he", name="he : hebrew / ヘブライ語"),
            app_commands.Choice(value="hi", name="hi : hindi / ヒンディー語"),
            app_commands.Choice(value="hmn", name="hmn : hmong / モン語"),
            app_commands.Choice(value="hu", name="hu : hungarian / ハンガリー語"),
            app_commands.Choice(value="is", name="is : icelandic / アイスランド語"),
            app_commands.Choice(value="ig", name="ig : igbo / イボ語"),
            app_commands.Choice(value="id", name="id : indonesian / インドネシア語"),
            app_commands.Choice(value="ga", name="ga : irish / アイルランド語"),
            app_commands.Choice(value="it", name="it : italian / イタリア語"),
            app_commands.Choice(value="ja", name="ja : japanese / 日本語"),
            app_commands.Choice(value="jw", name="jw : javanese / ジャワ語"),
            app_commands.Choice(value="kn", name="kn : kannada / カンナダ語"),
            app_commands.Choice(value="kk", name="kk : kazakh / カザフ語"),
            app_commands.Choice(value="km", name="km : khmer / クメール語"),
            app_commands.Choice(value="ko", name="ko : korean / 韓国語"),
            app_commands.Choice(value="ku", name="ku : kurdish(kurmanji) / クルド語(クルマンジ)"),
            app_commands.Choice(value="ky", name="ky : kyrgyz / キルギス語"),
            app_commands.Choice(value="lo", name="lo : lao / ラオス語"),
            app_commands.Choice(value="la", name="la : latin / ラテン語"),
            app_commands.Choice(value="lv", name="lv : latvian / ラトビア語"),
            app_commands.Choice(value="lt", name="lt : lithuanian / リトアニア語"),
            app_commands.Choice(value="lb", name="lb : luxembourgish / ルクセンブルク語"),
            app_commands.Choice(value="mk", name="mk : macedonian / マケドニア語"),
            app_commands.Choice(value="mg", name="mg : malagasy / マラガシ語"),
            app_commands.Choice(value="ms", name="ms : malay / マレー語"),
            app_commands.Choice(value="ml", name="ml : malayalam / マラヤーラム語"),
            app_commands.Choice(value="mt", name="mt : maltese / マルタ語"),
            app_commands.Choice(value="mi", name="mi : maori / マオリ語"),
            app_commands.Choice(value="mr", name="mr : marathi / マラーティー語"),
            app_commands.Choice(value="mn", name="mn : mongolian / モンゴル語"),
            app_commands.Choice(value="my", name="my : myanmar(burmese) / ミャンマー語"),
            app_commands.Choice(value="ne", name="ne : nepali / ネパール語"),
            app_commands.Choice(value="no", name="no : norwegian / ノルウェー語"),
            app_commands.Choice(value="or", name="or : odia / オディア語"),
            app_commands.Choice(value="ps", name="ps : pashto / パシュトー語"),
            app_commands.Choice(value="fa", name="fa : persian / ペルシア語"),
            app_commands.Choice(value="pl", name="pl : polish / ポーランド語"),
            app_commands.Choice(value="pt", name="pt : portuguese / ポルトガル語"),
            app_commands.Choice(value="pa", name="pa : punjabi / パンジャブ語"),
            app_commands.Choice(value="ro", name="ro : romanian / ルーマニア語"),
            app_commands.Choice(value="ru", name="ru : russian / ロシア語"),
            app_commands.Choice(value="sm", name="sm : samoan / サモア語"),
            app_commands.Choice(value="gd", name="gd : scotsgaelic / スコットランド・ゲール語"),
            app_commands.Choice(value="sr", name="sr : serbian / セルビア語"),
            app_commands.Choice(value="st", name="st : sesotho / セソト語"),
            app_commands.Choice(value="sn", name="sn : shona / ショナ語"),
            app_commands.Choice(value="sd", name="sd : sindhi / シンディ語"),
            app_commands.Choice(value="si", name="si : sinhala / シンハラ語"),
            app_commands.Choice(value="sk", name="sk : slovak / スロバキア語"),
            app_commands.Choice(value="sl", name="sl : slovenian / スロベニア語"),
            app_commands.Choice(value="so", name="so : somali / ソマリア語"),
            app_commands.Choice(value="es", name="es : spanish / スペイン語"),
            app_commands.Choice(value="su", name="su : sundanese / スンダ語"),
            app_commands.Choice(value="sw", name="sw : swahili / スワヒリ語"),
            app_commands.Choice(value="sv", name="sv : swedish / スウェーデン語"),
            app_commands.Choice(value="tg", name="tg : tajik / タジク語"),
            app_commands.Choice(value="ta", name="ta : tamil / タミル語"),
            app_commands.Choice(value="te", name="te : telugu / テルグ語"),
            app_commands.Choice(value="th", name="th : thai / タイ語"),
            app_commands.Choice(value="tr", name="tr : turkish / トルコ語"),
            app_commands.Choice(value="uk", name="uk : ukrainian / ウクライナ語"),
            app_commands.Choice(value="ur", name="ur : urdu / ウルドゥー語"),
            app_commands.Choice(value="ug", name="ug : uyghur / ウイグル語"),
            app_commands.Choice(value="uz", name="uz : uzbek / ウズベク語"),
            app_commands.Choice(value="vi", name="vi : vietnamese / ベトナム語"),
            app_commands.Choice(value="cy", name="cy : welsh / ウェールズ語"),
            app_commands.Choice(value="xh", name="xh : xhosa / ホサ語"),
            app_commands.Choice(value="yi", name="yi : yiddish / イディッシュ語"),
            app_commands.Choice(value="yo", name="yo : yoruba / ヨルバ語"),
            app_commands.Choice(value="zu", name="zu : zulu / ズールー語"),
        ]
    )
    async def ctranslate(self, interaction: discord.Interaction, text: str, language: Optional[str] = None):
        await interaction.response.defer(thinking=True)
        translator = Translator()
        textlang = translator.detect(text)

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
                translationsource = textlang.lang
                translationtarget = language.value
                translated_text = await translator.translate(text, dest=language.value)

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
