/** @odoo-module **/
 
import publicWidget from "@web/legacy/js/public/public_widget";
 
publicWidget.registry.MinQtyValidator = publicWidget.Widget.extend({
    selector: '.o_wsale_product_page',
    events: {
        'input input[name="add_qty"]': '_onQtyChange',
        'change input[name="add_qty"]': '_onQtyChange',
        'click .js_add_cart_json': '_onQtyChange',
        'click .js_subtract_cart_json': '_onQtyChange',
        'click #add_to_cart': '_onAddToCart',
    },
 
    start() {
        this._super.apply(this, arguments);
        this._onQtyChange();
    },
 
    _onQtyChange() {
        const $input = this.$el.find('input[name="add_qty"]');
        const minQty = parseInt(this.$el.find('#moq_hidden_value').val()) || 1;
        const enteredQty = parseInt($input.val()) || 0;
 
        const $btn = this.$el.find('#add_to_cart');
        const $msg = this.$el.find('#moq_warning');
 
        if (enteredQty >= minQty) {
            $btn.removeClass('disabled').css('pointer-events', 'auto');
            $msg.addClass('d-none');
        } else {
            $btn.addClass('disabled').css('pointer-events', 'none');
            $msg.removeClass('d-none');
        }
    },
 
    _onAddToCart(ev) {
        const minQty = parseInt(this.$el.find('#moq_hidden_value').val()) || 1;
        const enteredQty = parseInt(this.$el.find('input[name="add_qty"]').val()) || 0;
 
        if (enteredQty < minQty) {
            ev.preventDefault();
            alert(`Minimum order quantity is ${minQty}`);
        }
    },
});