/**
 * Stage "we did X" into recursion-gate.
 * Rule-based: no LLM. suggested_ix_section comes from simple text cues when present,
 * else from skill_tag default (THINK→IX-A, WRITE→IX-C, WORK→IX-B). Companion gates at review.
 *
 * See docs/project-6week-coding.md Week 2.
 */

const path = require("path");
const { load, createCandidate, saveRecursionGate } = require("../schema/record");


// Default mapping: skill_tag -> { mind_category, suggested_ix_section }
const SKILL_MAP = {
  THINK: { mind_category: "knowledge", suggested_ix_section: "IX-A" },
  WRITE: { mind_category: "personality", suggested_ix_section: "IX-C" },
  WORK: { mind_category: "curiosity", suggested_ix_section: "IX-B" },
};

/**
 * Suggest IX section from raw_text cues when present; otherwise use skill default.
 * Cues: learned/understood/realized → IX-A; curious/wonder/want to try/interested → IX-B;
 * prefer/love/hate/I'm the kind of/voice → IX-C.
 */
function suggestIxFromRawText(raw_text, skill_tag) {
  const t = (raw_text || "").toLowerCase();
  if (/\b(learned|understood|realized|figured out)\b/.test(t)) return { mind_category: "knowledge", suggested_ix_section: "IX-A" };
  if (/\b(curious|wonder|want to try|interested in|interested to)\b/.test(t)) return { mind_category: "curiosity", suggested_ix_section: "IX-B" };
  if (/\b(prefer|love|hate|i'm the kind of|voice|like to work)\b/.test(t)) return { mind_category: "personality", suggested_ix_section: "IX-C" };
  return SKILL_MAP[skill_tag] || SKILL_MAP.THINK;
}

function getRepoRoot() {
  return path.resolve(__dirname, "../..");
}

/**
 * Stage one activity. Append candidate to recursion-gate.json.
 * @param {{ text: string, skill_tag?: string }} input
 * @returns {import("../schema/record").RecursionGateCandidate}
 */
function stageActivity(input, userId = "demo") {
  const repoRoot = getRepoRoot();
  const skill_tag = (input.skill_tag || "THINK").toUpperCase();
  const raw_text = String(input.text || "").trim();
  const { mind_category, suggested_ix_section } = suggestIxFromRawText(raw_text, skill_tag);

  const candidate = createCandidate({
    raw_text,
    skill_tag,
    mind_category,
    suggested_ix_section,
  });

  const { recursionGate } = load(repoRoot, userId);
  recursionGate.push(candidate);
  saveRecursionGate(repoRoot, userId, recursionGate);

  return candidate;
}

/**
 * Get pending candidates from recursion-gate.
 * @param {string} [userId] - User id (default "demo")
 */
function getPendingCandidates(userId = "demo") {
  const repoRoot = getRepoRoot();
  const { recursionGate } = load(repoRoot, userId);
  return recursionGate.filter((c) => c.status === "pending");
}

module.exports = { stageActivity, getPendingCandidates };
