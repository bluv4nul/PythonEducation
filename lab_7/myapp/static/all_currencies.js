function displayCurrencies(currencies) {
    const container = document.getElementById('currencies')

    if (!currencies || currencies.length === 0) {
        container.innerHTML = '<p>Нет данных о валютах</p>'
        return
    }

    let html = ''
    for (let i = 0; i < currencies.length; i++) {
        const currency = currencies[i]
        html += `
            <div class="currency">
                <div class="currency-header">
                    <p class="currency-name">${currency._name}</p>
                    <p class="currency-char-code">${currency._char_code}</p>
                </div>
                <p class="currency-price">${currency._value} RUB</p>
                <div class="currency-info">
                    <p class="currency-nominal">Номинал: ${currency._nominal}</p>
                    <p class="currency-num-code">Num code: ${currency._num_code}</p>
                    <p class="currency-id">ID: ${currency._id}</p>
                </div>
            </div>
            `
    }
    container.innerHTML = html;
}