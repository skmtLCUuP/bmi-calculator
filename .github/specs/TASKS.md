# BMI Calculator - Implementation Tasks

*Generated using GitHub Spec Kit methodology for granular task breakdown*

## 🎯 Task Organization

### Task Categories
- **SETUP**: Project infrastructure and tooling
- **MODEL**: Data models and business logic  
- **VIEW**: User interface components
- **TEST**: Quality assurance and validation
- **DOCS**: Documentation and guides
- **DEPLOY**: Packaging and distribution

### Priority Levels
- **P0**: Critical path, blocks other tasks
- **P1**: High priority, core functionality
- **P2**: Medium priority, enhanced features  
- **P3**: Low priority, polish and optimization

## 🏗️ SETUP Tasks - Project Foundation

### SETUP-001: Initialize Project Structure [P0]
```bash
# Create directory structure
mkdir -p src/{models,views,controllers,utils}
mkdir -p tests/{unit,integration,e2e}
mkdir -p docs/{user-guide,api,examples}
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

# Initialize Python package files
touch src/__init__.py
touch src/{models,views,controllers,utils}/__init__.py
touch tests/__init__.py
```

**Acceptance Criteria:**
- [ ] Directory structure matches specification
- [ ] All `__init__.py` files created
- [ ] Git repository initialized with appropriate `.gitignore`

### SETUP-002: Configure Development Environment [P0]
```python
# requirements.txt
customtkinter>=5.2.0
Pillow>=9.0.0  
matplotlib>=3.5.0

# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
mypy>=0.991
bandit>=1.7.0
```

**Acceptance Criteria:**
- [ ] All dependencies install without conflicts
- [ ] Virtual environment activated and tested
- [ ] Development tools (black, mypy) configured

### SETUP-003: GitHub Actions CI/CD Pipeline [P1]
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
      - name: Install dependencies
      - name: Run tests
      - name: Check code style
      - name: Type checking
```

**Acceptance Criteria:**
- [ ] Pipeline runs on push/PR
- [ ] Tests execute across Python versions
- [ ] Code quality gates enforced

## 🧮 MODEL Tasks - Core Business Logic

### MODEL-001: BMI Data Models [P0]
```python
# src/models/bmi_calculator.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

@dataclass
class BMIResult:
    height: float
    weight: float  
    bmi: float
    category: 'HealthCategory'
    timestamp: datetime
    notes: Optional[str] = None

class HealthCategory(Enum):
    UNDERWEIGHT = ("Underweight", "#3498db", "Consider weight gain")
    NORMAL = ("Normal Weight", "#2ecc71", "Maintain healthy weight")  
    OVERWEIGHT = ("Overweight", "#f1c40f", "Exercise and diet management")
    OBESE_1 = ("Obese Class I", "#e67e22", "Consult healthcare provider")
    OBESE_2 = ("Obese Class II", "#e74c3c", "Active medical intervention") 
    OBESE_3 = ("Obese Class III", "#c0392b", "Specialized treatment needed")
```

**Acceptance Criteria:**
- [ ] All data classes properly typed
- [ ] Enum values match WHO standards
- [ ] Color codes are valid hex values
- [ ] Post-init validation implemented

### MODEL-002: BMI Calculation Engine [P0]
```python
class BMICalculator:
    # WHO BMI Classification Ranges
    BMI_RANGES = {
        HealthCategory.UNDERWEIGHT: (0, 18.5),
        HealthCategory.NORMAL: (18.5, 25.0),
        HealthCategory.OVERWEIGHT: (25.0, 30.0),
        HealthCategory.OBESE_1: (30.0, 35.0),
        HealthCategory.OBESE_2: (35.0, 40.0),
        HealthCategory.OBESE_3: (40.0, float('inf'))
    }
    
    @staticmethod
    def calculate_bmi(height: float, weight: float) -> float:
        """Calculate BMI = weight(kg) / (height(m))²"""
        height_m = height / 100  # Convert cm to m
        bmi = weight / (height_m ** 2)
        return round(bmi, 1)
    
    @classmethod
    def get_health_category(cls, bmi: float) -> HealthCategory:
        """Map BMI value to WHO health category"""
        for category, (min_bmi, max_bmi) in cls.BMI_RANGES.items():
            if min_bmi <= bmi < max_bmi:
                return category
        return HealthCategory.OBESE_3
```

**Acceptance Criteria:**  
- [ ] BMI calculation mathematically correct
- [ ] Health category mapping accurate per WHO standards
- [ ] Edge cases handled properly (boundary values)
- [ ] Return types match specifications

### MODEL-003: Input Validation System [P0]
```python
# src/utils/validators.py

from typing import Tuple, Any

class InputValidator:
    HEIGHT_RANGE = (100, 250)  # cm - realistic human height range
    WEIGHT_RANGE = (20, 300)   # kg - realistic human weight range
    
    @staticmethod  
    def validate_height(height: Any) -> Tuple[bool, str]:
        """Validate height input with detailed error messages"""
        if not isinstance(height, (int, float)):
            return False, "Height must be a number"
        
        if height <= 0:
            return False, "Height must be positive"
            
        if not (InputValidator.HEIGHT_RANGE[0] <= height <= InputValidator.HEIGHT_RANGE[1]):
            return False, f"Height must be between {InputValidator.HEIGHT_RANGE[0]} and {InputValidator.HEIGHT_RANGE[1]} cm"
            
        return True, ""
    
    @staticmethod
    def validate_weight(weight: Any) -> Tuple[bool, str]:
        """Validate weight input with detailed error messages"""
        # Similar implementation for weight validation
        pass
```

**Acceptance Criteria:**
- [ ] Type checking prevents non-numeric inputs
- [ ] Range validation matches specification
- [ ] Error messages are user-friendly
- [ ] Edge cases covered (zero, negative, extreme values)

### MODEL-004: Data Persistence Layer [P1]
```python
# src/utils/data_manager.py

import json
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime

class DataManager:
    def __init__(self, data_file: str = "bmi_history.json"):
        self.data_file = Path(data_file)
        self.ensure_data_file_exists()
    
    def save_measurement(self, result: BMIResult) -> bool:
        """Append new measurement to history file"""
        try:
            history = self.load_history()
            history.append(self._result_to_dict(result))
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_history(self) -> List[BMIResult]:
        """Load all measurement history from file"""
        # Implementation details
        pass
```

**Acceptance Criteria:**
- [ ] JSON serialization/deserialization works correctly  
- [ ] File I/O errors handled gracefully
- [ ] Data integrity maintained across operations
- [ ] Backup/recovery mechanism implemented

## 🎨 VIEW Tasks - User Interface

### VIEW-001: CustomTkinter Main Window [P0]
```python
# src/views/gui_interface.py

import customtkinter as ctk
from typing import Optional

class BMIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("BMI Calculator - Health Checker")
        self.geometry("700x600")
        self.minsize(600, 500)
        
        # Theme setup
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Create main interface
        self.create_widgets()
        
    def create_widgets(self):
        """Create main tabbed interface"""
        self.tabview = ctk.CTkTabview(self, width=680, height=580)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Calculator")
        self.tabview.add("History")  
        self.tabview.add("Graphs")
        self.tabview.add("Settings")
        
        # Initialize tab content
        self.setup_calculator_tab()
        self.setup_history_tab()
        self.setup_graphs_tab()
        self.setup_settings_tab()
```

**Acceptance Criteria:**
- [ ] Main window displays correctly with proper sizing
- [ ] Tabbed interface functions without errors  
- [ ] Theme system works (light/dark/system modes)
- [ ] Window is resizable with minimum size constraints

### VIEW-002: Calculator Input Interface [P0]
```python
def setup_calculator_tab(self):
    """Create BMI calculator input form"""
    calc_frame = self.tabview.tab("Calculator")
    
    # Title
    title = ctk.CTkLabel(calc_frame, text="BMI Calculator", 
                        font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=(20, 30))
    
    # Input section
    input_frame = ctk.CTkFrame(calc_frame)
    input_frame.pack(padx=40, pady=20, fill="x")
    
    # Height input
    height_label = ctk.CTkLabel(input_frame, text="Height (cm):", 
                               font=ctk.CTkFont(size=16))
    height_label.pack(pady=(20, 5))
    
    self.height_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 170",
                                    font=ctk.CTkFont(size=14), height=40, width=200)
    self.height_entry.pack(pady=(0, 15))
    self.height_entry.bind("<KeyRelease>", self.validate_input_realtime)
    
    # Weight input  
    weight_label = ctk.CTkLabel(input_frame, text="Weight (kg):", 
                               font=ctk.CTkFont(size=16))
    weight_label.pack(pady=(10, 5))
    
    self.weight_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 65",
                                    font=ctk.CTkFont(size=14), height=40, width=200)  
    self.weight_entry.pack(pady=(0, 15))
    self.weight_entry.bind("<KeyRelease>", self.validate_input_realtime)
    
    # Calculate button
    self.calc_button = ctk.CTkButton(calc_frame, text="Calculate BMI",
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    height=50, width=200, command=self.calculate_bmi)
    self.calc_button.pack(pady=20)
```

**Acceptance Criteria:**
- [ ] Input fields accept numeric input with validation
- [ ] Real-time input validation provides immediate feedback
- [ ] Calculate button state changes based on input validity
- [ ] Placeholder text guides user input expectations

### VIEW-003: Results Display Interface [P1]
```python
def display_result(self, result: BMIResult):
    """Display BMI calculation results with visual feedback"""
    category_name, color, advice = result.category.value
    
    # Results section
    if not hasattr(self, 'results_frame'):
        self.results_frame = ctk.CTkFrame(self.tabview.tab("Calculator"))
        self.results_frame.pack(padx=40, pady=20, fill="x")
    
    # Clear previous results
    for widget in self.results_frame.winfo_children():
        widget.destroy()
    
    # BMI value and category
    result_text = f"BMI: {result.bmi} | {category_name}"
    self.result_label = ctk.CTkLabel(self.results_frame, text=result_text,
                                    font=ctk.CTkFont(size=20, weight="bold"),
                                    text_color=color)
    self.result_label.pack(pady=(20, 10))
    
    # Progress bar showing position within category
    progress, _ = self.calculator.get_bmi_progress(result.bmi)
    self.progress_bar = ctk.CTkProgressBar(self.results_frame, width=300, height=20)
    self.progress_bar.set(progress)  
    self.progress_bar.pack(pady=10)
    
    # Health advice
    self.advice_label = ctk.CTkLabel(self.results_frame, text=advice,
                                    font=ctk.CTkFont(size=14), wraplength=400)
    self.advice_label.pack(pady=(10, 20))
```

**Acceptance Criteria:**  
- [ ] Results display immediately after calculation
- [ ] Color coding matches health category appropriately
- [ ] Progress bar accurately represents position within category
- [ ] Health advice is relevant and helpful

### VIEW-004: CLI Interface Implementation [P1]
```python  
# src/views/cli_interface.py

import argparse
from typing import Optional
from ..models.bmi_calculator import BMICalculator

class CLIInterface:
    def __init__(self):
        self.calculator = BMICalculator()
        
    def create_parser(self) -> argparse.ArgumentParser:
        """Create command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="BMI Calculator - Health status checker",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py --cli                # Interactive mode
  python main.py --cli 170 65         # Direct calculation
  python main.py --cli 170 65 --notes "Morning measurement"
            """
        )
        
        parser.add_argument("--cli", action="store_true", help="Use command-line interface")
        parser.add_argument("height", nargs="?", type=float, help="Height in cm")  
        parser.add_argument("weight", nargs="?", type=float, help="Weight in kg")
        parser.add_argument("--notes", help="Optional notes for measurement")
        parser.add_argument("--history", action="store_true", help="Show measurement history")
        
        return parser
    
    def run_interactive_mode(self):
        """Run interactive CLI session"""
        print("=" * 50)
        print("BMI Calculator - Interactive Mode")  
        print("=" * 50)
        
        while True:
            try:
                # Get user input
                height_input = input("Enter height (cm) [q to quit]: ").strip()
                if height_input.lower() == 'q':
                    break
                    
                height = float(height_input)
                weight = float(input("Enter weight (kg): ").strip())
                notes = input("Notes (optional): ").strip() or None
                
                # Calculate and display result
                result = self.calculator.process_measurement(height, weight, notes)
                self.display_result(result)
                
            except ValueError as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
```

**Acceptance Criteria:**
- [ ] Interactive mode accepts user input gracefully
- [ ] Direct calculation mode processes command-line arguments
- [ ] Error handling provides clear, actionable feedback
- [ ] Help text is comprehensive and useful

## 🧪 TEST Tasks - Quality Assurance

### TEST-001: Unit Test Suite for BMI Calculations [P0]
```python
# tests/unit/test_bmi_calculator.py

import pytest
from datetime import datetime
from src.models.bmi_calculator import BMICalculator, BMIResult, HealthCategory

class TestBMICalculator:
    def setup_method(self):
        """Setup test fixtures"""
        self.calculator = BMICalculator()
        
    def test_calculate_bmi_normal_values(self):
        """Test BMI calculation with standard inputs"""
        # Test case: 170cm, 65kg should yield BMI 22.5
        bmi = self.calculator.calculate_bmi(170, 65)
        assert bmi == 22.5
        
        # Test case: 160cm, 50kg should yield BMI 19.5  
        bmi = self.calculator.calculate_bmi(160, 50)
        assert bmi == 19.5
    
    def test_get_health_category_boundaries(self):
        """Test health category classification at boundary values"""
        # Test underweight boundary
        assert self.calculator.get_health_category(18.4) == HealthCategory.UNDERWEIGHT
        assert self.calculator.get_health_category(18.5) == HealthCategory.NORMAL
        
        # Test overweight boundary
        assert self.calculator.get_health_category(24.9) == HealthCategory.NORMAL
        assert self.calculator.get_health_category(25.0) == HealthCategory.OVERWEIGHT
        
        # Test obesity boundaries
        assert self.calculator.get_health_category(29.9) == HealthCategory.OVERWEIGHT
        assert self.calculator.get_health_category(30.0) == HealthCategory.OBESE_1
        
    def test_input_validation_edge_cases(self):
        """Test input validation with edge cases and invalid inputs"""  
        # Valid boundary cases
        is_valid, _ = self.calculator.validate_input(100, 20)  # Minimum values
        assert is_valid == True
        
        is_valid, _ = self.calculator.validate_input(250, 300)  # Maximum values  
        assert is_valid == True
        
        # Invalid cases
        is_valid, message = self.calculator.validate_input(50, 65)  # Height too low
        assert is_valid == False
        assert "100cm" in message
        
        is_valid, message = self.calculator.validate_input(170, 500)  # Weight too high
        assert is_valid == False  
        assert "300kg" in message
```

**Acceptance Criteria:**
- [ ] Test coverage ≥ 95% for BMI calculation logic
- [ ] All WHO boundary values tested accurately
- [ ] Edge cases and error conditions covered
- [ ] Tests run consistently across Python versions

### TEST-002: Integration Tests for GUI Workflow [P1]
```python
# tests/integration/test_gui_workflow.py

import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch
from src.views.gui_interface import BMIApp

class TestGUIWorkflow:
    def setup_method(self):
        """Setup GUI test environment"""
        self.app = BMIApp()
        
    def teardown_method(self):
        """Cleanup GUI after tests"""
        self.app.destroy()
        
    def test_complete_calculation_workflow(self):
        """Test end-to-end BMI calculation through GUI"""
        # Enter height value
        self.app.height_entry.delete(0, tk.END)
        self.app.height_entry.insert(0, "170")
        
        # Enter weight value  
        self.app.weight_entry.delete(0, tk.END)
        self.app.weight_entry.insert(0, "65")
        
        # Trigger calculation
        self.app.calculate_bmi()
        
        # Verify results displayed
        assert hasattr(self.app, 'result_label')
        result_text = self.app.result_label.cget("text")
        assert "22.5" in result_text
        assert "Normal Weight" in result_text
        
    def test_input_validation_feedback(self):
        """Test real-time input validation in GUI"""
        # Enter invalid height
        self.app.height_entry.delete(0, tk.END)
        self.app.height_entry.insert(0, "50")  # Too low
        
        # Trigger validation
        self.app.validate_input_realtime()
        
        # Check that calculate button is disabled
        button_state = self.app.calc_button.cget("state")
        assert button_state == "disabled"
```

**Acceptance Criteria:**
- [ ] GUI components interact correctly in end-to-end scenarios  
- [ ] Input validation provides appropriate UI feedback
- [ ] Error states are handled gracefully
- [ ] Results display matches expected format and styling

### TEST-003: Performance and Load Testing [P2]
```python
# tests/performance/test_performance.py

import pytest
import time
from src.models.bmi_calculator import BMICalculator

class TestPerformance:
    def setup_method(self):
        self.calculator = BMICalculator()
        
    def test_calculation_response_time(self):
        """Ensure BMI calculation completes within performance threshold"""
        start_time = time.time()
        
        # Perform 1000 calculations
        for i in range(1000):
            height = 150 + (i % 100)  # Vary height 150-250
            weight = 50 + (i % 150)   # Vary weight 50-200
            bmi = self.calculator.calculate_bmi(height, weight)
            assert bmi > 0
            
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete 1000 calculations in under 1 second
        assert total_time < 1.0
        
        # Average per calculation should be under 1ms  
        avg_time = total_time / 1000
        assert avg_time < 0.001
```

**Acceptance Criteria:**
- [ ] 1000 BMI calculations complete in under 1 second
- [ ] Average calculation time under 1 millisecond
- [ ] Memory usage remains stable during load testing
- [ ] No performance degradation over extended usage

## 📚 DOCS Tasks - Documentation

### DOCS-001: User Guide with Screenshots [P2]
```markdown
# docs/user-guide/README.md

# BMI Calculator User Guide

## Getting Started

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`  
3. Run the application: `python main.py`

### Using the GUI Version
[Screenshot of main interface]

1. **Enter your measurements**
   - Height: Enter in centimeters (e.g., 170)
   - Weight: Enter in kilograms (e.g., 65)
   
2. **Get your results**  
   - Click "Calculate BMI"
   - View your BMI value and health category
   - Read personalized health advice

3. **Track your progress**
   - Switch to "History" tab
   - View past measurements
   - See trends in "Graphs" tab

### Using the CLI Version
[Command examples with sample output]
```

**Acceptance Criteria:**
- [ ] User guide covers all major features
- [ ] Screenshots are current and high-quality
- [ ] Step-by-step instructions are clear
- [ ] Troubleshooting section addresses common issues

### DOCS-002: API Documentation [P2]
```python
# docs/api/bmi_calculator.md

# BMI Calculator API Reference

## Classes

### BMICalculator
Core calculation engine for BMI operations.

#### Methods

##### calculate_bmi(height: float, weight: float) -> float
Calculate Body Mass Index from height and weight.

**Parameters:**
- `height` (float): Height in centimeters (100-250)
- `weight` (float): Weight in kilograms (20-300)

**Returns:**
- `float`: BMI value rounded to 1 decimal place

**Raises:**
- `ValueError`: If inputs are outside valid ranges

**Example:**
```python
calculator = BMICalculator()
bmi = calculator.calculate_bmi(170, 65)
print(f"BMI: {bmi}")  # Output: BMI: 22.5
```
```

**Acceptance Criteria:**
- [ ] All public methods documented with examples
- [ ] Parameter types and constraints specified
- [ ] Return values clearly described
- [ ] Common usage patterns demonstrated

## 🚀 DEPLOY Tasks - Packaging & Distribution

### DEPLOY-001: Executable Packaging [P2]  
```python
# build_executable.py

import PyInstaller.__main__
import os
from pathlib import Path

def build_windows_executable():
    """Build Windows .exe using PyInstaller"""
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--windowed',  
        '--name=BMI_Calculator',
        '--icon=assets/icon.ico',
        '--add-data=src;src',
        '--distpath=dist/windows'
    ])

def build_macos_app():
    """Build macOS .app bundle"""  
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--windowed',
        '--name=BMI Calculator',
        '--icon=assets/icon.icns',
        '--distpath=dist/macos'
    ])
```

**Acceptance Criteria:**
- [ ] Windows executable builds successfully
- [ ] macOS application bundle creates properly
- [ ] Linux binary works across distributions
- [ ] All dependencies included in executable

### DEPLOY-002: Release Automation [P3]
```yaml
# .github/workflows/release.yml

name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-executables:
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python  
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
          
      - name: Build executable
        run: python build_executable.py
        
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: executables-${{ matrix.os }}
          path: dist/
```

**Acceptance Criteria:**
- [ ] Automated builds trigger on version tags
- [ ] Cross-platform executables generated successfully  
- [ ] Release artifacts uploaded to GitHub Releases
- [ ] Download links work correctly

## ✅ Task Completion Tracking

### Sprint Planning
- **Sprint 1**: SETUP-001 → SETUP-003, MODEL-001 → MODEL-002
- **Sprint 2**: MODEL-003 → MODEL-004, TEST-001, VIEW-001
- **Sprint 3**: VIEW-002 → VIEW-004, TEST-002
- **Sprint 4**: TEST-003, DOCS-001 → DOCS-002  
- **Sprint 5**: DEPLOY-001 → DEPLOY-002

### Definition of Done Checklist
For each task to be considered complete:

- [ ] Implementation matches acceptance criteria
- [ ] Unit tests written and passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Manual testing completed
- [ ] CI/CD pipeline passes
- [ ] Performance requirements met

---

*These implementation tasks follow GitHub Spec Kit methodology for structured, AI-assisted development with Claude Code*