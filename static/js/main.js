const API_URL = "/zoro/v1";
var success = false;

getListings();

setTimeout(function () {
  if (!success) {
    $("#loading").hide();
    $("#filter").hide();
    $("#errors").html(`
    <div class="ui error message">
      <div class="header">User unauthorized</div>
      <p>Please login to your account to view the contents of this page.</p>
    </div>
    `)
      .fadeIn('fast');
  }
}, 5000);

$('.ui.search')
  .search({
    apiSettings: {
      url: '/zoro/v1/jobs?q={query}'
    },
    fields: {
      results : 'jobs',
      title   : 'title',
      url     : '/jobs/{unique}/'
    },
    minCharacters : 3
  })
  .on('.ui.search', function() {
    console.log("hello")
    });

// Get the listings from the API, and return them as a JSON array
function getListings(query = undefined) {
    let url = query != undefined ? `${API_URL}/jobs?q=${query}` : `${API_URL}/jobs/`;
    $.getJSON(url, function (data) {
        success = true;
        console.log("Fetch " + url);
        let results = data.jobs;
        console.log(results);
        let html = "";
        for (let i = 0; i < results.length; i++) {
            html += `
            <div class="ui card">
              <div class="content">
                <div class="header">${results[i].title}</div>
                <div class="meta">
                  <span>${results[i].date_published}</span>
                  <a>$${results[i].salary}</a>
                </div>
                <div class="description">
                  ${results[i].content}
                </div>
                <p></p>
              </div>
            </div>`;
        }
        $("#results").hide();
        $("#filter").removeClass("disabled");
        $("#loading").fadeOut('fast');
        $("#results").html(html).delay(200).fadeIn('slow');
    });
}