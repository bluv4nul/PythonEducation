function displayCurrencies(currencies){
    const container = document.getElementById('currencies')

    if(!currencies || currencies.length === 0){
        container.innerHTML = '<p>Нет данных о валютах</p>'
        return
    }

    let html = ''
    for(let i = 0; i<currencies.length; i++){
        const currency = currencies[i]
        html+=`
            <div class="currency">
                <div class="currency-header">
                    <p class="currency-name">${currency._name}</p>
                </div>
                <div class="currency-info">
                    <p class="currency-value">Цена валюты: ${currency._value} RUB</p>
                    <p class="currency-nominal">Номинал: ${currency._nominal}</p>
                    <p class="currency-char-code">Cимвольный код: ${currency._char_code}</p>
                    <p class="currency-num-code">Номерной код: ${currency._num_code}</p>
                </div>
            </div>
            `
        }
    container.innerHTML = html;
}