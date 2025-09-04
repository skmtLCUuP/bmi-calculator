"""
BMI Calculator Test Suite
SuperClaude Framework - 仕様駆動開発

BMI計算機のユニットテスト
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# srcディレクトリをパスに追加
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from bmi_calculator import BMICalculator, BMIResult, HealthCategory


class TestBMICalculator:
    """BMICalculatorクラスのテスト"""
    
    def setup_method(self):
        """テストメソッドごとの初期化"""
        self.calculator = BMICalculator()
    
    def test_calculate_bmi_normal_values(self):
        """通常の値でのBMI計算テスト"""
        # 170cm, 65kg の場合
        bmi = self.calculator.calculate_bmi(170, 65)
        expected_bmi = 22.5  # 65 / (1.7^2) = 22.491... ≈ 22.5
        assert bmi == expected_bmi
        
        # 160cm, 50kg の場合
        bmi = self.calculator.calculate_bmi(160, 50)
        expected_bmi = 19.5  # 50 / (1.6^2) = 19.531... ≈ 19.5
        assert bmi == expected_bmi
    
    def test_calculate_bmi_edge_cases(self):
        """境界値でのBMI計算テスト"""
        # 最小値付近
        bmi = self.calculator.calculate_bmi(100, 20)
        assert bmi > 0
        
        # 最大値付近
        bmi = self.calculator.calculate_bmi(250, 300)
        assert bmi > 0
    
    def test_get_health_category(self):
        """健康カテゴリ判定テスト"""
        # 低体重
        assert self.calculator.get_health_category(17.0) == HealthCategory.UNDERWEIGHT
        assert self.calculator.get_health_category(18.4) == HealthCategory.UNDERWEIGHT
        
        # 普通体重
        assert self.calculator.get_health_category(18.5) == HealthCategory.NORMAL
        assert self.calculator.get_health_category(22.0) == HealthCategory.NORMAL
        assert self.calculator.get_health_category(24.9) == HealthCategory.NORMAL
        
        # 過体重
        assert self.calculator.get_health_category(25.0) == HealthCategory.OVERWEIGHT
        assert self.calculator.get_health_category(29.9) == HealthCategory.OVERWEIGHT
        
        # 肥満1度
        assert self.calculator.get_health_category(30.0) == HealthCategory.OBESE_1
        assert self.calculator.get_health_category(34.9) == HealthCategory.OBESE_1
        
        # 肥満2度
        assert self.calculator.get_health_category(35.0) == HealthCategory.OBESE_2
        assert self.calculator.get_health_category(39.9) == HealthCategory.OBESE_2
        
        # 肥満3度
        assert self.calculator.get_health_category(40.0) == HealthCategory.OBESE_3
        assert self.calculator.get_health_category(50.0) == HealthCategory.OBESE_3
    
    def test_validate_input_valid_cases(self):
        """有効な入力値の検証テスト"""
        # 通常の値
        is_valid, message = self.calculator.validate_input(170, 65)
        assert is_valid == True
        assert message == ""
        
        # 境界値
        is_valid, message = self.calculator.validate_input(100, 20)
        assert is_valid == True
        
        is_valid, message = self.calculator.validate_input(250, 300)
        assert is_valid == True
    
    def test_validate_input_invalid_cases(self):
        """無効な入力値の検証テスト"""
        # 負の値
        is_valid, message = self.calculator.validate_input(-170, 65)
        assert is_valid == False
        assert "正の数" in message
        
        # ゼロ
        is_valid, message = self.calculator.validate_input(0, 65)
        assert is_valid == False
        assert "正の数" in message
        
        # 範囲外（身長が小さすぎる）
        is_valid, message = self.calculator.validate_input(99, 65)
        assert is_valid == False
        assert "100cm〜250cm" in message
        
        # 範囲外（身長が大きすぎる）
        is_valid, message = self.calculator.validate_input(251, 65)
        assert is_valid == False
        assert "100cm〜250cm" in message
        
        # 範囲外（体重が小さすぎる）
        is_valid, message = self.calculator.validate_input(170, 19)
        assert is_valid == False
        assert "20kg〜300kg" in message
        
        # 範囲外（体重が大きすぎる）
        is_valid, message = self.calculator.validate_input(170, 301)
        assert is_valid == False
        assert "20kg〜300kg" in message
        
        # 文字列型（この場合はPythonが自動的に型チェックするが）
        is_valid, message = self.calculator.validate_input("170", "65")
        assert is_valid == False
        assert "数値" in message
    
    def test_calculate_ideal_weight(self):
        """理想体重計算テスト"""
        # デフォルトBMI（22.0）
        ideal_weight = self.calculator.calculate_ideal_weight(170)
        expected = 22.0 * (1.7 ** 2)  # 22.0 * 2.89 = 63.58
        assert ideal_weight == round(expected, 1)
        
        # カスタムBMI
        ideal_weight = self.calculator.calculate_ideal_weight(160, 20.0)
        expected = 20.0 * (1.6 ** 2)  # 20.0 * 2.56 = 51.2
        assert ideal_weight == 51.2
    
    def test_get_weight_difference(self):
        """体重差分計算テスト"""
        # 理想体重より重い場合
        diff, message = self.calculator.get_weight_difference(70, 170, 22.0)
        assert diff > 0
        assert "減量" in message
        
        # 理想体重より軽い場合
        diff, message = self.calculator.get_weight_difference(60, 170, 22.0)
        assert diff < 0
        assert "増量" in message
        
        # 理想的な体重の場合（±0.5kg以内）
        ideal_weight = self.calculator.calculate_ideal_weight(170, 22.0)
        diff, message = self.calculator.get_weight_difference(ideal_weight, 170, 22.0)
        assert abs(diff) < 0.5
        assert "理想的" in message
    
    def test_get_bmi_progress(self):
        """BMI進捗計算テスト"""
        # 普通体重の中間あたり
        progress, category = self.calculator.get_bmi_progress(21.75)
        assert category == HealthCategory.NORMAL
        assert 0.4 < progress < 0.6  # 18.5-25.0の範囲内の中間あたり
        
        # カテゴリの境界値
        progress, category = self.calculator.get_bmi_progress(18.5)
        assert category == HealthCategory.NORMAL
        assert progress == 0.0
        
        progress, category = self.calculator.get_bmi_progress(24.9)
        assert category == HealthCategory.NORMAL
        assert progress > 0.9
    
    def test_process_measurement_valid(self):
        """測定処理テスト（有効な値）"""
        result = self.calculator.process_measurement(170, 65, "テスト測定")
        
        assert isinstance(result, BMIResult)
        assert result.height == 170
        assert result.weight == 65
        assert result.bmi == 22.5
        assert result.category == HealthCategory.NORMAL
        assert result.notes == "テスト測定"
        assert isinstance(result.timestamp, datetime)
    
    def test_process_measurement_invalid(self):
        """測定処理テスト（無効な値）"""
        with pytest.raises(ValueError):
            self.calculator.process_measurement(50, 65)  # 身長が範囲外
        
        with pytest.raises(ValueError):
            self.calculator.process_measurement(170, 10)  # 体重が範囲外
    
    def test_format_result(self):
        """結果フォーマットテスト"""
        result = self.calculator.process_measurement(170, 65)
        formatted = self.calculator.format_result(result)
        
        assert "BMI計算結果" in formatted
        assert "170cm" in formatted
        assert "65kg" in formatted
        assert "22.5" in formatted
        assert "普通体重" in formatted
        assert "健康的な体重を維持してください" in formatted


class TestBMIResult:
    """BMIResultクラスのテスト"""
    
    def test_bmi_result_creation(self):
        """BMIResult作成テスト"""
        timestamp = datetime.now()
        result = BMIResult(
            height=170.0,
            weight=65.0,
            bmi=22.5,
            category=HealthCategory.NORMAL,
            timestamp=timestamp,
            notes="テスト"
        )
        
        assert result.height == 170.0
        assert result.weight == 65.0
        assert result.bmi == 22.5
        assert result.category == HealthCategory.NORMAL
        assert result.timestamp == timestamp
        assert result.notes == "テスト"
    
    def test_bmi_result_invalid_bmi(self):
        """無効なBMI値でのBMIResult作成テスト"""
        with pytest.raises(ValueError):
            BMIResult(
                height=170.0,
                weight=65.0,
                bmi=0.0,  # 無効な値
                category=HealthCategory.NORMAL,
                timestamp=datetime.now()
            )


class TestHealthCategory:
    """HealthCategoryクラスのテスト"""
    
    def test_health_category_values(self):
        """HealthCategoryの値テスト"""
        # 各カテゴリの値を確認
        underweight = HealthCategory.UNDERWEIGHT.value
        assert underweight[0] == "低体重"
        assert underweight[1] == "#3498db"  # 青色
        assert "体重を増やす" in underweight[2]
        
        normal = HealthCategory.NORMAL.value
        assert normal[0] == "普通体重"
        assert normal[1] == "#2ecc71"  # 緑色
        assert "維持" in normal[2]
        
        obese_3 = HealthCategory.OBESE_3.value
        assert obese_3[0] == "肥満(3度)"
        assert obese_3[1] == "#c0392b"  # 濃い赤色
        assert "専門医" in obese_3[2]


class TestIntegration:
    """統合テスト"""
    
    def test_complete_workflow(self):
        """完全なワークフローテスト"""
        calculator = BMICalculator()
        
        # 1. 入力値検証
        is_valid, _ = calculator.validate_input(170, 65)
        assert is_valid
        
        # 2. BMI計算
        bmi = calculator.calculate_bmi(170, 65)
        assert bmi == 22.5
        
        # 3. カテゴリ判定
        category = calculator.get_health_category(bmi)
        assert category == HealthCategory.NORMAL
        
        # 4. 完全な測定処理
        result = calculator.process_measurement(170, 65)
        assert result.bmi == 22.5
        assert result.category == HealthCategory.NORMAL
        
        # 5. 結果フォーマット
        formatted = calculator.format_result(result)
        assert "22.5" in formatted
        assert "普通体重" in formatted
    
    def test_multiple_measurements(self):
        """複数測定テスト"""
        calculator = BMICalculator()
        
        test_cases = [
            (150, 40, HealthCategory.UNDERWEIGHT),
            (170, 65, HealthCategory.NORMAL),
            (180, 90, HealthCategory.OVERWEIGHT),
            (160, 80, HealthCategory.OBESE_1),
        ]
        
        results = []
        for height, weight, expected_category in test_cases:
            result = calculator.process_measurement(height, weight)
            assert result.category == expected_category
            results.append(result)
        
        # すべての結果が適切に作成されていることを確認
        assert len(results) == 4
        for result in results:
            assert isinstance(result, BMIResult)
            assert result.bmi > 0


if __name__ == "__main__":
    # テストの実行
    pytest.main([__file__, "-v", "--tb=short"])