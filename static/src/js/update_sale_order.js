/** @odoo-module **/

console.log("Sale Order Status Update JS Loaded");

import { rpc } from "@web/core/network/rpc";

// Function to update order status
function patchSaleOrderStatus(orderId, newStatus) {
    console.log("Patching sale order status for ID:", orderId, "New Status:", newStatus);

    rpc('/sale/order/patch', {
        params: {
            order_id: orderId,
            status: newStatus,
        },
        method: 'PATCH',
    }).then(response => {
        if (response.status === "success") {
            console.log("Sale order status patched successfully:", response.message);
            alert(response.message);
        } else {
            console.error("Error patching sale order status:", response.message);
            alert("Failed to update sale order status: " + response.message);
        }
    }).catch(err => {
        console.error("Error in PATCH request:", err);
    });
}

// Attach functionality to buttons
function attachSaleOrderPatchListener() {
    console.log("Looking for sale order patch buttons");

    const buttons = document.querySelectorAll('.update-sale-order-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const orderId = this.dataset.orderId;
            const newStatus = this.dataset.newStatus;

            if (orderId && newStatus) {
                patchSaleOrderStatus(orderId, newStatus);
            } else {
                alert("Order ID or Status is missing!");
            }
        });
    });
}

// Add listener on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded, attaching sale order patch listeners");
    attachSaleOrderPatchListener();
});
