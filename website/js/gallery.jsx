import React, { useState, useEffect } from "react";
import Post from "./post";
import Tag from "./tag";

export default function Gallery() {
  const [postUrls, setPostUrls] = useState([]); // State to store the URLs
  const [next, setNext] = useState("");
  const [hasMore, setHasMore] = useState(true);
  const [tagUrls, setTagUrls] = useState([]);

  const fetchPost = (url) => {
    console.log(`Fetching posts from ${url}`);
    let ignoreStaleRequest = false;

    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json(); // Parse the JSON response
      })
      .then((data) => {
        console.log("Fetched posts:", data.results); // Log posts data
        if (!ignoreStaleRequest) {
          const newUrls = data.results.map((item) => item.url);
          setPostUrls(newUrls);

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
    fetchTags();
  }, []); // Only runs on the first render

  //fetch posts for a certain tag id
  const fetchPostByTag = (tagid) => {
    fetchPost(`/api/v1/posts/?tagid=${tagid}`);
  };

  // Fetch the next page
  const fetchNext = () => {
    if (next) {
      fetchPost(next);
    }
  };

  const fetchTags = () => {
    let ignoreStaleRequest = false;

    fetch("/api/v1/tags/", { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json(); // Parse the JSON response
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
        setTagUrls((prevTagUrls) => {
          const newUrls = data.map((item) => item.url);
          return [...new Set([...prevTagUrls, ...newUrls])];
        });
        }
      })
      .catch((error) => console.log(error));

    return () => {
      console.log("Cleaning up fetch");
      ignoreStaleRequest = true;
    };
  };

  return (
  <div>
  <div className="tags">
  <button
          id="all-posts-btn"
          className="tag_btn" // same style as the tags
          onClick={() => fetchPost("/api/v1/posts/")}
        >
          All
        </button>
  {tagUrls.map((url) => (
        <Tag key={url} url={url} onClick={fetchPostByTag} />
    ))}
  </div>
  <div className="gallery">
  {postUrls.map((url) => (
            <Post key={url} url={url} />
          ))}
  </div>
  </div>
  );
}