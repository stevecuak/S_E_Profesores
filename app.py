from flask import Flask, render_template, request

import rule_engine

criterios_evaluacion = [
    {"criterio": "portada_completa == true", "puntos": 5},
    {"criterio": "portada_completa == false", "puntos": 0},
    {"criterio": "resolucion_correcta == true", "puntos": 60},
    {"criterio": "resolucion_correcta == false", "puntos": 0},
    {"criterio": "conclusion_coherente == true", "puntos": 15},
    {"criterio": "conclusion_coherente == false", "puntos": 0},
    {"criterio": "texto_justificado == true", "puntos": 10},
    {"criterio": "texto_justificado == false", "puntos": 0},
    {"criterio": "no_errores_ortograficos == true", "puntos": 10},
    {"criterio": "no_errores_ortograficos == false", "puntos": 0}
]
rules = [(rule_engine.Rule(rule["criterio"]), rule["puntos"]) for rule in criterios_evaluacion]

app = Flask(__name__)

def evaluar_puntaje(trabajo):
    puntosT = 0
    for rule, puntos in rules:
        if rule.matches(trabajo):
            puntosT = puntosT + puntos
    return puntosT

def evaluar_calificacion(trabajo):
    calificacion = evaluar_puntaje(trabajo)
    if calificacion <= 69:
        return "Calificación Reprobatoria"
    elif calificacion >= 70:
        return "Calificación Aprobatoria"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        portada_completa = request.form['portada'] == 'si'
        resolucion_correcta = request.form['resolucion'] == 'si'
        conclusion_coherente = request.form['conclusion'] == 'si'
        texto_justificado = request.form['justificado'] == 'si'
        no_errores_ortograficos = request.form['ortografia'] == 'si'

        trabajo = {
            "nombre": nombre,
            "portada_completa": portada_completa,
            "resolucion_correcta": resolucion_correcta,
            "conclusion_coherente": conclusion_coherente,
            "texto_justificado": texto_justificado,
            "no_errores_ortograficos": no_errores_ortograficos
        }

        puntaje = evaluar_puntaje(trabajo)
        calificacion = evaluar_calificacion(trabajo)

        return render_template('resultado.html', nombre=nombre, puntaje=puntaje, calificacion=calificacion)

    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)