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
    const quantity_files = Array.from(document.getElementsByClassName("file"));
    if(str == "") 
    {
        console.log("User enter empty str...");
        for(i = 0; i < quantity_files.length; i++) {
            var iter = quantity_files[i];
            if(iter.hidden) {
                iter.hidden = false;
            }
        }
        return;
    }
    
    const url = "/search-file";
    send_data(url, str);
    //console.log("User entered: ", str)

    var find_files = JSON.parse(search_list_files)['find_files'];
    let obj = Array.from(find_files);

    for(i = 0; i < quantity_files.length; i++) {
        var iter_index = quantity_files[i];
        var iter = quantity_files[i].querySelector('.files').name;

        if(obj.some(item => item.includes(iter))) 
        {
            iter_index.hidden = false;
        } else 
        {
            iter_index.hidden = true;
        }
    }
}

document.getElementById("IdCreateZipArchive").addEventListener('click', create_zip_archive);
document.getElementById("IdSecurityFile").addEventListener('click', securityFile);
document.getElementById("IdDeleteSecurityFile").addEventListener('click', deleteSecurityFile);