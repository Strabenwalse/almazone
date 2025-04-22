document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('filter-form');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const queryString = new URLSearchParams(formData).toString();

    fetch(form.action + "?" + queryString, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => {
      if (!response.ok) throw new Error("Ошибка сети");
      return response.text();
    })
    .then(data => {
      document.getElementById('ad-list').innerHTML = data;
    })
    .catch(error => {
      console.error("Ошибка фильтрации:", error);
    });
  });
});
