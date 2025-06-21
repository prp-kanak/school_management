/** @odoo-module **/
 
import { rpc } from "@web/core/network/rpc";

rpc('/student/data',{
    params : {
        name:'name',
        roll_no :'roll_number',
    }
 
}).then(function (result) {
    if (result.error) {
        console.error("Error from server:",result.error);
    }else {
        result.forEach(function (student){
            console.log("Student Name:",student.name);
            console.log("Roll Number:",student.roll_number);
        });
    }
}).catch(function(error) {
    console.error("RPC Exception:",error);
});


function createStudentRecord() {
    return rpc('/student/create', {
            name: "Suhani Sharma",          // Required: String
            age: 22,                        // Required: Integer
            roll_number: "11A",             // Required: String
    });

    // return rpc('/student/create', {
    //         // product_id: this.productTemplateID,
    //         // sequence: widgetValue,
    //     }).then(() => this._reloadEditable());
    // rpc('/student/create', {
    //     params: {
    //         class_id: 1,                    // Required: Integer (valid ID from 'school.standard')
    //         total_fees: 50000,              // Required: Float
    //         address: "123 Street, City",
    //         email: "suhani.sharma@example.com",
    //         gender: "female",
    //         admission_date: "2025-06-20",
    //         father_name: "Raj Sharma",
    //         mother_name: "Anita Sharma"
    //     }
    // }).then(function (result) {
    //     if (result.error) {
    //         console.error("Error from server:", result.error);
    //     } else {
    //         console.log("Student created successfully. ID:", result.student_id);
    //     }
    // }).catch(function (error) {
    //     console.error("Error creating student record:", error);
    // });
}

createStudentRecord();
