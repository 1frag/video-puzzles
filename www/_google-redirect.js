if (window.opener && typeof _META !== 'undefined') {
    const customEvent = new CustomEvent('oauth-redirect', {detail: _META});
    window.localStorage.setItem('accessToken', _META.access_token);
    window.opener.dispatchEvent(customEvent);
    window.close();
} else {
    throw new Error('Invalid usage');
}
