/**
 * Stage "we did X" into recursion-gate.
 * Rule-based: no LLM; skill_tag drives mind_category and suggested_ix_section.
 *
 * See docs/project-6week-coding.md Week 2.
 */

const path = require("path");
const { load, createCandidate, saveRecursionGate } = require("../schema/record");

const DEMO_USER = "demo";

// Rule-based mapping: skill_tag -> { mind_category, suggested_ix_section }
const SKILL_MAP = {
  THINK: { mind_category: "knowledge", suggested_ix_section: "IX-A" },
  WRITE: { mind_category: "personality", suggested_ix_section: "IX-C" },
  WORK: { mind_category: "curiosity", suggested_ix_section: "IX-B" },
};

function getRepoRoot() {
  return path.resolve(__dirname, "../..");
}

/**
 * Stage one activity. Append candidate to recursion-gate.json.
 * @param {{ text: string, skill_tag?: string }} input
 * @returns {import("../schema/record").RecursionGateCandidate}
 */
function stageActivity(input) {
  const repoRoot = getRepoRoot();
  const skill_tag = (input.skill_tag || "THINK").toUpperCase();
  const { mind_category, suggested_ix_section } = SKILL_MAP[skill_tag] || SKILL_MAP.THINK;

  const candidate = createCandidate({
    raw_text: String(input.text || "").trim(),
    skill_tag,
    mind_category,
    suggested_ix_section,
  });

  const { recursionGate } = load(repoRoot, DEMO_USER);
  recursionGate.push(candidate);
  saveRecursionGate(repoRoot, DEMO_USER, recursionGate);

  return candidate;
}

/**
 * Get pending candidates from recursion-gate.
 */
function getPendingCandidates() {
  const repoRoot = getRepoRoot();
  const { recursionGate } = load(repoRoot, DEMO_USER);
  return recursionGate.filter((c) => c.status === "pending");
}

module.exports = { stageActivity, getPendingCandidates };
