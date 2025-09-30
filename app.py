from flask import Flask, render_template, abort, jsonify, request, url_for
import json
from pathlib import Path


app = Flask(__name__)


# Load data from JSON once
DATA_PATH = Path(__file__).parent / 'data' / 'courses.json'
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    DATA = json.load(f)


# Helpers
def get_course(slug):
    for c in DATA['cursos']:
        if c['slug'] == slug:
            return c
    return None


def get_tema(course, tema_slug):
    for t in course.get('temas', []):
        if t['slug'] == tema_slug:
            return t
    return None


@app.route('/')
def home():
    cursos = DATA['cursos']
    return render_template('index.html', cursos=cursos)


@app.route('/curso/<slug>')
def curso(slug):
    course = get_course(slug)
    if not course:
        abort(404)
    return render_template('curso.html', curso=course)


@app.route('/curso/<curso_slug>/tema/<tema_slug>')
def tema(curso_slug, tema_slug):
    course = get_course(curso_slug)
    if not course:
        abort(404)
    t = get_tema(course, tema_slug)
    if not t:
        abort(404)
    return render_template('tema.html', curso=course, tema=t)


# API simple para búsqueda (devuelve coincidencias en título/descripcion/contenido)
@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip().lower()
    results = []
    if q:
        for c in DATA['cursos']:
            if q in c.get('titulo','').lower() or q in c.get('descripcion','').lower():
                results.append({'type':'curso','curso_slug':c['slug'], 'titulo': c['titulo']})
        for t in c.get('temas', []):
            if q in t.get('titulo','').lower() or q in t.get('contenido','').lower():
                results.append({'type':'tema','curso_slug':c['slug'],'tema_slug':t['slug'],'titulo': t['titulo']})
    return jsonify({'q': q, 'results': results})


if __name__ == '__main__':
    app.run(debug=True)