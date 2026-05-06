import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import database


async def seed():
    await database.connect()
    print("🌱 Starting seed...")

    # --- BRANDS ---
    print("Adding brands...")
    brands = [
        (
            "Trek",
            1,
            "complete_bike",
            "Global Tier 1 brand, widely available in PH",
            "low",
        ),
        ("Giant", 1, "complete_bike", "Global Tier 1 brand, strong PH presence", "low"),
        ("Specialized", 1, "complete_bike", "Premium global brand", "low"),
        ("Merida", 2, "complete_bike", "Mid-high tier, good PH availability", "low"),
        ("Scott", 2, "complete_bike", "Mid-high tier European brand", "low"),
        ("Trinx", 3, "complete_bike", "Budget brand, very common in PH", "low"),
        ("Mountainpeak", 3, "complete_bike", "PH local budget brand", "low"),
        ("Shimano", 1, "drivetrain", "Industry standard drivetrain components", "low"),
        ("Sram", 1, "drivetrain", "Premium drivetrain components", "low"),
        ("Rockshox", 1, "fork", "Premium suspension brand", "low"),
        ("Manitou", 2, "fork", "Mid-tier suspension brand", "low"),
        ("LTWOO", 2, "drivetrain", "Mid-tier Chinese drivetrain", "low"),
        ("Tektro", 2, "brakes", "Reliable mid-tier brake brand", "low"),
        ("Toseek", 3, "components", "Budget components", "medium"),
        ("WTB", 2, "wheels", "Mid-tier wheel brand", "low"),
        ("Maxxis", 1, "wheels", "Premium tire brand", "low"),
    ]

    for brand in brands:
        await database.execute(
            """
            INSERT INTO brands (name, tier, category, reason, counterfeit_risk)
            VALUES (:name, :tier, :category, :reason, :counterfeit_risk)
            ON CONFLICT (name) DO NOTHING
            """,
            {
                "name": brand[0],
                "tier": brand[1],
                "category": brand[2],
                "reason": brand[3],
                "counterfeit_risk": brand[4],
            },
        )

    # Get brand IDs
    def get_brand_id(name):
        return database.fetch_one(f"SELECT id FROM brands WHERE name = '{name}'")

    trek_id = (await database.fetch_one("SELECT id FROM brands WHERE name = 'Trek'"))[
        "id"
    ]
    giant_id = (await database.fetch_one("SELECT id FROM brands WHERE name = 'Giant'"))[
        "id"
    ]
    specialized_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Specialized'")
    )["id"]
    merida_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Merida'")
    )["id"]
    trinx_id = (await database.fetch_one("SELECT id FROM brands WHERE name = 'Trinx'"))[
        "id"
    ]
    mountainpeak_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Mountainpeak'")
    )["id"]
    scott_id = (await database.fetch_one("SELECT id FROM brands WHERE name = 'Scott'"))[
        "id"
    ]
    shimano_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Shimano'")
    )["id"]
    sram_id = (await database.fetch_one("SELECT id FROM brands WHERE name = 'Sram'"))[
        "id"
    ]
    rockshox_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Rockshox'")
    )["id"]
    manitou_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Manitou'")
    )["id"]
    ltwoo_id = (await database.fetch_one("SELECT id FROM brands WHERE name = 'LTWOO'"))[
        "id"
    ]
    tektro_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Tektro'")
    )["id"]
    toseek_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Toseek'")
    )["id"]
    wtb_id = (await database.fetch_one("SELECT id FROM brands WHERE name = 'WTB'"))[
        "id"
    ]
    maxxis_id = (
        await database.fetch_one("SELECT id FROM brands WHERE name = 'Maxxis'")
    )["id"]

    # Clear existing products
    await database.execute("DELETE FROM order_items")
    await database.execute("DELETE FROM cart_items")
    await database.execute("DELETE FROM wishlist_items")
    await database.execute("DELETE FROM products")
    print("Cleared existing products...")

    print("Adding complete bikes...")
    complete_bikes = [
        # Road / Fitness Bikes
        {
            "name": "Trek FX 3 Disc",
            "price": 45000,
            "stock_quantity": 8,
            "low_stock_threshold": 3,
            "brand_id": trek_id,
            "category": "road_bike",
            "riding_style": "fitness",
            "frame_size": "S",
            "component_type": "complete_bike",
            "description": "Fast fitness bike with disc brakes. Shimano 24-speed.",
        },
        {
            "name": "Trek FX 3 Disc",
            "price": 45000,
            "stock_quantity": 6,
            "low_stock_threshold": 3,
            "brand_id": trek_id,
            "category": "road_bike",
            "riding_style": "fitness",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "Fast fitness bike with disc brakes. Shimano 24-speed.",
        },
        {
            "name": "Trek FX 3 Disc",
            "price": 45000,
            "stock_quantity": 4,
            "low_stock_threshold": 3,
            "brand_id": trek_id,
            "category": "road_bike",
            "riding_style": "fitness",
            "frame_size": "L",
            "component_type": "complete_bike",
            "description": "Fast fitness bike with disc brakes. Shimano 24-speed.",
        },
        {
            "name": "Giant Contend 3",
            "price": 38000,
            "stock_quantity": 6,
            "low_stock_threshold": 2,
            "brand_id": giant_id,
            "category": "road_bike",
            "riding_style": "road",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "Entry-level road bike. Great for beginners.",
        },
        {
            "name": "Giant Contend 3",
            "price": 38000,
            "stock_quantity": 4,
            "low_stock_threshold": 2,
            "brand_id": giant_id,
            "category": "road_bike",
            "riding_style": "road",
            "frame_size": "L",
            "component_type": "complete_bike",
            "description": "Entry-level road bike. Great for beginners.",
        },
        {
            "name": "Specialized Sirrus 3.0",
            "price": 55000,
            "stock_quantity": 3,
            "low_stock_threshold": 2,
            "brand_id": specialized_id,
            "category": "road_bike",
            "riding_style": "fitness",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "Premium fitness bike with hydraulic disc brakes.",
        },
        # Mountain Bikes
        {
            "name": "Merida Big Nine 20",
            "price": 32000,
            "stock_quantity": 7,
            "low_stock_threshold": 3,
            "brand_id": merida_id,
            "category": "mountain_bike",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "XC mountain bike with 29-inch wheels. Shimano 21-speed.",
        },
        {
            "name": "Merida Big Nine 20",
            "price": 32000,
            "stock_quantity": 5,
            "low_stock_threshold": 3,
            "brand_id": merida_id,
            "category": "mountain_bike",
            "riding_style": "mountain",
            "frame_size": "L",
            "component_type": "complete_bike",
            "description": "XC mountain bike with 29-inch wheels. Shimano 21-speed.",
        },
        {
            "name": "Scott Aspect 950",
            "price": 28000,
            "stock_quantity": 5,
            "low_stock_threshold": 2,
            "brand_id": scott_id,
            "category": "mountain_bike",
            "riding_style": "trail",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "Trail mountain bike with Manitou fork. Great for beginners.",
        },
        {
            "name": "Trinx M100",
            "price": 8500,
            "stock_quantity": 15,
            "low_stock_threshold": 5,
            "brand_id": trinx_id,
            "category": "mountain_bike",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "Budget mountain bike. Perfect for beginners.",
        },
        {
            "name": "Trinx M100",
            "price": 8500,
            "stock_quantity": 10,
            "low_stock_threshold": 5,
            "brand_id": trinx_id,
            "category": "mountain_bike",
            "riding_style": "mountain",
            "frame_size": "S",
            "component_type": "complete_bike",
            "description": "Budget mountain bike. Perfect for beginners.",
        },
        {
            "name": "Mountainpeak Explorer 26",
            "price": 6500,
            "stock_quantity": 20,
            "low_stock_threshold": 5,
            "brand_id": mountainpeak_id,
            "category": "mountain_bike",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "Entry level PH local brand mountain bike.",
        },
        # Hybrid/All-Around
        {
            "name": "Giant Escape 3",
            "price": 25000,
            "stock_quantity": 10,
            "low_stock_threshold": 3,
            "brand_id": giant_id,
            "category": "hybrid_bike",
            "riding_style": "versatile",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "All-around hybrid bike for commuting and fitness.",
        },
        {
            "name": "Giant Escape 3",
            "price": 25000,
            "stock_quantity": 7,
            "low_stock_threshold": 3,
            "brand_id": giant_id,
            "category": "hybrid_bike",
            "riding_style": "versatile",
            "frame_size": "L",
            "component_type": "complete_bike",
            "description": "All-around hybrid bike for commuting and fitness.",
        },
        {
            "name": "Trek Marlin 5",
            "price": 35000,
            "stock_quantity": 6,
            "low_stock_threshold": 2,
            "brand_id": trek_id,
            "category": "mountain_bike",
            "riding_style": "all-around",
            "frame_size": "M",
            "component_type": "complete_bike",
            "description": "Versatile mountain bike for trails and daily rides.",
        },
        {
            "name": "Trek Marlin 5",
            "price": 35000,
            "stock_quantity": 4,
            "low_stock_threshold": 2,
            "brand_id": trek_id,
            "category": "mountain_bike",
            "riding_style": "all-around",
            "frame_size": "L",
            "component_type": "complete_bike",
            "description": "Versatile mountain bike for trails and daily rides.",
        },
    ]

    print("Adding frames...")
    frames = [
        {
            "name": "Trek Marlin Aluminum Frame",
            "price": 12000,
            "stock_quantity": 5,
            "low_stock_threshold": 2,
            "brand_id": trek_id,
            "category": "frame",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "frame",
            "description": "Lightweight Alpha Gold aluminum frame. 29-inch compatible.",
        },
        {
            "name": "Trek Marlin Aluminum Frame",
            "price": 12000,
            "stock_quantity": 4,
            "low_stock_threshold": 2,
            "brand_id": trek_id,
            "category": "frame",
            "riding_style": "mountain",
            "frame_size": "L",
            "component_type": "frame",
            "description": "Lightweight Alpha Gold aluminum frame. 29-inch compatible.",
        },
        {
            "name": "Giant ATX Aluminum Frame",
            "price": 9500,
            "stock_quantity": 6,
            "low_stock_threshold": 2,
            "brand_id": giant_id,
            "category": "frame",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "frame",
            "description": "ALUXX aluminum mountain bike frame. 26-inch compatible.",
        },
        {
            "name": "Giant ATX Aluminum Frame",
            "price": 9500,
            "stock_quantity": 4,
            "low_stock_threshold": 2,
            "brand_id": giant_id,
            "category": "frame",
            "riding_style": "mountain",
            "frame_size": "S",
            "component_type": "frame",
            "description": "ALUXX aluminum mountain bike frame. 26-inch compatible.",
        },
        {
            "name": "Trinx MTB Aluminum Frame",
            "price": 3500,
            "stock_quantity": 10,
            "low_stock_threshold": 3,
            "brand_id": trinx_id,
            "category": "frame",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "frame",
            "description": "Budget aluminum mountain bike frame.",
        },
        {
            "name": "Merida Road Aluminum Frame",
            "price": 8000,
            "stock_quantity": 4,
            "low_stock_threshold": 2,
            "brand_id": merida_id,
            "category": "frame",
            "riding_style": "road",
            "frame_size": "M",
            "component_type": "frame",
            "description": "Lightweight road bike aluminum frame.",
        },
    ]

    print("Adding forks...")
    forks = [
        {
            "name": "Rockshox Judy Silver TK",
            "price": 8500,
            "stock_quantity": 5,
            "low_stock_threshold": 2,
            "brand_id": rockshox_id,
            "category": "fork",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "fork",
            "description": "100mm travel air suspension fork. 29-inch. Rebound adjustment.",
        },
        {
            "name": "Manitou Markhor",
            "price": 5500,
            "stock_quantity": 7,
            "low_stock_threshold": 2,
            "brand_id": manitou_id,
            "category": "fork",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "fork",
            "description": "100mm travel coil fork. 26/27.5 inch. Great value.",
        },
        {
            "name": "Toseek Rigid Fork",
            "price": 1200,
            "stock_quantity": 15,
            "low_stock_threshold": 5,
            "brand_id": toseek_id,
            "category": "fork",
            "riding_style": "road",
            "frame_size": "M",
            "component_type": "fork",
            "description": "Budget rigid carbon-look fork. Road/hybrid use.",
        },
    ]

    print("Adding drivetrains...")
    drivetrains = [
        {
            "name": "Shimano Deore M5100 11-Speed",
            "price": 7500,
            "stock_quantity": 8,
            "low_stock_threshold": 3,
            "brand_id": shimano_id,
            "category": "drivetrain",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "drivetrain",
            "description": "11-speed MTB groupset. Shadow Plus rear derailleur. Reliable and smooth.",
        },
        {
            "name": "Shimano Altus M2000 9-Speed",
            "price": 3500,
            "stock_quantity": 12,
            "low_stock_threshold": 4,
            "brand_id": shimano_id,
            "category": "drivetrain",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "drivetrain",
            "description": "9-speed entry MTB groupset. Great value for budget builds.",
        },
        {
            "name": "Shimano Claris R2000 8-Speed",
            "price": 4200,
            "stock_quantity": 8,
            "low_stock_threshold": 3,
            "brand_id": shimano_id,
            "category": "drivetrain",
            "riding_style": "road",
            "frame_size": "M",
            "component_type": "drivetrain",
            "description": "8-speed road groupset. Entry-level road cycling performance.",
        },
        {
            "name": "SRAM SX Eagle 12-Speed",
            "price": 9800,
            "stock_quantity": 4,
            "low_stock_threshold": 2,
            "brand_id": sram_id,
            "category": "drivetrain",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "drivetrain",
            "description": "12-speed 1x drivetrain. Wide range cassette. Trail ready.",
        },
        {
            "name": "LTWOO A5 9-Speed",
            "price": 2800,
            "stock_quantity": 10,
            "low_stock_threshold": 3,
            "brand_id": ltwoo_id,
            "category": "drivetrain",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "drivetrain",
            "description": "Budget 9-speed MTB drivetrain. Good value alternative.",
        },
    ]

    print("Adding wheels...")
    wheels = [
        {
            "name": "WTB ST i25 29-inch Wheelset",
            "price": 5500,
            "stock_quantity": 6,
            "low_stock_threshold": 2,
            "brand_id": wtb_id,
            "category": "wheels",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "wheels",
            "description": "29-inch tubeless-ready wheelset. Strong and lightweight.",
        },
        {
            "name": "Maxxis Ardent 29x2.25 Tire Set",
            "price": 3200,
            "stock_quantity": 10,
            "low_stock_threshold": 3,
            "brand_id": maxxis_id,
            "category": "wheels",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "wheels",
            "description": "29-inch MTB tires. Excellent traction on dirt and gravel.",
        },
        {
            "name": "Generic 26-inch Alloy Wheelset",
            "price": 1800,
            "stock_quantity": 15,
            "low_stock_threshold": 5,
            "brand_id": toseek_id,
            "category": "wheels",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "wheels",
            "description": "Budget 26-inch aluminum wheelset. Good for entry builds.",
        },
    ]

    print("Adding brakes...")
    brakes = [
        {
            "name": "Shimano MT200 Hydraulic Disc Brake Set",
            "price": 3800,
            "stock_quantity": 8,
            "low_stock_threshold": 3,
            "brand_id": shimano_id,
            "category": "brakes",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "brakes",
            "description": "Entry hydraulic disc brakes. Reliable stopping power for trails.",
        },
        {
            "name": "Tektro HD-M275 Hydraulic Disc Set",
            "price": 2800,
            "stock_quantity": 10,
            "low_stock_threshold": 3,
            "brand_id": tektro_id,
            "category": "brakes",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "brakes",
            "description": "Mid-range hydraulic disc brakes. Good value for the price.",
        },
        {
            "name": "Tektro MD-M310 Mechanical Disc Set",
            "price": 1500,
            "stock_quantity": 12,
            "low_stock_threshold": 4,
            "brand_id": tektro_id,
            "category": "brakes",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "brakes",
            "description": "Budget mechanical disc brakes. Good for beginners.",
        },
    ]

    print("Adding accessories...")
    accessories = [
        {
            "name": "WTB Devo Team Saddle",
            "price": 1800,
            "stock_quantity": 10,
            "low_stock_threshold": 3,
            "brand_id": wtb_id,
            "category": "accessories",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "accessory",
            "description": "Comfortable trail saddle with pressure relief channel.",
        },
        {
            "name": "Shimano PD-EF205 Flat Pedals",
            "price": 950,
            "stock_quantity": 15,
            "low_stock_threshold": 4,
            "brand_id": shimano_id,
            "category": "accessories",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "accessory",
            "description": "Wide platform flat pedals. Great grip for trail riding.",
        },
        {
            "name": "Generic MTB Handlebar + Stem Set",
            "price": 1200,
            "stock_quantity": 12,
            "low_stock_threshold": 4,
            "brand_id": toseek_id,
            "category": "accessories",
            "riding_style": "mountain",
            "frame_size": "M",
            "component_type": "accessory",
            "description": "Budget aluminum riser handlebar and stem combo.",
        },
    ]

    # Insert all products
    all_products = (
        complete_bikes + frames + forks + drivetrains + wheels + brakes + accessories
    )
    for product in all_products:
        await database.execute(
            """
            INSERT INTO products
            (name, price, stock_quantity, low_stock_threshold, brand_id,
             category, riding_style, frame_size, component_type, description, image_url)
            VALUES (:name, :price, :stock_quantity, :low_stock_threshold, :brand_id,
             :category, :riding_style, :frame_size, :component_type, :description, :image_url)
            """,
            {**product, "image_url": ""},
        )

    # --- SIZING CHART ---
    print("Adding sizing chart...")
    await database.execute("DELETE FROM sizing_chart")
    sizes = [
        (100, 154, "XS"),
        (155, 164, "S"),
        (165, 174, "M"),
        (175, 184, "L"),
        (185, 194, "XL"),
        (195, 250, "XXL"),
    ]
    for s in sizes:
        await database.execute(
            "INSERT INTO sizing_chart (height_min, height_max, recommended_size) VALUES (:min, :max, :size)",
            {"min": s[0], "max": s[1], "size": s[2]},
        )

    # --- COMPATIBILITY MATRIX ---
    print("Adding compatibility matrix...")
    await database.execute("DELETE FROM compatibility_matrix")
    compatibility = [
        ("29_inch_wheels", "29_inch_frame", "yes", "Standard 29 inch compatibility"),
        ("26_inch_wheels", "26_inch_frame", "yes", "Standard 26 inch compatibility"),
        (
            "26_inch_wheels",
            "29_inch_frame",
            "no",
            "26 inch wheels cannot fit 29 inch frame",
        ),
        (
            "29_inch_wheels",
            "26_inch_frame",
            "no",
            "29 inch wheels too large for 26 inch frame",
        ),
        ("hydraulic_disc", "disc_rotor", "yes", "Hydraulic disc requires disc rotor"),
        ("mechanical_disc", "disc_rotor", "yes", "Mechanical disc requires disc rotor"),
        ("rim_brake", "disc_rotor", "no", "Rim brakes incompatible with disc rotors"),
        (
            "shimano_drivetrain",
            "sram_drivetrain",
            "no",
            "Shimano and SRAM are not cross-compatible",
        ),
        ("mountain_frame", "road_fork", "no", "Mountain frames need suspension forks"),
        (
            "road_frame",
            "suspension_fork",
            "no",
            "Road frames designed for rigid forks only",
        ),
    ]
    for c in compatibility:
        await database.execute(
            """
            INSERT INTO compatibility_matrix
            (matrix_type, row_item, col_item, is_compatible, condition_note)
            VALUES ('parts', :row, :col, :compat, :note)
            """,
            {"row": c[0], "col": c[1], "compat": c[2], "note": c[3]},
        )

    print("✅ Seed complete!")
    print(f"   - {len(brands)} brands")
    print(f"   - {len(complete_bikes)} complete bikes")
    print(f"   - {len(frames)} frames")
    print(f"   - {len(forks)} forks")
    print(f"   - {len(drivetrains)} drivetrains")
    print(f"   - {len(wheels)} wheelsets")
    print(f"   - {len(brakes)} brake sets")
    print(f"   - {len(accessories)} accessories")
    print(f"   - {len(sizes)} sizing entries")
    print(f"   - {len(compatibility)} compatibility rules")

    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(seed())
