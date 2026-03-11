function copyLink() {
    const text = window.articleConfig ? window.articleConfig.textCopied : "Lien copié !";
    navigator.clipboard.writeText(window.location.href);
    alert(text);
}

function confirmDelete() {
    const text = window.articleConfig ? window.articleConfig.textConfirmDelete : "Confirmer ?";
    return confirm(text);
}
