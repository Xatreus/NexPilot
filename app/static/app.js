const $ = (selector) => document.querySelector(selector);
const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
async function api(path, options = {}) {
  const response = await fetch(path, {headers: {"Content-Type":"application/json"}, ...options});
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`);
  return body;
}
function list(items) { return `<ul>${(items || []).map(item => `<li>${esc(item)}</li>`).join("")}</ul>`; }
function showError(target, error) { target.classList.remove("empty"); target.innerHTML = `<strong>Something went wrong</strong><p>${esc(error.message || error)}</p>`; }
$("#plan-form").addEventListener("submit", async (event) => {
  event.preventDefault(); const button = event.currentTarget.querySelector("button"); const target = $("#plan-result");
  button.disabled = true; button.textContent = "Building your plan…"; target.classList.remove("empty"); target.textContent = "Reviewing scope, risks, and verification…";
  try {
    const result = await api("/api/v1/plans", {method:"POST", body:JSON.stringify({task:$("#task").value, repository_url:$("#repo-url").value || null})});
    target.innerHTML = `<h3>${esc(result.title)}</h3><p>${esc(result.summary)}</p><span class="pill">${esc(result.generated_by)}</span><h4>Implementation sequence</h4><ol>${result.steps.map(step => `<li><strong>${esc(step.title)}</strong> <span class="pill">${esc(step.category)}</span><br>${esc(step.details)}</li>`).join("")}</ol><h4>Risks to consider</h4>${list(result.risks)}<h4>Acceptance criteria</h4>${list(result.acceptance_criteria)}<h4>Assumptions</h4>${list(result.assumptions)}`;
    await loadHistory();
  } catch (error) { showError(target,error); } finally { button.disabled = false; button.innerHTML = 'Generate engineering plan <span>↗</span>'; }
});
$("#repo-form").addEventListener("submit", async (event) => {
  event.preventDefault(); const button = event.currentTarget.querySelector("button"); const target = $("#repo-result");
  button.disabled = true; button.textContent = "Inspecting GitHub…"; target.classList.remove("empty"); target.textContent = "Reading public repository metadata and file paths…";
  try {
    const result = await api("/api/v1/repositories/inspect", {method:"POST",body:JSON.stringify({repository_url:$("#inspect-url").value})});
    target.innerHTML = `<h3>${esc(result.repository)}</h3><p>${esc(result.description || "No repository description supplied.")}</p><span class="pill">${esc(result.language || "Language unknown")}</span><span class="pill">★ ${esc(result.stars)}</span><h4>Delivery signals</h4>${result.findings.map(f => `<div style="border-top:1px solid #263246;padding:9px 0"><span class="pill">${esc(f.status)}</span><strong>${esc(f.category)}</strong><p>${esc(f.evidence)}</p><small>${esc(f.recommendation)}</small></div>`).join("")}<h4>Limitations</h4>${list(result.limitations)}`;
    await loadHistory();
  } catch (error) { showError(target,error); } finally { button.disabled = false; button.innerHTML = 'Inspect repository <span>↗</span>'; }
});
async function loadHistory() {
  const target = $("#history");
  try {
    const items = await api("/api/v1/history?limit=8");
    target.innerHTML = items.length ? items.map(item => `<div class="history-row"><span class="history-kind">${esc(item.kind)}</span><span class="history-subject">${esc(item.subject)}</span><span class="history-date">${esc(new Date(item.created_at).toLocaleString())}</span></div>`).join("") : '<div class="empty">No activity yet. Create a plan or inspect a repository to get started.</div>';
  } catch (error) { target.innerHTML = `<div class="empty">${esc(error.message)}</div>`; }
}
$("#refresh-history").addEventListener("click", loadHistory);
api("/api/v1/health").then(() => { $("#model-status").textContent = "API online"; }).catch(() => { $("#model-status").textContent = "Unavailable"; });
loadHistory();
