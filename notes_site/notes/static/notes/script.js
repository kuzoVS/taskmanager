document.querySelectorAll("form[data-confirm]").forEach(function (form) {
  form.addEventListener("submit", function (event) {
    if (!confirm(form.dataset.confirm)) {
      event.preventDefault();
    }
  });
});

var body = document.getElementById("body");
var counter = document.getElementById("counter");
if (body && counter) {
  body.addEventListener("input", function () {
    counter.textContent = body.value.length + "/1000";
  });
}
