from django.db import migrations

INSTITUTIONS = [
    {
        "name": "Uluk-Ata",
        "description": "Традиционные блюда, приготовленные по старинным рецептам.",
        "delivery_time": 30,
        "delivery_price": "100 сом",
    },
    {
        "name": "Soima",
        "description": "Кафе Soima в городе Ош.",
        "delivery_time": 30,
        "delivery_price": "100 сом",
    },
]

# Tabs per institution (brand sub-tabs from mobile mockups).
TABS = {
    "Uluk-Ata": [
        ("Uluk-Ata", "Кафе Улук-Ата"),
        ("Бука Стейк Хаус", "Стейки на углях"),
    ],
    "Soima": [
        ("Soima", "Кафе Soima"),
    ],
}

# Category filter tabs from mobile mockups ("Все" is virtual, not stored).
CATEGORIES = ["Бургеры", "Выпечка", "Гарниры", "Горячее", "Десерты"]

# Example dishes visible on screenshots: (name, description, price, category, tab).
DISHES = [
    (
        "Блэк бургер",
        "Оригинальный бургер на черной булочке с говяжьей котлетой.",
        380,
        "Бургеры",
        "Uluk-Ata",
    ),
    (
        "Бургер с двумя котлетами",
        "Двойная говяжья котлета, сыр, овощи.",
        480,
        "Бургеры",
        "Uluk-Ata",
    ),
    (
        "Классический бургер",
        "Классический бургер с говяжьей котлетой.",
        360,
        "Бургеры",
        "Uluk-Ata",
    ),
    (
        "Алатская самса с мясом",
        "Традиционная алатская самса из тонкого теста.",
        50,
        "Выпечка",
        "Uluk-Ata",
    ),
    ("Боорсок", "Боорсок — традиционная выпечка.", 350, "Выпечка", "Uluk-Ata"),
    ("Картофель фри", "Хрустящий картофель фри.", 150, "Гарниры", "Uluk-Ata"),
    ("Айрим сай", "Фирменное блюдо.", 250, "Горячее", "Uluk-Ata"),
    (
        "Блэк бургер",
        "Блэк бургер в Бука Стейк Хаус.",
        380,
        "Бургеры",
        "Бука Стейк Хаус",
    ),
]


def seed_forward(apps, schema_editor):
    Institution = apps.get_model("Restaurant", "Institution")
    EstablishmentTab = apps.get_model("Restaurant", "EstablishmentTab")
    Category = apps.get_model("Restaurant", "Category")
    Dish = apps.get_model("Restaurant", "Dish")

    for inst in INSTITUTIONS:
        Institution.objects.get_or_create(
            name=inst["name"],
            defaults={
                "description": inst["description"],
                "delivery_time": inst["delivery_time"],
                "delivery_price": inst["delivery_price"],
            },
        )

    for inst_name, tabs in TABS.items():
        try:
            institution = Institution.objects.get(name=inst_name)
        except Institution.DoesNotExist:
            continue
        for tab_name, tab_desc in tabs:
            tab, _ = EstablishmentTab.objects.get_or_create(
                name=tab_name,
                institution=institution,
                defaults={"description": tab_desc},
            )
            for cat_name in CATEGORIES:
                Category.objects.get_or_create(
                    name=cat_name,
                    tab=tab,
                    defaults={"description": cat_name},
                )

    for name, desc, price, cat_name, tab_name in DISHES:
        tab = EstablishmentTab.objects.filter(name=tab_name).first()
        if not tab:
            continue
        category = Category.objects.filter(name=cat_name, tab=tab).first()
        if not category:
            continue
        if not Dish.objects.filter(name=name, category=category).exists():
            Dish.objects.create(
                name=name,
                description=desc,
                price=price,
                category=category,
                cooking_time=20,
            )


def seed_reverse(apps, schema_editor):
    Institution = apps.get_model("Restaurant", "Institution")
    EstablishmentTab = apps.get_model("Restaurant", "EstablishmentTab")
    Category = apps.get_model("Restaurant", "Category")
    Dish = apps.get_model("Restaurant", "Dish")
    Dish.objects.filter(name__in=[d[0] for d in DISHES]).delete()
    Category.objects.filter(name__in=CATEGORIES).delete()
    for tabs in TABS.values():
        for tab_name, _ in tabs:
            EstablishmentTab.objects.filter(name=tab_name).delete()
    Institution.objects.filter(name__in=[i["name"] for i in INSTITUTIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("Restaurant", "0002_alter_cart_options_alter_cartitem_options_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
