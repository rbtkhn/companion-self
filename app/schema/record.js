/**
 * Record schema and recursion-gate types.
 * Load/save demo user from users/<id>/*.md + recursion-gate.json.
 *
 * See docs/schema-record-api.md for API contract.
 */

const fs = require("fs");
const path = require("path");

// --- Types (runtime validation) ---

const SKILL_TAGS = ["READ", "WRITE", "WORK"];
const IX_SECTIONS = ["IX-A", "IX-B", "IX-C"];
const MIND_CATEGORIES = ["knowledge", "curiosity", "personality"];

/**
 * @typedef {Object} Record
 * @property {string} self - Raw self.md content or parsed baseline
 * @property {string[]} selfKnowledge - IX-A entries (one per line)
 * @property {string[]} selfCuriosity - IX-B entries (one per line)
 * @property {string[]} selfPersonality - IX-C entries (one per line)
 * @property {string[]} selfSkillRead - READ entries
 * @property {string[]} selfSkillWrite - WRITE entries
 * @property {string[]} selfSkillWork - WORK entries
 * @property {EvidenceEntry[]} selfEvidence - Activity log entries
 */

/**
 * @typedef {Object} EvidenceEntry
 * @property {string} id - e.g. ACT-XXXX
 * @property {string} date - ISO date
 * @property {string} summary - Short description
 * @property {string} skill_tag - READ | WRITE | WORK
 */

/**
 * @typedef {Object} RecursionGateCandidate
 * @property {string} id - Unique id (uuid or timestamp)
 * @property {string} raw_text - Raw "we did X" or activity text
 * @property {string} skill_tag - READ, WRITE, or WORK
 * @property {string} mind_category - knowledge, curiosity, or personality
 * @property {string} suggested_ix_section - IX-A, IX-B, or IX-C
 * @property {string} created_at - ISO date or timestamp
 * @property {string} status - "pending" until approved/rejected
 */

// --- Parsing helpers ---

/**
 * Extract bullet-list entries from markdown (lines starting with "- " or "- • ").
 * Returns trimmed content, excluding empty lines and template placeholders.
 */
function parseBulletList(content) {
  if (!content || typeof content !== "string") return [];
  return content
    .split(/\r?\n/)
    .map((line) => {
      const m = line.match(/^-\s*(?:•\s*)?(.+)$/);
      return m ? m[1].trim() : null;
    })
    .filter((s) => s && s !== "(e.g." && !s.startsWith("(Placeholder") && !/^[.\-]+$/.test(s));
}

/**
 * Parse self-evidence.md Activity Log section for entries with id, date, summary, skill_tag.
 * Format: "- ACT-XXXX — summary — YYYY-MM-DD — READ|WRITE|WORK"
 * Or simpler: "- id: summary (date, skill_tag)"
 * We use: "- ACT-XXXX | summary | date | skill_tag" for machine-readable.
 * Fallback: treat lines as freeform if no strict format.
 */
function parseEvidenceEntries(content) {
  if (!content || typeof content !== "string") return [];
  const entries = [];
  const lines = content.split(/\r?\n/);
  for (const line of lines) {
    const m = line.match(/^-\s*(ACT-\w+)\s*[—|-]\s*(.+?)\s*[—|-]\s*(\d{4}-\d{2}-\d{2})\s*[—|-]\s*(READ|WRITE|WORK)\s*$/i);
    if (m) {
      entries.push({ id: m[1], summary: m[2].trim(), date: m[3], skill_tag: m[4].toUpperCase() });
    }
  }
  return entries;
}

// --- Load ---

/**
 * Load Record from users/<id>/ directory.
 * @param {string} repoRoot - Path to companion-self repo root
 * @param {string} userId - e.g. "demo"
 * @returns {{ record: Record, recursionGate: RecursionGateCandidate[] }}
 */
function load(repoRoot, userId = "demo") {
  const userDir = path.join(repoRoot, "users", userId);
  if (!fs.existsSync(userDir)) {
    throw new Error(`users/${userId}/ not found`);
  }

  const read = (file) => {
    const p = path.join(userDir, file);
    return fs.existsSync(p) ? fs.readFileSync(p, "utf-8") : "";
  };

  const selfKnowledge = parseBulletList(read("self-knowledge.md"));
  const selfCuriosity = parseBulletList(read("self-curiosity.md"));
  const selfPersonality = parseBulletList(read("self-personality.md"));
  const selfSkillRead = parseBulletList(read("self-skill-read.md"));
  const selfSkillWrite = parseBulletList(read("self-skill-write.md"));
  const selfSkillWork = parseBulletList(read("self-skill-work.md"));
  const selfEvidence = parseEvidenceEntries(read("self-evidence.md"));

  let recursionGate = [];
  const gatePath = path.join(userDir, "recursion-gate.json");
  if (fs.existsSync(gatePath)) {
    try {
      recursionGate = JSON.parse(fs.readFileSync(gatePath, "utf-8"));
    } catch (_) {
      recursionGate = [];
    }
  }

  return {
    record: {
      self: read("self.md"),
      selfKnowledge,
      selfCuriosity,
      selfPersonality,
      selfSkillRead,
      selfSkillWrite,
      selfSkillWork,
      selfEvidence,
    },
    recursionGate,
  };
}

// --- Save (for merge) ---

/**
 * Append a bullet line to a section in a markdown file.
 * Uses simple append to "## Section" or creates section if missing.
 */
function appendBulletToFile(filePath, sectionHeader, bulletText) {
  let content = "";
  if (fs.existsSync(filePath)) {
    content = fs.readFileSync(filePath, "utf-8");
  }
  // Ensure section exists and append
  if (!content.includes(sectionHeader)) {
    content += `\n\n## ${sectionHeader}\n\n`;
  }
  const line = `- • ${bulletText}\n`;
  if (!content.endsWith("\n")) content += "\n";
  content += line;
  fs.writeFileSync(filePath, content, "utf-8");
}

/**
 * Append evidence entry to self-evidence.md Activity Log.
 */
function appendEvidenceEntry(filePath, entry) {
  let content = "";
  if (fs.existsSync(filePath)) {
    content = fs.readFileSync(filePath, "utf-8");
  }
  // Ensure Activity Log section
  if (!content.includes("## Activity Log")) {
    content += "\n\n## Activity Log\n\n";
  }
  const line = `- ${entry.id} — ${entry.summary} — ${entry.date} — ${entry.skill_tag}\n`;
  content += line;
  fs.writeFileSync(filePath, content, "utf-8");
}

/**
 * Save recursion-gate.json (replace entire file).
 */
function saveRecursionGate(repoRoot, userId, candidates) {
  const p = path.join(repoRoot, "users", userId, "recursion-gate.json");
  fs.writeFileSync(p, JSON.stringify(candidates, null, 2), "utf-8");
}

/**
 * Merge approved candidate into Record and remove from gate.
 * Called by pipeline/merge.js; exposed here for schema ownership.
 *
 * @param {string} repoRoot
 * @param {string} userId
 * @param {RecursionGateCandidate} candidate
 * @param {{ record: Record, recursionGate: RecursionGateCandidate[] }} data - from load()
 */
function mergeCandidate(repoRoot, userId, candidate, data) {
  const userDir = path.join(repoRoot, "users", userId);
  const today = new Date().toISOString().slice(0, 10);
  const suffix = candidate.id.split("-").pop() || candidate.id.slice(-8).replace(/\D/g, "");
  const evidenceId = `ACT-${suffix}`;

  // 1. Append to self-evidence
  const evidencePath = path.join(userDir, "self-evidence.md");
  appendEvidenceEntry(evidencePath, {
    id: evidenceId,
    summary: candidate.raw_text,
    date: candidate.created_at.slice(0, 10) || today,
    skill_tag: candidate.skill_tag,
  });

  // 2. Append to dimension file from suggested_ix_section
  const sectionMap = { "IX-A": "self-knowledge.md", "IX-B": "self-curiosity.md", "IX-C": "self-personality.md" };
  const dimFile = sectionMap[candidate.suggested_ix_section];
  if (dimFile) {
    const dimPath = path.join(userDir, dimFile);
    const sectionHeader = candidate.suggested_ix_section === "IX-A" ? "Topics / Understanding" : candidate.suggested_ix_section === "IX-B" ? "Interests" : "Observed Voice / Expression";
    appendBulletToFile(dimPath, sectionHeader, `${candidate.raw_text} — ${evidenceId}`);
  }

  // 3. Remove from gate
  const next = data.recursionGate.filter((c) => c.id !== candidate.id);
  saveRecursionGate(repoRoot, userId, next);
}

// --- Validation ---

function validateSkillTag(tag) {
  if (!SKILL_TAGS.includes(tag)) throw new Error(`skill_tag must be one of ${SKILL_TAGS.join(", ")}`);
}

function validateIxSection(section) {
  if (!IX_SECTIONS.includes(section)) throw new Error(`suggested_ix_section must be one of ${IX_SECTIONS.join(", ")}`);
}

function validateMindCategory(cat) {
  if (!MIND_CATEGORIES.includes(cat)) throw new Error(`mind_category must be one of ${MIND_CATEGORIES.join(", ")}`);
}

/**
 * Create a new recursion-gate candidate.
 */
function createCandidate({ raw_text, skill_tag, mind_category = "curiosity", suggested_ix_section = "IX-B" }) {
  validateSkillTag(skill_tag);
  validateIxSection(suggested_ix_section);
  validateMindCategory(mind_category);
  const id = `cand-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
  return {
    id,
    raw_text,
    skill_tag,
    mind_category,
    suggested_ix_section,
    created_at: new Date().toISOString(),
    status: "pending",
  };
}

// --- CLI test ---

if (require.main === module) {
  const repoRoot = path.resolve(__dirname, "../..");
  try {
    const { record, recursionGate } = load(repoRoot, "demo");
    console.log("Loaded Record:");
    console.log("  selfKnowledge:", record.selfKnowledge.length, "entries");
    console.log("  selfCuriosity:", record.selfCuriosity.length, "entries");
    console.log("  selfPersonality:", record.selfPersonality.length, "entries");
    console.log("  selfEvidence:", record.selfEvidence.length, "entries");
    console.log("  recursionGate:", recursionGate.length, "candidates");
    console.log("\n✓ Load OK");
  } catch (err) {
    console.error("Load failed:", err.message);
    process.exit(1);
  }
}

module.exports = {
  load,
  saveRecursionGate,
  mergeCandidate,
  createCandidate,
  parseBulletList,
  parseEvidenceEntries,
  SKILL_TAGS,
  IX_SECTIONS,
  MIND_CATEGORIES,
};
