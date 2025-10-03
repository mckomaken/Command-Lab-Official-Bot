import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
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


class DeleteButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()


class CTranslate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith("Ctr"):
            text = str(message.content.split(" ")[1])
            translator = Translator()
            textlang = await translator.detect(text)

            try:
                if textlang.lang == "ja":
                    translated_text = await translator.translate(text, src="ja", dest="en")
                else:
                    translated_text = await translator.translate(text, dest="ja")

                translated_embed = discord.Embed(
                    title="翻訳結果",
                    description=f"{translated_text.text}",
                    color=0x008c00
                )
                translated_embed.set_author(name=message.author.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if message.author.avatar is None else message.author.avatar.url)
                await message.reply(embed=translated_embed)

            except Exception as e:
                delete_button = DeleteButton(
                    label="削除",
                    style=discord.ButtonStyle.gray
                )
                view = discord.ui.View(timeout=None)
                view.add_item(delete_button)
                await message.reply(f"【翻訳失敗/エラー発生】\n{e}", view=view)

    @app_commands.command(name="ctranslate", description="各言語に翻訳できます(Can be translated into any language)")
    @app_commands.describe(text="翻訳したい文章(Text-to-be-translated)", language="翻訳先言語(translation-target-language)")
    async def ctranslate(self, interaction: discord.Interaction, text: str, language: str = None):
        await interaction.response.defer(thinking=True)
        translator = Translator()
        textlang = await translator.detect(text)

        try:
            if language is None:
                if textlang.lang == "ja":
                    translationsource = "ja"
                    translationtarget = "English/英語"
                    translated_text = await translator.translate(text, src="ja", dest="en")
                else:
                    translationsource = textlang.lang
                    translationtarget = "Japanese/日本語"
                    translated_text = await translator.translate(text, dest="ja")
            else:
                langcode = str(language.split(" ")[0])
                langname = f"({str(language.split(" ")[3])}/{str(language.split(" ")[5])})"
                translationsource = textlang.lang
                translationtarget = langname
                translated_text = await translator.translate(text, dest=langcode)

            translated_embed = discord.Embed(
                title="翻訳結果",
                description=f"【翻訳元(translation source)/{translationsource}】\n```{text}```\n【翻訳先(translation target)】\n{translationtarget}\n```{translated_text.text}```",
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
        filtered_languages = [lang for lang in LANGUAGES if current.lower() in lang.lower()]
        return [app_commands.Choice(name=lang, value=lang) for lang in filtered_languages[:25]]


async def setup(bot: commands.Bot):
    await bot.add_cog(CTranslate(bot))
