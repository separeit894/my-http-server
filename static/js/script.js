async function send_files(url, result) {
    try {
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(result),
            headers: {
                "Content-Type": "application/json",
            },
        });
        const json = await response.json();
        console.log("Успех:", JSON.stringify(json));
    } catch (error) {
        console.error("Ошибка:", error);
    }
}

function check_checkbox() {
    result = []
    const checkbox_class_elements = document.getElementsByClassName("files");
    for(i = 0; i< checkbox_class_elements.length; i++) {
        if (checkbox_class_elements[i]["checked"]) {
            result.push(checkbox_class_elements[i]['name'])
        }
    }
    
    if (result.length === 0) {
        alert("Выберите хотя бы один чекбокс")
        window.location.href="/"
        return;
    } 
    console.log("result: ", result)
    send_files("/create-zip-archive", result)
    

}

document.getElementById("check_checkbox").addEventListener('click', check_checkbox);
