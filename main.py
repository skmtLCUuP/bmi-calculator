#!/usr/bin/env python3
"""
BMI Calculator - Main Entry Point
SuperClaude Framework - 仕様駆動開発

BMI計算機アプリケーションのメインエントリーポイント
"""

import sys
import os
import argparse
from pathlib import Path

# srcディレクトリをパスに追加
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from bmi_calculator import BMICalculator
from gui_interface import BMIApp


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="BMI Calculator - 身長と体重から健康状態をチェック",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python main.py              # GUI版を起動
  python main.py --cli         # CLI版を起動
  python main.py --cli 170 65  # CLI版で直接計算
        """
    )
    
    parser.add_argument(
        "--cli",
        action="store_true",
        help="コマンドライン版を使用"
    )
    
    parser.add_argument(
        "height",
        nargs="?",
        type=float,
        help="身長（cm）- CLI版でのみ使用"
    )
    
    parser.add_argument(
        "weight",
        nargs="?",
        type=float,
        help="体重（kg）- CLI版でのみ使用"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="BMI Calculator 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        if args.cli:
            run_cli_mode(args.height, args.weight)
        else:
            run_gui_mode()
    except KeyboardInterrupt:
        print("\n\nアプリケーションを終了しました。")
        sys.exit(0)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)


def run_cli_mode(height=None, weight=None):
    """CLI版の実行"""
    calculator = BMICalculator()
    
    print("=" * 50)
    print("BMI Calculator - コマンドライン版")
    print("=" * 50)
    
    if height is not None and weight is not None:
        # コマンドライン引数で直接計算
        try:
            result = calculator.process_measurement(height, weight)
            print(calculator.format_result(result))
            
            # 理想体重の情報も表示
            ideal_weight = calculator.calculate_ideal_weight(height)
            weight_diff, weight_message = calculator.get_weight_difference(weight, height)
            print(f"\n理想体重: {ideal_weight}kg")
            print(f"{weight_message}")
            
        except ValueError as e:
            print(f"エラー: {e}")
            sys.exit(1)
    else:
        # インタラクティブモード
        run_interactive_cli(calculator)


def run_interactive_cli(calculator):
    """インタラクティブCLI実行"""
    while True:
        try:
            print("\n" + "-" * 30)
            
            # 身長入力
            while True:
                height_input = input("身長を入力してください (cm) [終了: q]: ").strip()
                if height_input.lower() == 'q':
                    print("終了します。")
                    return
                
                try:
                    height = float(height_input)
                    break
                except ValueError:
                    print("有効な数値を入力してください。")
            
            # 体重入力
            while True:
                weight_input = input("体重を入力してください (kg): ").strip()
                try:
                    weight = float(weight_input)
                    break
                except ValueError:
                    print("有効な数値を入力してください。")
            
            # メモ入力（オプション）
            notes = input("メモ（任意、Enter でスキップ）: ").strip() or None
            
            # 計算実行
            result = calculator.process_measurement(height, weight, notes)
            
            # 結果表示
            print("\n" + "=" * 40)
            print(calculator.format_result(result))
            
            # 追加情報
            ideal_weight = calculator.calculate_ideal_weight(height)
            weight_diff, weight_message = calculator.get_weight_difference(weight, height)
            progress, _ = calculator.get_bmi_progress(result.bmi)
            
            print(f"\n理想体重: {ideal_weight}kg")
            print(f"{weight_message}")
            print(f"カテゴリ内進捗: {progress:.1%}")
            
            # 継続確認
            continue_input = input("\n続けますか？ [y/N]: ").strip().lower()
            if continue_input not in ['y', 'yes']:
                break
                
        except ValueError as e:
            print(f"エラー: {e}")
        except KeyboardInterrupt:
            print("\n終了します。")
            break


def run_gui_mode():
    """GUI版の実行"""
    try:
        # CustomTkinterの利用可能性チェック
        import customtkinter as ctk
        
        print("BMI Calculator GUI版を起動中...")
        app = BMIApp()
        app.mainloop()
        
    except ImportError as e:
        print("エラー: GUI版の実行に必要なライブラリが見つかりません。")
        print("以下のコマンドでインストールしてください:")
        print("pip install -r requirements.txt")
        print(f"\n詳細: {e}")
        
        # CLI版にフォールバック
        fallback = input("\nCLI版で実行しますか？ [y/N]: ").strip().lower()
        if fallback in ['y', 'yes']:
            run_cli_mode()
        else:
            sys.exit(1)
    
    except Exception as e:
        print(f"GUI版の起動でエラーが発生しました: {e}")
        print("CLI版で実行します。")
        run_cli_mode()


if __name__ == "__main__":
    main()