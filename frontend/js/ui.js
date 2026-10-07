const ui = {
  meta: document.getElementById("results-meta"),
  chip: document.getElementById("status-chip"),
  alert: document.getElementById("alert"),
  table: document.getElementById("results-table"),
  tbody: document.querySelector("#results-table tbody"),
  card: document.getElementById("single-card"),
  pagination: document.getElementById("pagination"),
};

function setStatus(kind, label) {
  ui.chip.className = `chip ${kind}`;
  ui.chip.textContent = label;
}

function showAlert(message) {
  ui.alert.hidden = !message;
  ui.alert.textContent = message || "";
}

function renderEmpty(message) {
  ui.table.hidden = true;
  ui.card.hidden = true;
  ui.pagination.hidden = true;
  ui.meta.textContent = message;
}

function renderSingle(item) {
  ui.table.hidden = true;
  ui.card.hidden = false;
  ui.card.innerHTML = `
    <h3>${item.nome}</h3>
    <dl>
      <dt>Cargo</dt><dd>${item.cargo.descricao}</dd>
      <dt>Carreira</dt><dd>${item.cargo.carreira || "—"}</dd>
      <dt>Órgão</dt><dd>${item.orgao.sigla} · ${item.orgao.nome}</dd>
      <dt>UF</dt><dd>${item.uf}</dd>
      <dt>Situação</dt><dd>${item.situacao}</dd>
      <dt>CPF</dt><dd>${item.cpf_mascarado || "—"}</dd>
      <dt>Matrícula</dt><dd>${item.matricula || "—"}</dd>
      <dt>Regime</dt><dd>${item.regime_juridico || "—"}</dd>
      <dt>Aposentadoria</dt><dd>${item.tipo_aposentadoria || "—"} ${item.data_aposentadoria || ""}</dd>
    </dl>
  `;
}

function renderTable(items) {
  ui.card.hidden = true;
  ui.table.hidden = false;
  ui.tbody.innerHTML = items
    .map(
      (item) => `
        <tr>
          <td>${item.nome}</td>
          <td>${item.cargo.descricao}</td>
          <td>${item.orgao.sigla || item.orgao.nome}</td>
          <td>${item.uf}</td>
          <td>${item.situacao}</td>
        </tr>`
    )
    .join("");
}

function fillSelect(select, values, getValue, getLabel) {
  values.forEach((item) => {
    const option = document.createElement("option");
    option.value = getValue(item);
    option.textContent = getLabel(item);
    select.appendChild(option);
  });
}

function fillDatalist(list, values) {
  list.innerHTML = values.map((value) => `<option value="${value}"></option>`).join("");
}
