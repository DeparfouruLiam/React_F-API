import {useState} from "react";

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
