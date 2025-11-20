import { useState } from "react";

// New PaymentModal component
function PaymentModal({ visible, onCancel, onPay }) {
    const [paymentInfo, setPaymentInfo] = useState("");

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
                <h3>Payment Details</h3>
                <input
                    type="text"
                    placeholder="Payment info"
                    value={paymentInfo}
                    onChange={(e) => setPaymentInfo(e.target.value)}
                    style={{ width: "100%", padding: "8px", marginBottom: "15px" }}
                />
                <button
                    onClick={() => { onPay(paymentInfo); setPaymentInfo(""); }}
                    style={{ padding: "8px 12px", marginRight: "10px" }}
                >
                    Pay
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

export default function AmountModal({ visible, onCancel, onConfirm }) {
    const [amount, setAmount] = useState("");
    const [paymentVisible, setPaymentVisible] = useState(false);

    if (!visible) return null;

    const handlePayment = (info) => {
        console.log("Payment info:", info);
        setPaymentVisible(false);
        // Here you could call a payment API or do something with the info
    };

    return (
        <>
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
                zIndex: 1000
            }}>
                <div style={{
                    background: "black",
                    padding: "20px",
                    borderRadius: "8px",
                    width: "300px",
                    textAlign: "center"
                }}>
                    <h3>Entrez le montant</h3>

                    <input
                        type="number"
                        placeholder="Montant"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        style={{ width: "100%", padding: "8px", marginBottom: "15px" }}
                    />

                    <button
                        onClick={() => onConfirm(Number(amount))}
                        style={{ padding: "8px 12px", marginRight: "10px" }}
                    >
                        Confirmer
                    </button>

                    <button
                        onClick={onCancel}
                        style={{ padding: "8px 12px", background: "tomato", color: "white" }}
                    >
                        Annuler
                    </button>


                </div>
            </div>

            <PaymentModal
                visible={paymentVisible}
                onCancel={() => setPaymentVisible(false)}
                onPay={handlePayment}
            />
        </>
    );
}
