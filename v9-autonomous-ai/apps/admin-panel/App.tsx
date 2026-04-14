import { useEffect, useState } from "react";

type InferData = {
  score: number;
  uncertainty?: number;
  policy?: number;
};

export default function App() {
  const [data, setData] = useState<InferData>({ score: 0 });

  useEffect(() => {
    const timer = setInterval(async () => {
      const res = await fetch("/infer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seq: [0.3, 0.7, 0.5, 0.6] }),
      });
      const json = await res.json();
      setData(json);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div>
      <h1>AI Control Panel</h1>
      <h2>Score: {data.score.toFixed(4)}</h2>
      <p>Uncertainty: {data.uncertainty?.toFixed(4) ?? "-"}</p>
      <p>Policy: {data.policy?.toFixed(4) ?? "-"}</p>
    </div>
  );
}
