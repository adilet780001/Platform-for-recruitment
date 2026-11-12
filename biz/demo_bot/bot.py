"""Демо AI-администратор: FAQ + запись + уведомление админа. Бесплатно (Telegram Bot API).

Запуск:  BOT_TOKEN=... python bot.py   (токен от @BotFather)
Админ:   напишите боту /admin — бот покажет ваш chat_id, впишите его в config.json.
"""
import csv, json, os, re
from datetime import datetime
from pathlib import Path
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

HERE = Path(__file__).parent
CFG = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
SERVICE, WHEN, PHONE = range(3)
PHONE_RE = re.compile(r"^\+?[78]\d{10}$")


def main_kb():
    rows = [[k] for k in CFG["faq"]] + [[CFG["booking_button"]]]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def normalize_phone(text: str) -> str | None:
    digits = re.sub(r"[^\d+]", "", text)
    return digits if PHONE_RE.match(digits) else None


def save_booking(row: dict, path: Path = HERE / "bookings.csv") -> None:
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)


async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text(CFG["greeting"], reply_markup=main_kb())


async def admin(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text(f"Ваш chat_id: {u.effective_chat.id} — впишите в config.json → admin_chat_id")


async def faq(u: Update, c: ContextTypes.DEFAULT_TYPE):
    answer = CFG["faq"].get(u.message.text)
    if answer:
        await u.message.reply_text(answer, reply_markup=main_kb())
    else:
        await u.message.reply_text("Не нашёл ответ 🙏 Нажмите «Записаться» — администратор свяжется с вами.",
                                   reply_markup=main_kb())


async def book_start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    kb = ReplyKeyboardMarkup([[s] for s in CFG["services"]], resize_keyboard=True, one_time_keyboard=True)
    await u.message.reply_text("На какую услугу записать?", reply_markup=kb)
    return SERVICE


async def book_service(u: Update, c: ContextTypes.DEFAULT_TYPE):
    c.user_data["service"] = u.message.text
    await u.message.reply_text("Когда удобно? Например: «завтра после 18:00»")
    return WHEN


async def book_when(u: Update, c: ContextTypes.DEFAULT_TYPE):
    c.user_data["when"] = u.message.text
    await u.message.reply_text("Оставьте номер телефона (например +77011234567):")
    return PHONE


async def book_phone(u: Update, c: ContextTypes.DEFAULT_TYPE):
    phone = normalize_phone(u.message.text)
    if not phone:
        await u.message.reply_text("Похоже, номер с ошибкой. Пример: +77011234567")
        return PHONE
    row = {"created": datetime.now().isoformat(timespec="minutes"),
           "name": u.effective_user.full_name, "username": u.effective_user.username or "",
           "service": c.user_data["service"], "when": c.user_data["when"], "phone": phone}
    save_booking(row)
    if CFG.get("admin_chat_id"):
        await c.bot.send_message(CFG["admin_chat_id"],
                                 "🔔 Новая заявка\n" + "\n".join(f"{k}: {v}" for k, v in row.items()))
    await u.message.reply_text("✅ Готово! Администратор подтвердит время в ближайшее время.",
                               reply_markup=main_kb())
    return ConversationHandler.END


async def cancel(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("Отменено.", reply_markup=main_kb())
    return ConversationHandler.END


def build_app(token: str) -> Application:
    app = Application.builder().token(token).build()
    txt = filters.TEXT & ~filters.COMMAND
    app.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(f"^{re.escape(CFG['booking_button'])}$"), book_start)],
        states={SERVICE: [MessageHandler(txt, book_service)],
                WHEN: [MessageHandler(txt, book_when)],
                PHONE: [MessageHandler(txt, book_phone)]},
        fallbacks=[CommandHandler("cancel", cancel)]))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(txt, faq))
    return app


if __name__ == "__main__":
    build_app(os.environ["BOT_TOKEN"]).run_polling()
