import json
import time
import os


USER_FILE = "users.json"
PRODUCT_FILE = "products.json"


def read_json(filename, default=None):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default or []

def write_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def login():
    users = read_json(USER_FILE)
    username = input("Istifadəçi adi: ").strip()
    for user in users:
        if user["username"] == username:
            for tries in range(3):
                password = input("Parol: ").strip()
                if password == user["password"]:
                    print("✅ Giriş uğurlu!")
                    return username
                else:
                    print("❌ Yanlış parol.")
            print("⏳ 3 səhv cəhd. 10 saniyə gözləyin.")
            for i in range(10, 0, -1):
                print(f"Gözləyin... {i}", end="\r")
                time.sleep(1)
            print()
            return None
    print("❌ İstifadəçi tapılmadı.")
    return None

def show_categories():
    products = read_json(PRODUCT_FILE)
    print("\n--- Kateqoriyalar ---")
    categories = list(products.keys())
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    print("0. Geri")
    choice = input("Seçim: ").strip()
    if choice == "0":
        return None, None
    try:
        idx = int(choice) - 1
        return categories[idx], products[categories[idx]]
    except:
        print("❌ Yanlış seçim.")
        return None, None

def show_products(category, product_list):
    print(f"\n--- {category} ---")
    for p in product_list:
        print(f"{p['id']}. {p['name']} - {p['price']} AZN")
    print("0. Geri")
    prod_id = input("Məhsul ID: ").strip()
    if prod_id == "0":
        return None
    for p in product_list:
        if str(p["id"]) == prod_id:
            return p
    print("❌ Yanlış ID.")
    return None

def add_to_basket(username, product, category):
    qty = input("Miqdar: ").strip()
    if not qty.isdigit() or int(qty) <= 0:
        print("❌ Miqdar müsbət tam ədəd olmalıdır.")
        return
    qty = int(qty)
    item = {
        "category": category,
        "product": product["name"],
        "unit_price": product["price"],
        "qty": qty,
        "total": round(product["price"] * qty, 2)
    }
    basket = read_json(f"basket_{username}.json", [])
    basket.append(item)
    write_json(basket, f"basket_{username}.json")
    print("✅ Səbətə əlavə edildi.")

def show_basket(username):
    basket = read_json(f"basket_{username}.json", [])
    if not basket:
        print("\nSəbət boşdur.")
        return
    print("\n--- Səbətim ---")
    total = 0
    for i, item in enumerate(basket, 1):
        print(f"{i}. {item['product']} x{item['qty']} = {item['total']} AZN")
        total += item["total"]
    print(f"Ümumi: {round(total, 2)} AZN")

    print("\ncheckout | back")
    choice = input("> ").strip().lower()
    if choice == "checkout":
        users = read_json(USER_FILE)
        for user in users:
            if user["username"] == username:
                if user["balance"] >= total:
                    user["balance"] = round(user["balance"] - total, 2)
                    write_json(users, USER_FILE)
                    print("✅ Alış uğurlu!")
                    # Clear basket
                    write_json([], f"basket_{username}.json")
                    # Save purchase
                    purchases = read_json(f"purchases_{username}.json", [])
                    purchases.append({
                        "items": basket,
                        "total": total
                    })
                    write_json(purchases, f"purchases_{username}.json")
                else:
                    print("❌ Balans yetərli deyil.")
                return

def main():
    print("🛒 Mini Mağazaya xoş gəldin!")
    username = login()
    if not username:
        return

    while True:
        print("\n--- Ana Menyu ---")
        print("1. Kateqoriyalar")
        print("2. Səbətim")
        print("3. Balans")
        print("0. Çıxış")
        choice = input("Seçim: ").strip()
        if choice == "1":
            while True:
                cat, prod_list = show_categories()
                if not cat:
                    break
                product = show_products(cat, prod_list)
                if product:
                    add_to_basket(username, product, cat)
        elif choice == "2":
            show_basket(username)
        elif choice == "3":
            users = read_json(USER_FILE)
            for user in users:
                if user["username"] == username:
                    print(f"Balans: {user['balance']} AZN")
        elif choice == "0":
            print("👋 Sağolun!")
            break
        else:
            print("❌ Yanlış seçim.")

if __name__ == "__main__":
    main()