from openai import OpenAI
import sqlite3
import random
import re

from chernovik import inventory
from game_db import player_info, save_message, export_message

bot = OpenAI(base_url="https://api.groq.com/openai/v1",api_key= "АПИ_КЕЙ")
def lachuga(id, user_message):
    messages = []
    system_prompt = SYSTEM_PROMPT()
    chat_history = export_message(id)
    for row in chat_history:
        if row["user_message"]:
            messages.append({"role":"user","content":row["user_message"]})
        if row["ai_message"]:
            messages.append({"role":"assistant","content":row["ai_message"]})
    if not chat_history:
        save_message(id, ai_message=system_prompt, role="system")
        messages.append({"role": "system", "content": system_prompt})  # append=добавление
    save_message(chat_id=id, user_message = user_message, role = "user")
    messages.append({"role": "user", "content": user_message})

    try:
        completion = bot.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.7)
        bot_answer = completion.choices[0].message.content
        messages.append({"role": "assistant","content": bot_answer})
        save_message(chat_id=id, ai_message=bot_answer,role="assistant")
        if "Инвентарь: " in bot_answer:
            right_part_hp = bot_answer.split("HP: ")[1]
            hp = right_part_hp.split("\n")[0]
            right_part_exp = bot_answer.split("exp: ")[1]
            exp = right_part_exp.split("\n")[0]
            right_part_gold = bot_answer.split("Gold: ")[1]
            gold = right_part_gold.split("\n")[0]
            right_part_inventory = bot_answer.split("Инвентарь: ")[1]
            inventory = right_part_inventory.split("\n")[0]
            save_message(chat_id=id, ai_message=bot_answer,role="assistant",hp=hp, exp=exp, gold=gold, inventory=inventory)
        return bot_answer
    except Exception as e:
        print(e)
def SYSTEM_PROMPT():
    dice1 = random.randint(1, 20)

    SYSTEM_PROMPT = f"""Ты данжен мастер(ведущий и рассказчик создающий мир управляющий npc и монстрами а 
    также интерпретирующий правила) придумывай на ходу сюжет для партии в DnD. Развивай сюжет ️.
    Дай игроку больше свободы действия в том что он будет делать(НИКОГДА: не говори за него, не решай за него, не помогай ему ни при каких ситуациях) И НИКАКИХ ОТ ТЕБЯ "Ты бросил 20‑гранный кубик и ты делаешь чтото" 
    ИГРОК САМ РЕШАЕТ ЧТО ДЕЛАТЬ А ТЫ КАК МАСТЕР ПОДЗЕМЕЛЬЯ ПОДСТРАИВАЙСЯ ПОД ФАНТАЗИЮ ИГРОКА
    и ожидай от него более менее понятных описаний что он делает(например "загляну под камень(чтобы найти там сокровища)" или "своим ударом божественного клинка я отрубаю гоНЕ РЕШАЙ САМ ЧТО ОН ДЕЛАЕТ ПОКА ОН НЕ НАПИШЕТ ЧТО ОН СДЕЛАЕТ(вместо этого говори просто результат 
    И СПРАШИВАЙ ИГРОКА ЧТО ОН БУДЕТ ДЕЛАТЬ(И ЕСЛИ ИНВЕНТАРЬ ПУСТОЙ ТО ЗНАЧИТ ЧТО ИНВЕНТАРЬ ПУСТОЙ И ИГРОК БЕЗ ОРУЖИЯ И ОН НЕ В БОЖЕСТВЕННОЙ БРОНЕ ЧТО ИМЕЕТ СОПРОТИВЛЕНИЕ НА ВСЕ ВИДЫ УРОНА)
    Сюжет:Добро пожаловать в Подземелье! Ты очнулся в сырой темноте. 
    У тебя 100 HP, а в карманах пусто. Можешь использовать сленг игроков в DnD.Хп у игрока 100 на начале игры и может меняться. 
    монет у игрока в начале игры 0 и количество монет может меняться. Сейчас у тебя выпало на кубике {dice1} и  говори результат игроку. 
    Логика для 20 гранного кубика: меньше 7:неудача. больше 17:удача. остальное нейтрал. За каждую удачу даешь новые вещи и побольше хп. 
    За нейтральную удачу даешь немного монет и сам решаешь немного хп дать или забрать. За неудачу игрок теряет много хп. 
    Будет магазин в котором ты сам придумаешь вещи их цену и что они могут делать. Игрок появляется ТОЛЬКО СО 100 ХП НИ БОЛЬШЕ НИ МЕНЬШЕ, но при этом хп может быть бесконечно максимальным. 
    Используй обычный русский текст без использования шрифтов и НИКАКОГО!! markdown и html.
    Выводи сначала историю и в конце пиши 
    "Инвентарь: [(здесь должен быть список всех предметов)]
    HP: (количество хп)
    exp: (количество опыта)
    Gold: (количество монет)" 
    """
    return SYSTEM_PROMPT
