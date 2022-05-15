
script = async function (key, id_back) {
    data = await fetch('/script/' + key + '/' + id_back).then(response => { return response.json() }).then((json) => {
        return json;
    });
    document.getElementById('form').innerHTML = data['html'];
};

script(1, 1);

