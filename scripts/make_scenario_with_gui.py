import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import re
import numpy as np


class GFootballScenarioViewer:
    """
    GFootballのシナリオをGUIで表示し、プレイヤーとボールをインタラクティブに操作するビューアである。
    """

    def __init__(self, master):
        self.master = master
        master.title("GFootball Scenario Viewer")

        self.ball_position = None
        self.left_team_players = []  # [(x, y, role_str), ...]
        self.right_team_players = []  # [(x, y, role_str), ...]
        self.active_object = None  # 現在ドラッグ中のオブジェクト (player or ball)
        self.offset_x = 0
        self.offset_y = 0
        self.is_left_team_active = (
            False  # TrueならLeft Team、FalseならRight Teamのプレイヤーがアクティブ
        )

        # シナリオ設定値を保持する辞書
        self.scenario_config = {
            "game_duration": 3000,
            "right_team_difficulty": 1.0,
            "left_team_difficulty": 1.0,
            "deterministic": False,
            "end_episode_on_score": True,
        }

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # ツールバーの追加
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # イベントハンドラのバインド
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_drag)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        # UIボタン
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.load_button = tk.Button(
            button_frame, text="Load Scenario", command=self.load_scenario
        )
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(
            button_frame, text="Save Scenario", command=self.save_scenario
        )
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button.config(state=tk.DISABLED)  # 初期状態では無効

        self.draw_field()

    def draw_field(self):
        """
        Matplotlibの軸を初期化し、GFootballフィールドを描画する。
        """
        self.ax.clear()
        self.ax.set_title("GFootball Scenario Viewer (Drag Players/Ball)", fontsize=14)
        self.ax.set_xlabel("X-coordinate", fontsize=12)
        self.ax.set_ylabel("Y-coordinate", fontsize=12)
        self.ax.grid(True, linestyle="--", alpha=0.7)
        self.ax.axvline(x=0, color="gray", linestyle="--", linewidth=0.8)  # フィールド中央のライン
        self.ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
        self.ax.set_xlim([-1.0, 1.0])
        self.ax.set_ylim([-0.5, 0.5])
        self.ax.set_aspect("equal", adjustable="box")

        # 凡例用のダミープロット
        self.ax.scatter([], [], color="blue", marker="o", label="Left Team Player")
        self.ax.scatter([], [], color="red", marker="x", label="Right Team Player")
        self.ax.legend(loc="upper right")

        self.canvas.draw_idle()

    def load_scenario(self):
        """
        シナリオファイルを読み込み、プレイヤーとボールのデータを抽出してプロットを更新する。
        """
        filepath = filedialog.askopenfilename(
            title="Select GFootball Scenario File",
            filetypes=[("Scenario files", "*.py"), ("All files", "*.*")],
        )
        if not filepath:
            return

        try:
            (
                self.ball_position,
                self.left_team_players,
                self.right_team_players,
                self.scenario_config,
            ) = self._extract_gfootball_scenario_data(filepath)
            self.draw_scenario_elements()
            self.save_button.config(state=tk.NORMAL)  # ファイル読み込み後、保存ボタンを有効化
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load scenario: {e}")
            self.ball_position = None
            self.left_team_players = []
            self.right_team_players = []
            self.scenario_config = {  # エラー時はデフォルト値に戻す
                "game_duration": 3000,
                "right_team_difficulty": 1.0,
                "left_team_difficulty": 1.0,
                "deterministic": False,
                "end_episode_on_score": True,
            }
            self.draw_scenario_elements()  # エラー時はクリアされた状態を描画
            self.save_button.config(state=tk.DISABLED)

    def save_scenario(self):
        """
        現在のプレイヤーとボールの位置をGFootballシナリオファイル形式で保存する。
        元のシナリオファイルの設定情報も保持する。
        """
        filepath = filedialog.asksaveasfilename(
            title="Save GFootball Scenario File",
            defaultextension=".txt",
            filetypes=[("Scenario files", "*.py"), ("All files", "*.*")],
        )
        if not filepath:
            return

        try:
            with open(filepath, "w") as f:
                f.write("from gfootball.scenarios import *\n\n")  # scenariosのインポートを追加

                f.write("def build_scenario(builder):\n")
                # 抽出したconfig設定を記述
                f.write(
                    f"    builder.config().game_duration = {self.scenario_config.get('game_duration', 3000)}\n"
                )
                f.write(
                    f"    builder.config().right_team_difficulty = {self.scenario_config.get('right_team_difficulty', 1.0)}\n"
                )
                f.write(
                    f"    builder.config().left_team_difficulty = {self.scenario_config.get('left_team_difficulty', 1.0)}\n"
                )
                f.write(
                    f"    builder.config().deterministic = {self.scenario_config.get('deterministic', False)}\n"
                )
                f.write(
                    f"    builder.config().end_episode_on_score = {self.scenario_config.get('end_episode_on_score', True)}\n"
                )

                if self.ball_position:
                    f.write(
                        f"    builder.SetBallPosition({self.ball_position[0]:.6f}, {self.ball_position[1]:.6f})\n"
                    )

                # 元ファイルのEpisodeNumber() % 2 == 0 ロジックを再現
                f.write("    if builder.EpisodeNumber() % 2 == 0:\n")
                f.write("        first_team = Team.e_Left\n")
                f.write("        second_team = Team.e_Right\n")
                f.write("    else:\n")
                f.write("        first_team = Team.e_Right\n")
                f.write("        second_team = Team.e_Left\n")

                f.write("    builder.SetTeam(first_team)\n")
                for x, y, role in self.left_team_players:
                    f.write(
                        f"    builder.AddPlayer({x:.6f}, {y:.6f}, e_PlayerRole_{role})\n"
                    )

                f.write("    builder.SetTeam(second_team)\n")
                # Right teamのデータは、シナリオファイルではX座標が反転した状態で記述されるため、再反転する
                for x, y, role in self.right_team_players:
                    f.write(
                        f"    builder.AddPlayer({-x:.6f}, {y:.6f}, e_PlayerRole_{role})\n"
                    )  # ここで反転

            messagebox.showinfo("Success", f"Scenario saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save scenario: {e}")

    def _extract_gfootball_scenario_data(self, filepath):
        """
        GFootballのシナリオファイルを読み込み、ボール位置、両チームの
        プレイヤー情報（座標と役割）、および設定値を抽出する。
        Right TeamのX座標は、GUI表示のために全体座標系に反転させる。
        """
        with open(filepath, "r") as f:
            content = f.read()

        ball_position = None
        left_team_players = []
        right_team_players = []
        scenario_config = {
            "game_duration": 3000,  # デフォルト値
            "right_team_difficulty": 1.0,
            "left_team_difficulty": 1.0,
            "deterministic": False,
            "end_episode_on_score": True,
        }

        # ボールの位置を抽出
        ball_match = re.search(
            r"builder\.SetBallPosition\(([-+]?\d+\.\d+),\s*([-+]?\d+\.\d+)\)", content
        )
        if ball_match:
            ball_position = (float(ball_match.group(1)), float(ball_match.group(2)))

        # builder.config() の設定値を抽出
        config_matches = re.findall(
            r"builder\.config\(\)\.([a-zA-Z_]+)\s*=\s*(.+)", content
        )
        for key, value_str in config_matches:
            try:
                # 文字列を適切な型に変換
                if value_str.lower() == "true":
                    scenario_config[key] = True
                elif value_str.lower() == "false":
                    scenario_config[key] = False
                elif "." in value_str:
                    scenario_config[key] = float(value_str)
                else:
                    scenario_config[key] = int(value_str)
            except ValueError:
                # 変換できない場合は元の文字列を保持するか、無視する
                scenario_config[key] = value_str

        # builder.SetTeam(first_team) と builder.SetTeam(second_team) の間のブロックを抽出
        first_team_block_match = re.search(
            r"builder\.SetTeam\(\s*first_team\s*\)\s*(.*?)(?=builder\.SetTeam\(\s*second_team\s*\))",
            content,
            re.DOTALL,
        )
        if first_team_block_match:
            first_team_block = first_team_block_match.group(1)
            player_matches = re.findall(
                r"builder\.AddPlayer\(([-+]?\d+\.\d+),\s*([-+]?\d+\.\d+),\s*e_PlayerRole_([A-Za-z_]+)\)",
                first_team_block,
            )
            left_team_players = [
                (float(x), float(y), role) for x, y, role in player_matches
            ]

        # builder.SetTeam(second_team) 以降のブロックを抽出
        second_team_block_match = re.search(
            r"builder\.SetTeam\(\s*second_team\s*\)\s*(.*)", content, re.DOTALL
        )
        if second_team_block_match:
            second_team_block = second_team_block_match.group(1)
            player_matches = re.findall(
                r"builder\.AddPlayer\(([-+]?\d+\.\d+),\s*([-+]?\d+\.\d+),\s*e_PlayerRole_([A-Za-z_]+)\)",
                second_team_block,
            )
            # GUI表示のため、Right TeamのX座標を反転
            right_team_players = [
                (-float(x), float(y), role) for x, y, role in player_matches
            ]

        return ball_position, left_team_players, right_team_players, scenario_config

    def draw_scenario_elements(self):
        """
        現在のプレイヤーとボールの位置に基づいて、プロットを再描画する。
        """
        self.draw_field()  # フィールドを再描画して既存の要素をクリア

        # Left Teamのプレイヤーを役割のテキストでプロット
        for i, (x, y, role) in enumerate(self.left_team_players):
            self.ax.text(
                x,
                y,
                role,
                color="blue",
                ha="center",
                va="center",
                fontsize=9,
                bbox=dict(
                    facecolor="lightblue",
                    alpha=0.5,
                    edgecolor="blue",
                    boxstyle="round,pad=0.3",
                ),
                picker=True,  # ピッキング可能にする
                gid=f"left_player_{i}",
            )  # 一意なIDを設定

        # Right Teamのプレイヤーを役割のテキストでプロット
        for i, (x, y, role) in enumerate(self.right_team_players):
            self.ax.text(
                x,
                y,
                role,
                color="red",
                ha="center",
                va="center",
                fontsize=9,
                bbox=dict(
                    facecolor="salmon",
                    alpha=0.5,
                    edgecolor="red",
                    boxstyle="round,pad=0.3",
                ),
                picker=True,  # ピッキング可能にする
                gid=f"right_player_{i}",
            )  # 一意なIDを設定

        # ボールの位置をプロット
        if self.ball_position:
            self.ax.scatter(
                self.ball_position[0],
                self.ball_position[1],
                color="black",
                label="Ball",
                marker="*",
                s=300,
                zorder=5,
                picker=True,  # ピッキング可能にする
                gid="ball",
            )  # 一意なIDを設定

        self.canvas.draw_idle()

    def on_press(self, event):
        """
        マウスボタンが押されたときのイベントハンドラである。
        クリックされた位置に最も近いプレイヤーまたはボールを選択する。
        """
        if event.inaxes != self.ax:
            self.active_object = None
            return

        # ボールがクリックされたかチェック
        if self.ball_position:
            dist_ball = np.sqrt(
                (event.xdata - self.ball_position[0]) ** 2
                + (event.ydata - self.ball_position[1]) ** 2
            )
            # ボールが最も近いオブジェクトか、または非常に近い距離でクリックされた場合
            if dist_ball < 0.03:  # 検出感度を調整
                self.active_object = {"type": "ball", "index": None}
                self.offset_x = event.xdata - self.ball_position[0]
                self.offset_y = event.ydata - self.ball_position[1]
                return

        # プレイヤーがクリックされたかチェック
        min_dist = float("inf")
        closest_player_info = None

        # Left Team
        for i, (x, y, role) in enumerate(self.left_team_players):
            dist = np.sqrt((event.xdata - x) ** 2 + (event.ydata - y) ** 2)
            if dist < min_dist and dist < 0.05:  # 検出感度を調整
                min_dist = dist
                closest_player_info = {"type": "player", "team": "left", "index": i}

        # Right Team (表示座標で距離計算)
        for i, (x, y, role) in enumerate(self.right_team_players):
            dist = np.sqrt((event.xdata - x) ** 2 + (event.ydata - y) ** 2)
            if dist < min_dist and dist < 0.05:  # 検出感度を調整
                min_dist = dist
                closest_player_info = {"type": "player", "team": "right", "index": i}

        if closest_player_info:
            self.active_object = closest_player_info
            if closest_player_info["team"] == "left":
                player_x, player_y, _ = self.left_team_players[
                    closest_player_info["index"]
                ]
            else:  # right team
                player_x, player_y, _ = self.right_team_players[
                    closest_player_info["index"]
                ]

            self.offset_x = event.xdata - player_x
            self.offset_y = event.ydata - player_y
        else:
            self.active_object = None

    def on_drag(self, event):
        """
        マウスがドラッグされたときのイベントハンドラである。
        選択中のオブジェクトをマウスの位置に合わせて移動させる。
        """
        if self.active_object is None or event.inaxes != self.ax:
            return

        if event.xdata is None or event.ydata is None:
            return  # マウスがプロット範囲外に出た場合

        new_x = event.xdata - self.offset_x
        new_y = event.ydata - self.offset_y

        # フィールド境界の制限
        new_x = max(min(new_x, self.ax.get_xlim()[1]), self.ax.get_xlim()[0])
        new_y = max(min(new_y, self.ax.get_ylim()[1]), self.ax.get_ylim()[0])

        if self.active_object["type"] == "ball":
            self.ball_position = (new_x, new_y)
        elif self.active_object["type"] == "player":
            idx = self.active_object["index"]
            if self.active_object["team"] == "left":
                role = self.left_team_players[idx][2]
                self.left_team_players[idx] = (new_x, new_y, role)
            else:  # right team
                role = self.right_team_players[idx][2]
                self.right_team_players[idx] = (new_x, new_y, role)  # 表示座標で更新

        self.draw_scenario_elements()

    def on_release(self, event):
        """
        マウスボタンが離されたときのイベントハンドラである。
        アクティブなオブジェクトをリセットする。
        """
        self.active_object = None


# メイン処理
if __name__ == "__main__":
    root = tk.Tk()
    app = GFootballScenarioViewer(root)
    root.mainloop()
