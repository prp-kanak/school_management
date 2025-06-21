/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";

function getAllClasses() {
    rpc({
        route: '/school/standard/get_all',
    }).then(classes => {
        console.log("Fetched Classes:", classes);
        alert("Classes fetched. Check console for details.");
    }).catch(error => {
        console.error("Error fetching classes:", error);
    });
}

function updateClass(classId, updateValues) {
    rpc({
        route: '/school/standard/update',
        params: {
            class_id: classId,
            vals: updateValues,
        },
    }).then(response => {
        if (response.error) {
            console.error("Error updating class:", response.error);
        } else {
            console.log(response.success);
            alert(response.success);
        }
    }).catch(error => {
        console.error("Error updating class:", error);
    });
}

function deleteClass(classId) {
    rpc({
        route: '/school/standard/delete',
        params: {
            class_id: classId,
        },
    }).then(response => {
        if (response.error) {
            console.error("Error deleting class:", response.error);
        } else {
            console.log(response.success);
            alert(response.success);
        }
    }).catch(error => {
        console.error("Error deleting class:", error);
    });
}

// Test Functions
document.addEventListener('DOMContentLoaded', () => {
    // Fetch all classes on page load
    getAllClasses();

    // Update a specific class
    document.getElementById('update_button').addEventListener('click', () => {
        const classId = parseInt(document.getElementById('class_id_input').value);
        const updateValues = {
            name: 'Updated Class Name',
            section: 'b',
        };
        updateClass(classId, updateValues);
    });

    // Delete a specific class
    document.getElementById('delete_button').addEventListener('click', () => {
        const classId = parseInt(document.getElementById('class_id_input').value);
        deleteClass(classId);
    });
});
