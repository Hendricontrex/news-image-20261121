// News image entry: copy the pre-rendered front page to the output dir.
//
// Node 22, stdlib only, no network. The program reads entry.png next to
// this file, refuses anything that is not a 1024x1024 PNG of at most
// 1 MiB, then writes the identical bytes to
// $MAKEFUN_OUTPUT_DIR/entry.png (default /output) and re-reads the
// result to prove the copy landed byte-for-byte.

import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;
const WANT_WIDTH = 1024;
const WANT_HEIGHT = 1024;

function abort(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

function pngDimensions(buf: Buffer): { width: number; height: number } {
  if (buf.length < 24 || !buf.subarray(0, 8).equals(PNG_SIGNATURE)) {
    abort("entry.png is not a PNG file (bad magic bytes)");
  }
  if (buf.toString("ascii", 12, 16) !== "IHDR") {
    abort("entry.png is not a PNG file (missing IHDR chunk)");
  }
  // A well-formed PNG ends with the 12-byte IEND chunk; a truncated file
  // would still carry a valid IHDR, so check the tail too.
  const tail = buf.subarray(buf.length - 12);
  if (tail.readUInt32BE(0) !== 0 || tail.toString("ascii", 4, 8) !== "IEND") {
    abort("entry.png is truncated (missing IEND chunk)");
  }
  return {
    width: buf.readUInt32BE(16),
    height: buf.readUInt32BE(20),
  };
}

async function main(): Promise<void> {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");

  let bytes: Buffer;
  try {
    bytes = await readFile(source);
  } catch {
    abort(`cannot read ${source}`);
  }

  const { width, height } = pngDimensions(bytes);
  if (width !== WANT_WIDTH || height !== WANT_HEIGHT) {
    abort(
      `entry.png is ${width}x${height}, expected ${WANT_WIDTH}x${WANT_HEIGHT}`,
    );
  }
  if (bytes.length > MAX_BYTES) {
    abort(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const target = join(outDir, "entry.png");
  await mkdir(outDir, { recursive: true });
  await writeFile(target, bytes);

  // Prove the copy: re-read and compare against the source bytes.
  const written = await readFile(target);
  if (!written.equals(bytes)) {
    abort(`${target} does not match entry.png after writing`);
  }
  const info = await stat(target);
  console.log(
    `wrote ${target} (${info.size} bytes, ${width}x${height} PNG, verified identical)`,
  );
}

main().catch((err: unknown) => {
  abort(err instanceof Error ? err.message : String(err));
});
