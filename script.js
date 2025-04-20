const API = "http://localhost:8000";

document.getElementById("patient-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const date = document.getElementById("date").value;
  const priority = parseInt(document.getElementById("priority").value);
  await fetch(`${API}/add_patient/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, date, priority })
  });
  alert("Patient Added");
});

async function fetchPatients() {
  const date = document.getElementById("search-date").value;
  const res = await fetch(`${API}/patients/${date}`);
  const patients = await res.json();
  const list = document.getElementById("patient-list");
  list.innerHTML = "";
  patients.forEach(p => {
    const li = document.createElement("li");
    li.textContent = `${p.name} (Priority: ${p.priority})`;
    list.appendChild(li);
  });
}

async function removeFIFO() {
  const date = document.getElementById("search-date").value;
  await fetch(`${API}/remove_fifo/${date}`, { method: "DELETE" });
  alert("First patient removed");
  fetchPatients();
}

async function removeByName() {
  const name = document.getElementById("remove-name").value;
  await fetch(`${API}/remove_by_name/${name}`, { method: "DELETE" });
  alert(`${name} removed`);
  fetchPatients();
}
