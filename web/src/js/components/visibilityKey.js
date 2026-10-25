const secretKeyInput = document.getElementById('secret-key');
const toggleSecretKeyButton = document.getElementById('toggle-secret-key');
const toggleSecretKeyIcon = document.getElementById('toggle-secret-key-icon');

export function toggleSecretKeyVisibility() {
    toggleSecretKeyButton.addEventListener('click', () => {
        if (secretKeyInput.type === 'password') {
            secretKeyInput.type = 'text';
            toggleSecretKeyIcon.textContent = 'visibility_off';
        } else {
            secretKeyInput.type = 'password';
            toggleSecretKeyIcon.textContent = 'visibility';
        }
    });
}