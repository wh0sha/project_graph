// static/js/graph-renderer.js
class GraphRenderer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.network = null;
        this.options = {
            nodes: { 
                shape: 'circle', size: 24, 
                font: { size: 15, face: 'system-ui, sans-serif', strokeWidth: 0 },
                borderWidth: 2, borderWidthSelection: 3
            },
            edges: { width: 2, smooth: { type: 'continuous', roundness: 0.2 } },
            interaction: { dragNodes: true, zoomView: true, hover: true },
            physics: { enabled: true, stabilization: { iterations: 120 } },
            ...options
        };
        
        window.addEventListener('themeChanged', () => this._applyThemeToNetwork());
    }

    render(data) {
        if (!this.container || !data) return;
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const labelColor = isDark ? '#eee' : '#333';
        const nodeBg = isDark ? '#4a5568' : '#e0e0e0';
        const nodeBorder = isDark ? '#718096' : '#333';

        const visData = {
            nodes: new vis.DataSet(data.nodes.map(n => ({
                ...n,
                color: { background: nodeBg, border: nodeBorder, highlight: { background: '#007bff', border: '#0056b3' } },
                font: { color: labelColor },
                label: n.label || String(n.id)
            }))),
            edges: new vis.DataSet(data.edges.map(e => ({
                ...e,
                color: { color: isDark ? '#888' : '#999', highlight: '#007bff' },
                font: { size: 12, color: isDark ? '#ccc' : '#666', strokeWidth: 2, strokeColor: isDark ? '#222' : '#fff' }
            })))
        };
        
        this.network = new vis.Network(this.container, visData, this.options);
        this._applyThemeToNetwork();
        return this.network;
    }

    _applyThemeToNetwork() {
        if (!this.network) return;
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const labelColor = isDark ? '#eee' : '#333';
        
        const nodes = this.network.body.data.nodes;
        const updates = nodes.get().map(n => ({ id: n.id, font: { color: labelColor } }));
        nodes.update(updates);

        const edges = this.network.body.data.edges;
        edges.update(edges.get().map(e => ({
            id: e.id,
            font: { color: isDark ? '#ccc' : '#666', strokeColor: isDark ? '#222' : '#fff' }
        })));
    }

    // 🔥 НОВЫЙ МЕТОД: анимация обхода вершин
    animateTraversal(order, { delay = 600, onStep = null, onComplete = null } = {}) {
        if (!this.network || !order || order.length === 0) return;
        
        let step = 0;
        const nodes = this.network.body.data.nodes;
        const originalColors = {};
        
        // Сохраняем исходные цвета
        nodes.get().forEach(n => {
            originalColors[n.id] = n.color?.background || '#e0e0e0';
        });

        const highlightStep = () => {
            if (step >= order.length) {
                if (onComplete) onComplete();
                return;
            }
            
            const vertexId = order[step];
            
            // Подсвечиваем текущую вершину
            nodes.update({
                id: vertexId,
                color: { background: '#FFD700', border: '#FFA500', highlight: { background: '#FFD700', border: '#FF8C00' } },
                shadow: { enabled: true, color: 'rgba(255, 215, 0, 0.8)' }
            });
            
            if (onStep) onStep(vertexId, step, order.length);
            
            step++;
            if (step < order.length) {
                setTimeout(highlightStep, delay);
            } else {
                if (onComplete) onComplete();
            }
        };
        
        // Сброс перед началом
        this.resetNodeHighlights(originalColors);
        setTimeout(highlightStep, 300);
    }

    // 🔥 Вспомогательный: сброс подсветки вершин
    resetNodeHighlights(originalColors = {}) {
        if (!this.network) return;
        const nodes = this.network.body.data.nodes;
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const defaultBg = isDark ? '#4a5568' : '#e0e0e0';
        const defaultBorder = isDark ? '#718096' : '#333';
        
        nodes.update(nodes.get().map(n => ({
            id: n.id,
            color: { 
                background: originalColors[n.id] || defaultBg, 
                border: originalColors[n.id] ? defaultBorder : defaultBorder,
                highlight: { background: '#007bff', border: '#0056b3' }
            },
            shadow: { enabled: false }
        })));
    }

    highlightEdges(edgeList) {
        if (!this.network) return;
        const edges = this.network.body.data.edges;
        const targetIds = new Set(edgeList.map(e => `${e.from}-${e.to}`));
        edges.update(edges.get().map(e => {
            const isMST = targetIds.has(`${e.from}-${e.to}`) || targetIds.has(`${e.to}-${e.from}`);
            return {
                id: e.id,
                width: isMST ? 5 : 1.5,
                color: isMST ? { color: '#28a745', highlight: '#28a745' } : { color: '#aaa', highlight: '#007bff' }
            };
        }));
    }

    colorNodes(colorsMap) {
        if (!this.network || !colorsMap) return;
        const palette = {1:'#FF9800', 2:'#4CAF50', 3:'#2196F3', 4:'#9C27B0', 5:'#F44336', 6:'#00BCD4', 7:'#E91E63', 8:'#3F51B5'};
        const nodes = this.network.body.data.nodes;
        
        nodes.update(nodes.get().map(n => {
            const colorId = colorsMap[n.id];
            const bg = palette[colorId] || '#888';
            const r = parseInt(bg.slice(1, 3), 16);
            const g = parseInt(bg.slice(3, 5), 16);
            const b = parseInt(bg.slice(5, 7), 16);
            const brightness = (r * 299 + g * 587 + b * 114) / 1000;
            const textColor = brightness > 128 ? '#000' : '#fff';

            return { 
                id: n.id, 
                color: { background: bg, border: '#333', highlight: bg }, 
                font: { color: textColor } 
            };
        }));
    }

    highlightComponents(components) {
        if (!this.network) return;
        const colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336'];
        const nodes = this.network.body.data.nodes;
        nodes.update(nodes.get().map(n => {
            let color = '#ddd';
            for (let i = 0; i < components.length; i++) {
                if (components[i].includes(n.id)) { color = colors[i % colors.length]; break; }
            }
            return { id: n.id, color: { background: color, border: '#333' } };
        }));
    }
}
window.GraphRenderer = GraphRenderer;