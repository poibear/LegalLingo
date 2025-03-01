function searchBox() {
  // click on placebo, then hide placebo to show actual search bar
  let actualSearchBtn = 'input[id="form-searchbox"]';
  let form_query = $(actualSearchBtn);
  form_query.on("input", async function () {
    let serv_resp = await fetch("/query?form=" + form_query.val());
    let forms = await serv_resp.text();
    $("#form-results-table").html(forms);
  });
}

$(document).ready(searchBox());