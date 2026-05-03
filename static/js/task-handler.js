// static/js/task-handler.js
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.task-wrapper');
    if (!wrapper) return;

    const taskId = wrapper.dataset.taskId;
    const renderer = new GraphRenderer('graph-container');
    const solutionBox = document.getElementById('solution');
    const feedbackBox = document.getElementById('feedback');
    const form = document.getElementById('answer-form');
    const inputField = document.getElementById('user-input');

    // Load task data
    fetch(`/api/task/${taskId}/show`)
        .then(res => res.ok ? res.json() : Promise.reject('Не удалось загрузить задачу'))
        .then(data => {
            renderer.render(data.graph);
            renderSolution(data.solution, taskId, renderer);
        })
        .catch(err => window.handleAppError(err));

    // Toggle solution visibility
    document.getElementById('toggle-solution')?.addEventListener('click', () => {
        solutionBox.classList.toggle('hidden');
    });

    // Handle form submission
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!inputField) return;

        let payload = {};
        try {
            const raw = inputField.value.trim();
            switch (taskId) {
                case '6': payload = { components: parseComponentsInput(raw) }; break;
                case '10': payload = { sequence: parseSequenceInput(raw) }; break;
                case '11': payload = { edges: raw }; break;
                case '12': payload = { colors: raw }; break;
                default: payload = { order: raw };
            }
        } catch {
            showFeedback("Ошибка формата ввода. Проверьте подсказку.", false);
            return;
        }

        try {
            const res = await fetch(`/api/task/${taskId}/check`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await res.json();
            showFeedback(result.feedback || result.message, result.correct);

            if (result.correct) {
                if (result.expected?.edges) renderer.highlightEdges(result.expected.edges);
                if (result.expected?.colors) renderer.colorNodes(result.expected.colors);
                if (result.expected?.components) renderer.highlightComponents(result.expected.components);
            }
        } catch {
            showFeedback("Ошибка соединения с сервером.", false);
        }
    });

    function parseComponentsInput(input) {
        const groups = input.match(/\[[^\]]+\]/g) || [];
        return groups.map(g => g.replace(/[\[\]\s]/g, '').split(',').map(Number));
    }

    function parseSequenceInput(input) {
        return input.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
    }

    function showFeedback(text, isCorrect) {
        if (!feedbackBox) return;
        feedbackBox.textContent = text;
        feedbackBox.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
        feedbackBox.classList.remove('hidden');
    }

    function renderSolution(sol, taskId, renderer) {
        if (!solutionBox || !sol) return;
        let html = '';
        if (sol.explanation) html += `<p>${sol.explanation}</p>`;
        if (sol.message) html += `<p>${sol.message}</p>`;
        if (sol.stats) html += `<p>Вершин: ${sol.stats.vertices}, Рёбер: ${sol.stats.edges}</p>`;

        if (taskId === '7' && sol.edges) {
            html += `<h4>Рёбра MST:</h4><ul>${sol.edges.map(e => `<li>${e.from} → ${e.to} (вес: ${e.weight})</li>`).join('')}</ul>`;
            renderer.highlightEdges(sol.edges);
        }
        if (taskId === '8' && sol.distances) {
            html += `<table><tr><th>Вершина</th>${Object.keys(sol.distances).sort((a,b)=>a-b).map(v=>`<td>${v}</td>`).join('')}</tr>`;
            html += `<tr><td><b>d(0,v)</b></td>${Object.keys(sol.distances).sort((a,b)=>a-b).map(v=>`<td>${sol.distances[v]===Infinity?'∞':sol.distances[v]}</td>`).join('')}</tr></table>`;
        }
        if (taskId === '9' && sol.matrix) {
            html += `<table><tr><th></th>${sol.vertices.map(v=>`<th>${v}</th>`).join('')}</tr>`;
            sol.matrix.forEach((row, i) => { html += `<tr><th>${sol.vertices[i]}</th>${row.map(val=>`<td>${val===Infinity?'∞':val}</td>`).join('')}</tr>`; });
            html += `</table>`;
        }
        if (taskId === '10' && sol.sequence) html += `<p><b>Ответ:</b> [${sol.sequence.join(', ')}]</p>`;
        if (taskId === '11' && sol.edges) html += `<p><b>Рёбра:</b> ${sol.edges.map(e => `(${e[0]},${e[1]})`).join(', ')}</p>`;
        if (taskId === '12' && sol.colors) html += `<p><b>Цвета:</b> ${JSON.stringify(sol.colors)} (использовано ${sol.num_colors})</p>`;

        solutionBox.innerHTML = html;
    }
});