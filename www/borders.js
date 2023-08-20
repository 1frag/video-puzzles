class BordersController {
    init() {
        this.canvas = document.getElementById('canvas');
        this.canvasContext = this.canvas.getContext('2d', {willReadFrequently: true});
    }

    videoById(id) {
        const element = game.idToElement[id];
        return element.getElementsByTagName('video')[0];
    }

    getPixel(id, x, y) {
        const video = this.videoById(id);
        this.canvasContext.drawImage(video, 0, 0, video.width, video.height);
        const data = game.borders.canvasContext.getImageData(x, y, 1, 1).data;
        game.borders.canvasContext.clearRect(0, 0, video.width, video.height);
        return data;
    }

    isVisible(id, x, y) {
        return this.getPixel(id, x, y)[3] !== 0;
    }
}
