/** @odoo-module **/

console.log("Patch functionality JS loaded");

import { rpc } from "@web/core/network/rpc";

function patchStudentRecord(studentId, data) {
    console.log("Patching student record with ID:", studentId, "Data:", data);

    rpc('/student/patch', {
        params: {
            student_id: studentId,
            ...data, // Spread operator to include all updated fields
        },
        method: 'PATCH',
    }).then(response => {
        if (response.status === "success") {
            console.log("Student record patched successfully:", response.message);
            alert("Student record updated successfully!");
        } else {
            console.error("Error patching student record:", response.message);
            alert("Failed to update student record: " + response.message);
        }
    }).catch(err => {
        console.error("Error in PATCH request:", err);
    });
}

// Attach patch functionality to a button
function attachPatchListener() {
    console.log("Looking for patch button");

    const btn = document.getElementById('patch_student_btn');
    if (btn) {
        console.log("Patch button found, adding listener");
        btn.addEventListener('click', function () {
            console.log("Patch button clicked");

            const studentId = document.getElementById('student_id_input').value;
            const updatedName = document.getElementById('student_name_input').value;
            const updatedAge = document.getElementById('student_age_input').value;

            const data = {
                name: updatedName,
                age: parseInt(updatedAge),
            };

            patchStudentRecord(studentId, data);
        });
    } else {
        console.error("Patch button NOT found");
    }
}

// Add listener after DOM content is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded, attaching patch listener");
    attachPatchListener();
});
