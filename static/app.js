document.addEventListener("DOMContentLoaded", function() {
  const expenseForm = document.getElementById("expenseForm");
  const budgetForm = document.getElementById("budgetForm");
  const runReport = document.getElementById("runReport");

  expenseForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      title: document.getElementById("title").value,
      category: document.getElementById("category").value,
      amount: parseFloat(document.getElementById("amount").value),
      date: document.getElementById("date").value || null,
      split_count: document.getElementById("split_count").value ? parseInt(document.getElementById("split_count").value) : null,
      note: document.getElementById("note").value || null
    };
    const res = await fetch("/api/expense", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    const alertBox = document.getElementById("expenseAlert");
    if (res.ok) {
      alertBox.textContent = data.alert ? data.alert : "Expense added successfully.";
    } else {
      alertBox.textContent = data.error || "Error adding expense";
    }
    setTimeout(()=> alertBox.textContent="", 5000);
    expenseForm.reset();
  });

  budgetForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      category: document.getElementById("budgetCategory").value,
      month: document.getElementById("budgetMonth").value,
      amount: parseFloat(document.getElementById("budgetAmount").value)
    };
    const res = await fetch("/api/budget", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    const msg = document.getElementById("budgetMsg");
    if (res.ok) msg.textContent = "Budget saved.";
    else msg.textContent = data.error || "Error setting budget.";
    setTimeout(()=> msg.textContent="", 4000);
    budgetForm.reset();
  });

  runReport.addEventListener("click", async () => {
    const month = document.getElementById("reportMonth").value;
    if (!month) { document.getElementById("reportResult").textContent = "Choose month"; return; }
    const res1 = await fetch(`/api/report/monthly?month=${month}`);
    const monthly = await res1.json();
    const res2 = await fetch(`/api/report/compare?month=${month}`);
    const compare = await res2.json();
    document.getElementById("reportResult").textContent = JSON.stringify({monthly, compare}, null, 2);
  });
});