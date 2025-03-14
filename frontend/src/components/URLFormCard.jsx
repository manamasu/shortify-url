import { useState } from "react";
import { postURL } from "../api/api";

export default function URLFormCard() {
  const [title, setTitle] = useState();
  const [longURL, setLongURL] = useState();

  function handleSubmit(e) {
    e.preventDefault();

    postURL({ title: title, long_url: `${longURL}` });

    setTitle(null);
    setLongURL(null);
  }

  return (
    <div className="border-2 p-4 shadow-2xl border-purple-300">
      <h1 className="text-2xl pb-2">Shorten your URL now!</h1>
      <form
        className="flex flex-col gap-4 items-center"
        onSubmit={handleSubmit}
      >
        <input
          className="rounded border-2 p-1 w-full"
          type="text"
          placeholder="Enter your title here (Optional)"
          onChange={(ev) => {
            setTitle(ev.currentTarget.value);
          }}
        ></input>
        <input
          className="rounded border-2 p-1 w-full"
          type="url"
          placeholder="Enter your long URL here"
          required
          onChange={(ev) => {
            setLongURL(ev.currentTarget.value);
          }}
        />
        <button
          type="submit"
          className="mt-4 border-2 rounded p-1 w-full cursor-pointer"
        >
          Shortify
        </button>
      </form>
    </div>
  );
}
