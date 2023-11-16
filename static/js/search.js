const status = document.getElementById("status");
const status_text = document.getElementById("status-text");
const bar = document.getElementById("search-bar");
const bar_btn = document.getElementById("search-bar-btn");
const vendor_btn = document.getElementById("search-vendor-btn");
const num_input = document.getElementById("search-num");

const decoder = new TextDecoder();

// Read chunks from a stream and pass them to a function.
// If the passed function returns false for any chunk, this one stops reading and likewise returns false.
async function readChunks(stream, fun) {
    const reader = stream.getReader();

    // Iterate returned chunks until the stream is closed
    let chunk, end;
    while (!end) {
        ({value: chunk, done: end} = await reader.read());
        if (end) {
            return true;
        }

        if (!fun(chunk)) {
            console.log("False returned top level for chunk: " + chunk);
            return false;
        }
    }

    return true;
}

function handleResponseJson(msg) {
    switch (msg.type) {
        case "status":
            status.classList.remove("d-none");
            status_text.innerText = msg.message;
            return true;
        case "product":
            addProduct(msg);
            return true;
        case "error":
        default:
            alert("Error: " + msg.error);
            return false;
    }
}

// Returns false if the chunk couldn't be read or if it contained an error status
function handleResponseChunk(chunk) {
    let str = decoder.decode(chunk);
    try {
        let msg = JSON.parse(str);

        console.log(msg);

        // If two messages were sent in the same chunk, they'll be in an array
        if (Array.isArray(msg)) {
            return !msg.map(handleResponseJson).some(r => !r);
        } else {
            // Otherwise, just handle the message
            return handleResponseJson(msg);
        }
    } catch (e) {
        console.log("Failed to parse chunk: " + e);
        console.log("Chunk: " + str);
        // return false;
        return true;
    }
}

function search(query, vendor, num) {
    clearProducts();
    bar.disabled = true;
    bar_btn.classList.add("disabled");
    vendor_btn.classList.add("disabled");
    num_input.disabled = true;

    let url = `/compare/${query}?vendor=${vendor}&num=${num}`;
    fetch(url).then(res => {
        let stream = res.body;
        readChunks(stream, handleResponseChunk).then(success => {
            console.log("Done reading product stream");
            status.classList.add("d-none");
            bar.disabled = false;
            bar_btn.classList.remove("disabled");
            vendor_btn.classList.remove("disabled");
            num_input.disabled = false;

            if (!success) {
                console.log("Failed to read product stream");
            }
        })
    });
}

function search_callback() {
    let query = bar.value;
    let vendor = vendor_btn.dataset.vendor;
    let num = num_input.value;

    search(query, vendor, num);
}

bar.addEventListener("keydown", e => {
    if (e.key === "Enter") {
        search_callback();
        e.preventDefault();
    }
});

bar_btn.addEventListener("click", search_callback);
