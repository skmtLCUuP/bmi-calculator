# BMI Calculator - GitHub Spec Kit Specification

*Generated using GitHub Spec Kit methodology for spec-driven development*

## 🎯 Project Overview

### What are we building?
A comprehensive BMI (Body Mass Index) calculator application that helps users assess their health status through intuitive interfaces and data visualization.

### Why are we building this?
- **Health Awareness**: Enable individuals to easily monitor their BMI and understand health implications
- **Accessibility**: Provide both GUI and CLI interfaces for different user preferences
- **Data Tracking**: Allow users to track BMI changes over time with visual analytics
- **Educational**: Deliver WHO-standard health guidance with each calculation

## 👥 Target Users

### Primary Users
- **Health-conscious individuals** seeking regular BMI monitoring
- **Fitness enthusiasts** tracking body composition changes
- **Healthcare professionals** needing quick BMI calculations

### Secondary Users
- **Students** learning about health metrics
- **Developers** seeking a well-structured Python GUI application example

## 🎨 User Experience Goals

### Core Experience
Users should be able to:
1. Input height and weight with immediate validation feedback
2. Receive instant BMI calculation with health category classification  
3. View historical BMI data trends through interactive graphs
4. Access personalized health advice based on WHO standards
5. Customize application appearance and target health goals

### Interface Requirements
- **Intuitive Design**: Clean, modern interface using CustomTkinter
- **Responsive Feedback**: Real-time input validation and error handling
- **Visual Clarity**: Color-coded health categories with progress indicators
- **Cross-Platform**: Consistent experience across Windows, macOS, Linux

## 🔧 Functional Requirements

### FR-1: BMI Calculation Engine
- **Input**: Height (cm), Weight (kg)
- **Process**: BMI = weight(kg) / (height(m))²
- **Output**: BMI value (rounded to 1 decimal place)
- **Validation**: Height: 100-250cm, Weight: 20-300kg

### FR-2: Health Category Classification
- **Categories**: 6 WHO-standard classifications
- **Color Coding**: Visual indicators for each category
- **Advice**: Personalized recommendations per category

| BMI Range | Category | Color | Health Advice |
|-----------|----------|-------|---------------|
| < 18.5 | Underweight | Blue | Consider weight gain |
| 18.5-24.9 | Normal | Green | Maintain healthy weight |
| 25.0-29.9 | Overweight | Yellow | Exercise and diet management |
| 30.0-34.9 | Obese I | Orange | Consult healthcare provider |
| 35.0-39.9 | Obese II | Red | Active medical intervention |
| ≥ 40.0 | Obese III | Dark Red | Specialized medical treatment |

### FR-3: Data Persistence
- **Storage**: JSON-based local storage (`bmi_history.json`)
- **Structure**: Timestamped records with optional notes
- **Operations**: Create, Read, Delete historical records

### FR-4: Trend Visualization
- **Graph Type**: Line chart with matplotlib integration
- **Data Points**: BMI values over time
- **Features**: BMI range indicators, trend lines
- **Interactivity**: Zoom, pan, data point inspection

### FR-5: Dual Interface Support
- **GUI Mode**: CustomTkinter-based desktop application
- **CLI Mode**: Command-line interface with interactive/direct modes
- **Consistency**: Identical calculation logic across interfaces

## ⚙️ Non-Functional Requirements

### NFR-1: Performance
- **Calculation Response**: < 100ms
- **Application Startup**: < 3 seconds
- **Memory Usage**: < 80MB during normal operation
- **File I/O**: < 500ms for history operations

### NFR-2: Usability
- **Learning Curve**: First-time users productive within 2 minutes
- **Error Recovery**: Clear error messages with corrective guidance
- **Accessibility**: Keyboard navigation, screen reader compatibility
- **Visual Design**: Modern, professional appearance

### NFR-3: Reliability
- **Input Validation**: Comprehensive range and type checking
- **Error Handling**: Graceful degradation without crashes  
- **Data Integrity**: Automatic backup and recovery for history data
- **Cross-Platform**: Consistent behavior across operating systems

### NFR-4: Maintainability
- **Code Structure**: MVC architecture with clear separation
- **Testing**: 100% coverage for core calculation logic
- **Documentation**: Comprehensive README and API documentation
- **Type Safety**: Full type hints throughout codebase

## 🏗️ Technical Constraints

### Technology Stack
- **Language**: Python 3.8+ (for broad compatibility)
- **GUI Framework**: CustomTkinter (modern, theme-aware)
- **Data Visualization**: matplotlib (established, feature-rich)
- **Testing**: pytest (industry standard)
- **Data Format**: JSON (human-readable, lightweight)

### Platform Requirements
- **Operating Systems**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python Runtime**: 3.8, 3.9, 3.10, 3.11 (verified compatibility)
- **Dependencies**: Minimal external dependencies for security

### Development Standards
- **Code Style**: Black formatting, consistent naming conventions
- **Type Checking**: mypy static analysis
- **Version Control**: Git with conventional commits
- **CI/CD**: GitHub Actions for automated testing

## ✅ Success Criteria

### Launch Readiness
- [ ] All functional requirements implemented and tested
- [ ] Cross-platform compatibility verified
- [ ] Performance benchmarks met
- [ ] Documentation complete and accurate
- [ ] Security review passed

### User Adoption Metrics
- User can complete first BMI calculation within 30 seconds
- Historical data visualization loads within 2 seconds
- Zero crashes during normal operation flows
- Positive user feedback on interface intuitiveness

### Technical Quality Gates
- 100% test coverage for BMI calculation logic
- All CI/CD pipeline tests passing across Python versions
- Static analysis (mypy, black) with zero violations
- Memory leak testing shows stable usage over 1000 calculations

---

*This specification follows GitHub Spec Kit methodology for AI-assisted development*