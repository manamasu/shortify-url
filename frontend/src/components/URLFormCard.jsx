export default function URLFormCard() {
  return (
    <div className="border-2 p-4 shadow-2xl border-purple-300 h-56 w-80">
      <h1>Shorten your URL now!</h1>
      <form className="flex flex-col gap-4 items-center">
        <input
          className="rounded border-2 p-1 w-full"
          type="text"
          placeholder="Enter your title here (Optional)"
        ></input>
        <input
          className="rounded border-2 p-1 w-full"
          type="url"
          placeholder="Enter your long URL here"
          required
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
