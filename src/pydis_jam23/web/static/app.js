window.onload = () => {
    document.getElementById("fileInput").onchange = (event) => {
        let file = event.target.files[0];
        let data = new FormData();
        data.append("image", file);
        fetch("/current_image", {
            method: "POST",
            body: data,
        }).then(() => window.location.reload());
    };
};
