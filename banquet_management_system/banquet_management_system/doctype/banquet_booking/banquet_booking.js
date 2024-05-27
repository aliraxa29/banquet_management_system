// Copyright (c) 2024, Ali Raza and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Banquet Booking", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Selected Menu", {
    qty: function(frm, cdt, cdn) {
        calculateTotals(frm, cdt, cdn);
        setTotalValue(frm);
    },
    price: function(frm, cdt, cdn) {
        calculateTotals(frm, cdt, cdn);
        setTotalValue(frm);
    }
});

function calculateTotals(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let amount = row.qty * row.price;
    frappe.model.set_value(cdt, cdn, 'amount', amount);
}

function setTotalValue(frm) {
    var total_amount = 0;
    $.each(frm.doc.selected_menu || [], function(i, row) {
        total_amount += row.amount || 0;
    });
    frm.set_value('grand_total', total_amount);
    frm.set_value('total_in_words', frappe.utils.money_in_words(total_amount))
}