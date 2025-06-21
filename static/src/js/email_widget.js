/** @odoo-module **/

import { registry } from "@web/core/registry";
import { EmailField } from "@web/views/fields/email/email_field";
import { useState } from "@odoo/owl";

class ValidEmailField extends EmailField {
    setup() {
        super.setup();
        const email = this.props.record.data[this.props.name];
        this.state = useState({ isValid: this._validateEmail(email) });

        console.log("✅ ValidEmailField setup initialized.");
        console.log("Field Value:", email);
    }

    _validateEmail(email) {
        const emailRegex = /\S+@\S+\.\S+/; 
        return emailRegex.test(email || "");
    }

    willUpdateProps(nextProps) {
        const newValue = nextProps.record.data[nextProps.name];
        this.state.isValid = this._validateEmail(newValue);
    }
}

ValidEmailField.template = "school_management.ValidEmailField";

registry.category("fields").add("valid_email", {
    component: ValidEmailField,
    supportedTypes: ["char"],
});
