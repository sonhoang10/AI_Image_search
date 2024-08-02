document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    
    fetch(`/search-image?query=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.image_urls) {
                const imagesDiv = document.getElementById('images');
                imagesDiv.innerHTML = '';
                data.image_urls.forEach(imageUrl => {
                    const img = document.createElement('img');
                    img.src = imageUrl;
                    img.style.maxWidth = '200px';
                    img.style.margin = '10px';
                    imagesDiv.appendChild(img);
                });
            } else {
                alert('No images found');
            }
        })
        .catch(error => console.error('Error:', error));
});
