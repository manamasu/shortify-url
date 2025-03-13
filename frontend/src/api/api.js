import axios from "axios";

export async function getURLs() {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/v1/urls");
    return response.data;
  } catch (err) {
    console.log("There was an error retrieving all urls", err);
  }
}

export async function deleteURL(id) {
  try {
    const response = await axios.delete(
      `http://127.0.0.1:8000/api/v1/urls/${id}`
    );
    console.log(response.data);
    return;
  } catch (err) {
    console.log("There was an error retrieving all urls", err);
  }
}
