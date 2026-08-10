function deleteNote(expenseId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
  }).then((_res) => {
    window.location.href = "/expense";
  });
}

function deleteCategory(category) {
  fetch("/delete-category", {
    method: "POST",
    body: JSON.stringify({ category: category }),
  }).then((_res) => {
    window.location.href = "/budget";
  });
}