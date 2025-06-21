/** @odoo-module **/
 
import publicWidget from "@web/legacy/js/public/public_widget";
 
publicWidget.registry.TimeLoggerWidget = publicWidget.Widget.extend({
    selector: '.time-logger-widget',
 
    init: function (parent, options) {
        this._super.apply(this, arguments);
        console.log("INIT - Widget created but DOM not ready yet");
    },
 
    willStart: function () {
        console.log("WILLSTART - Preparing before rendering");
        return Promise.resolve();
    },
 
    start: function () {
        console.log("START - Widget fully loaded into DOM");
        const now = new Date().toLocaleTimeString();
        this.$el.find('.time-output').text(`Current Time: ${now}`);
        return this._super(...arguments);
    },
 
    destroy: function () {
        console.log("DESTROY - Widget is being removed from the page");
        this._super.apply(this, arguments);
    },
});