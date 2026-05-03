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
    }

    render(data) {
        if (!this.container || !data) return;
        const visData = {
            nodes: new vis.DataSet(data.nodes.map(n => ({
                ...n,
                color: { background: '#e0e0e0', border: '#333', highlight: { background: '#007bff', border: '#0056b3' } },
                label: n.label || String(n.id)
            }))),
            edges: new vis.DataSet(data.edges.map(e => ({
                ...e,
                color: { color: '#888', highlight: '#007bff' }
            })))
        };
        this.network = new vis.Network(this.container, visData, this.options);
        
        // Принудительно обновляем цвета меток при смене темы
        this._applyThemeLabels();
        document.getElementById('themeToggle')?.addEventListener('click', () => {
            setTimeout(() => this._applyThemeLabels(), 50);
        });
        return this.network;
    }

    _applyThemeLabels() {
        if (!this.network) return;
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const color = isDark ? '#eee' : '#333';
        const nodes = this.network.body.data.nodes;
        const updates = nodes.get().map(n => ({
            id: n.id,
            font: { ...n.font, color: color }
        }));
        nodes.update(updates);
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
        const palette = {1:'#FF9800', 2:'#4CAF50', 3:'#2196F3', 4:'#9C27B0', 5:'#F44336', 6:'#00BCD4'};
        const nodes = this.network.body.data.nodes;
        nodes.update(nodes.get().map(n => {
            const colorId = colorsMap[n.id];
            const bg = palette[colorId] || '#888';
            return { 
                id: n.id, 
                color: { background: bg, border: '#333', highlight: bg }, 
                font: { color: '#fff' } 
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