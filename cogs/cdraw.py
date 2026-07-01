from discord.ext import commands
from discord import app_commands
from discord.ext import commands
import discord

import numpy as np
from fractions import Fraction as Frac
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


########## グラフ描画プログラム #############


def solve(a, b, c) -> list:
    """
    二次方程式
    ax^2 + b^x + c = 0
    の解を返す
    """
    if a == b == c == 0:
        return True # 恒真式なので、呼び出し元に例外処理をさせる
    if a == b == 0:
        return []
    if a == 0:
        return [-c/b]

    D = b**2 - 4*a*c
    ans = -b/(2*a)
    if D < 0:
        return []
    elif D == 0:
        return [ans]
    else:
        return [ans+np.sqrt(D)/(2*a), ans-np.sqrt(D)/(2*a)]


class Curve():
    def __init__(self, a, b, c, d, e, f):
        """
        二次曲線
        a + bx + cy + dx^2 + ey^2 + fxy = 0
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.theta = 0

        # 一次変換により xy の項が消えるような θ を設定する
        if d == e and f != 0:
            self.theta = np.pi / 4
        if d != e and f != 0:
            self.theta = np.arctan(f/(e-d)) / 2

        self.phi = 0 # 一次変換してもとに戻るような角度

    def __str__(self):
        a, b, c, d, e, f = self.a, self.b, self.c, self.d, self.e, self.f
        return f"{a} + {b}x + {c}y + {d}x^2 + {e}y^2 + {f}xy = 0"
        
    def regularize(self) -> Curve:
        """
        設定した θ による一次変換
        (X, Y) = (cosθ -sinθ, sinθ cosθ)(x, y)
        をほどこした二次曲線
        A + BX + CY + DX^2 + EY^2 = 0
        を返す
        """
        a, b, c, d, e, f = self.a, self.b, self.c, self.d, self.e, self.f
        COS, SIN = np.cos(self.theta), np.sin(self.theta)
        curve = Curve(
            a,
            b*COS - c*SIN,
            b*SIN + c*COS,
            d*COS**2 + e*SIN**2 - f*SIN*COS,
            d*SIN**2 + e*COS**2 + f*SIN*COS,
            0
        )
        curve.phi = self.phi - self.theta
        return curve


class Area():
    """
    start_x <= x <= end_x かつ start_y <= y <= end_y
    なる(x, y)長方形領域を表すクラス
    """
    def __init__(self, start_x:int, start_y:int, end_x:int, end_y:int):
        if start_x > end_x:
            start_x, end_x = end_x, start_x
        if start_y > end_y:
            start_y, end_y = end_y, start_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def __contains__(self, target:Area|tuple[int, int]) -> bool:
        """
        領域や点(x, y)が含まれているか否か
        """
        if isinstance(target, tuple):
            x, y = target
            return self.start_x <= x <= self.end_x and self.start_y <= y <= self.end_y
        elif isinstance(target, Area):
            return all(
                self.start_x <= target.start_x,
                target.end_x <= self.end_x,
                self.start_y <= target.start_y,
                target.end_y <= self.end_y,
                )
        
    def is_painted(self, x:int, y:int, curve:Curve) -> bool:
        """
        (x, y)を塗るか否かを返す
        """
        cell = Cell(x, y)
        return cell.is_painted(curve)
    
    def painted_pos(self, curve:Curve) -> list[tuple[int, int]]:
        """
        塗る座標を返す
        """
        posses = []

        for x in range(self.start_x, self.end_x):
            for y in range(self.start_y, self.end_y):
                if self.is_painted(x, y, curve):
                    posses.append((x, y))

        return posses
        

class Cell(Area):
    """
    X <= x <= X+1 かつ Y <= y <= Y+1
    なる(x, y)正方形領域（格子）を表すクラス
    """
    def __init__(self, X:int, Y:int):
        super().__init__(X, Y, X+1, Y+1)

    def intersections(self, curve:Curve) -> set[tuple]:
        """
        格子の辺と曲線の交点を返す
        """
        a, b, c, d, e, f = curve.a, curve.b, curve.c, curve.d, curve.e, curve.f
        X, Y = self.start_x, self.start_y

        intersection_points = set()

        # 左側の辺
        solutions = solve(e, f*X+c, d*X**2+b*X+a)
        if solutions is True:
            # Trueが返された場合、曲線が辺とぴったり重なってる直線の場合
            # こうなると処理に困るので、曲線自体を微小距離下にずらして
            # ぴったり重なってないようにする
            curve.a += 0.0001
            return self.intersections(curve)
        else:
            intersection_points |= {(X, y) for y in solutions if (X, y) in self}
        # 右側の辺
        solutions = solve(e, f*(X+1)+c, d*(X+1)**2+b*(X+1)+a)
        if solutions is True:
            curve.a += 0.0001
            return self.intersections(curve)
        else:
            intersection_points |= {((X+1), y) for y in solutions if ((X+1), y) in self}
        # 下側の辺
        solutions = solve(d, f*Y+b, e*Y**2+c*Y+a)
        if solutions is True:
            curve.a += 0.0001
            return self.intersections(curve)
        else:
            intersection_points |= {(x, Y) for x in solutions if (x, Y) in self}
        # 上側の辺
        solutions = solve(d, f*(Y+1)+b, e*(Y+1)**2+c*(Y+1)+a)
        if solutions is True:
            curve.a += 0.0001
            return self.intersections(curve)
        else:
            intersection_points |= {(x, (Y+1)) for x in solutions if (x, (Y+1)) in self}

        return intersection_points
    
    def is_painted(self, curve:Curve) -> bool:
        """
        塗るか否かを返す
        """
        X, Y = self.start_x, self.start_y
        points = self.intersections(curve)
        
        # 格子を4分割し、それぞれに含まれているか否かの関数をつくる
        is_left, is_right, is_bottom, is_top = lambda x: X <= x <= X+0.5, lambda x: X+0.5 <= x <= X+1, lambda y: Y <= y <= Y+0.5, lambda y: Y+0.5 <= y <= Y+1
        is_right_top = lambda x, y: is_right(x) and is_top(y)
        is_right_bottom = lambda x, y: is_right(x) and is_bottom(y)
        is_left_top = lambda x, y: is_left(x) and is_top(y)
        is_left_bottom = lambda x, y: is_left(x) and is_bottom(y)

        funcs = [is_right_top, is_right_bottom, is_left_top, is_left_bottom]

        # 分割した4部分のうち、いくつが交点を含んでいるか？(part_num)
        part_num = len([object() for func in funcs if any(func(*point) for point in points)])

        # 2部分以上なら塗る。そうでないなら塗らない。
        return part_num >= 2


def decide_area(curve:Curve, min_size=50, max_size=100) -> Area:
    """
    描画領域を出力
    max_size : 領域の最大サイズ
    """
    curve = curve.regularize()

    # curve:
    # A + BX + CY + DX^2 + EY^2 = 0
    A, B, C, D, E = curve.a, curve.b, curve.c, curve.d, curve.e

    ### ひとまず曲線がすっぽり収まる領域を計算

    if B == C == D == E == 0:
        # A = 0
        raise Exception("式 A = 0 は曲線ではありません！")
    
    elif D == E == 0:
        # A + BX + CY = 0 (直線)

        if C == 0:
            # Y軸に平行な直線の場合、90度回転させて
            # X軸に平行な直線に帰着させる
            curve.theta = np.pi / 2
            return decide_area(curve)
        
        # Y = (-B/C)X - A/C
        m = Frac(-B/C) # 傾き(分数)
        m1, m2 = m.numerator, m.denominator # 分子と分母。互いに素で m2>0
        
        center = (0, -A/C)
        width, height = 4*m2, 4*m1
        
    elif D*E == 0:
        # 放物線

        if D == 0:
            # X軸方向に開く放物線の場合、90度回転させて
            # Y軸方向に開く放物線に帰着させる
            curve.theta = np.pi / 2
            return decide_area(curve)
        
        # A + BX + CY + DX^2 = 0 (Y軸方向に開く放物線)
        # Y = -D/C (X + B/2D)^2 + (B^2 - 4AD)/4D

        axis_X = -B/(2*D) # 放物線の軸のX座標（焦点のX座標でもある）
        focus_Y = (B*B-4*A*D-C)/(4*D) # 焦点のY座標
        
        center = (axis_X, focus_Y) # 焦点を描画領域の中心とする
        width, height = np.abs(2*np.sqrt(2)*C/D), np.abs(C/D)

    else:
        # A + BX + CY + DX^2 + EY^2 = 0 (楕円 or 双曲線)
        bunshi = B*B*E + C*C*D - 4*A*D*E
        P_ = bunshi / (4*D*D*E)
        Q_ = bunshi / (4*D*E*E)

        if P_ < Q_:
            # 焦点がY軸上にある楕円か双曲線の場合、90度回転させて
            # X軸上にある場合に帰着させる
            curve.theta = np.pi / 2
            return decide_area(curve)
        
        center = (-B/(2*D), C/(2*E))
        width = 4*np.sqrt(P_ - Q_)
        height = 4*np.sqrt(Q_*Q_/P_)

    ### 領域を回転させて、xy平面での領域中心と幅と高さを計算

    def linear_transform(x, y, theta):
        COS, SIN = np.cos(theta), np.sin(theta)
        return (COS*x-SIN*y, SIN*x+COS*y)
    
    def expand_transform(x, y, theta):
        COS, SIN = np.abs(np.cos(theta)), np.abs(np.sin(theta))
        return (COS*x+SIN*y, SIN*x+COS*y)

    center = linear_transform(*center, curve.phi)
    width, height = expand_transform(width, height, curve.phi)

    # 領域を正方形にする（最大幅も考慮）
    true_width = max((min_size, width, height)) # 正方形の辺の長さ
    true_width = min((true_width, max_size))

    # 格子点処理
    true_width = int(true_width)
    center_x, center_y = int(center[0]), int(center[1])

    start = (center_x - true_width//2, center_y - true_width//2)
    end = (start[0] + true_width, start[1] + true_width)

    return Area(*start, *end)


def draw(curve:Curve):

    # 描画領域
    area = decide_area(curve)

    fig, ax = plt.subplots(figsize=(8, 8))

    # 格子目盛り
    xticks = np.arange(area.start_x, area.end_x + 1, 1)
    yticks = np.arange(area.start_y, area.end_y + 1, 1)

    ax.set_xticks(np.arange(area.start_x, area.end_x + 1, 1))
    ax.set_yticks(np.arange(area.start_y, area.end_y + 1, 1))

    ### 目盛りラベル
    # 5の倍数以外は非表示

    # x軸ラベル
    xlabels = []
    for x in xticks:
        if x % 5 == 0:
            xlabels.append(str(x))
        else:
            xlabels.append("")

    # y軸ラベル
    ylabels = []
    for y in yticks:
        if y % 5 == 0:
            ylabels.append(str(y))
        else:
            ylabels.append("")

    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)

    # 格子線
    ax.grid(True, linewidth=0.5)

    # 格子の着色
    for x, y in area.painted_pos(curve):
        rect = patches.Rectangle(
            (x, y),   # 左下座標
            1,
            1,
            facecolor='turquoise'
        )
        ax.add_patch(rect)

    # 表示範囲を設定
    ax.set_xlim(area.start_x, area.end_x)
    ax.set_ylim(area.start_y, area.end_y)

    # 正方形グリッド
    ax.set_aspect('equal')

    plt.savefig("graph.png", format="png", dpi=300)


############################## 


class CDraw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cdraw", description="二次曲線 a+bx+cy+dx²+ey²+fxy=0 を描きます")
    @app_commands.describe(a="a", b="b", c="c", d="d", e="e", f="f")
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id))
    async def cdraw(
        self, interaction: discord.Interaction,
        a:float, b:float, c:float, d:float, e:float, f:float
    ):
        curve = Curve(a, b, c, d, e, f)
        try:
            draw(curve)
        except Exception as error:
            await interaction.response.send_message(str(error))
            
        with open("graph.png", mode="rb") as file:
            await interaction.response.send_message(fp=file)


async def setup(bot: commands.Bot):
    await bot.add_cog(CDraw(bot))
