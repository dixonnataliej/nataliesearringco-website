import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

export default function Tag({ url, onClick }) {
    const [tagid, setTagid] = useState("");
    const [tagName, setTagName] = useState("");
    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;

       // Call REST API to get the tag's information
        fetch(url, { credentials: "same-origin" })
          .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
          })
          .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
              setTagid(data.tagid);
              setTagName(data.name);
            }
          })
          .catch((error) => console.log(error));

        return () => {
          // This is a cleanup function that runs whenever the Tag component
          // unmounts or re-renders. If a Tag is about to unmount or
          // re-render, we should avoid updating state.
          ignoreStaleRequest = true;
        };
    }, [url]);

  return (
  <div className="tag_btn">
  <button id="tag-name-btn" onClick={() => onClick(tagid)} >
     {tagName}
  </button>
  </div>
  )
};

Tag.propTypes = {
  url: PropTypes.string.isRequired,
};