# Changelog

All notable changes to the BMI Calculator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Web版の開発（Flask/FastAPI）
- モバイルアプリ対応
- クラウド同期機能
- AI健康アドバイザー
- 多言語対応（英語、中国語など）

## [1.0.0] - 2025-01-04

### ✨ Added
- **CustomTkinter GUI**: モダンで美しいユーザーインターフェース
- **CLI インターフェース**: インタラクティブモードと直接実行モード
- **BMI計算エンジン**: WHO基準による6段階健康判定
- **データ永続化**: JSON形式による測定履歴保存
- **グラフ表示**: matplotlib統合によるBMI変化トレンド可視化
- **リアルタイム入力検証**: エラーハンドリングとユーザーフィードバック
- **テーマ機能**: ダークモード対応とカスタマイズ可能なカラーテーマ
- **理想体重計算**: 目標BMI設定と体重差分表示
- **完全なテストスイート**: pytest による包括的テスト

### 🎯 Features
- **健康カテゴリ判定**: 低体重、普通体重、過体重、肥満(1-3度)
- **進捗バー表示**: BMIカテゴリ内での位置を視覚化
- **測定履歴管理**: 過去の記録の保存・表示・削除
- **設定カスタマイズ**: テーマ、目標BMI、外観設定
- **エラー処理**: 堅牢な入力値検証とユーザーフレンドリーなエラーメッセージ

### 🏗️ Technical
- **アーキテクチャ**: MVC パターンによる設計
- **型安全性**: Type Hints による静的解析対応
- **データ構造**: Dataclasses と Enum による構造化
- **国際化対応**: 将来的な多言語サポートの基盤

### 📦 Dependencies
- Python 3.8+
- CustomTkinter 5.2.0+
- Pillow 9.0.0+
- matplotlib 3.5.0+

### 🧪 Quality Assurance
- SuperClaude Framework による仕様駆動開発
- 100% テストカバレッジ（コア機能）
- 包括的な入力値検証
- エラー処理とログ機能

### 📚 Documentation
- 完全な README.md
- 詳細な仕様書（SPECIFICATION.md）
- API ドキュメント
- 使用例とスクリーンショット

---

## Version Legend

- **Added** for new features
- **Changed** for changes in existing functionality  
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes