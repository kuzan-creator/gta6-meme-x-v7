// Leonida Impound Lot — GTA VI meme entry (program/v1).
// Copies the finished entry files into the output directory.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const FILES = [
  "meme.png",
  "meme.jpg",
  "draw_meme.py",
  "POST.json",
  "README.md",
  "LICENSE",
];

mkdirSync(OUT, { recursive: true });
for (const name of FILES) {
  const src = join(HERE, name);
  if (!existsSync(src)) {
    throw new Error(`missing entry file: ${src}`);
  }
  copyFileSync(src, join(OUT, name));
}
console.log(`copied ${FILES.length} files to ${OUT}`);
