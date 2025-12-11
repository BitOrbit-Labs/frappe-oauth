import React, { useEffect, useState } from "react";

function App() {
  const [tokenData, setTokenData] = useState(null);
  const [items, setItems] = useState(null);

  const backend = process.env.REACT_APP_BACKEND_URL;

  const handleLogin = () => {
    window.location.href = `${backend}/login`;
  };

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (code) {
      fetch(`${backend}/callback?code=${code}`)
        .then((res) => res.json())
        .then((data) => {
          setTokenData(data);
          // fetch items
          return fetch(`${backend}/items?access_token=${data.access_token}`);
        })
        .then((res) => res.json())
        .then(setItems)
        .catch(console.error);
    }
  }, [backend]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Frappe OAuth2 Demo</h1>
      {!tokenData && <button onClick={handleLogin}>Login with Frappe</button>}
      {tokenData && (
        <>
          <h2>Access Token</h2>
          <pre>{JSON.stringify(tokenData, null, 2)}</pre>
        </>
      )}
      {items && (
        <>
          <h2>Items</h2>
          <pre>{JSON.stringify(items, null, 2)}</pre>
        </>
      )}
    </div>
  );
}

export default App;
