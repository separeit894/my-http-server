// if true, to append log alert
const verbose = true;
var search_list_files;

async function send_data(url, result) {
    try {
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(result),
            headers: {
                "Content-Type": "application/json",
            },
        });
        const json = await response.json();
        if (url == "/search-file") search_list_files = JSON.stringify(json);

        console.log("Успех:", JSON.stringify(json));
    } catch (error) {
        console.error("Ошибка:", error);
    }
}

async function create_zip_archive() {
    const result = check_checkbox();
    const url = "/create-zip-archive";
    send_data(url, result);
}

function check_checkbox() {
    result = []
    const checkbox_class_elements = document.getElementsByClassName("files");
    for(i = 0; i < checkbox_class_elements.length; i++) {
        if (checkbox_class_elements[i]["checked"]) {
            result.push(checkbox_class_elements[i]['name']);
        }
    }

    if (result.length === 0) {
        alert("Выберите хотя бы один чекбокс");
        window.location.href="/";
        return;
    }
    // console.log("result: ", result);
    return result;

}

async function get_zip_archive() {
    setTimeout(() => {
        window.location.href="/get-zip-archive";
        if (verbose) alert("ZIP ARCHIVE CREATE");
    }, 
    2000
    );
}

async function securityFile() {
    const result = check_checkbox();
    const url = "/security-file";
    send_data(url, result);

    setTimeout(() => {
        window.location.reload();
        if (verbose) alert("SECURITY: " + result)
    }, 1300);
}

async function deleteSecurityFile() {
    const url = "/delete-security-file";
    const result = check_checkbox();
    send_data(url, result);
    setTimeout(() => {
        window.location.reload(); 
        if (verbose) alert("DELETE SECURITY: " + result)
    }, 
    1300);
}

async function SearchFileInList(str) {
    if(str == "") {
        location.href="/";
    }
    
    const url = "/search-file";
    send_data(url, str);

    const quantity_files = Array.from(document.getElementsByClassName("file"));
    let obj = Array.from(JSON.parse(search_list_files)['find_files']);

    //const result = quantity_files.filter(file=>obj.includes(file.name.trim()))
    //console.log("РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ ФУНКЦИИ: ", result)
    for(i = 0; i < quantity_files.length; i++) {
        if(obj.some(item => item == quantity_files[i].querySelector('.files').name)) {} 
        else {
            quantity_files[i].remove();
        }
    }
}

document.getElementById("IdCreateZipArchive").addEventListener('click', create_zip_archive);
document.getElementById("IdSecurityFile").addEventListener('click', securityFile);
document.getElementById("IdDeleteSecurityFile").addEventListener('click', deleteSecurityFile);