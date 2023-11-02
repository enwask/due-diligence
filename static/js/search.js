const decoder = new TextDecoder();

// Read chunks from a stream and pass them to a function.
// If the passed function returns false for any chunk, this one stops reading and likewise returns false.
async function readChunks(stream, fun) {
    const reader = stream.getReader();

    // Iterate returned chunks until the stream is closed
    let chunk, end;
    while (!end) {
        ({value: chunk, done: end} = await reader.read());
        if (end) return true;

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
            return true;
        case "product":
            addProduct(msg);
            return true;
        case "error":
        default:
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
        // return false;
        return true;
    }
}

function search(query, vendor) {
    clearProducts();

    let url = `/compare/${query}?vendor=${vendor}`;
    fetch(url).then(res => {
        let stream = res.body;
        readChunks(stream, handleResponseChunk).then(success => {
            if (!success) {
                console.log("Failed to read product stream");
            }
        })
    });
}
