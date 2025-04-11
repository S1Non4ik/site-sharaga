function loadContent(url, elementId) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            const element = document.getElementById(elementId);
            if (element) {
                element.innerHTML = data;

                // Найти и добавить стили в <head>
                const styleTags = element.getElementsByTagName('style');
                for (let i = 0; i < styleTags.length; i++) {
                    const style = document.createElement('style');
                    style.textContent = styleTags[i].textContent;
                    document.head.appendChild(style);
                }
            } else {
                console.error(`Элемент с ID "${elementId}" не найден.`);
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке:', error);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    loadContent('header.html', 'header'); // Загружаем header
    loadContent('footer.html', 'footer'); // Загружаем footer
});