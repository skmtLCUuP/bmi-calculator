# BMI計算機 - 仕様書（SuperClaude仕様駆動開発）

## 📋 プロジェクト概要

### 目的
身長と体重を入力してBMI（Body Mass Index）を計算し、健康状態を判定するPythonアプリケーション

### 対象ユーザー
- 健康管理に関心のある一般ユーザー
- 医療従事者
- フィットネス愛好家

## 🎯 機能仕様

### 1. 基本機能
#### BMI計算
- **入力**: 身長（cm）、体重（kg）
- **計算式**: BMI = 体重(kg) ÷ (身長(m))²
- **出力**: BMI値（小数点第1位まで）

#### 健康状態判定
| BMI範囲 | 判定 | 色分け |
|---------|------|--------|
| < 18.5 | 低体重 | 青 |
| 18.5-24.9 | 普通体重 | 緑 |
| 25.0-29.9 | 過体重 | 黄 |
| 30.0-34.9 | 肥満(1度) | オレンジ |
| 35.0-39.9 | 肥満(2度) | 赤 |
| ≥ 40.0 | 肥満(3度) | 濃赤 |

### 2. 高度機能
- **履歴管理**: 過去の測定記録保存
- **トレンド表示**: BMI変化のグラフ表示
- **目標設定**: 理想体重・BMI目標の設定
- **アドバイス**: 健康状態に応じた改善提案

## 🏗️ 技術仕様

### 開発言語
- **Python 3.8+**
- モダンUI実装

### 必須ライブラリ
```python
# コア機能
import math
import json
import datetime
from dataclasses import dataclass
from typing import Optional, List, Tuple

# モダンGUI
import customtkinter as ctk
from PIL import Image, ImageTk

# データ可視化（オプション）
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
```

### アーキテクチャパターン
- **MVC（Model-View-Controller）**
- **単一責任原則**
- **依存性注入**

## 📊 データ構造

### BMI記録
```python
@dataclass
class BMIRecord:
    height: float          # 身長(cm)
    weight: float          # 体重(kg)
    bmi: float            # BMI値
    category: str         # 健康カテゴリ
    timestamp: datetime   # 測定日時
    notes: Optional[str]  # メモ
```

### 設定情報
```python
@dataclass
class UserSettings:
    target_weight: Optional[float]
    target_bmi: Optional[float]
    preferred_units: str  # metric/imperial
    theme: str           # light/dark/system
    accent_color: str    # カスタムカラー
```

## 🔍 入力値検証

### 身長
- **範囲**: 100cm - 250cm
- **型**: 正の数値
- **形式**: 整数または小数

### 体重
- **範囲**: 20kg - 300kg
- **型**: 正の数値
- **形式**: 整数または小数

### エラーハンドリング
- 範囲外の値: モダンな警告ダイアログ表示
- 無効な入力: リアルタイム検証と再入力要求
- 計算エラー: 例外処理とログ出力

## 🎨 ユーザーインターフェース

### CLI版
```
=== BMI計算機 ===
身長を入力してください (cm): 170
体重を入力してください (kg): 65

結果:
BMI: 22.5
判定: 普通体重 ✅
```

### GUI版（CustomTkinter）
#### デザインテーマ
- **ダークモード対応**: システム設定に従う
- **モダンな外観**: rounded corners, smooth animations
- **レスポンシブデザイン**: 画面サイズに応じた最適化
- **カラーテーマ**: blue, green, dark-blue から選択可能

#### ウィンドウ構成
- **メインウィンドウ**: モダンな入力フォーム + 結果表示
  - CTkEntry: 身長・体重入力フィールド
  - CTkButton: 計算ボタン
  - CTkLabel: 結果表示（色分け対応）
  - CTkProgressBar: BMI範囲の視覚表示
- **履歴ウィンドウ**: CTkScrollableFrameによる記録一覧
- **グラフウィンドウ**: matplotlib統合によるトレンド表示
- **設定ウィンドウ**: CTkTabview、CTkSwitch、CTkSliderによる設定

## 📁 ファイル構成

```
bmi-calculator/
├── src/
│   ├── __init__.py
│   ├── bmi_calculator.py     # コア計算ロジック
│   ├── health_advisor.py     # 健康アドバイス
│   ├── data_manager.py       # データ保存・読込
│   ├── cli_interface.py      # CLI実装
│   └── gui_interface.py      # CustomTkinter GUI実装
├── assets/
│   ├── icons/               # アイコンファイル
│   └── themes/              # カスタムテーマ
├── tests/
│   ├── test_bmi_calculator.py
│   ├── test_health_advisor.py
│   └── test_data_manager.py
├── docs/
│   ├── README.md
│   ├── API.md
│   └── USAGE.md
├── requirements.txt
├── setup.py
└── main.py
```

## 🎨 CustomTkinter UI仕様

### メインウィンドウ
```python
# ウィンドウサイズ: 600x500
# テーマ: システム設定またはユーザー選択
# カラーテーマ: blue（デフォルト）

class BMIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ウィンドウ設定
        self.title("BMI Calculator - 健康チェッカー")
        self.geometry("600x500")
        self.resizable(True, True)
        
        # テーマ設定
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
```

### UI コンポーネント
- **CTkEntry**: 数値入力（リアルタイム検証付き）
- **CTkButton**: グラデーションボタン
- **CTkLabel**: 結果表示（動的色変更）
- **CTkFrame**: コンテンツグループ化
- **CTkProgressBar**: BMI範囲視覚化
- **CTkTabview**: 設定タブ
- **CTkScrollableFrame**: 履歴表示

## 🧪 テスト仕様

### ユニットテスト
- BMI計算の正確性
- 健康カテゴリ分類の正確性
- 入力値検証の動作
- データ保存・読込の動作

### GUI テスト
- CustomTkinter ウィジェットの動作確認
- テーマ切り替えの動作
- レスポンシブデザインの検証

### テストケース例
```python
def test_bmi_calculation():
    assert calculate_bmi(170, 65) == 22.5
    assert calculate_bmi(160, 50) == 19.5

def test_health_category():
    assert get_health_category(18.0) == "低体重"
    assert get_health_category(22.0) == "普通体重"
    assert get_health_category(27.0) == "過体重"
```

## 🎯 パフォーマンス要件

- **応答時間**: 1秒以内
- **メモリ使用量**: 80MB以下（GUI含む）
- **起動時間**: 3秒以内
- **アニメーション**: 60fps smooth transitions

## 📦 依存関係

### 必須パッケージ
```
customtkinter>=5.2.0
Pillow>=9.0.0
matplotlib>=3.5.0
```

### オプションパッケージ
```
darkdetect  # システムテーマ検出
packaging   # バージョン管理
```

## 🔐 セキュリティ要件

- 個人データの暗号化保存
- 入力値のサニタイゼーション
- エラー情報の適切なマスキング

## 🌐 国際化対応

- 日本語・英語対応
- メートル法・ヤード・ポンド法対応
- 地域別BMI基準の考慮

## 📈 将来の拡張計画

1. **Web版の開発** (Flask/FastAPI)
2. **モバイルアプリ連携**
3. **クラウド同期機能**
4. **AI健康アドバイザー**
5. **ウェアラブルデバイス連携**
6. **カスタムテーマエディタ**

---
*この仕様書は SuperClaude Framework による仕様駆動開発手法で作成されました*