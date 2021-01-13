function createFloatInput(name, value) {
  return '<input type="float" class="form-control" name="' + name + '" id="' + name + '" value="' + value + '"/>'
}

function createDateInput(name, value) {
	return '<input type="Date" class="form-control" name="' + name + '" id="' + name + '" value="' + value + '"/>'
}

function createStringInput(name, value) {
  return '<input type="string" class="form-control" name="' + name + '" id="' + name + '" value="' + value + '"/>'
}

function wrapInTableColumn(value) {
	return '<td>' + value + '</td>'
}

function wrapInTableColumns(values) {
	var i
	var text = ""
	for (i = 0; i < values.length; i++) {
  		text += wrapInTableColumn(values[i])
	}
	return text
}

function makeColumnInput(row, index, create) {
	row.find('td').eq(index).html(create(row.find('td').eq(index).text()));
}