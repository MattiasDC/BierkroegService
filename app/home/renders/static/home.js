function addLink(url, name) {
	$('.pager').append('<li><a href=\"' + url + '\">' + name + '</a></li>')
}

function addWaiterLinks() {
	addLink($('#waiter-url').data('url'), 'Bestelling')
}

function addCashDeskLinks() {
	addLink($('#cash-desk-url').data('url'), 'Kassa Bestelling')
	addLink($('#order-history-url').data('url'), 'Bestelling Geschiedenis')
}

function addAdminLinks() {
	addLink($('#pubmanagement-url').data('url'), 'Bierkroeg Management')
	addLink($('#productmanagement-url').data('url'), 'Product Management')
	addLink($('#usermanagement-url').data('url'), 'User management')
}

$(document).ready(function () {
	$.getJSON($('#roles-url').data('url'), function (roles) {
		$.getJSON($('#waiter-role-url').data('url'), function (id) {
			if (roles['roles'].includes(id['id']))
				addWaiterLinks()
		})

		$.getJSON($('#cash-desk-role-url').data('url'), function (id) {
			if (roles['roles'].includes(id['id']))
				addCashDeskLinks()
		})

		$.getJSON($('#admin-role-url').data('url'), function (id) {
			if (roles['roles'].includes(id['id'])){
				addWaiterLinks()
				addCashDeskLinks()
				addAdminLinks()
			}
		})
	})
})