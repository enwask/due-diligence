const dropdown_btn = document.getElementById("search-vendor-btn");
const dropdown_options = [...document.getElementsByClassName("search-vendor-option")];

function selectVendor(el) {
    // dropdown_options.forEach(el => el.classList.remove("active"))
    // el.classList.add("active");

    dropdown_btn.innerHTML = el.innerHTML + "&nbsp;";
    dropdown_btn.dataset.vendor = el.id;
}

dropdown_options.forEach(el => {
    el.addEventListener("click", () => {
        selectVendor(el);
    });
});

window.onload = () => {
    let vendor = dropdown_btn.dataset.vendor;
    selectVendor(document.getElementById(vendor));
}
