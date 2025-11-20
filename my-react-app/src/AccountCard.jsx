import { useState } from "react";
import AmountModal from "./AccountModal";
import PaymentModal from "./PaymentModal";
import TransactionsModal from "./TransactionModal";   // <== ADD THIS

export default function AccountCard({ account, token, refreshAccounts }) {
    const [open, setOpen] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [showPaymentModal, setShowPaymentModal] = useState(false);

    // NEW STATE:
    const [showTransactions, setShowTransactions] = useState(false);
    const [transactions, setTransactions] = useState([]);

    async function getTransactions() {
        try {
            const res = await fetch(`http://127.0.0.1:8000/transaction/transactions/${account.iban}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            const data = await res.json();
            setTransactions(data.transactions || []);
            setShowTransactions(true); // Open modal
        } catch (e) {
            console.error(e);
            alert("Error loading transactions");
        }
    }

    async function sendMoney(amount, iban) {
        try {
            const res = await fetch("http://127.0.0.1:8000/transaction/add_money", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ amount, iban }),
            });
            const data = await res.json();
            alert(JSON.stringify(data));
            refreshAccounts();
        } catch (e) {
            console.error(e);
            alert("Error adding money");
        }
    }

    async function makePayment(sender_iban, receiver_iban, amount) {
        try {
            const res = await fetch("http://127.0.0.1:8000/transaction/transfer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ sender_iban, receiver_iban, amount }),
            });

            const data = await res.json();
            alert(JSON.stringify(data));
            setShowPaymentModal(false);
            refreshAccounts();
        } catch (e) {
            console.error(e);
            alert("Error making payment");
        }
    }

    async function deleteAccount(iban,token) {
        const inputs = {iban};

        const res = await fetch("http://127.0.0.1:8000/accounts/delete_account", {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}`,"Content-Type": "application/json" },
            body: JSON.stringify(inputs)
        });

        console.log("Account deleted");
    }

    return (
        <div style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "12px",
            marginBottom: "12px",
            position: "relative",
            background: "black",
            color: "white"
        }}>

            <div
                onClick={() => setOpen(!open)}
                style={{
                    position: "absolute",
                    top: "10px",
                    right: "10px",
                    cursor: "pointer",
                    fontSize: "18px",
                    transform: open ? "rotate(90deg)" : "rotate(0deg)",
                }}
            >
                ➤
            </div>

            <h3>IBAN : {account.iban}</h3>
            <p>Solde : {account.amount} Zennys</p>

            {open && (
                <div style={{ marginTop: "12px" }}>
                    <button onClick={() => setShowModal(true)} style={{ padding: "8px", marginRight: "10px" }}>
                        Ajouter
                    </button>

                    {/* NEW BUTTON */}
                    <button
                        style={{ padding: "8px", background: "#444", color: "white", marginRight: "10px" }}
                        onClick={getTransactions}
                    >
                        View Transactions
                    </button>

                    <button
                        onClick={() => setShowPaymentModal(true)}
                        style={{ padding: "8px", marginRight: "10px", background: "green", color: "white" }}
                    >
                        Payment
                    </button>

                    <button
                        onClick={async () => {
                            await deleteAccount(account.iban, token);
                            await refreshAccounts();}}
                        style={{
                            padding: "8px",
                            background: "tomato",
                            color: "white",
                        }}
                    >
                        Clôturer
                    </button>
                </div>
            )}
            <AmountModal
                visible={showModal}
                onCancel={() => setShowModal(false)}
                onConfirm={async (amount) => {
                    setShowModal(false);
                    await sendMoney(amount, account.iban);
                }}
            />
            <PaymentModal
                visible={showPaymentModal}
                onCancel={() => setShowPaymentModal(false)}
                onPay={async (receiverIban, amount) => {
                    setShowPaymentModal(false);
                    await makePayment(account.iban, receiverIban, amount);
                }}
            />

            <TransactionsModal
                visible={showTransactions}
                transactions={transactions}
                type={account.iban}
                onClose={() => setShowTransactions(false)}
            />
        </div>
    );
}
