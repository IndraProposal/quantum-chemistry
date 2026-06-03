# Quantum Chemistry 2048

Quantum Chemistry 2048 is an MVP for an interactive schoolbook that can exist as a paper book while staying alive through QR-linked web pages. A printed page can point to an iPad-friendly lesson, dynamic hints, analytics snapshots, and self-exploration trails that continue to evolve after the physical book is shipped.

## What is included

- `live/index.html` — the first live page for the QR-linked schoolbook experience.
- `live/assets/app.js` — local-first analytics, hint interactions, unknown-link queueing, and exploration graph rendering.
- `live/exploration-cache.json` — the seed cache for continuous exploration trails.
- `scripts/validate-cache.mjs` — validates graph integrity so every exploration link resolves.
- `scripts/build.mjs` — copies live-page assets into `dist/` and writes a hashed artifact manifest.
- `.github/workflows/ci.yml` — CI for cache validation, MVP tests, and live-page artifact builds.
- `.github/workflows/deploy.yml` — CD for publishing the built live pages to GitHub Pages.
- `.github/workflows/auto_update.yml` — scheduled update automation for future content refreshes.

## MVP goals

1. Demonstrate a paper-to-live bridge for an Amazon-ready schoolbook with QR codes.
2. Prove an iPad-first live page can support interactive Quantum Chemistry 2048 content.
3. Capture privacy-preserving analytics locally before any hosted collector exists.
4. Maintain a self-exploration graph as an "infinite cache" of known and unknown learning trails.
5. Ship with CI/CD checks that protect the cache and build the live-page artifact.

## Run locally

```bash
npm run validate:cache
npm test
npm run build
python3 -m http.server 8080 --directory live
```

Then open <http://localhost:8080> on an iPad, browser, or simulator.

## Documentation

See [`docs/mvp.md`](docs/mvp.md) for the product architecture, production path, and QR publishing notes.
