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

async function create_zip_archive() {
    const result = check_checkbox()
    const url = "/create-zip-archive"
    send_files(url, result)
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
    return result

}

async function get_zip_archive() {
    setTimeout(() => {
        window.location.href="/get-zip-archive"
    }, 
    2000
    )
}

async function securityFile() {
    const result = check_checkbox()
    const url = "/security-file"
    send_files(url, result)

}

document.getElementById("create_zip_archive").addEventListener('click', create_zip_archive);
document.getElementById("securityFile").addEventListener('click', securityFile);