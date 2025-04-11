window.onload = () => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  setupDrawing(canvas, ctx);
};

function setupDrawing(canvas, ctx) {
  let drawing = false;

  canvas.addEventListener("mousedown", () => drawing = true);
  canvas.addEventListener("mouseup", () => drawing = false);
  canvas.addEventListener("mouseout", () => drawing = false);

  canvas.addEventListener("mousemove", (e) => {
    if (!drawing) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(x, y, 8, 0, Math.PI * 2);
    ctx.fill();
  });
}

document.getElementById("predictBtn").addEventListener("click", async () => {
  const canvas = document.getElementById("canvas");
  canvas.toBlob(async (blob) => {
    const formData = new FormData();
    formData.append("file", blob, "digit.png");

    document.getElementById("loader").classList.remove("hidden");
    document.getElementById("prediction").innerText = "Processing...";

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData
      });

      const result = await response.json();
      document.getElementById("prediction").innerText = result.prediction;
    } catch (error) {
      console.error("Prediction failed:", error);
      document.getElementById("prediction").innerText = "Error";
    }

    document.getElementById("loader").classList.add("hidden");
  });
});

document.getElementById("clearBtn").addEventListener("click", () => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  document.getElementById("prediction").innerText = "None";
});
