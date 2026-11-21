// news-image-20261121 — "The day in five stories", Saturday 21 November 2026.
//
// This program is the whole entry: it writes one image to
// /output/entry.png. The image is a newspaper front page — masthead
// with the day, then the five stories that led Saturday 21 November
// 2026 (the Friday market plunge, Russia's mass strike on Ukraine
// with missiles landing in Poland, Mexico's capture of "El Chapo
// Isidro", the FBI's probe into a breach of its national crime
// database, and the daraxonrasib pancreatic-cancer pill trial) — and
// it lives in this repository as entry.png.
//
// The copy is byte-for-byte and uses no network, so running the
// program twice writes the same bytes twice. Before copying, the
// program checks the file really is a PNG of at most 1 MiB and
// 1024 by 1024 pixels, and fails loudly instead of handing the
// grader a broken file.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1048576;
const MAX_EDGE = 1024;
const SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function fail(message) {
  throw new Error(`entry.png rejected: ${message}`);
}

function run() {
  const here = new URL(".", import.meta.url).pathname;
  const source = join(here, "entry.png");
  const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const dest = join(destDir, "entry.png");

  const image = readFileSync(source);
  if (image.length > MAX_BYTES) {
    fail(`is ${image.length} bytes, over the 1 MiB limit`);
  }
  for (let i = 0; i < SIGNATURE.length; i++) {
    if (image[i] !== SIGNATURE[i]) fail("is not a PNG file");
  }
  // The IHDR chunk starts at byte 16: width then height, big-endian.
  const width = image.readUInt32BE(16);
  const height = image.readUInt32BE(20);
  if (width > MAX_EDGE || height > MAX_EDGE) {
    fail(`is ${width}x${height}, over the 1024 by 1024 limit`);
  }

  mkdirSync(destDir, { recursive: true });
  writeFileSync(dest, image);
  console.log(`wrote ${dest} (${image.length} bytes)`);
}

run();
