/**
 * @file ./client/src/App.js
 * @author Camden Smith
 * @course CIS350
 * @assignment Assignment 1
 * @date 5/22/2026
 * @brief React client for displaying and creating fish entries.
 */

import "./App.css";
import { useState, useEffect } from "react";
import Axios from "axios";

function App() {
  const [listOfFish, setListOfFish] = useState([]);
  const [fish, setFish] = useState("");
  const [length, setLength] = useState(0);
  const [weight, setWeight] = useState(0);
  const [location, setLocation] = useState("");

  useEffect(() => {
    Axios.get("http://localhost:3001/getFish").then((response) => {
      setListOfFish(response.data);
    });
  }, []);

  const createFish = () => {
    Axios.post("http://localhost:3001/createFish", {
      fish,
      length,
      weight,
      location,
    }).then((response) => {
      setListOfFish([
        ...listOfFish,
        {
          fish,
          length,
          weight,
          location,
        },
      ]);
    });
  };

  return (
    <div className="App">
      <div className="fishDisplay">
        {listOfFish.map((f) => {
          return (
            <div>
              <h1>Fish: {f.fish}</h1>
              <h3>Length: {f.length}</h3>
              <h3>Weight: {f.weight}</h3>
              <h3>Location: {f.location}</h3>
            </div>
          );
        })}
      </div>
      <div>
        <input
          type="text"
          placeholder="Fish..."
          onChange={(event) => {
            setFish(event.target.value);
          }}
        />
        <input
          type="number"
          step="0.1"
          placeholder="Length..."
          onChange={(event) => {
            setLength(parseFloat(event.target.value));
          }}
        />
        <input
          type="number"
          step="0.1"
          placeholder="Weight..."
          onChange={(event) => {
            setWeight(parseFloat(event.target.value));
          }}
        />
        <input
          type="text"
          placeholder="Location..."
          onChange={(event) => {
            setLocation(event.target.value);
          }}
        />
        <button onClick={createFish}> Create Fish </button>
      </div>
    </div>
  );
}

export default App;
