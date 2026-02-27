/**
 * Build curriculum_profile from Record, edge, evidence count, export date.
 * GET /api/export returns this JSON for tutor/curriculum.
 *
 * See docs/project-6week-coding.md Week 5.
 */

const path = require("path");
const { load } = require("../schema/record");
const { getEdge } = require("../pipeline/edge");

const REPO_ROOT = path.resolve(__dirname, "../..");
const DEMO_USER = "demo";

/**
 * Build curriculum profile.
 * @returns {{ knowledge: string[], curiosity: string[], personality: string[], edge: { THINK: string, WRITE: string, WORK: string }, evidenceCount: number, exportDate: string, screen_time_target_minutes?: number }}
 */
function buildCurriculumProfile() {
  const { record } = load(REPO_ROOT, DEMO_USER);
  const edge = getEdge();

  return {
    knowledge: record.selfKnowledge || [],
    curiosity: record.selfCuriosity || [],
    personality: record.selfPersonality || [],
    edge,
    evidenceCount: (record.selfEvidence || []).length,
    exportDate: new Date().toISOString(),
    screen_time_target_minutes: 120,
  };
}

module.exports = { buildCurriculumProfile };
