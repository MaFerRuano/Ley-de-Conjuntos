function aplicarLey(ley) {
    const conjuntoA = document.getElementById('conjuntoA').value.split(',').map(s => s.trim());
    const conjuntoB = document.getElementById('conjuntoB').value.split(',').map(s => s.trim());
    const conjuntoC = document.getElementById('conjuntoC').value.split(',').map(s => s.trim()).filter(Boolean);

    const datos = {
        conjuntoA: conjuntoA,
        conjuntoB: conjuntoB,
        conjuntoC: conjuntoC,
        ley: ley
    };

    fetch('http://127.0.0.1:5000/procesar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultado').innerHTML = `
            <p><strong>Resultado:</strong> { ${data.resultado.join(', ')} }</p>
            <p><strong>Explicación:</strong> ${data.explicacion}</p>
        `;
        document.getElementById('diagramaVenn').innerHTML = `
            <img src="data:image/svg+xml;base64,${data.diagrama}" alt="Diagrama de Venn">
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultado').innerHTML = '<p style="color: red;">Ocurrió un error. Asegúrate de que el servidor de Python esté ejecutándose.</p>';
    });
}
