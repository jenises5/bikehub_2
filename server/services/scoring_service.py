from config.scoring import (
    WEIGHTS,
    BRAND_TIER_SCORES,
    COUNTERFEIT_PENALTIES,
    DEFAULT_REVIEW_SCORE,
    BEST_BRAND_MULTIPLIER,
    BUDGET_PICK_MULTIPLIER,
)


def score_budget(price: float, budget_min: float, budget_max: float) -> float:
    """
    1.0 = perfectly within budget
    0.8 = below min (too cheap, may signal low quality)
    Drops proportionally if over budget
    0.0 if more than 2x the max budget
    """
    if price > budget_max * 2:
        return 0.0
    if price > budget_max:
        # Proportional drop between max and 2x max
        overage = (price - budget_max) / budget_max
        return max(0.0, 1.0 - overage)
    if price < budget_min:
        return 0.8
    return 1.0


def score_size(product_frame_size: str, recommended_size: str) -> float:
    """
    1.0 = exact match
    0.5 = one size off
    0.0 = completely incompatible
    """
    if not product_frame_size or not recommended_size:
        return 0.5  # No size info, neutral score

    size_order = ["XS", "S", "M", "L", "XL", "XXL"]

    prod = product_frame_size.upper().strip()
    rec = recommended_size.upper().strip()

    if prod == rec:
        return 1.0

    try:
        prod_idx = size_order.index(prod)
        rec_idx = size_order.index(rec)
        diff = abs(prod_idx - rec_idx)
        if diff == 1:
            return 0.5
        return 0.0
    except ValueError:
        # Size not in standard list, try string match
        return 0.5


def score_style(product_style: str, requested_style: str) -> float:
    """
    1.0 = exact match
    0.7 = product is all-around/versatile
    0.5 = close style match
    0.0 = no match
    """
    if not product_style or not requested_style:
        return 0.5

    prod = product_style.lower().strip()
    req = requested_style.lower().strip()

    if prod == req:
        return 1.0

    versatile_tags = ["all-around", "versatile", "all_around", "general"]
    if prod in versatile_tags:
        return 0.7

    # Close style matches
    close_matches = {
        "mountain": ["trail", "enduro", "xc"],
        "road": ["fitness", "gravel"],
        "fitness": ["road", "commute"],
        "trail": ["mountain", "enduro"],
        "commute": ["fitness", "urban"],
    }
    if req in close_matches and prod in close_matches.get(req, []):
        return 0.5

    return 0.0


def score_review(avg_rating) -> float:
    """
    Normalize 0-5 star rating to 0-1 score.
    Default to 0.6 (3 stars) if no reviews yet.
    """
    if avg_rating is None:
        return DEFAULT_REVIEW_SCORE
    return float(avg_rating) / 5.0


def score_brand_tier(tier: int, counterfeit_risk: str = "low") -> float:
    """
    Tier 1 = 1.0, Tier 2 = 0.67, Tier 3 = 0.33, None = 0.20
    Counterfeit risk penalty applied on top.
    """
    base_score = BRAND_TIER_SCORES.get(tier, BRAND_TIER_SCORES[None])
    penalty = COUNTERFEIT_PENALTIES.get(counterfeit_risk, 0.0)
    return max(0.0, base_score + penalty)


def calculate_final_score(
    price: float,
    budget_min: float,
    budget_max: float,
    frame_size: str,
    recommended_size: str,
    riding_style: str,
    requested_style: str,
    avg_rating,
    brand_tier: int,
    counterfeit_risk: str = "low",
) -> dict:
    """
    Calculate the full 5-factor score for a product.
    Returns individual factor scores AND the final weighted score.
    """
    budget = score_budget(price, budget_min, budget_max)
    size = score_size(frame_size, recommended_size)
    style = score_style(riding_style, requested_style)
    review = score_review(avg_rating)
    brand = score_brand_tier(brand_tier, counterfeit_risk)

    final = (
        budget * WEIGHTS["budget"]
        + size * WEIGHTS["size"]
        + style * WEIGHTS["style"]
        + review * WEIGHTS["review"]
        + brand * WEIGHTS["brand_tier"]
    )

    return {
        "final_score": round(final, 4),
        "breakdown": {
            "budget": round(budget, 4),
            "size": round(size, 4),
            "style": round(style, 4),
            "review": round(review, 4),
            "brand_tier": round(brand, 4),
        },
    }
