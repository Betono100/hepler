
// определить какая кнопка была нажата
document.addEventListener('click', ({ target: t }) => {
    if (t.className === 'popup__answer-button') {
        
        script(t.value, t.name);
        
    }
});