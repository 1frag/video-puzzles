const _API_ENDPOINT = `${window.location.origin}/api`;
const client = new HTTPClient(_API_ENDPOINT)

class Api {
    async googleLogin() {
        const login = await client.post('/auth/google/login', {ident: 'publish_result'});
        return login.url;
    }

    async verifyGame(durationSecs, name, puzzleId) {
        await client.post(`/puzzles/${puzzleId}/verify`, {
            duration_secs: durationSecs,
            name,
        });
    }

    async getLeaders(puzzleId) {
        const {leaders} = await client.get(`/puzzles/${puzzleId}/leaderboard`);
        return leaders.map(leader => ({
            name: leader.name,
            durationSecs: leader.duration_secs,
        }));
    }

    async getPuzzles() {
        const {puzzles} = await client.get(`/puzzles`);
        return puzzles.map(puzzle => ({
            id: puzzle.id,
            name: puzzle.name,
            preview: puzzle.preview,
            metadata: puzzle.metadata,
        }));
    }
}

const API = new Api();
