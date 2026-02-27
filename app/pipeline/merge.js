/**
 * Review (approve/reject) recursion-gate candidates.
 * Approve: merge into Record and self-evidence; remove from gate.
 * Reject: remove from gate only.
 *
 * See docs/project-6week-coding.md Week 4.
 */

const path = require("path");
const fs = require("fs");
const { load, mergeCandidate, saveRecursionGate } = require("../schema/record");

const DEMO_USER = "demo";

function getRepoRoot() {
  return path.resolve(__dirname, "../..");
}

/**
 * Review one candidate. Approve merges into Record; reject removes from gate.
 * @param {{ candidate_id: string, action: "approve" | "reject" }} input
 * @returns {{ ok: boolean, merged?: boolean }}
 */
function reviewCandidate(input) {
  const repoRoot = getRepoRoot();
  const { candidate_id, action } = input;

  if (!candidate_id || typeof candidate_id !== "string" || !candidate_id.trim()) {
    throw new Error("candidate_id is required");
  }
  if (!["approve", "reject"].includes(action)) {
    throw new Error("action must be approve or reject");
  }

  const data = load(repoRoot, DEMO_USER);
  const candidate = data.recursionGate.find((c) => c.id === candidate_id);
  if (!candidate) {
    throw new Error("candidate not found");
  }

  if (action === "reject") {
    const next = data.recursionGate.filter((c) => c.id !== candidate_id);
    saveRecursionGate(repoRoot, DEMO_USER, next);
    return { ok: true, merged: false };
  }

  // approve
  mergeCandidate(repoRoot, DEMO_USER, candidate, data);

  // Optional: merge receipt log (Week 4.4)
  const receiptPath = path.join(repoRoot, "users", DEMO_USER, "merge-receipts.jsonl");
  const line = JSON.stringify({
    candidate_id: candidate.id,
    raw_text: candidate.raw_text,
    suggested_ix_section: candidate.suggested_ix_section,
    merged_at: new Date().toISOString(),
  }) + "\n";
  fs.appendFileSync(receiptPath, line, "utf-8");

  return { ok: true, merged: true };
}

module.exports = { reviewCandidate };
