"""
Global Demografiya Tahlili - Backend (Flask REST API)
=====================================================
Turli davlatlar aholisi bo'yicha ochiq ma'lumotlarni tahlil qiluvchi API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from analyzer import DemographyAnalyzer

app = Flask(__name__)
CORS(app)

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'demographics.csv')
analyzer = DemographyAnalyzer(DATA_PATH)


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "xabar": "Global Demografiya Tahlili API",
        "versiya": "1.0.0",
        "endpointlar": {
            "/api/davlatlar": "Barcha davlatlar ro'yxati",
            "/api/umumiy-statistika": "Umumiy global statistika",
            "/api/davlat/<kod>": "Bitta davlat ma'lumotlari",
            "/api/qitalar": "Qitalar bo'yicha statistika",
            "/api/top-aholi": "Eng ko'p aholiga ega davlatlar",
            "/api/top-umr": "Eng yuqori umr ko'rish davlatlari",
            "/api/top-gdp": "Eng yuqori GDP davlatlar",
            "/api/taqqoslash": "Davlatlarni taqqoslash",
            "/api/qidirish": "Davlat qidirish",
            "/api/demografik-tasnif": "Demografik tasnif"
        }
    })


@app.route('/api/davlatlar', methods=['GET'])
def barcha_davlatlar():
    davlatlar = analyzer.barcha_davlatlar()
    return jsonify({"jami": len(davlatlar), "davlatlar": davlatlar})


@app.route('/api/umumiy-statistika', methods=['GET'])
def umumiy_statistika():
    stat = analyzer.umumiy_statistika()
    return jsonify(stat)


@app.route('/api/davlat/<kod>', methods=['GET'])
def davlat_malumoti(kod):
    malumot = analyzer.davlat_malumoti(kod.upper())
    if malumot is None:
        return jsonify({"xato": f"'{kod}' kodi topilmadi"}), 404
    return jsonify(malumot)


@app.route('/api/qitalar', methods=['GET'])
def qitalar_statistikasi():
    stat = analyzer.qitalar_statistikasi()
    return jsonify(stat)


@app.route('/api/top-aholi', methods=['GET'])
def top_aholi():
    n = min(max(request.args.get('n', 10, type=int), 1), 50)
    natija = analyzer.top_davlatlar('population', n, kamayuvchi=True)
    return jsonify({"top": n, "davlatlar": natija})


@app.route('/api/top-umr', methods=['GET'])
def top_umr():
    n = min(max(request.args.get('n', 10, type=int), 1), 50)
    natija = analyzer.top_davlatlar('life_expectancy', n, kamayuvchi=True)
    return jsonify({"top": n, "davlatlar": natija})


@app.route('/api/top-gdp', methods=['GET'])
def top_gdp():
    n = min(max(request.args.get('n', 10, type=int), 1), 50)
    natija = analyzer.top_davlatlar('gdp_per_capita', n, kamayuvchi=True)
    return jsonify({"top": n, "davlatlar": natija})


@app.route('/api/taqqoslash', methods=['GET'])
def davlatlarni_taqqoslash():
    kodlar_str = request.args.get('kodlar', 'USA,CHN,IND')
    kodlar = [k.strip().upper() for k in kodlar_str.split(',') if k.strip()]
    if len(kodlar) < 2:
        return jsonify({"xato": "Kamida 2 ta davlat kodi kiriting"}), 400
    if len(kodlar) > 10:
        return jsonify({"xato": "Maksimal 10 ta davlat taqqoslanadi"}), 400
    natija = analyzer.davlatlarni_taqqoslash(kodlar)
    return jsonify(natija)


@app.route('/api/aholi-tahlili', methods=['GET'])
def aholi_tahlili():
    qita = request.args.get('qita', None)
    natija = analyzer.aholi_turmush_tahlili(qita)
    return jsonify(natija)


@app.route('/api/qidirish', methods=['GET'])
def davlat_qidirish():
    qidiruv = request.args.get('q', '').strip()
    if len(qidiruv) < 2:
        return jsonify({"xato": "Kamida 2 ta belgi kiriting"}), 400
    natija = analyzer.qidirish(qidiruv)
    return jsonify({"qidiruv": qidiruv, "natijalar": natija})


@app.route('/api/demografik-tasnif', methods=['GET'])
def demografik_tasnif():
    natija = analyzer.demografik_tasnif()
    return jsonify(natija)


@app.route('/api/korrelatsiya', methods=['GET'])
def korrelatsiya():
    natija = analyzer.korrelatsiya_tahlili()
    return jsonify(natija)


@app.errorhandler(404)
def topilmadi(e):
    return jsonify({"xato": "Endpoint topilmadi", "kod": 404}), 404


@app.errorhandler(500)
def server_xato(e):
    return jsonify({"xato": "Server xatosi", "kod": 500}), 500


if __name__ == '__main__':
    print("=" * 55)
    print("  Global Demografiya Tahlili - Backend API")
    print("=" * 55)
    print(f"  Server: http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, host='0.0.0.0', port=5000)
