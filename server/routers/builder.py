from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import database
from services.scoring_service import calculate_final_score
from config.scoring import BEST_BRAND_MULTIPLIER, BUDGET_PICK_MULTIPLIER

router = APIRouter(prefix="/builder", tags=["Auto Builder"])

COMPONENT_TYPES = ["frame", "fork", "drivetrain", "wheels", "brakes", "accessory"]


class BuilderRequest(BaseModel):
    budget_min: float
    budget_max: float
    height_cm: float
    riding_style: str
    mode: str = "complete_bike"  # "complete_bike" or "custom_build"


async def get_recommended_size(height_cm: float) -> str:
    row = await database.fetch_one(
        """
        SELECT recommended_size FROM sizing_chart
        WHERE height_min <= :height AND height_max >= :height
        LIMIT 1
        """,
        {"height": height_cm},
    )
    if row:
        return row["recommended_size"]
    if height_cm < 155:
        return "XS"
    elif height_cm < 165:
        return "S"
    elif height_cm < 175:
        return "M"
    elif height_cm < 185:
        return "L"
    else:
        return "XL"


async def score_products(
    products, budget_min, budget_max, recommended_size, riding_style
):
    """Score a list of products and return them sorted by score."""
    scored = []
    for product in products:
        result = calculate_final_score(
            price=float(product["price"]),
            budget_min=budget_min,
            budget_max=budget_max,
            frame_size=product["frame_size"],
            recommended_size=recommended_size,
            riding_style=product["riding_style"],
            requested_style=riding_style,
            avg_rating=product["avg_rating"],
            brand_tier=product["brand_tier"],
            counterfeit_risk=product["counterfeit_risk"] or "low",
        )
        scored.append(
            {
                "id": product["id"],
                "name": product["name"],
                "price": float(product["price"]),
                "stock_quantity": product["stock_quantity"],
                "frame_size": product["frame_size"],
                "riding_style": product["riding_style"],
                "description": product["description"],
                "image_url": product["image_url"],
                "category": product["category"],
                "component_type": product["component_type"],
                "brand_name": product["brand_name"],
                "brand_tier": product["brand_tier"],
                "final_score": result["final_score"],
                "score_breakdown": result["breakdown"],
            }
        )
    scored.sort(key=lambda x: x["final_score"], reverse=True)
    return scored


async def fetch_products_by_type(component_type: str, budget_max: float):
    """Fetch all active in-stock products of a given component type."""
    return await database.fetch_all(
        """
        SELECT p.id, p.name, p.price, p.stock_quantity, p.frame_size,
               p.riding_style, p.description, p.image_url, p.category,
               p.component_type,
               b.name as brand_name, b.tier as brand_tier, b.counterfeit_risk,
               COALESCE(AVG(r.rating), NULL) as avg_rating
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN reviews r ON p.id = r.product_id
        WHERE p.is_active = TRUE
        AND p.stock_quantity > 0
        AND p.component_type = :component_type
        GROUP BY p.id, p.name, p.price, p.stock_quantity, p.frame_size,
                 p.riding_style, p.description, p.image_url, p.category,
                 p.component_type, b.name, b.tier, b.counterfeit_risk
        """,
        {"component_type": component_type},
    )


async def build_three_tiers(scored_products, budget_max, label_prefix=""):
    """Given scored products, return Best Match, Best Brand, Budget Pick."""
    best_match = next((p for p in scored_products if p["price"] <= budget_max), None)
    best_brand_budget = budget_max * BEST_BRAND_MULTIPLIER
    best_brand_candidates = sorted(
        [p for p in scored_products if p["price"] <= best_brand_budget],
        key=lambda x: (x["brand_tier"] or 99, -x["final_score"]),
    )
    best_brand = best_brand_candidates[0] if best_brand_candidates else None

    budget_pick_max = budget_max * BUDGET_PICK_MULTIPLIER
    budget_pick = next(
        (p for p in scored_products if p["price"] <= budget_pick_max), None
    )

    return best_match, best_brand, budget_pick


async def get_alternatives(product_id: int, component_type: str):
    """Get up to 3 alternatives from different brand tiers."""
    rows = await database.fetch_all(
        """
        SELECT p.id, p.name, p.price, b.name as brand_name, b.tier as brand_tier
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.component_type = :component_type
        AND p.id != :product_id
        AND p.is_active = TRUE
        AND p.stock_quantity > 0
        ORDER BY b.tier ASC, p.price ASC
        LIMIT 3
        """,
        {"component_type": component_type, "product_id": product_id},
    )
    return [dict(row) for row in rows]


@router.post("/generate")
async def generate_builds(body: BuilderRequest):
    # Validate inputs
    if body.budget_min < 0 or body.budget_max < 0:
        raise HTTPException(status_code=400, detail="Budget cannot be negative")
    if body.budget_min > body.budget_max:
        raise HTTPException(
            status_code=400, detail="Budget min cannot exceed budget max"
        )
    if body.height_cm < 100 or body.height_cm > 250:
        raise HTTPException(
            status_code=400, detail="Height must be between 100 and 250 cm"
        )
    if body.mode not in ["complete_bike", "custom_build"]:
        raise HTTPException(
            status_code=400, detail="Mode must be complete_bike or custom_build"
        )

    recommended_size = await get_recommended_size(body.height_cm)

    # -------------------------------------------------------
    # MODE 1: COMPLETE BIKE
    # -------------------------------------------------------
    if body.mode == "complete_bike":
        products = await fetch_products_by_type(
            "complete_bike", body.budget_max * BEST_BRAND_MULTIPLIER
        )

        if not products:
            raise HTTPException(
                status_code=404, detail="No complete bikes available right now."
            )

        scored = await score_products(
            products,
            body.budget_min,
            body.budget_max,
            recommended_size,
            body.riding_style,
        )

        best_match, best_brand, budget_pick = await build_three_tiers(
            scored, body.budget_max
        )

        results = {}
        if best_match:
            results["best_match"] = {
                "label": "Best Match",
                "badge": "green",
                "description": "Highest scoring complete bike within your exact budget",
                "product": best_match,
                "alternatives": await get_alternatives(
                    best_match["id"], "complete_bike"
                ),
            }
        if best_brand:
            results["best_brand"] = {
                "label": "Best Brand",
                "badge": "purple",
                "description": f"Best quality complete bike up to ₱{body.budget_max * BEST_BRAND_MULTIPLIER:,.0f}",
                "product": best_brand,
                "alternatives": await get_alternatives(
                    best_brand["id"], "complete_bike"
                ),
            }
        if budget_pick:
            results["budget_pick"] = {
                "label": "Budget Pick",
                "badge": "amber",
                "description": f"Best value complete bike under ₱{body.budget_max * BUDGET_PICK_MULTIPLIER:,.0f}",
                "product": budget_pick,
                "alternatives": await get_alternatives(
                    budget_pick["id"], "complete_bike"
                ),
            }

        if not results:
            raise HTTPException(
                status_code=404, detail="No complete bikes found matching your budget."
            )

        return {
            "mode": "complete_bike",
            "recommended_size": recommended_size,
            "height_cm": body.height_cm,
            "budget_min": body.budget_min,
            "budget_max": body.budget_max,
            "riding_style": body.riding_style,
            "results": results,
        }

    # -------------------------------------------------------
    # MODE 2: CUSTOM BUILD FROM COMPONENTS
    # -------------------------------------------------------
    else:
        # Score each component type separately
        component_results = {}
        total_prices = {"best_match": 0, "best_brand": 0, "budget_pick": 0}
        component_budgets = {
            "frame": 0.35,  # 35% of budget
            "fork": 0.15,  # 15% of budget
            "drivetrain": 0.20,  # 20% of budget
            "wheels": 0.15,  # 15% of budget
            "brakes": 0.08,  # 8% of budget
            "accessory": 0.07,  # 7% of budget
        }

        build_best_match = {}
        build_best_brand = {}
        build_budget_pick = {}

        for component_type, budget_ratio in component_budgets.items():
            component_budget = body.budget_max * budget_ratio
            component_budget_min = body.budget_min * budget_ratio

            products = await fetch_products_by_type(
                component_type, component_budget * BEST_BRAND_MULTIPLIER
            )

            if not products:
                # Skip if no components of this type available
                continue

            scored = await score_products(
                products,
                component_budget_min,
                component_budget,
                recommended_size,
                body.riding_style,
            )

            best_match, best_brand, budget_pick = await build_three_tiers(
                scored, component_budget
            )

            if best_match:
                build_best_match[component_type] = {
                    **best_match,
                    "alternatives": await get_alternatives(
                        best_match["id"], component_type
                    ),
                }
                total_prices["best_match"] += best_match["price"]

            if best_brand:
                build_best_brand[component_type] = {
                    **best_brand,
                    "alternatives": await get_alternatives(
                        best_brand["id"], component_type
                    ),
                }
                total_prices["best_brand"] += best_brand["price"]

            if budget_pick:
                build_budget_pick[component_type] = {
                    **budget_pick,
                    "alternatives": await get_alternatives(
                        budget_pick["id"], component_type
                    ),
                }
                total_prices["budget_pick"] += budget_pick["price"]

        if not build_best_match and not build_best_brand and not build_budget_pick:
            raise HTTPException(
                status_code=404,
                detail="Not enough components available to build a bike. Please check back later.",
            )

        results = {}

        if build_best_match:
            results["best_match"] = {
                "label": "Best Match Build",
                "badge": "green",
                "description": "Best scoring components within your budget",
                "components": build_best_match,
                "total_price": round(total_prices["best_match"], 2),
                "component_count": len(build_best_match),
            }

        if build_best_brand:
            results["best_brand"] = {
                "label": "Best Brand Build",
                "badge": "purple",
                "description": "Highest quality components near your budget",
                "components": build_best_brand,
                "total_price": round(total_prices["best_brand"], 2),
                "component_count": len(build_best_brand),
            }

        if build_budget_pick:
            results["budget_pick"] = {
                "label": "Budget Build",
                "badge": "amber",
                "description": "Most affordable complete build",
                "components": build_budget_pick,
                "total_price": round(total_prices["budget_pick"], 2),
                "component_count": len(build_budget_pick),
            }

        return {
            "mode": "custom_build",
            "recommended_size": recommended_size,
            "height_cm": body.height_cm,
            "budget_min": body.budget_min,
            "budget_max": body.budget_max,
            "riding_style": body.riding_style,
            "results": results,
        }


@router.get("/frame-size")
async def get_frame_size(height_cm: float):
    if height_cm < 100 or height_cm > 250:
        raise HTTPException(
            status_code=400, detail="Height must be between 100 and 250 cm"
        )
    size = await get_recommended_size(height_cm)
    products = await database.fetch_all(
        """
        SELECT p.id, p.name, p.price, p.frame_size, b.name as brand_name
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.frame_size = :size
        AND p.is_active = TRUE
        AND p.stock_quantity > 0
        ORDER BY p.price ASC
        """,
        {"size": size},
    )
    return {
        "height_cm": height_cm,
        "recommended_size": size,
        "matching_products": [dict(row) for row in products],
    }


@router.get("/compatibility")
async def check_compatibility(part1_category: str, part2_category: str):
    row = await database.fetch_one(
        """
        SELECT is_compatible, condition_note
        FROM compatibility_matrix
        WHERE (row_item = :part1 AND col_item = :part2)
        OR (row_item = :part2 AND col_item = :part1)
        LIMIT 1
        """,
        {"part1": part1_category, "part2": part2_category},
    )
    if not row:
        return {
            "is_compatible": "unknown",
            "condition_note": "No compatibility data for these parts.",
        }
    return {
        "part1": part1_category,
        "part2": part2_category,
        "is_compatible": row["is_compatible"],
        "condition_note": row["condition_note"],
    }


@router.get("/components")
async def get_available_components():
    """Returns all available component types and counts — useful for the frontend."""
    results = {}
    for component_type in COMPONENT_TYPES:
        count = await database.fetch_one(
            """
            SELECT COUNT(*) as count FROM products
            WHERE component_type = :type
            AND is_active = TRUE AND stock_quantity > 0
            """,
            {"type": component_type},
        )
        results[component_type] = count["count"]
    return {"available_components": results}
