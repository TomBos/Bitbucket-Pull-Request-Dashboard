import { AccordionElement } from "./accordion"
import { useEffect, useState } from "react"

function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch("/api/serve-content")
      .then(async (res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }
        const text = await res.text()
        try {
          const json = JSON.parse(text)
          console.dir(json)
          setData(json)
        } catch (e) {
          console.error("JSON parse error:", e, "Response text:", text)
        }
      }).catch((err) => {
        console.error("Fetch error:", err)
      })
  }, [])
  
  return (
    <div className="flex min-h-svh flex-col items-center justify-center px-[10%] py-[30px]">
        <AccordionElement entries={data ?? []} />
    </div>
  )


}

export default App
