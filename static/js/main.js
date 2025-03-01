function openSearchBox() {
    // cilck on placebo, then hide placebo to show actual search bar
    $('input[name="form-placebo"]').click(function() {
        
        let form_query = $('input[name="form-searchbox"]');
        form_query.on('input', async function() {
            let serv_resp = await fetch('/search?form=' + stock_query.val());
            let forms = await serv_resp.text();
            $('#form-results-table').html(forms);
        })
    })
}

$(document).ready(openSearchBox());