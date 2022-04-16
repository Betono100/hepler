async function return_content(key) {
    data = await fetch('/get_content/' + key).then(response => { return response.json() }).then((json) => {
        return json;
    });

    document.getElementById('article').innerHTML = data[key]['text'];
    document.getElementById('path_date').innerHTML = key + ' ' + data[key]['date'];
    document.getElementById('title').innerHTML = data[key]['title'];
}

search_btn.onclick = async function () {
    key = String(document.getElementById('search_input').value);
    console.log(key);
    data = await fetch('/get_content_text/' + key).then(response => { return response.json() }).then((json) => {
        return json;
    });
    key = Object.keys(data)[0];
    document.getElementById('article').innerHTML = data[key]['text'];
    document.getElementById('path_date').innerHTML = key + ' ' + data[key]['date'];
    document.getElementById('title').innerHTML = data[key]['title'];
}