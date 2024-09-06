from random import randint, shuffle


QUANTITY_OF_EACH_ITEM = 1

businessBrands = [
    "Briony",
    "Corneliani",
    "Hugo Boss",
    "Canali",
]

everydayBrands = [
    "H&M",
    "Zara",
    "Levi's",
    "Lacoste",
]

sportsBrands = [
    "Nike",
    "Adidas",
    "Puma",
    "Reebok"
]

sizes = [
    "S", "M", "L", "XL", "XXL"
]

colors = [
    "Белый",
    "Черный",
    "Серый",
    "Синий",
    "Голубой",
    "Красный",
    "Розовый"
]


def generateClothes(
        category: str, 
        brands: list[str],
        minPrice: int,
        maxPrice: int,
        hierarchy: str,
        genderDefault: str | None = None,
    ) -> list[str]:
    clothes = []

    for _ in range(QUANTITY_OF_EACH_ITEM):
        for brand in brands:
            while True:
                if not genderDefault:
                    gender = "м" if randint(0, 1) else "ж"
                else:
                    gender = genderDefault

                color = colors[randint(0, len(colors) - 1)]
                price = randint(minPrice, maxPrice) // 100 * 100
                size = sizes[randint(0, len(sizes) - 1)]
                name = f"{category} {brand}"
                
                item = f"{name};{gender};{color};{price};{size};{brand};{hierarchy}\n"
                if not item in clothes:
                    clothes.append(item)
                    break
        
    return clothes


if __name__ == "__main__":
    f = open('./data2.csv', 'w')

    clothes = []
    clothes.extend(generateClothes(
        category="Пиджак",
        brands=businessBrands,
        minPrice=10000,
        maxPrice=18000,
        hierarchy="Деловая одежда,Пиджаки"   
    ))

    clothes.extend(generateClothes(
        category="Брюки",
        brands=businessBrands,
        minPrice=7000,
        maxPrice=15000,
        hierarchy="Деловая одежда,Брюки"
    ))

    clothes.extend(generateClothes(
        category="Рубашка с коротким рукавом",
        brands=businessBrands,
        minPrice=2000,
        maxPrice=6000,
        hierarchy="Деловая одежда,Рубашки,Рубашки с коротким рукавом"
    ))

    clothes.extend(generateClothes(
        category="Рубашка с длинным рукавом",
        brands=businessBrands,
        minPrice=2000,
        maxPrice=6000,
        hierarchy="Деловая одежда,Рубашки,Рубашки с длинным рукавом"
    ))

    clothes.extend(generateClothes(
        category="Спортивная футболка",
        brands=sportsBrands,
        minPrice=1700,
        maxPrice=4000,
        hierarchy="Спортивная одежда,Спортивные футболки"
    ))

    clothes.extend(generateClothes(
        category="Спортивные шорты",
        brands=sportsBrands,
        minPrice=3300,
        maxPrice=4700,
        hierarchy="Спортивная одежда,Спортивные шорты"
    ))

    clothes.extend(generateClothes(
        category="Спортивные классические брюки",
        brands=sportsBrands,
        minPrice=4100,
        maxPrice=8200,
        hierarchy="Спортивная одежда,Спортивные брюки,Спортивные классические брюки"
    ))

    clothes.extend(generateClothes(
        category="Джоггеры",
        brands=sportsBrands,
        minPrice=3800,
        maxPrice=7900,
        hierarchy="Спортивная одежда,Спортивные брюки,Джоггеры"
    ))

    clothes.extend(generateClothes(
        category="Тайцы",
        brands=sportsBrands,
        minPrice=3200,
        maxPrice=5800,
        genderDefault="м",
        hierarchy="Спортивная одежда,Спортивные брюки,Тайцы"
    ))

    clothes.extend(generateClothes(
        category="Спортивная толстовка",
        brands=sportsBrands,
        minPrice=3500,
        maxPrice=6300,
        hierarchy="Спортивная одежда,Спортивные толстовки"
    ))

    clothes.extend(generateClothes(
        category="Свитшот",
        brands=everydayBrands,
        minPrice=1000,
        maxPrice=3000,
        hierarchy="Повседневная одежда,Свитеры и кофты,Свитшоты"
    ))

    clothes.extend(generateClothes(
        category="Худи",
        brands=everydayBrands,
        minPrice=1000,
        maxPrice=3000,
        hierarchy="Повседневная одежда,Свитеры и кофты,Худи"
    ))

    clothes.extend(generateClothes(
        category="Толстовка",
        brands=everydayBrands,
        minPrice=1000,
        maxPrice=3000,
        hierarchy="Повседневная одежда,Свитеры и кофты,Толстовки"
    ))

    clothes.extend(generateClothes(
        category="Футболка",
        brands=everydayBrands,
        minPrice=700,
        maxPrice=2500,
        hierarchy="Повседневная одежда,Футболки"
    ))

    clothes.extend(generateClothes(
        category="Лонгслив",
        brands=everydayBrands,
        minPrice=1300,
        maxPrice=2800,
        hierarchy="Повседневная одежда,Лонгсливы"
    ))

    clothes.extend(generateClothes(
        category="Джинсы",
        brands=everydayBrands,
        minPrice=3000,
        maxPrice=18000,
        hierarchy="Повседневная одежда,Джинсы"
    ))

    clothes.extend(generateClothes(
        category="Шорты",
        brands=everydayBrands,
        minPrice=1500,
        maxPrice=4000,
        hierarchy="Повседневная одежда,Шорты"
    ))

    shuffle(clothes)
    clothes.insert(0, "Название;Пол;Цвет;Цена;Размер;Бренд;Иерархия\n")
    for item in clothes:
        f.write(item)
    
    f.close()
