class HTTPClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async request(method, url, json) {
        const headers = {Authorization: window.localStorage.getItem('accessToken')};
        if (json) {
            headers['Content-Type'] = 'application/json';
        }
        const response = await fetch(this.baseUrl + url, {
            method: method,
            headers,
            body: json ? JSON.stringify(json) : undefined
        });
        return response.status !== 204 ? response.json() : null;
    }

    async post (url, json) {
        return this.request('POST', url, json);
    }

    async put (url) {
        return this.request('PUT', url);
    }

    async get (url) {
        return this.request('GET', url);
    }
}
