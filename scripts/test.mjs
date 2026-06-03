import { readFile } from 'node:fs/promises';

const html = await readFile(new URL('../live/index.html', import.meta.url), 'utf8');
const app = await readFile(new URL('../live/assets/app.js', import.meta.url), 'utf8');
const styles = await readFile(new URL('../live/assets/styles.css', import.meta.url), 'utf8');

const expectations = [
  [html.includes('viewport-fit=cover'), 'iPad viewport metadata is present'],
  [html.includes('data-action="export"'), 'analytics export control is present'],
  [app.includes('localStorage'), 'analytics uses local-first storage'],
  [app.includes('unknown_queued'), 'unknown-link queue instrumentation is present'],
  [styles.includes('@media (max-width: 840px)'), 'responsive tablet/mobile layout is present']
];

const failures = expectations.filter(([passed]) => !passed).map(([, label]) => label);

if (failures.length > 0) {
  console.error(`Failed MVP checks:\n- ${failures.join('\n- ')}`);
  process.exit(1);
}

console.log(`Passed ${expectations.length} MVP checks.`);
