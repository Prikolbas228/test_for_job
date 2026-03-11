import json
import datetime

data = (
    ("Утеплитель Роквул Скандик 50 мм", "Утеплитель", 1075, 1100, 950),
    ("Утеплитель Кнауф ТеплоКНАУФ 50 мм", "Утеплитель", 860, 900, 1300),
    ("Газобетон СК D400 100x250x625 мм", "Газобетон", 450, 430, 420),
    ("Газобетон ЛСР D400 100x250x625 мм", "Газобетон", 580, 550, 580),
    ("Кирпич лицевой пустотелый красный М150", "Кирпич", 75, 78, 70),
    ("Кирпич силикатный белый М150", "Кирпич", 65, 68, 60),
    ("Цемент М500 ПЦ 50 кг", "Цемент", 550, 570, 520),
    ("Цемент М400 ПЦ 50 кг", "Цемент", 500, 520, 480),
    ("Гипсокартон влагостойкий 2500x1200x12.5 мм", "Гипсокартон", 450, 470, 430),
    ("Гипсокартон стандартный 2500x1200x12.5 мм", "Гипсокартон", 400, 420, 390),
    ("Пеноблок D600 200x300x600 мм", "Пеноблок", 120, 125, 115),
    ("Сухая смесь пескобетон М300 40 кг", "Сухие смеси", 280, 300, 260),
)

region_map = {
    1: (2, "СПб"),
    2: (3, "Москва"),
    3: (4, "другой регион"),
}

def check_region():
    while True:
        try:
            region = int(input("здравствуйте, выберете свой регион:\n1: СПБ\n2: Москва\n3: другой регион\n"))
            if region not in region_map:
                print("Ошибка: неправильный номер региона")
            else:
                return region
        except ValueError:
            print("Ошибка: введите, пожалуйста, число 1, 2 или 3")

def show_product(region):
    price_idx, reg_name = region_map[region]
    print(f"\nТовары для региона {reg_name}:\n")

    nomer = 1
    nomer_tovara = {}
    tekushaya_kategoriya = None

    for name, cat, *prices in data:
        if cat != tekushaya_kategoriya:
            tekushaya_kategoriya = cat
            print(f"[ {cat} ]")

        price = prices[price_idx - 2]
        print(f"  {nomer}. {name} — {price} руб.")
        nomer_tovara[nomer] = (name, cat, price)
        nomer += 1

    return nomer_tovara

def sell(category, nomer_tovara):
    min_price = None
    min_name = None
    for item in nomer_tovara.values():
        name, cat, price = item
        if cat == category:
            if min_price is None or price < min_price:
                min_price = price
                min_name = name
    return min_name, min_price

def json_file(region, name, category, price, so_skidkoy=False):
    _, reg_name = region_map[region]
    zayavka = {
        "data_i_vremya": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "region": reg_name,
        "tovar": {
            "nazvanie": name,
            "kategoriya": category,
            "cena": price,
            "skidka_5_procentov": so_skidkoy,
        }
    }

    filename = f"zayavka_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(zayavka, f, ensure_ascii=False, indent=4)

    print(f"\nЗаявка сохранена в файл: {filename}")
    return filename

def choose_product(product, region, nomer_tovara):
    print("\nВыберите товар из списка, чтобы добавить его в заказ:")
    while True:
        try:
            number = int(input(">>> "))
            if number not in product:
                print(f"нет такого номера, введи от 1 до {len(product)}")
                continue

            name, category, price = product[number]
            print(f"Название: {name}")
            print(f"Категория: {category}")
            print(f"Цена: {price} руб.")

            offer = input("будем оформлять заказ?\ny/n\n").strip().lower()

            if offer == "y":
                json_file(region, name, category, price)
                print("спасибо за заказ!")
                return

            elif offer == "n":
                min_name, min_price = sell(category, nomer_tovara)
                if name == min_name:
                    discount_price = round(price * 0.95)
                    print(f"\nЭтот товар уже самый дешевый в категории «{category}».")
                    print(f"Специально для вас — скидка 5%: {discount_price} руб. (вместо {price} руб.)")

                    new_offer = input("\nОформим со скидкой? (y/n)\n>>> ").strip().lower()
                    if new_offer == "y":
                        json_file(region, name, category, discount_price, so_skidkoy=True)
                        print("Отлично, спасибо за заказ!")
                        return
                    else:
                        print("\nХорошо, выберите другой товар:\n")

                else:
                    print(f"\nВ категории «{category}» есть вариант дешевле:")
                    print(f"  {min_name} — {min_price} руб.")

                    new_offer = input("\nОформим с этим товаром? (y/n)\n>>> ").strip().lower()
                    if new_offer == "y":
                        json_file(region, min_name, category, min_price)
                        print("Отлично, спасибо за заказ!")
                        return
                    else:
                        print("\nХорошо, выберите другой товар:\n")

            else:
                print("введи y или n")

        except ValueError:
            print("введи число")


region = check_region()
product = show_product(region)
choose = choose_product(product, region, product)  