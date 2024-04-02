from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler

import os
from dotenv import load_dotenv
load_dotenv()

from ristocloud import Canteen, MenuType, Dish

CANTEEN_URL = "https://unitrieste.compasscloud.it/"
canteen = Canteen(CANTEEN_URL)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  menus: list[MenuType] = canteen.get_menus()
  keyboard = [
    [
      # InlineKeyboardButton(menu.name, callback_data=f"menu_{menu._id}")
      InlineKeyboardButton(menu.name, web_app=WebAppInfo(url="http://192.168.1.20:3000/menu_webapp.html"),)
    ] for menu in menus
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await update.message.reply_text("Select a menu", reply_markup=reply_markup)

async def menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  await query.answer()
  
  parts = query.data.split("_")
  menus: list[MenuType] = canteen.get_menus()
  try:
    menu_id = int(parts[1])
    meal_type_id = int(parts[2]) if len(parts) > 2 else None
    chosen_menu = next(filter(lambda m: m._id == menu_id, menus))
  except Exception as e:
    await query.message.reply_text("No such menu.")
    return

  if not meal_type_id and len(chosen_menu.meal_types) > 1:
    await query.message.reply_text("Please select a meal type.", reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            mt.name, 
            callback_data=f"menu_{menu_id}_{mt._id}"
          ) for mt in chosen_menu.meal_types
        ]
      ]
    ))
  else:
    dishes: list[Dish] = chosen_menu.get_dishes(meal_type_id=meal_type_id)
    await query.message.reply_markdown_v2(
      "\n".join([f"\U0001F35D • {dish.name}" for dish in dishes])
    )
  

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  pass

app = Application.builder().token(os.environ["TELEGRAM_BOT_API_KEY"]).build()
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(menu_button, "menu_.*"))
app.add_handler(MessageHandler(None, message))
app.run_polling(allowed_updates=Update.ALL_TYPES)