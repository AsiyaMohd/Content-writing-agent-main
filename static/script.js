// 





/* --- Form Submission Logic (Simplified for Single Input) --- */

// NOTE: All tab-related HTML elements must be removed from the page.
// We are only keeping the elements related to the single form.

const btn = document.getElementById("generateBtn");
const queryBox = document.getElementById("query");
const contentTypeDropdown = document.getElementById("content_type"); // Renamed for clarity
const responseBox = document.getElementById("response");
const loading = document.getElementById("loading");
const fileInput = document.getElementById("pdffile");
const downloadBtn = document.getElementById("downloadBtn");

const linksBox = document.getElementById("links-box");
const linksList = document.getElementById("links-list");
const fileNameDisplay = document.getElementById("file-name-display"); // Must exist in HTML
const loadingMessageEl = document.getElementById("loading-message");

let selectedContentType = "";
let messageInterval; // Variable to hold the interval timer

const creativeMessages = [
    "🧠 The AI is brainstorming brilliant ideas for you...",
    "✨ Polishing the prose and refining the rhetoric...",
    "🔍 Checking sources and gathering the best information...",
    "✍️ Crafting content that cuts through the noise...",
    "🚀 Preparing your content for launch, almost there...",
    "☕ Just a moment, brewing up something amazing...",
    "💡 Thinking deeply to provide the perfect response...",
];

/**
 * Toggles the disabled state of form elements during processing.
 * @param {boolean} isDisabled - True to disable (while loading), false to enable (on completion/error).
 */
function setFormState(isDisabled) {
    
    btn.disabled = isDisabled;
    
    contentTypeDropdown.disabled = isDisabled;
   
    queryBox.disabled = isDisabled;
   
    fileInput.disabled = isDisabled;
    console.log(fileInput)

  
    if (isDisabled) {
        btn.innerHTML = '<div class="spinner-small"></div> Generating...';
        btn.innerHTML = '<i class="fas fa-magic"></i> Generate Content';
    }
}


/**
 * Parses a URL string and returns its domain and full, clean href.
 * @param {string} linkUrl - The raw URL string from the server.
 * @returns {object|null} An object { domain, href } or null if parsing fails.
 */
function getDomainFromUrl(linkUrl) {
    try {
        // First, clean the link of any stray quotes or backslashes and trim whitespace
        let cleanedUrl = String(linkUrl).replace(/"/g, '').replace(/\\/g, '').trim();

        // Check for and fix partial/missing protocols (like "tps://" or "www.google.com")
        if (!cleanedUrl.startsWith('http://') && !cleanedUrl.startsWith('https://')) {
            if (cleanedUrl.includes('://')) {
                // Fixes "tps://", "ftp://", etc.
                cleanedUrl = 'https://' + cleanedUrl.split('://')[1];
            } else {
                // Adds protocol to "www.google.com"
                cleanedUrl = 'https://' + cleanedUrl;
            }
        }
        
        const url = new URL(cleanedUrl);
        
        // Return both the domain (for display) and the full href (for the link)
        return {
            domain: url.hostname, // e.g., "www.kiwiqa.com"
            href: url.href        // e.g., "https://www.kiwiqa.com/full/path"
        };

    } catch (e) {
        console.error("Could not parse URL:", linkUrl, e);
        return null; // Return null on failure so we can skip it
    }
}

// Event listener for file selection feedback
fileInput.addEventListener('change', () => {
    // Check if any files were selected
    if (fileInput.files.length > 0) {
        // Display the name of the first file
        fileNameDisplay.textContent = `✅ File selected: ${fileInput.files[0].name}`;
    } else {
        // Clear the display if the user cancels the selection
        fileNameDisplay.textContent = '';
    }
});


/**
 * Starts cycling through the creative loading messages.
 */
function startLoadingMessages() {
    let index = 0;
    
    // Set the initial message
    loadingMessageEl.textContent = creativeMessages[index];

    // Set an interval to change the message every few seconds
    messageInterval = setInterval(() => {
        index = (index + 1) % creativeMessages.length;
        loadingMessageEl.textContent = creativeMessages[index];
    }, 3000); // Change message every 3 seconds (3000ms)
}

/**
 * Stops cycling messages and clears the interval.
 */
function stopLoadingMessages() {
    clearInterval(messageInterval);
}

btn.addEventListener("click", async () => {
    const query = queryBox.value.trim();
    const query2 = contentTypeDropdown.value.trim(); // Use the new variable name
    const file = fileInput.files[0];
    selectedContentType = query2;

    // Optional: Add a check for minimum input
    if (!query && !file) {
        return alert("Please enter text or upload a file before generating!");
    }

    // 1. Reset the UI AND DISABLE THE FORM
    responseBox.value = "";
    loading.style.display = "flex";
    downloadBtn.style.display = "none";
    responseBox.style.display = "none";
    linksBox.style.display = "none";
    linksList.innerHTML = ""; 
    
    // 🔥 CORE CHANGE: Disable the form elements
    setFormState(true); 
    
    // Start message cycle
    startLoadingMessages();
    
    // 2. Prepare Form Data
    const formData = new FormData();
    
    // Append file only if it exists
    if (file) {
        formData.append("file", file);
    }

    formData.append("query2", query2);
    
    // Ensure 'query' is always sent, even if empty, as an empty string (" ")
    if (query) {
        formData.append("query", query);
    } else {
        formData.append("query", " ");
    }
    

    try {
        // 3. Make a single fetch request
        const res = await fetch("/generate", {
            method: "POST",
            body: formData,
        });

        // 4. Check for server errors
        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.error || `Server error: ${res.status}`);
        }

        // 5. Parse the complete JSON response
        const data = await res.json();

        // 6. Handle the 'response' text and cleanup
        const responseText = data.response || "No response generated.";
        
        // IMPROVED: Single, comprehensive cleanup regex
        let cleaned = responseText
            // 1. Remove common markdown symbols (*, #, >, `, ~, _, - at start of line, etc.)
            .replace(/[#*`~_]+/g, '') 
            .replace(/^- /gm, '') // remove list hyphens
            // 2. Collapse multiple consecutive empty lines to just two newlines (single blank line)
            .replace(/\n\s*\n\s*/g, '\n\n')
            .trim();
    
        responseBox.value = cleaned;
        responseBox.style.display = "block";

        // 7. Handle the 'links' (Unchanged)
        const linksString = data.links || "";
        let links = [];
        
        if (linksString) {
            links = linksString.split("\n\n---\n\n");
        }

        if (links.length > 0 && links[0] !== '') {
            linksList.innerHTML = links.map(link => {
                
                const urlParts = getDomainFromUrl(link);
                
                if (!urlParts) {
                    return ''; 
                }

                const domain = urlParts.domain;
                const cleanHrefe = urlParts.href; 
                const cleanHref = cleanHrefe.slice(0, -1);
                
                const favicon = `https://www.google.com/s2/favicons?domain=${domain}&sz=32`; 

                return `
                    <li class="link-pill">
                        <img src="${favicon}" alt="favicon" class="link-favicon">
                        <a href="${cleanHref}" target="_blank" rel="noopener noreferrer">
                            ${domain}
                        </a>
                    </li>
                `;
            }).join("");
            
            linksBox.style.display = "block";
        }

        // 8. Show download button if there is content
        if (responseBox.value.trim().length > 0) {
            downloadBtn.style.display = "inline-block"; 
        }

    } catch (e) {
        // Handle any network or parsing errors
        console.error("Failed to generate response:", e);
        responseBox.style.display = "block";
        responseBox.value = `An error occurred: ${e.message}`;
        alert(`An error occurred: ${e.message}`);
    } finally {
        // 9. Always hide the loader, stop messages, AND RE-ENABLE THE FORM
        loading.style.display = "none";
        stopLoadingMessages(); 
        
        setFormState(false);
    }
});


/* --- Download Button Logic --- */
downloadBtn.addEventListener("click", function () {
    const text = responseBox.value;
    if (!text.trim()) return alert("No content to download!");

    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `response_${selectedContentType || 'generated'}.txt`;
    link.click();
});