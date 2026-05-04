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
    const toggleSolutionBtn = document.getElementById('toggle-solution');

    let solutionData = null;
    let isAnimating = false;

    // Load task data
    fetch(`/api/task/${taskId}/show`)
        .then(res => res.ok ? res.json() : Promise.reject('Не удалось загрузить задачу'))
        .then(data => {
            solutionData = data.solution;
            renderer.render(data.graph);
            renderSolution(data.solution, taskId, renderer);
        })
        .catch(err => {
            console.error(err);
            if (feedbackBox) {
                feedbackBox.textContent = 'Ошибка загрузки задачи';
                feedbackBox.className = 'feedback incorrect';
                feedbackBox.classList.remove('hidden');
            }
        });

    // Toggle solution visibility + animation trigger
    toggleSolutionBtn?.addEventListener('click', () => {
        solutionBox.classList.toggle('hidden');
        const isHidden = solutionBox.classList.contains('hidden');
        toggleSolutionBtn.textContent = isHidden ? 'Показать решение' : 'Скрыть решение';
        
        // 🔥 Запускаем анимацию/визуализацию при открытии решения
        if (!isHidden && solutionData && !isAnimating) {
            applySolutionVisualization(taskId, solutionData, renderer);
        }
    });

    // Handle form submission
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!inputField || isAnimating) return;

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
                applySolutionVisualization(taskId, result.expected || solutionData, renderer);
            }
        } catch {
            showFeedback("Ошибка соединения с сервером.", false);
        }
    });

    // 🔥 НОВАЯ ФУНКЦИЯ: применяет визуализацию решения в зависимости от задачи
    function applySolutionVisualization(taskId, solution, renderer) {
        if (!solution) return;
        isAnimating = true;

        // Задания 1, 3: анимация обхода
        if ((taskId === '1' || taskId === '3') && solution.order) {
            renderer.animateTraversal(solution.order, {
                delay: 700,
                onStep: (vertex, step, total) => {
                    if (feedbackBox) {
                        feedbackBox.textContent = `Шаг ${step + 1}/${total}: вершина ${vertex}`;
                        feedbackBox.className = 'feedback correct';
                        feedbackBox.classList.remove('hidden');
                    }
                },
                onComplete: () => {
                    isAnimating = false;
                    if (feedbackBox) {
                        feedbackBox.textContent = 'Обход завершён ✓';
                        setTimeout(() => feedbackBox.classList.add('hidden'), 2000);
                    }
                }
            });
            return;
        }

        // Задание 12: раскраска вершин
        if (taskId === '12' && solution.colors) {
            renderer.colorNodes(solution.colors);
            isAnimating = false;
            return;
        }

        // Задание 7: MST — подсветка рёбер
        if (taskId === '7' && solution.edges) {
            renderer.highlightEdges(solution.edges);
        }

        // Задание 5: компоненты связности
        if (taskId === '5' && solution.components) {
            renderer.highlightComponents(solution.components);
        }

        isAnimating = false;
    }

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
        if (taskId === '12' && sol.colors) {
            const colorsStr = Object.entries(sol.colors).map(([v,c]) => `${v}→${c}`).join(', ');
            html += `<p><b>Цвета вершин:</b> {${colorsStr}}<br><small>Использовано цветов: ${sol.num_colors}</small></p>`;
        }
        if ((taskId === '1' || taskId === '3') && sol.order) {
            html += `<p><b>Порядок обхода:</b> ${sol.order.join(' → ')}</p>`;
            html += `<p><small>💡 Нажмите "Показать решение" для анимации</small></p>`;
        }

        solutionBox.innerHTML = html;
    }
});