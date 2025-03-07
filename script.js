document.getElementById("input-type").addEventListener("change", function () {
    const inputType = this.value;
    document.getElementById("text-input").style.display = inputType === "text" ? "block" : "none";
    document.getElementById("audio-input").style.display = inputType === "audio" ? "block" : "none";
    document.getElementById("image-input").style.display = inputType === "image" ? "block" : "none";
});

document.getElementById("translator-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const inputType = document.getElementById("input-type").value;
    const targetLanguage = document.getElementById("target-language").value;
    const formData = new FormData();

    formData.append("input_type", inputType);
    formData.append("target_language", targetLanguage);

    if (inputType === "text") {
        formData.append("text", document.getElementById("text").value);
    } else if (inputType === "audio") {
        formData.append("audio_file", document.getElementById("audio").files[0]);
    } else if (inputType === "image") {
        formData.append("image_file", document.getElementById("image").files[0]);
    }

    const response = await fetch("/translate", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();
    document.getElementById("original-text").textContent = result.original_text || "N/A";
    document.getElementById("translated-text").textContent = result.translated_text || "N/A";
});