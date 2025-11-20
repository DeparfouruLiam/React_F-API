
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

async function selectAccount({iban},setCurrentAccount,token) {
    const inputs = {iban};

    const res = await fetch("http://127.0.0.1:8000/accounts/choose_current_account", {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}`,"Content-Type": "application/json" },
        body: JSON.stringify(inputs)
    });

    const data = await res.json();
    const newIban = data["Current account successfully updated to"]
    if (newIban!=null){
        setCurrentAccount(newIban);
    }
    console.log(newIban);
}

const App = () => {
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [token, setToken] = useState('');
    const [currentAccount, setcurrentAccount] = useState([]);

    // Register variables
    const [message, setMessage] = useState("");
    const [usernameRegister, setUsernameRegister] = useState("");
    const [passwordRegister, setPasswordRegister] = useState("");
    const [ibanRegister, setIbanRegister] = useState("");

    // Login form state
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // Champs pour la recherche par IBAN
    const [ibanSearch, setIbanSearch] = useState('');
    const [searchedAccount, setSearchedAccount] = useState(null);

    // Login function
    async function loginUser() {
        try {
            const inputs = { username, password };

            const res = await fetch("http://127.0.0.1:8000/user/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(inputs),
            });

            if (!res.ok) {
                const errorData = await res.json();
                console.error("Login error:", errorData.detail || "Unknown error");
                setError(errorData.detail || "Login failed");
                return;
            }

            const data = await res.json();

            if (data.token) {
                setToken(data.token);
                localStorage.setItem("token", data.token);
                setError('');
                console.log("Login successful, token:", data.token);
            } else {
                console.error("Token not found in response", data);
            }
        } catch (error) {
            console.error("Network or parsing error:", error);
            setError("Network error");
        }
    }

    // Fetch accounts
    useEffect(() => {
        const fetchAccounts = async () => {
            const storedToken = localStorage.getItem("token") || token;
            if (!storedToken) {
                console.error("No token found. User not logged in.");
                setLoading(false);
                return;
            }

            try {
                const res = await fetch("http://127.0.0.1:8000/user/get_all_accounts", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${storedToken}`,
                    },
                });

                if (res.status === 401) {
                    console.error("Unauthorized - invalid or expired token");
                    setError("Unauthorized - please login");
                    setAccounts([]);
                    return;
                }

                const data = await res.json();
                setAccounts(data.accounts || []);
            } catch (err) {
                console.error(err);
                setError("Failed to fetch accounts");
            } finally {
                setLoading(false);
            }
        };

        fetchAccounts();
    }, [token]); // refetch if token changes

    return (
        <div style={{padding: "20px"}}>
            <h1>Gestion des Comptes</h1>

            {/* Login form */}
            {!token && (
                <div style={{marginBottom: "20px"}}>
                    <h2>Login</h2>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={{marginRight: "10px", padding: "6px"}}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{marginRight: "10px", padding: "6px"}}
                    />
                    <button onClick={loginUser}>Login</button>
                    {error && <p style={{color: 'red'}}>{error}</p>}
                </div>
            )}

            {/* Recherche par IBAN */}
            {token && (
                <div style={{marginBottom: "20px"}}>
                    <h2>Rechercher un compte par IBAN</h2>

                    <input
                        type="text"
                        placeholder="Entrez un IBAN"
                        value={ibanSearch}
                        onChange={(e) => setIbanSearch(e.target.value)}
                        style={{padding: "6px", marginRight: "10px"}}
                    />


                    {/* Résultat de la recherche */}
                    {searchedAccount && (
                        <div style={{marginTop: "10px", padding: "10px", background: "#eef"}}>
                            <p><strong>IBAN :</strong> {searchedAccount.iban}</p>
                            <p><strong>Solde :</strong> {searchedAccount.amount}</p>
                        </div>
                    )}
                </div>
            )}

            {/* Liste de tous les comptes */}
            {token && (
                loading ? (
                    <p>Chargement des comptes...</p>
                ) : (
                    <div>
                        <h2>Liste des comptes</h2>

                        {accounts.length > 0 ? (
                            <table>
                                <thead>
                                <tr>
                                    <th>IBAN</th>
                                    <th>Montant</th>
                                </tr>
                                </thead>
                                <tbody>
                                {accounts.map((account, index) => (
                                    <tr key={index}>
                                        <td>{account.iban}</td>
                                        <td>{account.amount} Zennys</td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        ) : (
                            <p>Aucun compte trouvé</p>
                        )}
                    </div>
                )
            )}
            <div>
                <h1>Créer un compte :</h1>
                <input
                    type="text"
                    placeholder="Username"
                    value={usernameRegister}
                    onChange={(e) => setUsernameRegister(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Password"
                    value={passwordRegister}
                    onChange={(e) => setPasswordRegister(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Iban"
                    value={ibanRegister}
                    onChange={(e) => setIbanRegister(e.target.value)}
                />
                <button onClick={() => registerUser({
                    username: usernameRegister,
                    password: passwordRegister,
                    iban: ibanRegister
                }, setMessage)}>Register
                </button>
                <p>{message}</p>
            </div>
            <button onClick={() => selectAccount({
                iban: ibanRegister
                },setcurrentAccount,token)}>SelectAccount
            </button>
            <h5>{currentAccount}</h5>
        </div>
    );
};

export default App;
