function update_total_price(pid, act) {
	let current_price = document.getElementById('total_price').innerText
	current_price = current_price.replace('Общая стоимость: ', '')
	current_price = current_price.replace('₽', '')
	current_price = parseInt(current_price)

	let product_price = parseInt(document.getElementById(`price-${pid}`).innerText.replace('₽', ''))
	if (act === '-')
		current_price -= product_price
	if (act === '+')
		current_price += product_price
	document.getElementById('total_price').innerText = `Общая стоимость: ${current_price}₽`
}

function up_count(pid) {
	let counter = document.getElementById(`counter-${pid}`)
	let value = parseInt(counter.value)
	counter.value = value + 1
	update_total_price(pid, '+')

	const XHR = new XMLHttpRequest();
    XHR.open("GET", "/up_count/" + pid);
    XHR.setRequestHeader('Content-type', 'application/json');
    XHR.send();

}

function check_button_state() {
    let counts = document.getElementsByClassName('input-count')
    let summa = 0
    for(let i=0;i<counts.length;i++){
        summa += parseInt(counts[i].value)
    }
    if (summa < 1){
        document.getElementById('knopka').innerHTML = ''
    }
}

function down_count(pid) {
	let counter = document.getElementById(`counter-${pid}`)
	if (counter.value > 0) {
		let value = parseInt(counter.value)
		counter.value = value - 1
		update_total_price(pid, '-')
		const XHR = new XMLHttpRequest();
        XHR.open("GET", "/down_count/" + pid);
        XHR.setRequestHeader('Content-type', 'application/json');
        XHR.responseType = 'json';

        XHR.onload = () => {
            if (XHR.readyState === XMLHttpRequest.DONE && XHR.status === 200) {
                    if (XHR.response['count'] < 1){
                        document.getElementById('product_' + pid).remove()
                    }
            }
        }

        XHR.send();

	}

	check_button_state()
}
