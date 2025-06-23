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


