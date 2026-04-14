import { useEffect, useState } from "react";

export default function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    const timer = setInterval(async () => {
      const response = await fetch("/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      setData(await response.json());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
