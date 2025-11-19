
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { useEffect, useState } from "react";

async function registerUser({username,password,iban}, setMessage) {
    const inputs = { username, password, iban };

    const res = await fetch("http://127.0.0.1:8000/user/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs)
    });

    const data = await res.json();
    setMessage(data.message);
}

async function loginUser({username,password}, setUser) {
    const inputs = { username, password };

    const res = await fetch("http://127.0.0.1:8000/user/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs)
    });

    const data = await res.json();
    setUser(data.token);
    console.log(data)
}

function App() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [iban, setIban] = useState("");

    const [message, setMessage] = useState("");
    const [token, setUser] = useState("");

    return (
        <div>
            <div>
                <input
                    type="text"
                    placeholder="Username"
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Iban"
                    onChange={(e) => setIban(e.target.value)}
                />
                <button onClick={() => registerUser({username, password, iban},setMessage)}>Register</button>
                <h1>Message du backend :</h1>
                <p>{message}</p>
            </div>
            <div>
                <button onClick={() => loginUser({username, password},setUser)}>Register</button>
                <h1>Message du backend :</h1>
                <p>{token}</p>
            </div>

        </div>
    );
}

export default App;