
script = async function (key) {
    data = await fetch('/script/' + key).then(response => { return response.json() }).then((json) => {
        return json;
    });
    document.getElementById('form').innerHTML = data['html'];
};

script(1);

