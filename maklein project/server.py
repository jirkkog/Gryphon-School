from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Подключение к PostgreSQL
DATABASE_URL = "postgres://user:password@host:port/dbname"
conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# Получение теста
@app.route('/api/get-test', methods=['GET'])
def get_test():
    test_id = request.args.get('id')
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tests WHERE id = %s", (test_id,))
        test = cur.fetchone()
    return jsonify(test)

# Проверка теста
@app.route('/api/submit-test', methods=['POST'])
def submit_test():
    data = request.json
    username = data['username']
    group = data['group']
    test_id = data['testId']
    answers = data['answers']

    # Получение правильных ответов
    with conn.cursor() as cur:
        cur.execute("SELECT correct_answers FROM tests WHERE id = %s", (test_id,))
        correct_answers = cur.fetchone()['correct_answers']

    # Подсчет баллов
    score = sum(1 for i in range(len(correct_answers)) if answers.get(f'answer-{i}') == correct_answers[i])

    # Сохранение результата
    with conn.cursor() as cur:
        cur.execute("INSERT INTO results (username, group, test_id, score) VALUES (%s, %s, %s, %s)",
                    (username, group, test_id, score))
        conn.commit()

    return jsonify({"score": score})

if __name__ == '__main__':
    app.run(debug=True)
