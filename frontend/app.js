const API_BASE = "http://localhost:8000/api/v1";

const byId = (id) => document.getElementById(id);

async function post(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return data;
}

byId("ingest-btn").onclick = async () => {
  const source = byId("ingest-source").value;
  const content = byId("ingest-content").value;
  const result = await post("/ingest/text", { source, content });
  byId("ingest-result").textContent = JSON.stringify(result, null, 2);
};

byId("retrieve-btn").onclick = async () => {
  const query = byId("retrieve-query").value;
  const top_k = Number(byId("retrieve-topk").value || 5);
  const result = await post("/retrieve/hybrid", { query, top_k });
  byId("retrieve-result").textContent = JSON.stringify(result, null, 2);
};

byId("memory-record-btn").onclick = async () => {
  const type = byId("memory-type").value;
  const payload = { type };
  if (type === "semantic") {
    payload.key = byId("memory-key").value;
    payload.value = byId("memory-value").value;
  } else {
    payload.content = byId("memory-content").value;
  }
  const result = await post("/memory/record", payload);
  byId("memory-record-result").textContent = JSON.stringify(result, null, 2);
};

byId("memory-recall-btn").onclick = async () => {
  const type = byId("recall-type").value;
  const query = byId("recall-query").value;
  const limit = Number(byId("recall-limit").value || 10);
  const payload = { type, limit };
  if (type === "semantic" && query) payload.query = query;
  const result = await post("/memory/recall", payload);
  byId("memory-recall-result").textContent = JSON.stringify(result, null, 2);
};

byId("eval-btn").onclick = async () => {
  const raw = byId("eval-items").value || "[]";
  let items = [];
  try {
    items = JSON.parse(raw);
  } catch (e) {
    byId("eval-result").textContent = "Invalid JSON";
    return;
  }
  const top_k = Number(byId("eval-topk").value || 5);
  const result = await post("/evaluate/retrieval", { items, top_k });
  byId("eval-result").textContent = JSON.stringify(result, null, 2);
};
