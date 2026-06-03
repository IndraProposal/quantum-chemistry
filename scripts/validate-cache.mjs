import { readFile } from 'node:fs/promises';

const cache = JSON.parse(await readFile(new URL('../live/exploration-cache.json', import.meta.url), 'utf8'));
const errors = [];

if (!Number.isInteger(cache.version)) errors.push('cache.version must be an integer');
if (!Array.isArray(cache.nodes) || cache.nodes.length === 0) errors.push('cache.nodes must be a non-empty array');

const ids = new Set();
for (const node of cache.nodes || []) {
  if (!node.id || typeof node.id !== 'string') errors.push('every node needs a string id');
  if (ids.has(node.id)) errors.push(`duplicate node id: ${node.id}`);
  ids.add(node.id);
  for (const field of ['title', 'summary', 'chapter']) {
    if (!node[field] || typeof node[field] !== 'string') errors.push(`${node.id || 'node'} missing ${field}`);
  }
  if (!Array.isArray(node.links) || node.links.length === 0) errors.push(`${node.id || 'node'} needs at least one link`);
}

for (const node of cache.nodes || []) {
  for (const link of node.links || []) {
    if (!ids.has(link)) errors.push(`${node.id} links to missing node ${link}`);
  }
}

if (errors.length > 0) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`Validated ${cache.nodes.length} exploration-cache nodes.`);
