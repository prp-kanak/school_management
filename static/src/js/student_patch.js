/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";

// Function to update a student record using the PATCH method
function patchStudentRecord(studentId, updatedFields) {
    console.log("Sending PATCH request for student ID:", studentId);

    rpc(`/student/update/${studentId}`, {
        method: 'PATCH',
        params: updatedFields,
    })
    .then(function (response) {
        if (response.success) {
            console.log("Student record updated successfully:", response);
        } else {
            console.error("Error updating student record:", response.error);
        }
    })
    .catch(function (error) {
        console.error("Error in PATCH request:", error);
    });
}

const studentId = 3;  
const updatedFields = { name: 'New Name', age: 22 };
patchStudentRecord(studentId, updatedFields);
