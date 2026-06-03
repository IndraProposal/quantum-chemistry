const cacheUrl = './exploration-cache.json';
const analyticsKey = 'qc2048.analytics.events';
const unknownsKey = 'qc2048.cache.unknowns';

const tiles = [
  'ψ', '2', 'node', '4',
  'orbital', '8', 'spin', '16',
  'bond', '32', 'MO', '64',
  'HOMO', '128', 'LUMO', '2048'
];

const hints = [
  'A wavefunction is not the particle; it is a compact rule for probability amplitude.',
  'Nodes are places where the sign changes and probability density falls to zero.',
  'Merging tiles is a metaphor: simple basis ideas combine into molecular orbitals.',
  'The live page can change after print, so a QR code becomes a doorway rather than a footnote.'
];

function loadEvents() {
  return JSON.parse(localStorage.getItem(analyticsKey) || '[]');
}

function saveEvents(events) {
  localStorage.setItem(analyticsKey, JSON.stringify(events.slice(-200)));
}

function track(type, detail = {}) {
  const event = {
    type,
    detail,
    path: window.location.pathname,
    timestamp: new Date().toISOString(),
    deviceClass: matchMedia('(pointer: coarse)').matches ? 'tablet-touch' : 'desktop'
  };
  const events = loadEvents();
  events.push(event);
  saveEvents(events);
  renderMetrics(events);
}

function renderMetrics(events = loadEvents()) {
  const counters = events.reduce((acc, event) => {
    acc[event.type] = (acc[event.type] || 0) + 1;
    return acc;
  }, {});
  document.querySelector('[data-metric="events"]').textContent = events.length;
  document.querySelector('[data-metric="hints"]').textContent = counters.hint_opened || 0;
  document.querySelector('[data-metric="unknowns"]').textContent = getUnknowns().length;
}

function getUnknowns() {
  return JSON.parse(localStorage.getItem(unknownsKey) || '[]');
}

function rememberUnknown(topic) {
  const unknowns = getUnknowns();
  unknowns.push({ topic, timestamp: new Date().toISOString(), status: 'queued-for-refresh' });
  localStorage.setItem(unknownsKey, JSON.stringify(unknowns.slice(-50)));
  track('unknown_queued', { topic });
}

function renderTiles() {
  const grid = document.querySelector('.game-grid');
  grid.innerHTML = tiles.map((tile, index) => {
    const rank = index > 12 ? 'high' : index > 7 ? 'mid' : 'low';
    return `<button class="tile" data-rank="${rank}" data-tile="${tile}" aria-label="Open ${tile} concept">${tile}</button>`;
  }).join('');
  grid.addEventListener('click', (event) => {
    const tile = event.target.closest('.tile');
    if (!tile) return;
    track('tile_opened', { tile: tile.dataset.tile });
    document.querySelector('[data-live-note]').textContent = `${tile.dataset.tile} opened a live exploration trail. The cache keeps this path warm for offline review.`;
  });
}

function wireHints() {
  let hintIndex = 0;
  document.querySelector('[data-action="hint"]').addEventListener('click', () => {
    const hint = hints[hintIndex % hints.length];
    hintIndex += 1;
    document.querySelector('[data-hint]').textContent = hint;
    track('hint_opened', { hintIndex });
  });
  document.querySelector('[data-action="unknown"]').addEventListener('click', () => {
    const topic = `unknown-link-${Date.now()}`;
    rememberUnknown(topic);
    document.querySelector('[data-hint]').textContent = `Queued ${topic}. In production, CI/CD would refresh the content graph and publish the new trail.`;
  });
}

async function renderGraph() {
  const response = await fetch(cacheUrl);
  const cache = await response.json();
  const graph = document.querySelector('.graph');
  graph.innerHTML = cache.nodes.map(node => `
    <article class="node">
      <p class="eyebrow">${node.chapter}</p>
      <h3>${node.title}</h3>
      <p>${node.summary}</p>
      <small>Links: ${node.links.join(', ')}</small><br>
      <button class="button secondary" data-node="${node.id}">Explore trail</button>
    </article>
  `).join('');
  graph.addEventListener('click', (event) => {
    const button = event.target.closest('[data-node]');
    if (!button) return;
    track('node_explored', { node: button.dataset.node });
    document.querySelector('[data-live-note]').textContent = `Exploring ${button.dataset.node}; adjacent hints are resolved from the infinite cache seed.`;
  });
}

function wireExport() {
  document.querySelector('[data-action="export"]').addEventListener('click', () => {
    const payload = {
      exportedAt: new Date().toISOString(),
      events: loadEvents(),
      unknowns: getUnknowns()
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'qc2048-analytics-snapshot.json';
    link.click();
    URL.revokeObjectURL(url);
    track('analytics_exported');
  });
}

renderTiles();
wireHints();
wireExport();
renderMetrics();
renderGraph().then(() => track('page_ready'));
