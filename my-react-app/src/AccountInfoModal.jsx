import React from "react";

export default function AccountInfoModal({ visible, onClose, account }) {
    if (!visible) return null;

    return (
        <div style={styles.modalOverlay}>
            <div style={styles.modal}>
                <h3>Account Information</h3>

                <p><strong>ID:</strong> {account.id}</p>
                <p><strong>IBAN:</strong> {account.iban}</p>
                <p><strong>Balance:</strong> {account.amount} Zennys</p>

                {/* NEW FIELDS FROM THE MODEL */}
                <p>
                    <strong>Main Account:</strong>{" "}
                    {account.is_main ? "Yes" : "No"}
                </p>


                <button onClick={onClose} style={styles.closeButton}>Close</button>
            </div>
        </div>
    );
}

const styles = {
    modalOverlay: {
        zIndex: 999,
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
    },
    modal: {
        background: "white",
        padding: "20px",
        borderRadius: "8px",
        width: "380px",
        color: "black"
    },
    closeButton: {
        marginTop: "10px",
        padding: "8px 12px",
        backgroundColor: "tomato",
        color: "white",
        border: "none",
        borderRadius: "6px",
        cursor: "pointer"
    }
};
