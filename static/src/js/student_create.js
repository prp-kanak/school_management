/** @odoo-module **/

console.log(" STEP 1: JS FILE LOADED");

import { rpc } from "@web/core/network/rpc";

// Function to create a student record
// function _createStudentRecord() {
//     console.log(" STEP 4: Inside _createStudentRecord()");

//     rpc('/web/dataset/call_kw', {
//         model: 'student.student',
//         method: 'create',
//         args: [{
//             name: 'John Doe',
//             age: 16,
//             roll_number: '12345',
//             class_id: 'class 1',  
//             total_fees: 5000,
//         }],
//         kwargs: {},
//     }).then(result => {
//         console.log(" STEP 5: Student created with ID:", result);
//         alert("Created student ID: " + result);
//     }).catch(err => {
//         console.error(" STEP 5: Create failed:", err);
//     });
// }

// Attach listener for create button
// function attachCreateListener() {
//     console.log(" STEP 2: Looking for create button");

//     const btn = document.getElementById('create_student_btn');
//     if (btn) {
//         console.log(" STEP 3: Create button found, adding listener");
//         btn.addEventListener('click', function () {
//             console.log(" STEP 3.1: Create button clicked");
//             _createStudentRecord();
//         });
//     } else {
//         console.error(" STEP 3: Create button NOT found");
//     }
// }

// Function to update a student record
// function _updateStudentRecord() {
//     console.log(" STEP 4: Inside _updateStudentRecord()");

//     rpc('/web/dataset/call_kw', {
//         model: 'student.student',
//         method: 'write',
//         args: [
//             [1],  
//             {
//                 name: 'Jane Doe',
//                 age: 17,
//                 roll_number: '54321',
//                 total_fees: 5500,
//             }
//         ],
//         kwargs: {},
//     }).then(result => {
//         console.log(" STEP 5: Write success:", result);
//         alert("Student record updated: " + result);
//     }).catch(err => {
//         console.error(" STEP 5: Update failed:", err);
//     });
// }

// Attach listener for update button
// function attachUpdateListener() {
//     console.log(" STEP 2: Looking for update button");

//     const btn = document.getElementById('update_student_btn');
//     if (btn) {
//         console.log(" STEP 3: Update button found, adding listener");
//         btn.addEventListener('click', function () {
//             console.log(" STEP 3.1: Update button clicked");
//             _updateStudentRecord();
//         });
//     } else {
//         console.error(" STEP 3: Update button NOT found");
//     }
// }

// Add listeners on DOM ready
// document.addEventListener('DOMContentLoaded', () => {
//     console.log(" DOMContentLoaded fired");
//     attachCreateListener();
//     attachUpdateListener();
// });

// if ('requestIdleCallback' in window) {
//     requestIdleCallback(() => {
//         console.log(" requestIdleCallback fired");
//         attachCreateListener();
//         attachUpdateListener();
//     });
// } else {
//     setTimeout(() => {
//         console.log(" setTimeout fallback fired");
//         attachCreateListener();
//         attachUpdateListener();
//     }, 1000);
// }
