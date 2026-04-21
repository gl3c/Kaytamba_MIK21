from flask import Flask, render_template, request, jsonify
import os
import traceback

app = Flask(__name__)

os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Простая оценка без тяжёлых библиотек
def evaluate_description(text: str):
    if not text or len(text.strip()) < 20:
        return 2.5
    
    words = len(text.split())
    length_score = min(len(text) / 30, 10)
    unique = len(set(text.lower().split()))
    diversity = unique / max(words, 1)
    
    score = length_score * 0.45 + diversity * 5 + (words > 70) * 2.5
    return round(min(max(score, 2.5), 10.0), 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    text = data.get('text', '')
    
    score = evaluate_description(text)
    
    if score >= 8.0:
        verdict = "Отличное описание! ✅"
        recs = "Можно добавить эмодзи или призыв к действию."
    elif score >= 6.0:
        verdict = "Хорошее описание 👍"
        recs = "Добавьте преимущества и технические характеристики."
    elif score >= 4.0:
        verdict = "Среднее — можно улучшить"
        recs = "Добавьте больше деталей и ключевые слова."
    else:
        verdict = "Слабое описание ❌"
        recs = "Рекомендуем полностью переписать."
    
    improved = f"🔥 {text}\n\n✅ Преимущества: высокое качество, удобство, лучшая цена.\n🚀 Быстрая доставка по всей России!"

    return jsonify({
        "score": score,
        "verdict": verdict,
        "recommendations": recs,
        "improved": improved
    })

if __name__ == '__main__':
    print("🚀 DescScore AI запущен!")
    print("🌐 Открой в браузере: http://127.0.0.1:5000")
    try:
        app.run(debug=True, port=5000)
    except Exception as e:
        print("❌ Ошибка запуска:")
        traceback.print_exc()