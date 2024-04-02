import requests
from datetime import date
from dataclasses import dataclass

@dataclass
class MealType:
  name: str
  _id: int
  slug: str

@dataclass
class Allergen:
  _id: int
  name: str
  short: str
  image_url: str
  svg_url: str
  _type: str

@dataclass
class DishType:
  _id: int
  name: str
  code: str

@dataclass
class Dish:
  _id: int
  _type: DishType
  name: str
  short: str
  image_url: str
  thumb_url: str
  major_allergens: list[Allergen]
  trace_allergens: list[Allergen]
  calories: str

@dataclass
class MenuType:
  canteen_url: str
  name: str
  short: str
  _id: int
  description: str
  visible: bool
  active: bool
  meal_types: list[MealType]

  def get_dishes(self, meal_type_id: int = None, menu_date=None) -> list[Dish]:
    if not meal_type_id:
      if len(self.meal_types) > 1:
        raise RuntimeError("meal_type_id is required if more than one meal_type is available")
      meal_type_id = self.meal_types[0]._id
    if not menu_date:
      menu_date = date.today().strftime("%Y-%m-%d")
    try:
      d = requests.post(f"{self.canteen_url}/dishes", data={
        "id": self._id,
        "lang": "it",
        "mealTypeId": meal_type_id,
        "startingDate": menu_date,
        "endingDate": menu_date
      }).json()
    except Exception as e:
      print(e)
      return []
    meal_type_idx = d["data"]["Dates"][menu_date]["MealTypes"].index(
      [mt for mt in d["data"]["Dates"][menu_date]["MealTypes"] if mt["ID"] == meal_type_id][0]
    )
    return [Dish(
      _id=dish["ID"],
      name=dish["Name"],
      short=dish["ShortName"],
      _type=DishType(
        _id=dt["ID"],
        name=dt["Name"],
        code=dt["Code"]
      ),
      image_url=dish["Image"]["URL"],
      thumb_url=dish["Image"]["Thumb"],
      major_allergens=[Allergen(
        _id=allergen["ID"],
        name=allergen["Name"],
        short=allergen["ShortName"],
        image_url=allergen["Image"]["URL"],
        svg_url=allergen["Image"]["URL-SVG"],
        _type=allergen["Type"]
      ) for allergen in dish["MajorAllergens"]],
      trace_allergens=[Allergen(
        _id=allergen["ID"],
        name=allergen["Name"],
        short=allergen["ShortName"],
        image_url=allergen["Image"]["URL"],
        svg_url=allergen["Image"]["URL-SVG"],
        _type=allergen["Type"]
      ) for allergen in dish["TraceAllergens"]],
      calories=dish["CaloricIcon"]["Description"]
    ) for dt, dishes in [(dt, dt["Dishes"]) for dt in d["data"]["Dates"][menu_date]["MealTypes"][meal_type_idx]["DishTypes"]] for dish in dishes]

class Canteen:
  def __init__(self, url):
    self._base_url = url + ("" if url.endswith("/") else "/") + "api/public/v1/menu/get"

  def get_menus(self) -> list[MenuType]:
    try:
      f = requests.get(f"{self._base_url}/frontend")
    except Exception as e:
      print(e)
      return []
    return [MenuType(
      canteen_url=self._base_url,
      name=menu["Name"],
      short=menu["ShortName"],
      _id=menu["ID"],
      description=menu["Description"],
      visible=menu["Visible"],
      active=menu["Active"],
      meal_types=[MealType(
        name=mt["Name"],
        _id=mt["ID"],
        slug=mt["ShortName"]
      ) for mt in menu["extendedMealTypes"]]
    ) for menu in f.json()["data"]["Menus"]]