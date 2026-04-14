import { useEffect, useState } from "react";

export default function App() {
  const [d, setD] = useState({});

  useEffect(() => {
    const t = setInterval(async () => {
      const r = await fetch("/event", { method: "POST", body: "{}" });
      setD(await r.json());
    }, 1000);

    return () => clearInterval(t);
  }, []);

  return <pre>{JSON.stringify(d, null, 2)}</pre>;
}
