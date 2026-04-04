# Fatsecret Nutrition Hand — Domain Expertise

## Overview
This hand monitors nutrition intake and goal alignment using the Fatsecret API.

## Key Concepts

### Macronutrients
| Macro | Calories/gram | Notes |
|-------|-------------|-------|
| Protein | 4 cal/g | Essential for muscle building/repair |
| Carbohydrates | 4 cal/g | Primary energy source |
| Fat | 9 cal/g | Hormone production, nutrient absorption |

### Body Composition
- **BMI** = weight_kg / (height_m)²
- Underweight: < 18.5
- Normal: 18.5 - 24.9
- Overweight: 25 - 29.9
- Obese: ≥ 30

### Energy Balance
- **TDEE** (Total Daily Energy Expenditure) ≈ BMR × activity factor
- 3500 calories ≈ 0.45 kg body weight
- Deficit of 500 cal/day ≈ 0.45 kg/week loss

### Protein Requirements
| Activity Level | grams/kg body weight |
|--------------|---------------------|
| Sedentary | 0.8 |
| Light activity | 1.2 |
| Moderate activity | 1.6 |
| Active/gym | 2.0 |
| Intense training | 2.4+ |

## CLI Commands Reference

### Get profile
```bash
fatcli profile
```
Returns: Height, current weight, goal weight, BMI, status

### Get daily meals with summary
```bash
fatcli meals --date YYYY-MM-DD --summary
```
Returns: Total calories, protein, carbs, fat, fiber, sodium, sugar

### Log weight
```bash
fatcli profile --weight 83.5 --goal 74
```
Updates current weight and goal weight

## Data Interpretation

### Goal Alignment Assessment
| Metric | On Track | Warning | Alert |
|--------|----------|---------|-------|
| Calories | ±15% of target | ±15-30% | >30% off |
| Protein | ≥75% of goal | 50-75% | <50% |
| Weight trend | Stable/decreasing | +0.5kg/week | +1kg+ week |

### Common Issues
- **Low protein**: Muscle loss risk, increased hunger
- **No meal logs**: Tracking non-compliance
- **Weight increasing**: Calorie surplus despite logging
- **Extreme deficits**: Energy deficit too aggressive

## CLI Output Parsing

Profile output format:
```
Profile
  Height:        173 cm
  Current Weight: 84.0 kg (as of 2026-04-03)
  Goal Weight:    74.0 kg
  Difference:     +10.0 kg
  BMI:            28.1
  Status:         Overweight
```

Meals summary format:
```
Macro Summary for 2026-04-03
  Cal:   1847
  Protein: 142.3g
  Carbs:  180.5g
  Fat:    65.2g
  Fiber:   18.4g
  Sodium:  2400mg
  Sugar:   45.2g
```
