import requests
import random
import json

attempts = 2
used_answers = []
fail = {"results": []}
number_question = 0
score = 0
random_answer = []
name = input("Напишите ваше имя>>>")

print("Ты попал на викторину")
print("Твоя задача-побить рекорд прошлого игрока или хотя бы досчить того же уровня,как и он,иначе ты проиграешь.")
with open("fail.json", "r", encoding="utf-8") as json_file:
    record = json.load(json_file)
print("Рекорд прошлого игрока:", record["results"][0]["name"], "-", record["results"][0]["score"])


def get_questions(level_question: int):
    questions_list = []
    response = requests.get(f"https://engine.lifeis.porn/api/millionaire.php?qType={level_question}&count=5").json()
    for question_data in response["data"]:
        correct_answer = question_data['answers'][0]
        question_answers = question_data['answers']
        random.shuffle(question_answers)
        questions_list.append(
            {
                'answers': question_answers,
                'question': question_data['question'].replace('\u2063', ''),
                'correct_answer': correct_answer,
                'score': level_question * 10
            }
        )
    return questions_list


def show_question(question_data):
    print(question_data['question'])
    print("---Варианты ответа---")
    print("\n".join(question_data['answers']) + "\n")


def user_answer_check(user_answ, question_data, score_user):
    if user_answ == question_data['correct_answer']:
        score_user += question_data['score']
        text = "Верно!"
        return score_user, text
    else:
        text = f"Неверно\n Правильный ответ {question_data['correct_answer']}"
        return score_user, text


for count_round in range(1, 4):
    questions = get_questions(level_question=count_round)
    for question in questions:
        show_question(question_data=question)
        user_answer = input("Введите ответ>>>")
        score, text_output = user_answer_check(user_answ=user_answer, question_data=question, score_user=score)
        print(text_output)


print("Ваш счет:", score)
random_answer = []
if record["results"][0]["score"] <= score:
    fail["results"].append({"name": name, "score": score})
    print("Поздравляем.Вы выиграли викторину и установили новый рекорд.")
else:
    fail["results"].append({"name": record["results"][0]["name"], "score": record["results"][0]["score"]})
    print("Вы проиграли.")
with open('fail.json', 'w', encoding='utf-8') as file:
    json.dump(fail, file, indent=4)
