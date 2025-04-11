async function countUser () {
    try {
        const response = await fetch('/api/visit', { method: 'POST' });
        if (response.ok) {
            window.location.href = 'reg.html';
        } else {
            console.error('Ошибка при подсчете пользователя:', response.statusText);
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
    }
}
