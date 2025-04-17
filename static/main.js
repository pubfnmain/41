const canvas = document.querySelector("canvas")
const ctx = canvas.getContext("2d")
const rect = canvas.getBoundingClientRect()
const button = document.querySelector("button")

ctx.fillStyle = "#0f0f0f"
ctx.fillRect(0, 0, 320, 320)

ctx.fillStyle = "#efefef"

let state = false;
let x, y

function create_data() {
  return Array(32).fill(0)
}

let data = create_data()

canvas.addEventListener("mousedown", () => state = true)
canvas.addEventListener("mouseup", () => state = false)
canvas.addEventListener("mousemove", e => {
  if (state)
    x = e.x - rect.left
    y = e.y - rect.top
    x = Math.floor(x / 10) * 10
    y = Math.floor(y / 10) * 10
    ctx.fillRect(x, y, 10, 10)
})

button.onclick = () => {
  fetch("http://127.0.0.1:8000", {
    method: "POST",
    body: JSON.stringify(data)
  })
}

