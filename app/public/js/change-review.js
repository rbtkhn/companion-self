/**
 * Change Review page: loads review-queue bundle + summary from Express API.
 */

function apiProfile(selectValue) {
  return selectValue === "_template" ? "template" : "demo";
}

function escapeHtml(s) {
  if (s == null) return "";
  const div = document.createElement("div");
  div.textContent = String(s);
  return div.innerHTML;
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function setHtml(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

async function loadChangeReview() {
  const select = document.getElementById("profileSelect");
  const profile = apiProfile(select ? select.value : "demo");
  setText(
    "summaryBox",
    CompanionStatusMicrocopy.phrase("maintenance", "loading", "Checking governed changes...")
  );
  setText("queueBox", "—");
  setText("decisionBox", "—");
  setText("diffBox", "—");
  setText("eventLogBox", "—");

  const [bundleRes, summaryRes] = await Promise.all([
    fetch("/api/change-review?profile=" + encodeURIComponent(profile)),
    fetch("/api/change-review/summary?profile=" + encodeURIComponent(profile)),
  ]);

  const bundle = await bundleRes.json().catch(() => ({}));
  const summary = await summaryRes.json().catch(() => ({}));

  if (!bundleRes.ok) {
    setText(
      "summaryBox",
      bundle.error || CompanionStatusMicrocopy.phrase("maintenance", "error", "Failed to load bundle")
    );
    setText("queueBox", "—");
    setText("decisionBox", "—");
    setText("diffBox", "—");
    setText("eventLogBox", "—");
    return;
  }

  const c = summary.counts || {};
  const lines = [
    "Proposals: " + (c.proposals ?? "—"),
    "Decisions: " + (c.decisions ?? "—"),
    "Diffs: " + (c.diffs ?? "—"),
    "Queue items: " + (c.queueItems ?? "—"),
    "Events: " + (c.events ?? "—"),
  ];
  setText("summaryBox", lines.join("\n"));

  const q = bundle.queue;
  if (q && q.items && q.items.length) {
    const ul = q.items
      .map(
        (it) =>
          "<li><strong>" +
          escapeHtml(it.proposalId) +
          "</strong> [" +
          escapeHtml(it.status) +
          "] " +
          escapeHtml(it.summary) +
          "</li>"
      )
      .join("");
    setHtml("queueBox", "<ul>" + ul + "</ul>");
  } else {
    setText("queueBox", "(no queue items)");
  }

  const latest = summary.latestDecision;
  if (latest) {
    setText(
      "decisionBox",
      latest.decision +
        " — " +
        (latest.decisionReason || "") +
        "\n(proposal: " +
        (latest.proposalId || "—") +
        ")"
    );
  } else {
    setText("decisionBox", "(no decisions)");
  }

  const diff = summary.latestDiff;
  if (diff) {
    const before = diff.before != null ? JSON.stringify(diff.before, null, 2) : "—";
    const after = diff.after != null ? JSON.stringify(diff.after, null, 2) : "—";
    setHtml(
      "diffBox",
      "<p><strong>" +
        escapeHtml(diff.changeSummary || "") +
        '</strong></p><p class="mono">before:\n' +
        escapeHtml(before) +
        "\n\nafter:\n" +
        escapeHtml(after) +
        "</p>"
    );
  } else {
    setText("diffBox", "(no diffs)");
  }

  const log = bundle.eventLog;
  if (log && log.events && log.events.length) {
    const ul = log.events
      .map(
        (e) =>
          "<li>" +
          escapeHtml(e.eventType) +
          " @ " +
          escapeHtml(e.timestamp) +
          " — " +
          escapeHtml(e.summary) +
          "</li>"
      )
      .join("");
    setHtml("eventLogBox", "<ul>" + ul + "</ul>");
  } else {
    setText("eventLogBox", "(no events)");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const reload = document.getElementById("reloadBtn");
  const sel = document.getElementById("profileSelect");
  if (reload) reload.addEventListener("click", loadChangeReview);
  if (sel) sel.addEventListener("change", loadChangeReview);
  loadChangeReview();
});
