from enum import Enum

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

import config


class UState(StatesGroup):
    START = State()
    RAISE_ROI = State()
    PLS_HELP = State()

    BANK = State()
    PSYCHO = State()
    JEWELRY = State()
    TUTORING = State()
    BUILDING = State()

    FOOD = State()
    BEAUTY = State()
    INFOB = State()

    LANDSCAPING = State()


GROUP1 = (UState.BANK, UState.PSYCHO, UState.JEWELRY, UState.TUTORING, UState.BUILDING)
GROUP2 = (UState.FOOD, UState.BEAUTY, UState.INFOB)


class Budget(Enum):
    B10K = "от 10 тыс. до 20 тыс."
    B20K = "от 20 тыс. до 40 тыс."
    B40K = "от 40 тыс. до 60 тыс."
    B60K = "от 60 тыс. до 80 тыс."
    B80K = "от 80 тыс. до 100 тыс."
    B100K = "более 100 тысяч"


class SiteTypes(Enum):
    TAPLINK = "Таплинк"
    BUSINESS = "Сайт-визитка"
    LANDING = "Лендинг"
    MULTIPAGE = "Многостраничный сайт"
    MULTIPAGE_ORDERING = "Многостраничный сайт с возможностью заказа"
    PRINTED_CARD = "Печатные визитки"


class BtnText(Enum):
    BANK = "Финансовая компания/Банк"
    PSYCHO = "Психология"
    JEWELRY = "Украшения/Одежда"
    TUTORING = "Репетиторство"
    BUILDING = "Строительная компания/Услуги по интерьеру"
    FOOD = "Рестораны"
    BEAUTY = "Салоны красоты/мастера"
    INFOB = "Инфобизнес/Школы курсов"
    LANDSCAPING = "Продажа букетов/Озеленение пространств"


class BtnTextMisc(Enum):
    MENU = "Назад"
    KNOW_ROI = "Хочу понять окупаемость сайта"
    PLS_HELP = "Я не понимаю какая услуга мне нужна"


budget_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for _ in Budget:
    budget_keyboard.row(KeyboardButton(_.value))
budget_keyboard.row(KeyboardButton(BtnTextMisc.MENU.value))

niche_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for _ in BtnText:
    niche_keyboard.row(KeyboardButton(_.value))
niche_keyboard.row(KeyboardButton(BtnTextMisc.MENU.value))

exit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
exit_keyboard.row(KeyboardButton("Назад"))

bot = Bot(token=config.TG_TOKEN)

storage = MemoryStorage()  # TODO: Redis
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(Text(equals=("/start", "назад"), ignore_case=True), state="*")
async def start_proc(message: types.Message, state: FSMContext) -> None:
    msg = "Привет, я бот-помощник по дизайну сайтов. Чем вам помочь?"
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton(BtnTextMisc.KNOW_ROI.value))
    keyboard.row(KeyboardButton(BtnTextMisc.PLS_HELP.value))
    await message.answer(msg, reply_markup=keyboard)
    await state.set_state(UState.START.state)


@dp.message_handler(Text(equals=BtnTextMisc.KNOW_ROI.value, ignore_case=True), state=UState.START)
async def raise_roi(message: types.Message, state: FSMContext) -> None:
    msg = "Ваша средняя выручка за месяц?"
    await message.answer(msg, reply_markup=budget_keyboard)
    await state.set_state(UState.RAISE_ROI.state)


@dp.message_handler(Text(equals=BtnTextMisc.PLS_HELP.value, ignore_case=True), state=UState.START)
async def pls_help(message: types.Message, state: FSMContext) -> None:
    msg = "Выберите свою нишу"
    await message.answer(msg, reply_markup=niche_keyboard)
    await state.set_state(UState.PLS_HELP.state)


@dp.message_handler(state=UState.PLS_HELP)
async def choice(message: types.Message, state: FSMContext) -> None:
    usr_msg = message.text
    match usr_msg:
        case BtnText.BANK.value: await state.set_state(UState.BANK.state)
        case BtnText.PSYCHO.value: await state.set_state(UState.PSYCHO.state)
        case BtnText.JEWELRY.value: await state.set_state(UState.JEWELRY.state)
        case BtnText.TUTORING.value: await state.set_state(UState.TUTORING.state)
        case BtnText.BUILDING.value: await state.set_state(UState.BUILDING.state)
        case BtnText.FOOD.value: await state.set_state(UState.FOOD.state)
        case BtnText.BEAUTY.value: await state.set_state(UState.BEAUTY.state)
        case BtnText.INFOB.value: await state.set_state(UState.INFOB.state)
        case BtnText.LANDSCAPING.value: await state.set_state(UState.LANDSCAPING.state)
    msg = "Ваша средняя выручка за месяц?"
    await message.answer(msg, reply_markup=budget_keyboard)


@dp.message_handler(state=GROUP1)
async def group1(message: types.Message, state: FSMContext) -> None:
    usr_msg = message.text.lower()
    msg = "Ваш выбор — "
    match usr_msg:
        case Budget.B10K.value: msg += SiteTypes.TAPLINK.value
        case Budget.B20K.value: msg += SiteTypes.BUSINESS.value
        case Budget.B40K.value: msg += SiteTypes.LANDING.value
        case Budget.B60K.value: msg += SiteTypes.MULTIPAGE.value
        case Budget.B80K.value: msg += SiteTypes.MULTIPAGE.value
        case Budget.B100K.value: msg += SiteTypes.MULTIPAGE.value
    await message.answer(msg, reply_markup=exit_keyboard)
    await state.reset_state()


@dp.message_handler(state=GROUP2)
async def group1(message: types.Message, state: FSMContext) -> None:
    usr_msg = message.text.lower()
    msg = "Ваш выбор — "
    match usr_msg:
        case Budget.B10K.value: msg += SiteTypes.PRINTED_CARD.value
        case Budget.B20K.value: msg += SiteTypes.BUSINESS.value
        case Budget.B40K.value: msg += SiteTypes.LANDING.value
        case Budget.B60K.value: msg += SiteTypes.MULTIPAGE.value
        case Budget.B80K.value: msg += SiteTypes.MULTIPAGE_ORDERING.value
        case Budget.B100K.value: msg += SiteTypes.MULTIPAGE_ORDERING.value
    await message.answer(msg, reply_markup=exit_keyboard)
    await state.reset_state()


@dp.message_handler(state=UState.LANDSCAPING)
async def landscape(message: types.Message, state: FSMContext) -> None:
    usr_msg = message.text.lower()
    msg = "Ваш выбор — "
    match usr_msg:
        case Budget.B10K.value: msg += SiteTypes.TAPLINK.value
        case Budget.B20K.value: msg += SiteTypes.TAPLINK.value
        case Budget.B40K.value: msg += SiteTypes.LANDING.value
        case Budget.B60K.value: msg += SiteTypes.MULTIPAGE.value
        case Budget.B80K.value: msg += SiteTypes.MULTIPAGE_ORDERING.value
        case Budget.B100K.value: msg += SiteTypes.MULTIPAGE_ORDERING.value
    await message.answer(msg, reply_markup=exit_keyboard)
    await state.reset_state()


@dp.message_handler(state=UState.RAISE_ROI)
async def raise_roi_final(message: types.Message, state: FSMContext) -> None:
    usr_msg = message.text.lower()
    msg = "Окупаемость среднестатистического сайта — "
    match usr_msg:
        case Budget.B10K.value: msg += "4,5 месяца"
        case Budget.B20K.value: msg += "3 месяца"
        case Budget.B40K.value: msg += "1 месяц"
        case Budget.B60K.value: msg += "25 дней"
        case Budget.B80K.value: msg += "18 дней"
        case Budget.B100K.value: msg += "12 дней"
    await message.answer(msg, reply_markup=exit_keyboard)
    await state.set_state(UState.RAISE_ROI.state)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
