search_btn.onclick = async function () {
    key = String(document.getElementById('search_input').value);
    console.log(key);
    data = await fetch('/get_content_text/' + key).then(response => { return response.json() }).then((json) => {
        return json;
    });
    document.getElementById('container').innerHTML = data['html'];
}

