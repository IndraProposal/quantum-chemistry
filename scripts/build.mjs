import { mkdir, copyFile, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const dist = new URL('../dist/', import.meta.url);
const files = [
  ['live/index.html', 'index.html'],
  ['live/exploration-cache.json', 'exploration-cache.json'],
  ['live/assets/app.js', 'assets/app.js'],
  ['live/assets/styles.css', 'assets/styles.css']
];

await mkdir(new URL('assets/', dist), { recursive: true });
const manifest = [];

for (const [source, target] of files) {
  const sourceUrl = new URL(source, root);
  const targetUrl = new URL(target, dist);
  await copyFile(sourceUrl, targetUrl);
  const contents = await readFile(sourceUrl);
  manifest.push({
    path: target,
    bytes: contents.length,
    sha256: createHash('sha256').update(contents).digest('hex')
  });
}

await writeFile(new URL('manifest.json', dist), JSON.stringify({
  name: 'Quantum Chemistry 2048 live pages',
  builtAt: new Date().toISOString(),
  files: manifest
}, null, 2));

console.log(`Built ${manifest.length} live-page assets into dist/.`);
