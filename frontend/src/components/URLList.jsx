import { useEffect, useState } from "react";
import URLCard from "./URLCard";
import { getURLs } from "../api/api";

export default function URLList() {
  const [urls, setURLs] = useState([]);

  useEffect(() => {
    getURLs().then((val) => {
      setURLs(val);
    });
  }, []);

  urls.map((url) => console.log(url));

  return (
    <div className="flex-1 border-2">
      <h1 className="m-2 font-semibold">My URLs</h1>
      {urls.map((url) => {
        return (
          <URLCard
            key={url.id}
            title={url.title}
            short_url={url.short_url}
            long_url={url.long_url}
          />
        );
      })}
    </div>
  );
}
