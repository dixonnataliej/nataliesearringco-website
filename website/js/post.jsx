import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

export default function Post({ url }) {
    const [APIPostUrl, setAPIPostUrl] = useState("");
    const [humanPostUrl, setHumanPostUrl] = useState("");
    const [imgUrl, setImgUrl] = useState("");
    const [name, setName] = useState("");
    const [price, setPrice] = useState("");
    const [description, setDescription] = useState("");
    const [status, setStatus] = useState("");
    const [timestamp, setTimestamp] = useState("");
    const [tags, setTags] = useState([]);
    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;
        setAPIPostUrl(url)

       // Call REST API to get the post's information
        fetch(url, { credentials: "same-origin" })
          .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
          })
          .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
              setHumanPostUrl(data.humanPostUrl);
              setImgUrl(data.img_url);
              setName(data.name);
              setPrice(data.price);
              setDescription(data.description);
              setStatus(data.status);
              setTimestamp(dayjs.utc(data.created).local().fromNow());
              setTags(data.tags);
            }
          })
          .catch((error) => console.log(error));

        return () => {
          // This is a cleanup function that runs whenever the Post component
          // unmounts or re-renders. If a Post is about to unmount or re-render, we
          // should avoid updating state.
          ignoreStaleRequest = true;
        };
    }, [url]);

  return (
     <div className="post">
     <a href={humanPostUrl}>
     this is where posturl should be:
     <p>{APIPostUrl}</p>
     <img src={imgUrl} alt={name} className="post-image" />
      <h2 className="post-name">{name}</h2>
      <p className="post-price">{price}</p>
      <p className="post-description">{description}</p>
      <p className="post-status">{status}</p>
      <p className="post-timestamp">{timestamp}</p>
      <ul className="post-tags">
        {tags.map((tag, index) => (
          <li key={index} className="post-tag">
            {tag}
          </li>
        ))}
      </ul>
      </a>
     </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};