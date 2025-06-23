import { AccordionElement } from "./accordion"
import { useEffect, useState } from "react"

function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch("/cache/6829.pr.json")
      .then(res => res.json())
      .then(setData)
      .catch(console.error)
  }, [])

  return (
    <div className="flex min-h-svh flex-col items-center justify-center px-[10%]">
      <AccordionElement entries={data ? [data] : []} />
    </div>
  )
}

export default App
