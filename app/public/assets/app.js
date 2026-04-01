// Shared app logic for status/loading/process microcopy.
(function(global) {
  var COPY = {
    grounded_record: {
      loading: [
        "Checking the Record...",
        "Reading what is already documented...",
        "Grounding in the current profile..."
      ],
      loaded: "Record loaded.",
      error: "Could not load the Record."
    },
    gate_review: {
      staging: "Staging for review...",
      reviewing: "Reviewing pending changes...",
      refreshing: "Refreshing the review queue...",
      approved: "Approved. Review queue refreshed.",
      rejected: "Rejected. Review queue refreshed.",
      merged: "Applying approved changes...",
      error: "Review action failed."
    },
    maintenance: {
      loading: "Checking governed changes...",
      refreshing: "Refreshing this view...",
      error: "Could not refresh this view."
    }
  };

  function pick(value) {
    if (Array.isArray(value)) {
      if (!value.length) return "";
      return value[Math.floor(Math.random() * value.length)];
    }
    return value || "";
  }

  function phrase(lane, key, fallback) {
    var laneCopy = COPY[lane] || {};
    return pick(laneCopy[key]) || fallback || "";
  }

  function setStatus(el, lane, key, fallback, className) {
    if (!el) return;
    el.textContent = phrase(lane, key, fallback);
    if (typeof className === "string") {
      el.className = className;
    }
  }

  global.CompanionStatusMicrocopy = {
    phrase: phrase,
    setStatus: setStatus
  };
})(window);
