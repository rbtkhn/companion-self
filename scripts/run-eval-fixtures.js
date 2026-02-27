#!/usr/bin/env node
/**
 * Run evaluation fixtures: stage and merge against users/eval-fixture, assert outcomes.
 * Exit 0 if all pass; non-zero on first failure.
 *
 * See docs/evaluation-design-and-regression.md.
 */

const path = require("path");
const fs = require("fs");

const REPO_ROOT = path.resolve(__dirname, "..");
const FIXTURE_USER = "eval-fixture";
const USER_DIR = path.join(REPO_ROOT, "users", FIXTURE_USER);

// Load record module (from app/schema/record.js)
const {
  load,
  createCandidate,
  saveRecursionGate,
  mergeCandidate,
  SKILL_TAGS,
  IX_SECTIONS,
} = require("../app/schema/record");

function ensureFixtureUser() {
  if (!fs.existsSync(USER_DIR)) {
    fs.mkdirSync(USER_DIR, { recursive: true });
  }
  const files = [
    "self.md",
    "self-knowledge.md",
    "self-curiosity.md",
    "self-personality.md",
    "self-skill-think.md",
    "self-skill-write.md",
    "self-skill-work.md",
    "self-evidence.md",
  ];
  for (const f of files) {
    const p = path.join(USER_DIR, f);
    if (!fs.existsSync(p)) fs.writeFileSync(p, "", "utf-8");
  }
  const gatePath = path.join(USER_DIR, "recursion-gate.json");
  if (!fs.existsSync(gatePath)) fs.writeFileSync(gatePath, "[]", "utf-8");
}

function assert(condition, message) {
  if (!condition) {
    console.error("Assertion failed:", message);
    process.exit(1);
  }
}

function run() {
  ensureFixtureUser();

  // Start with empty gate
  saveRecursionGate(REPO_ROOT, FIXTURE_USER, []);

  // --- Fixture 1 & 2: stage two activities ---
  const c1 = createCandidate({
    raw_text: "Read chapter 2 of Dragon Guide; summarized migration habits.",
    skill_tag: "THINK",
    mind_category: "knowledge",
    suggested_ix_section: "IX-A",
  });
  const c2 = createCandidate({
    raw_text: "Finished the dragon drawing; used watercolors.",
    skill_tag: "WORK",
    mind_category: "curiosity",
    suggested_ix_section: "IX-B",
  });
  let data = load(REPO_ROOT, FIXTURE_USER);
  data.recursionGate.push(c1, c2);
  saveRecursionGate(REPO_ROOT, FIXTURE_USER, data.recursionGate);

  data = load(REPO_ROOT, FIXTURE_USER);
  assert(data.recursionGate.length === 2, "gate has 2 candidates after stage");
  assert(data.recursionGate[0].skill_tag === "THINK" && data.recursionGate[0].suggested_ix_section === "IX-A", "THINK candidate has IX-A");
  assert(data.recursionGate[1].skill_tag === "WORK" && data.recursionGate[1].suggested_ix_section === "IX-B", "WORK candidate has IX-B");

  const evidenceCountBefore = (data.record.selfEvidence || []).length;
  const knowledgeBefore = (data.record.selfKnowledge || []).length;
  const curiosityBefore = (data.record.selfCuriosity || []).length;

  // --- Approve first candidate (THINK → IX-A) ---
  mergeCandidate(REPO_ROOT, FIXTURE_USER, data.recursionGate[0], data);

  data = load(REPO_ROOT, FIXTURE_USER);
  assert(data.recursionGate.length === 1, "gate has 1 candidate after one approve");
  assert(data.record.selfEvidence.length === evidenceCountBefore + 1, "one new evidence entry");
  assert(data.record.selfKnowledge.length === knowledgeBefore + 1, "one new IX-A line");
  assert(data.record.selfCuriosity.length === curiosityBefore, "IX-B unchanged after first approve");

  // --- Reject second candidate ---
  const next = data.recursionGate.filter((c) => c.id !== data.recursionGate[0].id);
  saveRecursionGate(REPO_ROOT, FIXTURE_USER, next);

  data = load(REPO_ROOT, FIXTURE_USER);
  assert(data.recursionGate.length === 0, "gate empty after reject");
  assert(data.record.selfEvidence.length === evidenceCountBefore + 1, "evidence unchanged after reject");

  console.log("run-eval-fixtures: all assertions passed.");
}

run();
