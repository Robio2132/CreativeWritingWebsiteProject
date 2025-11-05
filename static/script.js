const writingArea = document.getElementById("writingArea");
const wordCount = document.getElementById("wordCount");
const promptElement = document.getElementById("prompt");

// Expand textarea and track words
writingArea.addEventListener("input", () => {
  writingArea.style.height = "auto";
  writingArea.style.height = writingArea.scrollHeight + "px";

  const text = writingArea.value.trim();
  const words = text === "" ? 0 : text.split(/\s+/).length;
  wordCount.textContent = `Words: ${words}`;
});

// Fetch prompt from Flask API
async function loadPrompt() {
  const genre = document.getElementById("genre").value;
  const tone = document.getElementById("tone").value;

  promptElement.textContent = "Loading prompt...";

  try {
    const res = await fetch(`/api/prompt?genre=${encodeURIComponent(genre)}&tone=${encodeURIComponent(tone)}`);
    const data = await res.json();
    promptElement.textContent = data.prompt || "No prompt available.";
  } catch (err) {
    promptElement.textContent = "Error loading prompt. Try again.";
  }
}

// Event listeners
document.getElementById("newPromptBtn").addEventListener("click", loadPrompt);

// Auto-load a random prompt on page load
document.addEventListener("DOMContentLoaded", loadPrompt);
