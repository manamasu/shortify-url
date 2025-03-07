export default function URLShortener() {
  return (
    <div>
      <form>
        <input type="search" placeholder="Enter your URL here" />
        <button type="submit" className="border-2 rounded">
          Shortify
        </button>
      </form>
    </div>
  );
}
