"""
BMI Calculator Core Module
SuperClaude Framework - 仕様駆動開発

BMI計算と健康状態判定のコアロジックを実装
"""

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Optional
from enum import Enum


class HealthCategory(Enum):
    """健康カテゴリの定義"""
    UNDERWEIGHT = ("低体重", "#3498db", "体重を増やすことを検討してください")
    NORMAL = ("普通体重", "#2ecc71", "健康的な体重を維持してください")
    OVERWEIGHT = ("過体重", "#f1c40f", "適度な運動と食事管理をお勧めします")
    OBESE_1 = ("肥満(1度)", "#e67e22", "医師に相談し、生活習慣の改善を検討してください")
    OBESE_2 = ("肥満(2度)", "#e74c3c", "医師に相談し、積極的な治療を検討してください")
    OBESE_3 = ("肥満(3度)", "#c0392b", "専門医による治療が必要です")


@dataclass
class BMIResult:
    """BMI計算結果を格納するデータクラス"""
    height: float
    weight: float
    bmi: float
    category: HealthCategory
    timestamp: datetime
    notes: Optional[str] = None
    
    def __post_init__(self):
        """計算後の検証"""
        if self.bmi <= 0:
            raise ValueError("BMI値は正の数である必要があります")


class BMICalculator:
    """BMI計算機のコアクラス"""
    
    # BMI基準値（WHO基準）
    BMI_RANGES = {
        HealthCategory.UNDERWEIGHT: (0, 18.5),
        HealthCategory.NORMAL: (18.5, 25.0),
        HealthCategory.OVERWEIGHT: (25.0, 30.0),
        HealthCategory.OBESE_1: (30.0, 35.0),
        HealthCategory.OBESE_2: (35.0, 40.0),
        HealthCategory.OBESE_3: (40.0, float('inf'))
    }
    
    @staticmethod
    def validate_input(height: float, weight: float) -> Tuple[bool, str]:
        """
        入力値の検証
        
        Args:
            height: 身長（cm）
            weight: 体重（kg）
            
        Returns:
            Tuple[bool, str]: (検証結果, エラーメッセージ)
        """
        if not isinstance(height, (int, float)) or not isinstance(weight, (int, float)):
            return False, "身長と体重は数値で入力してください"
            
        if height <= 0 or weight <= 0:
            return False, "身長と体重は正の数で入力してください"
            
        if height < 100 or height > 250:
            return False, "身長は100cm〜250cmの範囲で入力してください"
            
        if weight < 20 or weight > 300:
            return False, "体重は20kg〜300kgの範囲で入力してください"
            
        return True, ""
    
    @staticmethod
    def calculate_bmi(height: float, weight: float) -> float:
        """
        BMIを計算する
        
        Args:
            height: 身長（cm）
            weight: 体重（kg）
            
        Returns:
            float: BMI値（小数点第1位まで）
        """
        # 身長をメートルに変換
        height_m = height / 100
        
        # BMI = 体重(kg) ÷ 身長(m)²
        bmi = weight / (height_m ** 2)
        
        # 小数点第1位で四捨五入
        return round(bmi, 1)
    
    @classmethod
    def get_health_category(cls, bmi: float) -> HealthCategory:
        """
        BMI値から健康カテゴリを判定する
        
        Args:
            bmi: BMI値
            
        Returns:
            HealthCategory: 健康カテゴリ
        """
        for category, (min_bmi, max_bmi) in cls.BMI_RANGES.items():
            if min_bmi <= bmi < max_bmi:
                return category
        
        # デフォルト（通常は到達しない）
        return HealthCategory.OBESE_3
    
    @classmethod
    def calculate_ideal_weight(cls, height: float, target_bmi: float = 22.0) -> float:
        """
        理想体重を計算する
        
        Args:
            height: 身長（cm）
            target_bmi: 目標BMI（デフォルト: 22.0）
            
        Returns:
            float: 理想体重（kg）
        """
        height_m = height / 100
        ideal_weight = target_bmi * (height_m ** 2)
        return round(ideal_weight, 1)
    
    @classmethod
    def get_weight_difference(cls, current_weight: float, height: float, 
                            target_bmi: float = 22.0) -> Tuple[float, str]:
        """
        理想体重との差分を計算する
        
        Args:
            current_weight: 現在の体重（kg）
            height: 身長（cm）
            target_bmi: 目標BMI
            
        Returns:
            Tuple[float, str]: (体重差分, メッセージ)
        """
        ideal_weight = cls.calculate_ideal_weight(height, target_bmi)
        difference = current_weight - ideal_weight
        
        if abs(difference) < 0.5:
            return difference, "理想的な体重です！"
        elif difference > 0:
            return difference, f"理想体重まで {difference:.1f}kg の減量が目標です"
        else:
            return difference, f"理想体重まで {abs(difference):.1f}kg の増量が目標です"
    
    @classmethod
    def get_bmi_progress(cls, bmi: float) -> Tuple[float, HealthCategory]:
        """
        BMI値の進捗（0-1の範囲）と次のカテゴリを取得
        
        Args:
            bmi: BMI値
            
        Returns:
            Tuple[float, HealthCategory]: (進捗率, 現在のカテゴリ)
        """
        current_category = cls.get_health_category(bmi)
        min_bmi, max_bmi = cls.BMI_RANGES[current_category]
        
        if max_bmi == float('inf'):
            progress = 1.0
        else:
            progress = (bmi - min_bmi) / (max_bmi - min_bmi)
            progress = max(0.0, min(1.0, progress))
        
        return progress, current_category
    
    def process_measurement(self, height: float, weight: float, 
                          notes: Optional[str] = None) -> BMIResult:
        """
        測定データを処理してBMI結果を生成する
        
        Args:
            height: 身長（cm）
            weight: 体重（kg）
            notes: メモ（オプション）
            
        Returns:
            BMIResult: BMI計算結果
            
        Raises:
            ValueError: 入力値が無効な場合
        """
        # 入力値検証
        is_valid, error_message = self.validate_input(height, weight)
        if not is_valid:
            raise ValueError(error_message)
        
        # BMI計算
        bmi = self.calculate_bmi(height, weight)
        
        # 健康カテゴリ判定
        category = self.get_health_category(bmi)
        
        # 結果オブジェクト作成
        result = BMIResult(
            height=height,
            weight=weight,
            bmi=bmi,
            category=category,
            timestamp=datetime.now(),
            notes=notes
        )
        
        return result
    
    @staticmethod
    def format_result(result: BMIResult) -> str:
        """
        BMI結果を見やすい文字列に整形する
        
        Args:
            result: BMI計算結果
            
        Returns:
            str: 整形された結果文字列
        """
        category_name, _, advice = result.category.value
        
        output = f"""
=== BMI計算結果 ===
身長: {result.height}cm
体重: {result.weight}kg
BMI: {result.bmi}
判定: {category_name}
アドバイス: {advice}
測定日時: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if result.notes:
            output += f"メモ: {result.notes}\n"
            
        return output.strip()


# 使用例とテスト用のmain関数
if __name__ == "__main__":
    calculator = BMICalculator()
    
    # テストケース
    test_cases = [
        (170, 65),   # 普通体重
        (160, 45),   # 低体重  
        (175, 80),   # 過体重
        (170, 90),   # 肥満
    ]
    
    print("BMI Calculator Test Cases:")
    print("=" * 40)
    
    for height, weight in test_cases:
        try:
            result = calculator.process_measurement(height, weight)
            print(calculator.format_result(result))
            
            # 進捗情報も表示
            progress, category = calculator.get_bmi_progress(result.bmi)
            print(f"カテゴリ内進捗: {progress:.1%}")
            print("-" * 40)
        except ValueError as e:
            print(f"エラー: {e}")
            print("-" * 40)