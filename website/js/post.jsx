import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

export default function Post({ url }) {
    const [postUrl, setPostUrl] = useState("");
    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;
        setPostUrl(url)

        /*    // Call REST API to get the post's information
        fetch(url, { credentials: "same-origin" })
          .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
          })
          .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
              setPostUrl(data.posturlsomethingsomething);
            }
          })
          .catch((error) => console.log(error)); */

        return () => {
          // This is a cleanup function that runs whenever the Post component
          // unmounts or re-renders. If a Post is about to unmount or re-render, we
          // should avoid updating state.
          ignoreStaleRequest = true;
        };
    }, [url]);

  return (
     <div className="post">
     this is where posturl should be:
     <p>{postUrl}</p>
     </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};