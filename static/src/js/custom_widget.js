/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Component } from "@odoo/owl";

class MyCustomWidget extends Component {
    static template = 'school_management.MyCustomWidgetTemplate';

    setup() {
        super.setup();
        this.message = "Hello, Odoo User!";
    }

    onClickButton() {
        alert(this.message);
    }
}

registry.category("view_widgets").add("my_custom_widget", {
    component: MyCustomWidget,
});
