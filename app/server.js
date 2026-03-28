/**
 * Companion-Self companion app server (local demo).
 * Minimal Express API for pipeline + seed-phase / change-review views.
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

// Allowed users (template: demo only; instances can add users)
let ALLOWED_USERS = ["demo"];
try {
  const configPath = path.join(__dirname, "config", "allowed-users.json");
  if (fs.existsSync(configPath)) {
    ALLOWED_USERS = JSON.parse(fs.readFileSync(configPath, "utf-8"));
  }
} catch (_) {
  // keep default
}

app.use(express.json());

/** Resolve userId from query or header; validate against allowlist. Returns { userId } or throws. */
function resolveUserId(req) {
  const userId = (req.query && req.query.user) || (req.headers && req.headers["x-user-id"]) || "demo";
  if (!ALLOWED_USERS.includes(userId)) {
    const err = new Error("User not in allowed list. Template supports demo only; add users to app/config/allowed-users.json for instances.");
    err.status = 403;
    throw err;
  }
  return userId;
}

// Graceful error message for missing/malformed user dir
function friendlyError(err) {
  if (err.message && err.message.includes("not found")) {
    return "User directory not found. Run from companion-self repo root and ensure users/<id>/ exists. See readme-app.md (companion app how-to).";
  }
  if (err.message && /parse|JSON|malformed/i.test(err.message)) {
    return "User data is malformed. Check users/<id>/ files. See readme-app.md (companion app how-to).";
  }
  return err.message || "Something went wrong.";
}

// --- API ---

/**
 * GET /api/record
 * Returns Record summary: IX-A/IX-B/IX-C, skills, pending count.
 * Optional: ?user=<id> or X-User-Id header (must be in allowed-users.json).
 */
app.get("/api/record", (req, res) => {
  try {
    const userId = resolveUserId(req);
    const { record, recursionGate } = load(REPO_ROOT, userId);
    const pending = recursionGate.filter((c) => c.status === "pending");
    const edge = getEdge(userId);
    res.json({
      knowledge: record.selfKnowledge,
      curiosity: record.selfCuriosity,
      personality: record.selfPersonality,
      skills: {
        THINK: record.selfSkillThink,
        WRITE: record.selfSkillWrite,
        WORK: record.selfSkillWork,
      },
      evidenceCount: record.selfEvidence.length,
      pendingCount: pending.length,
      edge,
    });
  } catch (err) {
    res.status(err.status === 403 ? 403 : 500).json({ error: err.message || friendlyError(err) });
  }
});

/**
 * GET /api/edge
 * Returns suggested next focus per THINK, WRITE, WORK.
 */
app.get("/api/edge", (req, res) => {
  try {
    const userId = resolveUserId(req);
    res.json(getEdge(userId));
  } catch (err) {
    res.status(err.status === 403 ? 403 : 500).json({ error: err.message || friendlyError(err) });
  }
});

/**
 * GET /api/export
 * Returns curriculum profile JSON for tutor/curriculum.
 */
app.get("/api/export", (req, res) => {
  try {
    const userId = resolveUserId(req);
    const profile = buildCurriculumProfile(userId);
    res.setHeader("Content-Type", "application/json");
    res.setHeader("Content-Disposition", "attachment; filename=curriculum-profile.json");
    res.json(profile);
  } catch (err) {
    res.status(500).json({ error: friendlyError(err) });
  }
});

/**
 * POST /api/activity
 * Body: { text: string, skill_tag?: "THINK" | "WRITE" | "WORK" }
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
    const userId = resolveUserId(req);
    const { candidate_id, action } = req.body || {};
    const result = reviewCandidate({ candidate_id, action }, userId);
    res.json(result);
  } catch (err) {
    res.status(err.status === 403 ? 403 : 400).json({ error: err.message });
  }
});

/**
 * GET /api/recursion-gate
 * Returns pending candidates for review UI.
 */
app.get("/api/recursion-gate", (req, res) => {
  try {
    const userId = resolveUserId(req);
    const candidates = getPendingCandidates(userId);
    res.json(candidates);
  } catch (err) {
    res.status(err.status === 403 ? 403 : 500).json({ error: err.message || friendlyError(err) });
  }
});

// --- Health ---

app.get("/api/health", (req, res) => {
  res.json({ ok: true });
});

/**
 * GET /api/seed-phase?profile=demo|template
 * Returns synthetic or scaffold seed-phase JSON bundle for dashboard (not the live Record).
 */
app.get("/api/seed-phase", (req, res) => {
  const profile = (req.query && req.query.profile) || "demo";
  const allowed = new Set(["demo", "template"]);
  if (!allowed.has(profile)) {
    return res.status(400).json({ error: "profile must be demo or template" });
  }
  const base = path.join(REPO_ROOT, "users", profile === "template" ? "_template" : "demo", "seed-phase");
  const names = [
    "seed-phase-manifest.json",
    "seed_intake.json",
    "seed_identity.json",
    "seed_curiosity.json",
    "seed_pedagogy.json",
    "seed_expression.json",
    "seed_memory_contract.json",
    "seed_trial_report.json",
    "seed_readiness.json",
    "seed_confidence_map.json",
    "work_business_seed.json",
    "work_dev_seed.json",
  ];
  const out = { profile, base: path.relative(REPO_ROOT, base), artifacts: {} };
  try {
    for (const n of names) {
      const fp = path.join(base, n);
      if (!fs.existsSync(fp)) {
        out.artifacts[n] = null;
        continue;
      }
      out.artifacts[n] = JSON.parse(fs.readFileSync(fp, "utf-8"));
    }
    const dossierPath = path.join(base, "seed_dossier.md");
    out.dossier_preview = fs.existsSync(dossierPath)
      ? fs.readFileSync(dossierPath, "utf-8").split("\n").slice(0, 25).join("\n")
      : "";
    res.json(out);
  } catch (err) {
    res.status(500).json({ error: err.message || "Failed to load seed-phase bundle" });
  }
});

/**
 * GET /api/change-review?profile=demo|template
 * Loads users/<demo|_template>/review-queue/ (queue, event log, proposals/, decisions/, diffs/).
 */
function loadReviewQueueBundle(profile) {
  const userDir = profile === "template" ? "_template" : "demo";
  const base = path.join(REPO_ROOT, "users", userDir, "review-queue");
  if (!fs.existsSync(base)) {
    return { error: "review-queue not found: " + path.relative(REPO_ROOT, base) };
  }
  const readJson = (rel) => {
    const fp = path.join(base, rel);
    if (!fs.existsSync(fp)) return null;
    return JSON.parse(fs.readFileSync(fp, "utf-8"));
  };
  const readDirObjects = (sub) => {
    const dir = path.join(base, sub);
    if (!fs.existsSync(dir)) return [];
    return fs
      .readdirSync(dir)
      .filter((f) => f.endsWith(".json"))
      .sort()
      .map((f) => {
        const fp = path.join(dir, f);
        return { file: f, ...JSON.parse(fs.readFileSync(fp, "utf-8")) };
      });
  };
  const readmePath = path.join(base, "README.md");
  const readme_preview = fs.existsSync(readmePath)
    ? fs.readFileSync(readmePath, "utf-8").split("\n").slice(0, 15).join("\n")
    : "";
  return {
    profile,
    base: path.relative(REPO_ROOT, base),
    queue: readJson("change_review_queue.json"),
    eventLog: readJson("change_event_log.json"),
    proposals: readDirObjects("proposals"),
    decisions: readDirObjects("decisions"),
    diffs: readDirObjects("diffs"),
    readme_preview,
  };
}

app.get("/api/change-review", (req, res) => {
  const profile = (req.query && req.query.profile) || "demo";
  const allowed = new Set(["demo", "template"]);
  if (!allowed.has(profile)) {
    return res.status(400).json({ error: "profile must be demo or template" });
  }
  try {
    const out = loadReviewQueueBundle(profile);
    if (out.error) {
      return res.status(404).json({ error: out.error });
    }
    res.json(out);
  } catch (err) {
    res.status(500).json({ error: err.message || "Failed to load change-review bundle" });
  }
});

/**
 * GET /api/change-review/summary?profile=demo|template
 * Compact counts + latest decision / diff for dashboard widgets.
 */
app.get("/api/change-review/summary", (req, res) => {
  const profile = (req.query && req.query.profile) || "demo";
  const allowed = new Set(["demo", "template"]);
  if (!allowed.has(profile)) {
    return res.status(400).json({ error: "profile must be demo or template" });
  }
  try {
    const bundle = loadReviewQueueBundle(profile);
    if (bundle.error) {
      return res.status(404).json({ error: bundle.error });
    }
    const decisions = bundle.decisions || [];
    const latestDecision =
      decisions.length === 0
        ? null
        : decisions.reduce((best, d) => {
            const t = d.decidedAt || "";
            const bt = best.decidedAt || "";
            return t >= bt ? d : best;
          });
    const diffs = bundle.diffs || [];
    const latestDiff = diffs.length === 0 ? null : diffs[0];
    const queueItems = (bundle.queue && bundle.queue.items) || [];
    const events = (bundle.eventLog && bundle.eventLog.events) || [];
    res.json({
      profile,
      base: bundle.base,
      counts: {
        proposals: bundle.proposals.length,
        decisions: decisions.length,
        diffs: diffs.length,
        queueItems: queueItems.length,
        events: events.length,
      },
      latestDecision,
      latestDiff,
    });
  } catch (err) {
    res.status(500).json({ error: err.message || "Failed to load change-review summary" });
  }
});

// --- Static ---

const publicDir = path.join(__dirname, "public");
app.use(express.static(publicDir));

// Serve HTML pages at clean routes
app.get("/", (req, res) => res.sendFile(path.join(publicDir, "index.html")));
app.get("/activity", (req, res) => res.sendFile(path.join(publicDir, "activity.html")));
app.get("/review", (req, res) => res.sendFile(path.join(publicDir, "review.html")));
app.get("/export", (req, res) => res.sendFile(path.join(publicDir, "export.html")));
app.get("/seed-phase", (req, res) => res.sendFile(path.join(publicDir, "seed-phase.html")));
app.get("/change-review", (req, res) => res.sendFile(path.join(publicDir, "change-review.html")));

const demoDir = path.join(REPO_ROOT, "users", "demo");
if (!fs.existsSync(demoDir)) {
  console.warn("Warning: users/demo/ not found. API will return errors until demo user exists. See readme-app.md (companion app how-to).");
}
// User resolution: ?user=<id> or X-User-Id header; must be in app/config/allowed-users.json (default ["demo"]).

app.listen(PORT, () => {
  console.log(`Companion-Self app at http://localhost:${PORT}`);
});
