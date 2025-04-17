const canvas = document.querySelector("canvas")
const ctx = canvas.getContext("2d")
const rect = canvas.getBoundingClientRect()
const button = document.getElementById("push")
// const screen = document.getElementById("screen")

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
canvas.addEventListener("touchstart", () => state = true)
canvas.addEventListener("touchend", () => state = false)

const draw = e => {
  if (state) {
    x = e.x - rect.left
    y = e.y - rect.top
    x = Math.floor(x / 10) * 10
    y = Math.floor(y / 10) * 10
    ctx.fillRect(x, y, 10, 10)
  }
}

canvas.addEventListener("touchmove", e => {
  if (state) {
    e = e.touches[0]
    x = e.clientX - rect.left
    y = e.clientY - rect.top
    x = Math.floor(x / 10) * 10
    y = Math.floor(y / 10) * 10
    ctx.fillRect(x, y, 10, 10)
  }
})

canvas.addEventListener("mousemove", draw)

button.onclick = () => {
  fetch("http://127.0.0.1:8000", {
    method: "POST",
    body: JSON.stringify(data)
  })
}

// screen.onclick = () => document.querySelector("main").requestFullscreen()

