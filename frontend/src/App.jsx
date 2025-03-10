import Header from "./components/Header";
import Footer from "./components/Footer";
import URLShortener from "./components/URLShortener";

function App() {
  return (
    <div className=" bg-linear-to-r from-indigo-400 to-sky-400 flex flex-col min-h-screen">
      <Header />
      <URLShortener />
      <Footer />
    </div>
  );
}

export default App;
