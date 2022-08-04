const API_URL = "/zoro/v1";
var success = false;

getListings();

setTimeout(function () {
  if (!success) {
    $("#loading").hide();
    $("#filter").hide();
    $("#errors").html(`
    <div style="margin-bottom:2em;" class="ui error message">
      <div class="header">401: Unauthorized</div>
      <p>Sorry, this content is protected, please <a href="/login">login</a> to view.</p>
    </div>
    `)
      .fadeIn('fast');
  }
}, 1000);

$('.ui.radio.checkbox')
  .checkbox()
;
$('.ui.floating.dropdown')
  .dropdown({
    allowCategorySelection: true,
    onChange: function (value, text, $selectedItem) {
      let sort = $selectedItem.find('span').text();
      console.log("sorting by " + sort);
      $("#results").hide();
      $("#loading").fadeIn('fast'); 
      getListings(undefined, sort);
    }
  })
;

$('nav.ui.search')
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
function getListings(query = undefined, sort = undefined) {
    
    let url = query != undefined ? `${API_URL}/jobs?q=${query}` : `${API_URL}/jobs/`;

    if (sort !== undefined) {
      url = `${API_URL}/jobs?sortBy=${sort}`;
    }

    $.getJSON(url, function (data) {
        success = true;
        console.log("Fetch " + url);
        let results = data.jobs;
        console.log(results);
        let html = "";
        for (let i = 0; i < results.length; i++) {
            html += `
              <a href="/view/${results[i].unique}/">
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
              </div>
              </a>`;
        }
        $("#results").hide();
        $("#filter").removeClass("disabled");
        $("#loading").fadeOut('fast');
        if (results.length > 0) {
          $("#results").html(html).delay(200).fadeIn('slow');
        } else {
          $("#results").html(`
          <div style="margin-bottom:2em;" class="ui message">
            <div class="header">No posts yet!</div>
            <p>Seems like there are no active posts at the moment, check back here later!</p>
          </div>`).delay(200).fadeIn('slow');
        }
        
    });
}