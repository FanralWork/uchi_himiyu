function loadVideos() {
    const classNumber = document.getElementById("classSelect").value;
    const videoContainer = document.getElementById("videoContainer");

    if (classNumber) {
        fetch(`/api/videos/${classNumber}`)
            .then(response => response.json())
            .then(videos => {
                videoContainer.innerHTML = '';
                if (videos.length > 0) {
                    videos.forEach(video => {
                        const videoCard = `
                            <div class="col-md-4 mb-4" onClick="window.location.href='/play/${classNumber}/${video.name}.mp4'">
                                <div class="card video-card align-items-stretch">
                                    <img src="/static/thumbnails/${video.thumbnail}" class="card-img-top" alt="Превью">
                                    <div class="card-body text-center">
                                        <p class="card-title">${video.name}</p>
                                    </div>
                                </div>
                        </div>`;
                        videoContainer.insertAdjacentHTML('beforeend', videoCard);
                    });
                } else {
                    videoContainer.innerHTML = '<p class="text-center">Видео не найдено</p>';
                }
            });
    } else {
        videoContainer.innerHTML = '';
    }
}
