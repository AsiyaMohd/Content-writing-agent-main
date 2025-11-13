/* =========================================================
   Content Generation Script
   Handles form submission, file input, word count slider,
   loading messages, and response rendering.
   ========================================================= */

/* --- Element References --- */
const btn = document.getElementById("generateBtn");
const queryBox = document.getElementById("query");
const contentTypeDropdown = document.getElementById("content_type");
const responseBox = document.getElementById("response");
const loading = document.getElementById("loading");
const fileInput = document.getElementById("pdffile");
const downloadBtn = document.getElementById("downloadBtn");
const linksBox = document.getElementById("links-box");
const linksList = document.getElementById("links-list");
const fileNameDisplay = document.getElementById("file-name-display");
const loadingMessageEl = document.getElementById("loading-message");
const range = document.getElementById("range2");
const rangeValue = document.getElementById("rangeValue");

let selectedContentType = "";
let messageInterval;

/* --- Creative Loading Messages --- */
const creativeMessages = [
    "🧠 The AI is brainstorming brilliant ideas for you...",
    "✨ Polishing the prose and refining the rhetoric...",
    "🔍 Checking sources and gathering the best information...",
    "✍️ Crafting content that cuts through the noise...",
    "🚀 Preparing your content for launch, almost there...",
    "☕ Just a moment, brewing up something amazing...",
    "💡 Thinking deeply to provide the perfect response..."
];

/* --- Helper: Enable/Disable Form Elements --- */
function setFormState(isDisabled) {
    btn.disabled = isDisabled;
    contentTypeDropdown.disabled = isDisabled;
    queryBox.disabled = isDisabled;
    fileInput.disabled = isDisabled;
    range.disabled = isDisabled;

    if (isDisabled) {
        btn.innerHTML = '<div class="spinner-small"></div> Generating...';
    } else {
        btn.innerHTML = '<i class="fas fa-magic"></i> Generate Content';
    }
}

/* --- Helper: Parse and Sanitize URL --- */
function getDomainFromUrl(linkUrl) {
    try {
        let cleanedUrl = String(linkUrl).replace(/"/g, '').replace(/\\/g, '').trim();

        if (!cleanedUrl.startsWith('http://') && !cleanedUrl.startsWith('https://')) {
            if (cleanedUrl.includes('://')) {
                cleanedUrl = 'https://' + cleanedUrl.split('://')[1];
            } else {
                cleanedUrl = 'https://' + cleanedUrl;
            }
        }

        const url = new URL(cleanedUrl);
        return { domain: url.hostname, href: url.href };
    } catch (e) {
        console.error("Could not parse URL:", linkUrl, e);
        return null;
    }
}

/* --- File Selection Feedback --- */
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        const names = Array.from(fileInput.files).map(f => f.name).join(", ");
        fileNameDisplay.textContent = `✅ File selected: ${names}`;
    } else {
        fileNameDisplay.textContent = "";
    }
});

/* --- Range Slider Display Update --- */
range.addEventListener("input", () => {
    rangeValue.textContent = range.value;
});

/* --- Loading Messages Cycle --- */
function startLoadingMessages() {
    let index = 0;
    loadingMessageEl.textContent = creativeMessages[index];

    messageInterval = setInterval(() => {
        index = (index + 1) % creativeMessages.length;
        loadingMessageEl.textContent = creativeMessages[index];
    }, 3000);
}

function stopLoadingMessages() {
    clearInterval(messageInterval);
}

/* =========================================================
   Main: Generate Button Click Handler
   ========================================================= */
btn.addEventListener("click", async () => {
    const query = queryBox.value.trim();
    const contentType = contentTypeDropdown.value.trim();
    const file = fileInput.files[0];
    const wordCount = range.value; // new addition
    selectedContentType = contentType;

    if (!query && !file) {
        return alert("Please enter text or upload a file before generating!");
    }

    // Reset UI
    responseBox.value = "";
    responseBox.style.display = "none";
    downloadBtn.style.display = "none";
    linksBox.style.display = "none";
    linksList.innerHTML = "";
    loading.style.display = "flex";

    // Disable form and start loading cycle
    setFormState(true);
    startLoadingMessages();

    // Prepare form data
    const formData = new FormData();
    if (file) formData.append("file", file);
    formData.append("query", query || " ");
    formData.append("content_type", contentType);
    formData.append("wordCount", wordCount);

    try {
        const res = await fetch("/generate", {
            method: "POST",
            body: formData,
        });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.error || `Server error: ${res.status}`);
        }

        const data = await res.json();
        const responseText = data.response || "No response generated.";

        // Clean markdown-style text
        const cleaned = responseText
            .replace(/[#*`~_]+/g, '')
            .replace(/^- /gm, '')
            .replace(/\n\s*\n\s*/g, '\n\n')
            .trim();

        responseBox.value = cleaned;
        responseBox.style.display = "block";

        // Handle source links
        const linksString = data.links || "";
        const links = linksString ? linksString.split("\n\n---\n\n") : [];

        if (links.length > 0 && links[0] !== "") {
            linksList.innerHTML = links.map(link => {
                const urlParts = getDomainFromUrl(link);
                if (!urlParts) return "";
                const { domain, href } = urlParts;
                const favicon = `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;

                return `
                    <li class="link-pill">
                        <img src="${favicon}" alt="favicon" class="link-favicon">
                        <a href="${href}" target="_blank" rel="noopener noreferrer">${domain}</a>
                    </li>
                `;
            }).join("");

            linksBox.style.display = "block";
        }

        // Show download button
        if (responseBox.value.trim().length > 0) {
            downloadBtn.style.display = "inline-block";
        }

    } catch (e) {
        console.error("Failed to generate response:", e);
        responseBox.style.display = "block";
        responseBox.value = `An error occurred: ${e.message}`;
        alert(`An error occurred: ${e.message}`);
    } finally {
        loading.style.display = "none";
        stopLoadingMessages();
        setFormState(false);
    }
});

/* =========================================================
   Download Button Handler
   ========================================================= */
downloadBtn.addEventListener("click", () => {
    const text = responseBox.value;
    if (!text.trim()) return alert("No content to download!");

    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `response_${selectedContentType || 'generated'}.txt`;
    link.click();
});
