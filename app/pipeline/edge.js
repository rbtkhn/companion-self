/**
 * Edge derivation: suggested next focus per THINK, WRITE, WORK.
 * Rule-based; no LLM. WORK uses self-personality (IX-C) for phrasing.
 *
 * See docs/schema-record-api.md and CONCEPT §4.
 */

const { load } = require("../schema/record");

const REPO_ROOT = require("path").resolve(__dirname, "../..");

/**
 * Derive edge (what's next) from Record.
 * @param {{ record, recursionGate }} data - from load()
 * @returns {{ THINK: string, WRITE: string, WORK: string }}
 */
function deriveEdge(data) {
  const { record } = data;
  const k = record.selfKnowledge || [];
  const c = record.selfCuriosity || [];
  const p = record.selfPersonality || [];
  const evidence = record.selfEvidence || [];

  const thinkEvidence = evidence.filter((e) => e.skill_tag === "THINK");
  const writeEvidence = evidence.filter((e) => e.skill_tag === "WRITE");
  const workEvidence = evidence.filter((e) => e.skill_tag === "WORK");

  // THINK: last topic from IX-A or IX-B, or default
  const THINK =
    k.length > 0
      ? `Continue with: ${k[k.length - 1].replace(/ — .*$/, "").trim()}`
      : c.length > 0
        ? `Explore: ${c[c.length - 1].replace(/ — .*$/, "").trim()}`
        : "Keep reading";

  // WRITE: last WRITE evidence or default
  const WRITE =
    writeEvidence.length > 0
      ? `Build on: "${writeEvidence[writeEvidence.length - 1].summary.slice(0, 40)}${writeEvidence[writeEvidence.length - 1].summary.length > 40 ? "…" : ""}"`
      : "Try a short story or journal entry";

  // WORK: use IX-C (self-personality) for phrasing where possible
  const personalityHint = p.length > 0 ? p[p.length - 1].replace(/ — .*$/, "").trim() : "";
  const WORK =
    personalityHint && /playful|ship|small|quick|one/.test(personalityHint.toLowerCase())
      ? "One small project—ship something you enjoy"
      : workEvidence.length > 0
        ? `Next: build on "${workEvidence[workEvidence.length - 1].summary.slice(0, 30)}…"`
        : "One small project";

  return { THINK, WRITE, WORK };
}

/**
 * Get edge for a user.
 * @param {string} [userId] - User id (default "demo")
 */
function getEdge(userId = "demo") {
  const data = load(REPO_ROOT, userId);
  return deriveEdge(data);
}

module.exports = { deriveEdge, getEdge };
