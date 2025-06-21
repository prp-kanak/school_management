// odoo.define('school_management.star', function (require) {
//     "use strict";

//     const publicWidget = require('web.public.widget');

//     publicWidget.registry.StarToggle = publicWidget.Widget.extend({
//         selector: '.static-star', // Attach to elements with the 'static-star' class
//         events: {
//             'click': '_onClickStar', // Bind the click event
//         },

//         /**
//          * Toggle the 'filled' class on the star when clicked.
//          */
//         _onClickStar: function (event) {
//             const target = $(event.currentTarget);
//             target.toggleClass('filled'); // Add/remove the 'filled' class to/from the clicked star
//         },
//     });
// });
