export default function TransactionsModal({ visible, transactions, myIban, onClose }) {
    if (!visible) return null;

    return (
        <div style={{
            zIndex:9999,
            position: "fixed",
            top: 0, left: 0,
            width: "100vw", height: "100vh",
            background: "rgba(0,0,0,0.6)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
        }}>
            <div style={{
                background: "white",
                padding: "20px",
                borderRadius: "10px",
                width: "400px",
                maxHeight: "80vh",
                overflowY: "auto",
                backgroundColor:"black"
            }}>
                <h2>Transactions</h2>

                {transactions.length === 0 ? (
                    <p>No transactions found</p>
                ) : (
                    <ul>
                        {transactions.map((t, idx) => {
                            const isDebit = t.ibanSender === myIban;
                            const type = isDebit ? "Debit" : "Credit";
                            const color = isDebit ? "red" : "green";

                            return (
                                <li key={idx} style={{
                                    marginBottom: "10px",
                                    paddingBottom: "10px",
                                    borderBottom: "1px solid #ccc"
                                }}>
                                    <h4 style={{ color }}>{type}</h4>
                                    <p><strong>Date:</strong> {new Date(t.date).toLocaleString()}</p>
                                    <p><strong>Sender:</strong> {t.ibanSender}</p>
                                    <p><strong>Receiver:</strong> {t.ibanReceiver}</p>
                                    <p><strong>Amount:</strong> {t.amount}</p>
                                    {t.cancelled && (
                                        <p style={{ color: "red" }}>
                                            <strong>Cancelled</strong>
                                        </p>
                                    )}
                                </li>
                            );
                        })}
                    </ul>
                )}

                <button onClick={onClose} style={{ marginTop: "10px", padding: "8px" }}>Close</button>
            </div>
        </div>
    );
}
