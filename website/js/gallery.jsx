import React, { useState, useEffect } from "react";
import Post from "./post";

export default function Gallery() {
  const [postUrls, setPostUrls] = useState([]); // State to store the URLs
  const [next, setNext] = useState("");
  const [hasMore, setHasMore] = useState(true);

  const fetchPost = (url) => {
    console.log(`Fetching posts from ${url}`);
    let ignoreStaleRequest = false;

    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json(); // Parse the JSON response
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
        setPostUrls((prevPostUrls) => {
          const newUrls = data.results.map((item) => item.url);
          return [...new Set([...prevPostUrls, ...newUrls])]; // Avoid duplicates
        });

          setNext(data.next);
          setHasMore(!!data.next); // Set hasMore to true if next page exists
        }
      })
      .catch((error) => console.log(error));

    return () => {
      console.log("Cleaning up fetch");
      ignoreStaleRequest = true;
    };
  };

  // Initial fetch
  useEffect(() => {
    fetchPost("/api/v1/posts/");
  }, []); // Only runs on the first render

  // Fetch the next page
  const fetchNext = () => {
    if (next) {
      fetchPost(next);
    }
  };

  return (
  <div className="feed">
  <p> Here's where the java script gallery is: </p>
  {postUrls.map((url) => (
            <Post key={url} url={url} />
          ))}
  </div>
  );
}