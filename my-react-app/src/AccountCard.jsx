import { useState } from "react";
import AmountModal from "./AccountModal";

// PaymentModal with IBAN + Amount
function PaymentModal({ visible, onCancel, onPay }) {
    const [iban, setIban] = useState("");
    const [amount, setAmount] = useState("");

    if (!visible) return null;

    return (
        <div style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            background: "rgba(0,0,0,0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1100
        }}>
            <div style={{
                background: "black",
                padding: "20px",
                borderRadius: "8px",
                width: "300px",
                textAlign: "center"
            }}>
                <h3>Make a Payment</h3>

                <input
                    type="text"
                    placeholder="Receiver IBAN"
                    value={iban}
                    onChange={(e) => setIban(e.target.value)}
                    style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
                />

                <input
                    type="number"
                    placeholder="Amount"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    style={{ width: "100%", padding: "8px", marginBottom: "15px" }}
                />

                <button
                    onClick={() => { onPay(iban, parseFloat(amount)); setIban(""); setAmount(""); }}
                    style={{ padding: "8px 12px", marginRight: "10px" }}
                >
                    Confirm
                </button>

                <button
                    onClick={onCancel}
                    style={{ padding: "8px 12px", background: "tomato", color: "white" }}
                >
                    Cancel
                </button>
            </div>
        </div>
    );
}

export default function AccountCard({ account, token, refreshAccounts }) {
    const [open, setOpen] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [showPaymentModal, setShowPaymentModal] = useState(false);

    async function sendMoney(amount,iban) {
        try {
            const res = await fetch("http://127.0.0.1:8000/transaction/add_money", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ amount ,iban}),
            });
            const data = await res.json();
            alert(JSON.stringify(data));
            refreshAccounts();
        } catch (e) {
            console.error(e);
            alert("Error adding money");
        }
    }

    async function makePayment(receiverIban, amount) {
        try {
            const res = await fetch("http://127.0.0.1:8000/transaction/transfer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ receiver_iban: receiverIban, amount }),
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

    return (
        <div
            style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "12px",
                marginBottom: "12px",
                position: "relative",
                background: "Black"
            }}
        >
            {/* Toggle arrow */}
            <div
                onClick={() => setOpen(!open)}
                style={{
                    position: "absolute",
                    top: "10px",
                    right: "10px",
                    cursor: "pointer",
                    fontSize: "18px",
                    transform: open ? "rotate(90deg)" : "rotate(0deg)"
                }}
            >
                ➤
            </div>

            <h3 style={{ margin: 0 }}>IBAN : {account.iban}</h3>
            <p>Solde : {account.amount} Zennys</p>

            {open && (
                <div style={{ marginTop: "12px" }}>
                    <button
                        onClick={() => setShowModal(true)}
                        style={{ padding: "8px", marginRight: "10px" }}
                    >
                        Ajouter
                    </button>

                    <button
                        onClick={() => setShowPaymentModal(true)}
                        style={{ padding: "8px", marginRight: "10px", background: "green", color: "white" }}
                    >
                        Payment
                    </button>

                    <button
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
                    await sendMoney(amount,account.iban);
                }}
            />
            <PaymentModal
                visible={showPaymentModal}
                onCancel={() => setShowPaymentModal(false)}
                onPay={makePayment}
            />
        </div>
    );
}
