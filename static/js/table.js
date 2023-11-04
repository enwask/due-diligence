const table = document.getElementById("result");
const thead = table.tHead;
const tbody = table.tBodies[0];

const price_format = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
});

let products = []

function fixColumnName(name) {
    if (name.length <= 3) return name.toUpperCase();

    return name.replace(/\w\S*/g, str => {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    });
}

function fixValue(value) {
    if (value === true) return "yes";
    if (value === false) return "no";

    return value;
}

function rebuildTable() {
    // Count occurrences of feature keys in all products
    let col_counts = {}
    products.forEach(p => {
        for (const key in p.features) {
            if (key in col_counts) col_counts[key]++
            else col_counts[key] = 1;
        }
    });

    // Find features in common and compute their display names
    let cols = Object.keys(col_counts)
        .filter(key => col_counts[key] >= Math.max(4, products.length / 2))
        .map(key => [key, fixColumnName(key)]);

    // Clear the table
    thead.innerHTML = "";
    tbody.innerHTML = "";

    // Create table header
    let tr = thead.insertRow();

    // Add a column for product names
    let th_product = document.createElement("th");
    th_product.scope = "col";
    th_product.innerHTML = "Product";
    tr.appendChild(th_product);

    // Add price column
    let th_price = document.createElement("th");
    th_price.scope = "col";
    th_price.innerHTML = "Price";
    tr.appendChild(th_price);

    // Add columns for features
    for (const [key, name] of cols) {
        // Create a column header element
        let th = document.createElement("th");

        // Set the scope and text
        th.scope = "col";
        th.innerHTML = name;

        // Append the column header
        tr.appendChild(th);
    }

    // Create table body
    for (const product of products) {
        // Create a row element
        let tr = tbody.insertRow();

        // Create the product name cell
        let td_product = tr.insertCell();
        td_product.innerHTML = `<a href="${product.url}">${product.name}</a>`;

        // Create the price cell
        let td_price = tr.insertCell();
        td_price.innerHTML = price_format.format(product.price);

        // Create columns
        for (const [key, name] of cols) {
            // Create a column element
            let td = tr.insertCell();

            // Set the text
            if (key in product.features) td.innerHTML = fixValue(product.features[key]);
            else td.innerHTML = "<span class='fg-subtle'>n/a</span>";
        }
    }

    // Show the table
    table.classList.remove("d-none");
}

function clearProducts() {
    products.length = 0;
}

function addProduct(product) {
    products.push(product);
    rebuildTable();
}
