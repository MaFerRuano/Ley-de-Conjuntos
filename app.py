from flask import Flask, request, jsonify
from flask_cors import CORS
from matplotlib_venn import venn2, venn3
from matplotlib import pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app) # Permite que el HTML se comunique con el servidor

# Función para generar el diagrama de Venn
def generar_diagrama_venn(sets, ley):
    plt.figure(figsize=(6,6))
    if len(sets) == 2:
        venn2(subsets=(sets[0], sets[1]), set_labels=('A', 'B'))
    elif len(sets) == 3:
        venn3(subsets=(sets[0], sets[1], sets[2]), set_labels=('A', 'B', 'C'))
    
    plt.title(f"Diagrama de Venn para: {ley}")
    
    # Guardar el diagrama en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='svg')
    buf.seek(0)
    img_svg = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return img_svg

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    A = set(data.get('conjuntoA'))
    B = set(data.get('conjuntoB'))
    C = set(data.get('conjuntoC'))
    ley = data.get('ley')
    
    resultado = set()
    explicacion = ""
    
    if ley == 'union':
        resultado = A.union(B)
        explicacion = f"La unión de A y B es el conjunto de todos los elementos que están en A, o en B, o en ambos."
    elif ley == 'interseccion':
        resultado = A.intersection(B)
        explicacion = f"La intersección de A y B es el conjunto de elementos que están en A y también en B."
    elif ley == 'diferencia':
        resultado = A.difference(B)
        explicacion = f"La diferencia de A menos B es el conjunto de elementos que están en A pero no en B."
    elif ley == 'complemento':
        # Para el complemento, necesitamos un conjunto universal, aquí usaremos la unión de todos los conjuntos.
        universal = A.union(B).union(C)
        resultado = universal.difference(A)
        explicacion = f"El complemento de A (relativo al conjunto universal de A, B y C) es el conjunto de elementos que no están en A."
    elif ley == 'deMorgan':
        # Ley de De Morgan: (A U B)^c = A^c n B^c
        universal = A.union(B)
        lado_izq = universal.difference(A.union(B))
        lado_der = universal.difference(A).intersection(universal.difference(B))
        resultado = lado_izq # Ambos lados deberían ser el mismo
        explicacion = "La ley de De Morgan establece que el complemento de la unión de dos conjuntos es igual a la intersección de sus complementos."
    elif ley == 'distributiva':
        # Ley Distributiva: A n (B U C) = (A n B) U (A n C)
        lado_izq = A.intersection(B.union(C))
        lado_der = A.intersection(B).union(A.intersection(C))
        resultado = lado_izq
        explicacion = "La ley distributiva de la intersección sobre la unión establece que A intersección (B unión C) es igual a (A intersección B) unión (A intersección C)."

    sets_para_diagrama = [A, B]
    if C:
        sets_para_diagrama.append(C)
    
    diagrama_svg = generar_diagrama_venn(sets_para_diagrama, ley)

    return jsonify({
        'resultado': sorted(list(resultado)),
        'explicacion': explicacion,
        'diagrama': diagrama_svg
    })

if __name__ == '__main__':
    app.run(debug=True)
