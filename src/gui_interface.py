"""
CustomTkinter GUI Interface for BMI Calculator
SuperClaude Framework - 仕様駆動開発

モダンなGUIインターフェースの実装
"""

import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from datetime import datetime, timedelta
from typing import List, Optional
import os

from bmi_calculator import BMICalculator, BMIResult, HealthCategory


class BMIApp(ctk.CTk):
    """BMI計算機のメインアプリケーション"""
    
    def __init__(self):
        super().__init__()
        
        # BMI Calculator インスタンス
        self.calculator = BMICalculator()
        
        # データ保存用
        self.history: List[BMIResult] = []
        self.data_file = "bmi_history.json"
        
        # ウィンドウ設定
        self.setup_window()
        
        # テーマ設定
        self.setup_theme()
        
        # UI作成
        self.create_widgets()
        
        # データロード
        self.load_history()
        
        # 初期フォーカス設定
        self.height_entry.focus()
    
    def setup_window(self):
        """ウィンドウの基本設定"""
        self.title("BMI Calculator - 健康チェッカー")
        self.geometry("700x600")
        self.minsize(600, 500)
        
        # ウィンドウを中央に配置
        self.center_window()
    
    def center_window(self):
        """ウィンドウを画面中央に配置"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_theme(self):
        """テーマとカラーの設定"""
        ctk.set_appearance_mode("system")  # システムテーマに従う
        ctk.set_default_color_theme("blue")  # デフォルトカラーテーマ
    
    def create_widgets(self):
        """UIウィジェットの作成"""
        # メインタブビューの作成
        self.tabview = ctk.CTkTabview(self, width=680, height=580)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # タブの作成
        self.tabview.add("計算")
        self.tabview.add("履歴")
        self.tabview.add("グラフ")
        self.tabview.add("設定")
        
        # 各タブの内容を作成
        self.create_calculator_tab()
        self.create_history_tab()
        self.create_graph_tab()
        self.create_settings_tab()
    
    def create_calculator_tab(self):
        """BMI計算タブの作成"""
        calc_frame = self.tabview.tab("計算")
        
        # タイトル
        title_label = ctk.CTkLabel(
            calc_frame, 
            text="BMI計算機", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # 入力フレーム
        input_frame = ctk.CTkFrame(calc_frame)
        input_frame.pack(padx=40, pady=20, fill="x")
        
        # 身長入力
        height_label = ctk.CTkLabel(input_frame, text="身長 (cm):", font=ctk.CTkFont(size=16))
        height_label.pack(pady=(20, 5))
        
        self.height_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="例: 170",
            font=ctk.CTkFont(size=14),
            height=40,
            width=200
        )
        self.height_entry.pack(pady=(0, 15))
        self.height_entry.bind("<KeyRelease>", self.validate_input_realtime)
        
        # 体重入力
        weight_label = ctk.CTkLabel(input_frame, text="体重 (kg):", font=ctk.CTkFont(size=16))
        weight_label.pack(pady=(10, 5))
        
        self.weight_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="例: 65",
            font=ctk.CTkFont(size=14),
            height=40,
            width=200
        )
        self.weight_entry.pack(pady=(0, 15))
        self.weight_entry.bind("<KeyRelease>", self.validate_input_realtime)
        
        # メモ入力
        notes_label = ctk.CTkLabel(input_frame, text="メモ（任意）:", font=ctk.CTkFont(size=16))
        notes_label.pack(pady=(10, 5))
        
        self.notes_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="例: 朝食後測定",
            font=ctk.CTkFont(size=14),
            height=40,
            width=300
        )
        self.notes_entry.pack(pady=(0, 20))
        
        # 計算ボタン
        self.calc_button = ctk.CTkButton(
            calc_frame,
            text="BMIを計算する",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=200,
            command=self.calculate_bmi
        )
        self.calc_button.pack(pady=20)
        
        # 結果表示フレーム
        self.result_frame = ctk.CTkFrame(calc_frame)
        self.result_frame.pack(padx=40, pady=20, fill="x")
        
        # 結果ラベル（初期は非表示）
        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        
        # BMI進捗バー
        self.progress_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        
        self.progress_bar = ctk.CTkProgressBar(
            self.result_frame,
            width=300,
            height=20
        )
        
        # アドバイスラベル
        self.advice_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=14),
            wraplength=400
        )
    
    def create_history_tab(self):
        """履歴タブの作成"""
        history_frame = self.tabview.tab("履歴")
        
        # タイトル
        title_label = ctk.CTkLabel(
            history_frame, 
            text="測定履歴", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # 履歴表示用スクロールフレーム
        self.history_scroll = ctk.CTkScrollableFrame(
            history_frame,
            width=600,
            height=400
        )
        self.history_scroll.pack(padx=20, pady=10, fill="both", expand=True)
        
        # クリアボタン
        clear_button = ctk.CTkButton(
            history_frame,
            text="履歴をクリア",
            command=self.clear_history,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        )
        clear_button.pack(pady=10)
    
    def create_graph_tab(self):
        """グラフタブの作成"""
        graph_frame = self.tabview.tab("グラフ")
        
        # タイトル
        title_label = ctk.CTkLabel(
            graph_frame, 
            text="BMI変化グラフ", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # グラフ更新ボタン
        update_graph_button = ctk.CTkButton(
            graph_frame,
            text="グラフを更新",
            command=self.update_graph
        )
        update_graph_button.pack(pady=10)
        
        # グラフフレーム
        self.graph_frame = ctk.CTkFrame(graph_frame)
        self.graph_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    def create_settings_tab(self):
        """設定タブの作成"""
        settings_frame = self.tabview.tab("設定")
        
        # タイトル
        title_label = ctk.CTkLabel(
            settings_frame, 
            text="設定", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 30))
        
        # テーマ設定
        theme_frame = ctk.CTkFrame(settings_frame)
        theme_frame.pack(padx=40, pady=20, fill="x")
        
        theme_label = ctk.CTkLabel(theme_frame, text="外観テーマ:", font=ctk.CTkFont(size=16))
        theme_label.pack(pady=(15, 10))
        
        self.theme_var = ctk.StringVar(value="system")
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["light", "dark", "system"],
            variable=self.theme_var,
            command=self.change_theme
        )
        theme_menu.pack(pady=(0, 15))
        
        # カラーテーマ設定
        color_label = ctk.CTkLabel(theme_frame, text="カラーテーマ:", font=ctk.CTkFont(size=16))
        color_label.pack(pady=(10, 10))
        
        self.color_var = ctk.StringVar(value="blue")
        color_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["blue", "green", "dark-blue"],
            variable=self.color_var,
            command=self.change_color_theme
        )
        color_menu.pack(pady=(0, 15))
        
        # 目標BMI設定
        target_frame = ctk.CTkFrame(settings_frame)
        target_frame.pack(padx=40, pady=20, fill="x")
        
        target_label = ctk.CTkLabel(target_frame, text="目標BMI:", font=ctk.CTkFont(size=16))
        target_label.pack(pady=(15, 10))
        
        self.target_bmi_var = ctk.DoubleVar(value=22.0)
        target_slider = ctk.CTkSlider(
            target_frame,
            from_=18.0,
            to=25.0,
            variable=self.target_bmi_var,
            number_of_steps=70
        )
        target_slider.pack(pady=(0, 10), padx=20, sticky="ew")
        
        self.target_value_label = ctk.CTkLabel(
            target_frame,
            text=f"目標BMI: {self.target_bmi_var.get():.1f}",
            font=ctk.CTkFont(size=14)
        )
        self.target_value_label.pack(pady=(0, 15))
        
        target_slider.configure(command=self.update_target_bmi)
    
    def validate_input_realtime(self, event=None):
        """リアルタイム入力検証"""
        height_text = self.height_entry.get()
        weight_text = self.weight_entry.get()
        
        # 両方の入力がある場合のみ検証
        if height_text and weight_text:
            try:
                height = float(height_text)
                weight = float(weight_text)
                is_valid, _ = self.calculator.validate_input(height, weight)
                
                # ボタンの状態を更新
                self.calc_button.configure(state="normal" if is_valid else "disabled")
            except ValueError:
                self.calc_button.configure(state="disabled")
        else:
            self.calc_button.configure(state="disabled")
    
    def calculate_bmi(self):
        """BMI計算の実行"""
        try:
            # 入力値の取得
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            notes = self.notes_entry.get() or None
            
            # BMI計算
            result = self.calculator.process_measurement(height, weight, notes)
            
            # 結果の表示
            self.display_result(result)
            
            # 履歴に追加
            self.history.append(result)
            self.save_history()
            self.update_history_display()
            
        except ValueError as e:
            messagebox.showerror("入力エラー", str(e))
        except Exception as e:
            messagebox.showerror("計算エラー", f"予期しないエラーが発生しました: {str(e)}")
    
    def display_result(self, result: BMIResult):
        """結果をGUIに表示"""
        category_name, color, advice = result.category.value
        
        # 結果ラベルの更新
        self.result_label.configure(
            text=f"BMI: {result.bmi}  |  {category_name}",
            text_color=color
        )
        self.result_label.pack(pady=(20, 10))
        
        # 進捗バーの更新
        progress, _ = self.calculator.get_bmi_progress(result.bmi)
        self.progress_bar.set(progress)
        self.progress_bar.pack(pady=10)
        
        self.progress_label.configure(text=f"カテゴリ内進捗: {progress:.1%}")
        self.progress_label.pack(pady=5)
        
        # アドバイスの表示
        ideal_weight = self.calculator.calculate_ideal_weight(result.height, self.target_bmi_var.get())
        weight_diff, weight_message = self.calculator.get_weight_difference(
            result.weight, result.height, self.target_bmi_var.get()
        )
        
        advice_text = f"{advice}\n理想体重: {ideal_weight}kg\n{weight_message}"
        self.advice_label.configure(text=advice_text)
        self.advice_label.pack(pady=(10, 20))
    
    def update_history_display(self):
        """履歴表示の更新"""
        # 既存のウィジェットを削除
        for widget in self.history_scroll.winfo_children():
            widget.destroy()
        
        if not self.history:
            no_data_label = ctk.CTkLabel(
                self.history_scroll,
                text="まだ測定記録がありません",
                font=ctk.CTkFont(size=16)
            )
            no_data_label.pack(pady=50)
            return
        
        # 最新の記録から表示（逆順）
        for i, record in enumerate(reversed(self.history[-10:])):  # 最新10件
            self.create_history_item(record, i)
    
    def create_history_item(self, record: BMIResult, index: int):
        """履歴アイテムの作成"""
        item_frame = ctk.CTkFrame(self.history_scroll)
        item_frame.pack(fill="x", padx=10, pady=5)
        
        category_name, color, _ = record.category.value
        
        # 日時表示
        date_label = ctk.CTkLabel(
            item_frame,
            text=record.timestamp.strftime("%Y-%m-%d %H:%M"),
            font=ctk.CTkFont(size=12)
        )
        date_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        # BMI結果表示
        result_text = f"身長: {record.height}cm  体重: {record.weight}kg  BMI: {record.bmi}  ({category_name})"
        result_label = ctk.CTkLabel(
            item_frame,
            text=result_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=color
        )
        result_label.pack(anchor="w", padx=15, pady=5)
        
        # メモ表示
        if record.notes:
            notes_label = ctk.CTkLabel(
                item_frame,
                text=f"メモ: {record.notes}",
                font=ctk.CTkFont(size=12),
                text_color=("gray40", "gray60")
            )
            notes_label.pack(anchor="w", padx=15, pady=(0, 10))
        else:
            # メモがない場合はパディングを追加
            ctk.CTkLabel(item_frame, text="").pack(pady=5)
    
    def update_graph(self):
        """グラフの更新"""
        # 既存のグラフをクリア
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        if len(self.history) < 2:
            no_data_label = ctk.CTkLabel(
                self.graph_frame,
                text="グラフ表示には2つ以上の測定記録が必要です",
                font=ctk.CTkFont(size=16)
            )
            no_data_label.pack(expand=True)
            return
        
        # Matplotlibグラフの作成
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # データの準備
        dates = [record.timestamp for record in self.history]
        bmis = [record.bmi for record in self.history]
        
        # グラフの描画
        ax.plot(dates, bmis, marker='o', linewidth=2, markersize=6)
        ax.set_title("BMI変化トレンド", fontsize=16, pad=20)
        ax.set_ylabel("BMI", fontsize=12)
        ax.set_xlabel("日付", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # BMI範囲の色分け線を追加
        ax.axhline(y=18.5, color='blue', linestyle='--', alpha=0.5, label='低体重境界')
        ax.axhline(y=25.0, color='orange', linestyle='--', alpha=0.5, label='過体重境界')
        ax.axhline(y=30.0, color='red', linestyle='--', alpha=0.5, label='肥満境界')
        
        ax.legend()
        fig.tight_layout()
        
        # Tkinterに埋め込み
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def change_theme(self, theme: str):
        """テーマの変更"""
        ctk.set_appearance_mode(theme)
    
    def change_color_theme(self, color: str):
        """カラーテーマの変更"""
        ctk.set_default_color_theme(color)
        messagebox.showinfo("テーマ変更", "カラーテーマの変更はアプリケーション再起動後に適用されます。")
    
    def update_target_bmi(self, value):
        """目標BMIスライダーの更新"""
        self.target_value_label.configure(text=f"目標BMI: {value:.1f}")
    
    def clear_history(self):
        """履歴のクリア"""
        result = messagebox.askyesno("履歴クリア", "本当に履歴をすべて削除しますか？")
        if result:
            self.history.clear()
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("完了", "履歴をクリアしました。")
    
    def save_history(self):
        """履歴をJSONファイルに保存"""
        try:
            data = []
            for record in self.history:
                data.append({
                    "height": record.height,
                    "weight": record.weight,
                    "bmi": record.bmi,
                    "category": record.category.name,
                    "timestamp": record.timestamp.isoformat(),
                    "notes": record.notes
                })
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"データ保存エラー: {e}")
    
    def load_history(self):
        """JSONファイルから履歴を読み込み"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.history = []
                for item in data:
                    try:
                        category = HealthCategory[item["category"]]
                        timestamp = datetime.fromisoformat(item["timestamp"])
                        
                        record = BMIResult(
                            height=item["height"],
                            weight=item["weight"],
                            bmi=item["bmi"],
                            category=category,
                            timestamp=timestamp,
                            notes=item.get("notes")
                        )
                        self.history.append(record)
                    except Exception as e:
                        print(f"履歴項目の読み込みエラー: {e}")
                
                self.update_history_display()
        except Exception as e:
            print(f"データ読み込みエラー: {e}")


def main():
    """アプリケーションのメイン実行"""
    app = BMIApp()
    app.mainloop()


if __name__ == "__main__":
    main()