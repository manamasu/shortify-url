import URLFormCard from "./URLFormCard";
import URLList from "./URLList";

export default function URLShortener() {
  return (
    <div className="flex-1 flex justify-between mt-4 mb-8 ml-4 mr-8 gap-12">
      <URLFormCard />
      <div className="flex flex-col w-72">
        <h1 className="text-2xl">Create shorter URLs with Shortify.</h1>
        <p className="">
          A short-url is being generated based on a machine learning model.
        </p>
        <p>Additionally you get a free QR-Code!</p>
      </div>
      <URLList />
    </div>
  );
}
