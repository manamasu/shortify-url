import { useEffect, useState } from "react";
import axios from "axios";
import URLCard from "./URLCard";

export default function URLList() {
  const [urls, setURLs] = useState([]);

  useEffect(() => {
    const fetchURLs = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/v1/urls");
        console.log(response.data);

        setURLs(response.data);
      } catch (err) {
        console.log("Theere was an error retrieving all urls", err);
      }
    };
    fetchURLs();
  }, []);

  urls.map((url) => console.log(url));

  return (
    <div className="flex-1 border-2">
      <h1 className="m-2 font-semibold">My URLs</h1>
      {urls.map((url) => {
        return <URLCard title={url.title} short_url={url.short_url} />;
      })}
    </div>
  );
}
