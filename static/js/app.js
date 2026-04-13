// Рисуем граф при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    if (typeof graphData !== 'undefined') {
        drawGraph(graphData);
    }
});

function drawGraph(data) {
    const container = document.getElementById('graph-network');
    
    const nodes = new vis.DataSet(data.nodes);
    const edges = new vis.DataSet(data.edges);
    
    const options = {
        nodes: {
            shape: 'circle',
            size: 30,
            font: {
                size: 16,
                color: '#ffffff'
            },
            color: {
                background: '#667eea',
                border: '#333'
            }
        },
        edges: {
            width: 2,
            color: {
                color: '#848484',
                highlight: '#667eea'
            },
            smooth: {
                type: 'continuous'
            }
        },
        physics: {
            enabled: true,
            stabilization: {
                iterations: 100
            }
        }
    };
    
    new vis.Network(container, {nodes: nodes, edges: edges}, options);
}

// Функция проверки ответа
async function checkAnswer() {
    const degreesInput = document.getElementById('degrees-input').value;
    const eulerSelect = document.getElementById('euler-select').value;
    
    // Парсим степени вершин
    const userDegrees = degreesInput.split(',').map(s => parseInt(s.trim()));
    const userEuler = eulerSelect === 'true';
    
    // Отправляем на сервер
    const response = await fetch('/api/task/0/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            degrees: userDegrees,
            is_euler: userEuler
        })
    });
    
    const result = await response.json();
    const resultDiv = document.getElementById('result');
    
    if (result.success) {
        resultDiv.className = 'result success';
        resultDiv.textContent = '✅ ' + result.message;
    } else {
        resultDiv.className = 'result error';
        resultDiv.textContent = '❌ ' + result.message;
    }
}