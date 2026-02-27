/**
 * Companion-Self student interface server.
 * Minimal Express API for Week 2 pipeline.
 *
 * Run: node server.js  (or npm start from app/)
 * App at http://localhost:3000
 */

const express = require("express");
const path = require("path");
const { load } = require("./schema/record");
const { stageActivity, getPendingCandidates } = require("./pipeline/stage");
const { reviewCandidate } = require("./pipeline/merge");
const { getEdge } = require("./pipeline/edge");
const { buildCurriculumProfile } = require("./export/curriculum-profile");

const fs = require("fs");
const app = express();
const REPO_ROOT = path.resolve(__dirname, "..");
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Graceful error message for missing/malformed users/demo/
function friendlyError(err) {
  if (err.message && err.message.includes("not found")) {
    return "Demo user not found. Run from companion-self repo root and ensure users/demo/ exists. See readme-student-app.md.";
  }
  if (err.message && /parse|JSON|malformed/i.test(err.message)) {
    return "Demo data is malformed. Check users/demo/ files. See readme-student-app.md.";
  }
  return err.message || "Something went wrong.";
}

// --- API ---

/**
 * GET /api/record
 * Returns Record summary for demo user: IX-A/IX-B/IX-C, skills, pending count.
 */
app.get("/api/record", (req, res) => {
  try {
    const { record, recursionGate } = load(REPO_ROOT, "demo");
    const pending = recursionGate.filter((c) => c.status === "pending");
    const edge = getEdge();
    res.json({
      knowledge: record.selfKnowledge,
      curiosity: record.selfCuriosity,
      personality: record.selfPersonality,
      skills: {
        READ: record.selfSkillRead,
        WRITE: record.selfSkillWrite,
        WORK: record.selfSkillWork,
      },
      evidenceCount: record.selfEvidence.length,
      pendingCount: pending.length,
      edge,
    });
  } catch (err) {
    res.status(500).json({ error: friendlyError(err) });
  }
});

/**
 * GET /api/edge
 * Returns suggested next focus per READ, WRITE, WORK.
 */
app.get("/api/edge", (req, res) => {
  try {
    res.json(getEdge());
  } catch (err) {
    res.status(500).json({ error: friendlyError(err) });
  }
});

/**
 * GET /api/export
 * Returns curriculum profile JSON for tutor/curriculum.
 */
app.get("/api/export", (req, res) => {
  try {
    const profile = buildCurriculumProfile();
    res.setHeader("Content-Type", "application/json");
    res.setHeader("Content-Disposition", "attachment; filename=curriculum-profile.json");
    res.json(profile);
  } catch (err) {
    res.status(500).json({ error: friendlyError(err) });
  }
});

/**
 * POST /api/activity
 * Body: { text: string, skill_tag?: "READ" | "WRITE" | "WORK" }
 * Creates candidate, appends to recursion-gate.json.
 */
app.post("/api/activity", (req, res) => {
  try {
    const { text, skill_tag } = req.body || {};
    if (!text || typeof text !== "string" || !text.trim()) {
      return res.status(400).json({ error: "text is required" });
    }
    const candidate = stageActivity({ text: text.trim(), skill_tag });
    res.status(201).json(candidate);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

/**
 * POST /api/review
 * Body: { candidate_id: string, action: "approve" | "reject" }
 * Approve: merge into Record, remove from gate. Reject: remove from gate only.
 */
app.post("/api/review", (req, res) => {
  try {
    const { candidate_id, action } = req.body || {};
    const result = reviewCandidate({ candidate_id, action });
    res.json(result);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

/**
 * GET /api/recursion-gate
 * Returns pending candidates for review UI.
 */
app.get("/api/recursion-gate", (req, res) => {
  try {
    const candidates = getPendingCandidates();
    res.json(candidates);
  } catch (err) {
    res.status(500).json({ error: friendlyError(err) });
  }
});

// --- Health ---

app.get("/api/health", (req, res) => {
  res.json({ ok: true });
});

// --- Static ---

const publicDir = path.join(__dirname, "public");
app.use(express.static(publicDir));

// Serve HTML pages at clean routes
app.get("/", (req, res) => res.sendFile(path.join(publicDir, "index.html")));
app.get("/activity", (req, res) => res.sendFile(path.join(publicDir, "activity.html")));
app.get("/review", (req, res) => res.sendFile(path.join(publicDir, "review.html")));
app.get("/export", (req, res) => res.sendFile(path.join(publicDir, "export.html")));

const demoDir = path.join(REPO_ROOT, "users", "demo");
if (!fs.existsSync(demoDir)) {
  console.warn("Warning: users/demo/ not found. API will return errors until demo user exists. See readme-student-app.md.");
}

app.listen(PORT, () => {
  console.log(`Companion-Self app at http://localhost:${PORT}`);
});
