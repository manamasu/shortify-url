export default function URLCard({ title, short_url }) {
  return (
    <div className="flex flex-wrap m-2 pb-2 border-2 rounded w-68">
      <div className="p-2 flex-1">
        <h2>{title}</h2>
        <p>{short_url}</p>
      </div>
    </div>
  );
}
