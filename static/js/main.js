const API_URL = "/zoro/v1";

getListings();

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
        console.log("Fetch " + url);
        let results = data.jobs;
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
                  ${atob(results[i].content).substring(0, 100)}
                </div>
                <p></p>
              </div>
            </div>`;
        }
        $("#results").hide();
        $("#loading").fadeOut('fast');
        $("#results").html(html).delay(200).fadeIn('slow');
    })
    ;
    ;
}

// Update a div with the results of the search
function setResults(JSON) {
    let results = JSON.jobs;
    
}

// Take JSON input and sort it by the given key
function sortListings(JSON, sortTerm) {

}
