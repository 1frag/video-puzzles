const _API_ENDPOINT = `${window.location.origin}/api`;
const client = new HTTPClient(_API_ENDPOINT)

class Api {
    async googleLogin() {
        const login = await client.post('/auth/google/login', {ident: 'publish_result'});
        return login.url;
    }

    async verifyGame(durationSecs, name) {
        await client.post('/game/verify', {
            duration_secs: durationSecs,
            name,
        });
    }

    async getLeaders(puzzleId) {
        const {leaders} = await client.get(`/game/leaderboard/${puzzleId}`);
        return leaders.map(leader => ({
            name: leader.name,
            durationSecs: leader.duration_secs,
        }));
    }
}

const API = new Api();
