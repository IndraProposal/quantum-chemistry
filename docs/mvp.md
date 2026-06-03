# Quantum Chemistry 2048 MVP

Quantum Chemistry 2048 is designed as a paper-first schoolbook with QR codes that open live, continuously updated pages. The initial form factor is an iPad-friendly static web page so a student can move from print to interactive exploration without installing an app.

## MVP pillars

1. **Paper-to-live navigation**: printed QR codes should resolve to stable live-page URLs. The demo page in `live/index.html` represents the canonical destination for the first QR target.
2. **Interactive learning loop**: concept tiles, adaptive hints, and self-exploration graph nodes invite students to keep asking questions after the printed page ends.
3. **Infinite cache contract**: `live/exploration-cache.json` seeds a graph of known trails. Unknown links are queued locally and can later be promoted into the graph by an editorial or automated refresh process.
4. **Local-first analytics**: the browser stores events in `localStorage` and exports snapshots. This keeps the MVP privacy-preserving while still proving that curiosity paths can guide future updates.
5. **CI/CD validation**: workflows run build, tests, and cache validation before live assets are published or pull requests are accepted.

## Production path

- Replace demo QR targets with stable redirect slugs such as `/qr/chapter-01/orbital-2048`.
- Add a consented analytics collector when the school, parent, or publisher requires cross-device reporting.
- Promote queued unknowns into editorial tasks or generated draft trails, then validate them through the cache schema.
- Publish `dist/` to GitHub Pages, S3, Cloudflare Pages, or another static host.
- Keep the paper book durable by making QR links point to evergreen slugs rather than version-specific files.
