# Fatsecret Nutrition Hand — CLI Reference Guide

## Overview

This hand uses `fatcli` (Fatsecret CLI) to track nutrition. ALL interactions happen via CLI commands.

---

## COMMAND 0: fatcli init (Authentication Setup)

### What it does
Sets up OAuth authentication with Fatsecret API. Required before using any other commands.

### IMPORTANT: This is a 2-Step Process for Agents

The `fatcli init` command requires user interaction (browser), so for an agent, you must split it into two steps.

### Step 1: Get Authorization URL
```bash
fatcli init --url-only
```
This outputs a URL. Tell user: "Please visit this URL and authorize the app, then give me the PIN code."

### Step 2: Complete with PIN
```bash
fatcli init --pin <PIN>
```
Replace `<PIN>` with the code the user gets from the authorization page.

### Full Auth Flow (for agent)
```
You: Run "fatcli init --url-only" to get the authorization URL.
     Tell user: "Please visit [URL] and authorize, then give me the PIN."

User provides PIN: 123456

You: Run "fatcli init --pin 123456" to complete authentication.
```

### Alternative: Interactive Mode (not for agents)
```bash
fatcli init
```
This does both steps in one go (opens URL, asks for PIN in terminal).
ONLY use this if running fatcli manually in a terminal.

### If "Not authenticated" error appears
If any command gives error: `Error: Not authenticated. Run 'fatcli init' first.`

THEN follow the 2-step process above:
1. `fatcli init --url-only`
2. `fatcli init --pin <PIN>`

### Environment Variables (Required)
Before running `init`, these must be set:
```bash
export FATSECRET_CONSUMER_KEY="your_consumer_key"
export FATSECRET_CONSUMER_SECRET="your_consumer_secret"
```

### Getting API Keys
1. Go to https://platform.fatsecret.com/api/
2. Sign up / Log in
3. Create a new app to get consumer key and secret

---

## COMMAND 1: fatcli profile

### What it does
Gets user's height, current weight, goal weight, and BMI.

### Command
```bash
fatcli profile
```

### Parameters
None.

### Output
```
Profile
  Height:        173 cm
  Current Weight: 84.0 kg (as of 2026-04-03)
  Goal Weight:    74.0 kg
  Difference:     +10.0 kg
  BMI:            28.1
  Status:         Overweight
```

### Use when
- Checking user's current weight and goals
- BMI assessment needed
- Setting protein/calorie targets

---

## COMMAND 2: fatcli profile --weight <kg> --goal <kg>

### What it does
Updates user's current weight and/or goal weight.

### Command
```bash
fatcli profile --weight <kg> --goal <kg>
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `--weight` | No | Current weight in kg (e.g., 83.5) |
| `--goal` | No | Goal weight in kg (e.g., 74) |

At least ONE must be provided.

### Examples
```bash
# Update only current weight
fatcli profile --weight 83.5

# Update only goal weight
fatcli profile --goal 74

# Update both
fatcli profile --weight 83.5 --goal 74
```

---

## COMMAND 3: fatcli meals --date <YYYY-MM-DD> --summary

### What it does
Shows all meals logged for a specific date with macro totals.

### Command
```bash
fatcli meals --date <YYYY-MM-DD> --summary
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `--date` | Yes | Date in YYYY-MM-DD format (e.g., 2026-04-04) |
| `--summary` | Yes | Flag to show macro summary (must be present) |

### Examples
```bash
# Today's summary
fatcli meals --date 2026-04-04 --summary

# Yesterday's summary
fatcli meals --date 2026-04-03 --summary
```

### Output
```
Macro Summary for 2026-04-04
  Cal:   1847
  Protein: 142.3g
  Carbs:  180.5g
  Fat:    65.2g
  Fiber:   18.4g
  Sodium:  2400mg
  Sugar:   45.2g
```

### Note
If no meals logged for the date, output will say "No meal entries found for [date]".

---

## COMMAND 4: fatcli meals search <query>

### What it does
Searches for food items by name. Returns a table with food IDs.

### Command
```bash
fatcli meals search <query>
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `<query>` | Yes | Search text (e.g., "chicken", "rice", "apple") |

Use quotes if query has spaces.

### Examples
```bash
# Simple search
fatcli meals search chicken

# Search with spaces
fatcli meals search "roasted chicken"
fatcli meals search "boneless skinless chicken breast"
```

### Output
```
                   Search results for 'chicken'
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Food Name                                                    ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┡
│ 1641    │ Chicken Breast                                               │
│ 1695    │ Chicken Thigh                                                │
│ 48833   │ Boneless Skinless Chicken Breasts                            │
│ 448901  │ Grilled Chicken                                              │
│ 4881229 │ Skinless Chicken Breast                                      │
│ 1623    │ Chicken                                                      │
│ 419178  │ Rotisserie Chicken                                           │
│ 1677    │ Chicken Drumstick                                            │
│ 34511   │ Chicken Meat (Stewing, Stewed, Cooked)                       │
│ 34499   │ Chicken Meat (Roasting, Roasted, Cooked)                     │
│ 3946778 │ Chicken Breast                                               │
│ 1697    │ Chicken Thigh (Skin Not Eaten)                               │
│ 1713    │ Chicken Wing                                                 │
│ 1660    │ Chicken Leg (Skin Eaten)                                     │
│ 1628    │ Roasted Broiled or Baked Chicken (Skin Not Eaten)            │
│ 1636    │ Baked or Fried Coated Chicken (Skin/Coating Eaten)           │
│ 1696    │ Chicken Thigh (Skin Eaten)                                   │
│ 1644    │ Roasted Brooled or Baked Chicken Breast                      │
│ 4718517 │ Boneless Skinless Chicken Breast                             │
└─────────┴──────────────────────────────────────────────────────────────┘
```

### Important
- Save the ID! You need it for the `info` and `add` commands.
- Choose the BEST match based on user's description.
- If unsure, present top 3-5 options and ask user to confirm.

---

## COMMAND 5: fatcli meals info <food_id>

### What it does
Shows detailed nutrition info and available serving sizes for a food.

### Command
```bash
fatcli meals info <food_id>
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `<food_id>` | Yes | Food ID from search results (e.g., 1641) |

### Examples
```bash
fatcli meals info 1641
fatcli meals info 1695
fatcli meals info 48833
```

### Output
```
Chicken Breast

                              Available servings
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━┳━━━┳━━━━━━━┓
┃ ID    ┃ Description                                       ┃ Cal ┃     P ┃ C ┃     F ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━╇━━━╇━━━━━━━┡
│ 50321 │ 100 g                                             │ 195 │ 29.55 │ 0 │  7.72 │
│ 5034  │ 1/2 small (yield after cooking, bone removed)     │ 164 │ 24.82 │ 0 │  6.48 │
│ 4833  │ 1 oz boneless, cooked                            │  55 │  8.38 │ 0 │  2.19 │
│ 5035  │ 1/2 medium (yield after cooking, bone removed)    │ 191 │ 28.96 │ 0 │  7.57 │
│ 5036  │ 1/2 large (yield after cooking, bone removed)    │ 216 │ 32.80 │ 0 │  8.57 │
│ 5041  │ 1 oz boneless (yield after cooking)               │  35 │  5.32 │ 0 │  1.39 │
│ 5040  │ 1 oz raw (yield after cooking, bone removed)      │  29 │  4.43 │ 0 │  1.16 │
│ 4834  │ 1 cup cooked, diced                               │ 263 │ 39.89 │ 0 │ 10.42 │
│ 5039  │ 1 oz, with bone cooked (yield after bone removed) │  47 │  7.09 │ 0 │  1.85 │
│ 5043  │ 1 serving (98 g)                                  │ 191 │ 28.96 │ 0 │  7.57 │
└───────┴───────────────────────────────────────────────────┴─────┴───────┴───┴───────┘
```

### Columns
| Column | Meaning |
|--------|---------|
| ID | Serving ID (needed for add command) |
| Description | Serving size description |
| Cal | Calories |
| P | Protein in grams |
| C | Carbohydrates in grams |
| F | Fat in grams |

### Important
- You MUST run this before adding a food!
- Pick the serving ID that best matches what user ate.
- Present serving options if user didn't specify exact amount.

---

## COMMAND 6: fatcli meals add <food_id> --serving <id> --units <num> --meal <type>

### What it does
Adds a food entry to a specific meal.

### Command
```bash
fatcli meals add <food_id> --serving <serving_id> --units <number> --meal <meal_type>
```

### Parameters (ALL MANDATORY)
| Parameter | Required | Description |
|-----------|----------|-------------|
| `<food_id>` | Yes | Food ID from search (e.g., 1641) |
| `--serving` | Yes | Serving ID from info command (e.g., 50321) |
| `--units` | Yes | Number of servings, can be decimal (e.g., 1, 1.5, 2) |
| `--meal` | Yes | Must be ONE of: breakfast, lunch, dinner, other |
| `--date` | No | Date, defaults to today. Format: YYYY-MM-DD |

### Valid meal types
```
breakfast
lunch
dinner
other
```

### Examples
```bash
# Add 1 serving of chicken breast (100g) for lunch
fatcli meals add 1641 --serving 50321 --units 1 --meal lunch

# Add 2 servings for dinner
fatcli meals add 1641 --serving 50321 --units 2 --meal dinner

# Add 1.5 servings for lunch
fatcli meals add 1641 --serving 50321 --units 1.5 --meal lunch

# Add for yesterday's dinner
fatcli meals add 1641 --serving 50321 --units 1 --meal dinner --date 2026-04-03

# Add as a snack (use "other")
fatcli meals add 1641 --serving 50321 --units 0.5 --meal other
```

### Common Mistakes to Avoid
| Wrong | Correct | Reason |
|-------|---------|--------|
| `fatcli meals add 1641` | Must include --serving, --units, --meal | ALL params required |
| `--meal lunchh` | `--meal lunch` | Must match exactly: breakfast/lunch/dinner/other |
| `--units one` | `--units 1` | Must be a number |
| `--date 04-04-2026` | `--date 2026-04-04` | Must be YYYY-MM-DD format |

### Success Output
Usually shows "Added food entry" or similar confirmation.

---

## COMMAND 7: fatcli meals delete <entry_id>

### What it does
Deletes a food entry that was previously added.

### Command
```bash
fatcli meals delete <entry_id>
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `<entry_id>` | Yes | Entry ID from meals list |

### How to find entry_id
Run: `fatcli meals --date <YYYY-MM-DD>` (without --summary)

### Example
```bash
# First, find the entry_id
fatcli meals --date 2026-04-04
# Output shows entry IDs

# Delete entry ID 12345
fatcli meals delete 12345
```

---

## WORKFLOW: Adding Food for a Meal

### Step 1: User says "I ate X for lunch"
Extract: food name ("X") and meal type ("lunch")

### Step 2: Search for the food
```bash
fatcli meals search "X"
```

### Step 3: Pick best match
- Match food name to what user said
- Save the food ID

### Step 4: Get serving options
```bash
fatcli meals info <food_id>
```

### Step 5: Present options to user (if unclear)
Ask user to confirm serving size, or pick best match if obvious.

### Step 6: Add the entry
```bash
fatcli meals add <food_id> --serving <serving_id> --units <num> --meal <lunch>
```

### Step 7: Confirm to user
Tell user what was added with macros.

### Example Conversation
```
User: I ate roasted chicken for lunch

You: (searches)
fatcli meals search "roasted chicken"

User picks: 419178 - Rotisserie Chicken

You: (gets info)
fatcli meals info 419178

User picks serving: 50321 (100g)

You: 
fatcli meals add 419178 --serving 50321 --units 1 --meal lunch

You: Added 100g Rotisserie Chicken to lunch. (195 cal, 29.55g protein, 0g carbs, 7.72g fat)
```

---

## WORKFLOW: Checking Daily Intake

### Command
```bash
fatcli profile
fatcli meals --date <YYYY-MM-DD> --summary
```

### Example
```bash
fatcli profile
fatcli meals --date 2026-04-04 --summary
```

### Report Format
```
Date: 2026-04-04
Calories: 1847 / ~2500 target
Protein: 142.3g / ~135g target (ON TRACK)
Carbs: 180.5g
Fat: 65.2g

Meals logged: 3 (breakfast, lunch, dinner)
Status: ✓ On Track
```

---

## IMPORTANT RULES

1. ALL parameters for `add` command are MANDATORY: --serving, --units, --meal
2. Meal type must be EXACTLY: breakfast, lunch, dinner, or other (no other values)
3. Date format must be YYYY-MM-DD (e.g., 2026-04-04, not 04-04-2026)
4. Units can be decimal: 1.5, 0.5, 2.25, etc.
5. Always run `info` before `add` to get correct serving ID
6. If user doesn't specify units, assume 1
7. If user doesn't specify serving, present options from `info` output
8. Search query can be simple; don't worry about exact wording
