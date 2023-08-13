class Timer {
    init () {
        this.board = document.getElementById('timer');
        this.startAt = Date.now();
        this._timerId = setInterval(this._tick.bind(this), 1000);
    }

    stop () {
        clearTimeout(this._timerId);
    }

    _tick () {
        const secs = Math.floor((Date.now() - this.startAt) / 1000);
        const mins = Math.floor(secs / 60);
        const format = v => v.toString().padStart(2, '0');
        this.board.innerText = `${format(mins)}:${format(secs % 60)}`;
        this.board.style.color = secs < 60 ? 'green' : (mins < 3 ? '#FF8F44' : 'red');
    }
}

const timerController = new Timer();
