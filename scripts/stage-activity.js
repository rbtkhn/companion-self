#!/usr/bin/env node
/**
 * CLI to stage one activity for testing.
 * Usage: node scripts/stage-activity.js "We drew a dragon" [READ|WRITE|WORK]
 */

const path = require("path");
const { stageActivity } = require(path.join(__dirname, "../app/pipeline/stage"));

const text = process.argv[2];
const skill_tag = process.argv[3] || "READ";

if (!text) {
  console.error("Usage: node scripts/stage-activity.js \"<activity text>\" [READ|WRITE|WORK]");
  process.exit(1);
}

try {
  const candidate = stageActivity({ text, skill_tag });
  console.log("Staged candidate:", candidate.id);
  console.log("  raw_text:", candidate.raw_text);
  console.log("  skill_tag:", candidate.skill_tag);
  console.log("  suggested_ix_section:", candidate.suggested_ix_section);
} catch (err) {
  console.error("Error:", err.message);
  process.exit(1);
}
