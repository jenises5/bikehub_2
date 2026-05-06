# Five-factor scoring weights
# These can be changed without touching the algorithm

WEIGHTS = {
    "budget": 0.30,
    "size": 0.25,
    "style": 0.15,
    "review": 0.15,
    "brand_tier": 0.15,
}

# Brand tier scores
BRAND_TIER_SCORES = {
    1: 1.00,  # Budget/Mid
    2: 0.67,  # Mid/High
    3: 0.33,  # Premium
    None: 0.20,  # Unverified brand
}

# Counterfeit risk penalties
COUNTERFEIT_PENALTIES = {"low": 0.00, "medium": -0.05, "high": -0.20}

# Default review score for products with no reviews yet
DEFAULT_REVIEW_SCORE = 0.6  # Equivalent to 3 stars out of 5

# Budget tier multipliers
BEST_BRAND_MULTIPLIER = 1.20  # Up to 120% of max budget
BUDGET_PICK_MULTIPLIER = 0.80  # Up to 80% of max budget
