#!/usr/bin/env node
/**
 * Validate evidence cross-links: every ACT-* referenced in IX and skill files
 * must exist in self-evidence.md. Reports orphans (referenced but not in evidence).
 *
 * Usage: node scripts/validate-evidence-links.js [userId]
 * Default userId: demo
 * Exit 0 if valid; 1 if orphan refs found.
 *
 * See docs/feedback-template-repo-evaluation.md (Action D1).
 */

const path = require("path");
const fs = require("fs");

const REPO_ROOT = path.resolve(__dirname, "..");
const USER_ID = process.argv[2] || "demo";
const USER_DIR = path.join(REPO_ROOT, "users", USER_ID);

function parseEvidenceIds(content) {
  if (!content || typeof content !== "string") return [];
  const ids = [];
  const re = /\b(ACT-[A-Za-z0-9\-]+)\b/g;
  let m;
  while ((m = re.exec(content)) !== null) ids.push(m[1]);
  return [...new Set(ids)];
}

function readFile(relPath) {
  const p = path.join(USER_DIR, relPath);
  return fs.existsSync(p) ? fs.readFileSync(p, "utf-8") : "";
}

function main() {
  if (!fs.existsSync(USER_DIR)) {
    console.error(`users/${USER_ID}/ not found`);
    process.exit(1);
  }

  const evidenceContent = readFile("self-evidence.md");
  const evidenceIds = new Set(parseEvidenceIds(evidenceContent));

  const refFiles = [
    "self-knowledge.md",
    "self-curiosity.md",
    "self-personality.md",
    "self-skill-think.md",
    "self-skill-write.md",
    "self-skill-work.md",
  ];

  const referencedIds = new Set();
  for (const file of refFiles) {
    const content = readFile(file);
    for (const id of parseEvidenceIds(content)) referencedIds.add(id);
  }

  const orphans = [...referencedIds].filter((id) => !evidenceIds.has(id));
  if (orphans.length > 0) {
    console.error(`Orphan ACT-* references (in IX/skill files but not in self-evidence.md): ${orphans.join(", ")}`);
    process.exit(1);
  }

  console.log(`validate-evidence-links: all ACT-* refs in users/${USER_ID} resolve.`);
}

main();
