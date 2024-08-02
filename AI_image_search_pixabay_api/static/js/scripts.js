$(document).ready(function() {
    $('#searchButton').click(function() {
        var query = $('#query').val();
        $.ajax({
            url: '/search',
            type: 'GET',
            data: { query: query },
            success: function(data) {
                var resultsDiv = $('#results');
                resultsDiv.empty();
                if (data && Array.isArray(data) && data.length > 0) {
                    data.forEach(function(image) {
                        var img = $('<img>').attr('src', image.localURL).attr('alt', image.tags).css('width', '200px');
                        resultsDiv.append(img);
                    });
                } else {
                    resultsDiv.text('No images found.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
