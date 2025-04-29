import { useEffect, useRef, useState } from "react"


function createData() {
  return Array.from({length: 50}, () => Array(50).fill(0))
}


export default function App() {
  const [data, setData] = useState(createData())
  const canvasRef = useRef(null)

  const letters = "абвгдеёжзийклмнңоөпрстуүфхцчшщъыьэюя".split('')
  const [result, setResult] = useState(Object.fromEntries(
    letters.map(letter => [letter, 0])
  ))

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    ctx.fillStyle = "#3f3f3f"
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = "#efefef"
  }, [data])

  const fill = (ctx, x, y) => {
      ctx.fillRect(x * 10, y * 10, 10, 10)
      data[y][x] = 1
      setData(data)
  }
  const vectors = [[1, 1], [1, 0], [0, 1]]

  console.log(1)

  let state = false
  let x, y
  const down = () => {
    state = true
  }
  const up = () => {
    state = false
    push()
  }
  const move = e => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const ctx = canvas.getContext("2d")
    if (state) {
      e = e.nativeEvent
      x = e.x - rect.left
      y = e.y - rect.top
      x = Math.floor(x / 10)
      y = Math.floor(y / 10)

      fill(ctx, x, y)
      for (const [dx, dy] of vectors)
        fill(ctx, x + dx, y + dy)
    }
  }

  function clear() {
    setData(createData())
    setResult(Object.fromEntries(
      letters.map(letter => [letter, 0])
    ))
  }


  function push() {
    console.log(data)
    fetch("http://127.0.0.1:8000", {
      method: "POST",
      body: JSON.stringify(data)
    })
    .then(data => data.json())
    .then(data => setResult(data))
  }
  
  return <>
    <div>
      <div>
        <button onClick={clear}>clear</button>
        <button onClick={push}>push</button>
      </div>
      <canvas
        ref={canvasRef}
        width={500}
        height={500}
        onMouseDown={down}
        onMouseUp={up}
        onMouseMove={move}
      />
      <div className="fs m-1">
        Result: {
          Object.values(result).some(i => i > 0)
            ? Object.keys(result).reduce((a, b) => result[a] > result[b] ? a : b)
            : null
        }
      </div>
    </div>
    <div id="result">{Object.entries(result).map(([k, v]) => <div key={k}>{k}: {v}</div>)}</div>
  </>
}
