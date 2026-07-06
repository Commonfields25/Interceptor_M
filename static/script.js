function copyToClipboard(text, btn) {
    // Resolve relative URLs to absolute if needed, or just copy as is
    const fullUrl = text.startsWith('/') ? window.location.origin + text : text;

    navigator.clipboard.writeText(fullUrl).then(() => {
        const originalContent = btn.innerHTML;
        // Success state: checkmark icon
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        btn.style.color = 'var(--status-ok)';
        btn.style.borderColor = 'var(--status-ok)';

        setTimeout(() => {
            btn.innerHTML = originalContent;
            btn.style.color = '';
            btn.style.borderColor = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}
