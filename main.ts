// "The World in One Day" — Friday 20 November 2026 (make.fun news-image-20261120).
// Node 22, standard library only. The entry image is drawn by compose.py and
// shipped beside this file as entry.png; this program copies it to the output
// directory the grader gives it (MAKEFUN_OUTPUT_DIR, default /output), then
// verifies the copy byte-for-byte with a SHA-256 integrity self-check so a
// truncated or corrupted write fails loudly instead of reaching the judge.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png is missing next to main.ts; run python3 compose.py first');
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);

// Integrity self-check: the copy must hash identically to the source, and
// stay inside the competition's 1 MiB cap.
const sha256 = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
const want = sha256(src);
const got = sha256(dest);
if (want !== got) {
  throw new Error(`entry.png copy failed integrity check: ${got} != ${want}`);
}
const bytes = readFileSync(dest).length;
if (bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB cap`);
}
console.log(`wrote ${dest} (${bytes} bytes, sha256 ${got})`);
