document.addEventListener("DOMContentLoaded", function () {
    function esLineaValida(row) {
        const requiredFields = [
            'id_treball', 'id_tasca', 'quantitat', 'id_recurso', 'total_linea'
        ];

        return requiredFields.every(name => {
            const input = row.querySelector(`[name*="${name}"]`);
            return input && input.value !== '';
        });
    }

    function actualizarTotalPressupost() {
        let total = 0;

        // Limpiar resaltado anterior
        document.querySelectorAll(".linea-invalida").forEach(el => {
            el.classList.remove("linea-invalida");
        });

        // Recorre todos los formularios inline
        document.querySelectorAll('div.inline-related').forEach(row => {
            if (esLineaValida(row)) {
                const input = row.querySelector('input[name$="total_linea"]');
                const valor = parseFloat(input.value.replace(",", "."));
                if (!isNaN(valor)) total += valor;
            } else {
                row.classList.add("linea-invalida");
            }
        });

        // Mostrar total
        const display = document.getElementById("pressupost-total-display");
        if (display) {
            display.innerText = `Total del Pressupost: ${total.toFixed(2)} €`;
        }
    }

    function enganxarListeners() {
        document.querySelectorAll('input, select').forEach(input => {
            input.addEventListener("input", actualizarTotalPressupost);
            input.addEventListener("change", actualizarTotalPressupost);
        });
    }

    // Añadir contenedor visual si no existe
    const inlineGroup = document.querySelector("#pressupostoslineas_set-group");
    if (inlineGroup && !document.getElementById("pressupost-total-display")) {
        const display = document.createElement("div");
        display.id = "pressupost-total-display";
        display.style = "font-weight: bold; margin-top: 20px; font-size: 1.1em;";
        inlineGroup.appendChild(display);
    }

    // Estilos para líneas incompletas
    const style = document.createElement("style");
    style.innerHTML = `
        .linea-invalida {
            background-color: #fff6f6 !important;
            border-left: 4px solid #e3342f;
        }
    `;
    document.head.appendChild(style);

    // Ejecutar
    enganxarListeners();
    actualizarTotalPressupost();
});

// static/js/pressupostos_total.js

document.addEventListener("DOMContentLoaded", function () {
    const inlineRows = document.querySelectorAll(".dynamic-pressupostoslineas");

    inlineRows.forEach(row => {
        setupRowEvents(row);
    });

    function setupRowEvents(row) {
        const tascaSelect = row.querySelector("select[id$='-id_tasca']");
        const recursoSelect = row.querySelector("select[id$='-id_recurso']");
        const horesSelect = row.querySelector("select[id$='-id_hora']");
        const quantitatInput = row.querySelector("input[id$='-quantitat']");
        const beneficiInput = row.querySelector("input[id$='-benefici_linea']");

        [tascaSelect, recursoSelect, horesSelect, quantitatInput, beneficiInput].forEach(input => {
            if (input) {
                input.addEventListener("change", () => updateRowFields(row));
            }
        });
    }

    function updateRowFields(row) {
        const tascaId = getValue(row, 'id_tasca');
        const recursoId = getValue(row, 'id_recurso');
        const horesId = getValue(row, 'id_hora');
        const quantitat = parseFloat(getValue(row, 'quantitat')) || 0;
        const beneficiPercent = parseFloat(getValue(row, 'benefici_linea')) || 0;

        const parroquiaId = document.querySelector("#id_id_parroquia")?.value;
        const ubicacioId = document.querySelector("#id_id_ubicacio")?.value;

        if (tascaId && recursoId && horesId && parroquiaId && ubicacioId) {
            // Get increment hores
            fetch(`/pressupostos/ajax/get_increment_hores/?parroquia=${parroquiaId}&ubicacio=${ubicacioId}&tasca=${tascaId}`)
                .then(response => response.json())
                .then(data => {
                    const increment = parseFloat(data.increment) || 0;
                    row.querySelector("input[id$='-increment_hores']").value = increment;

                    // Get dades recurs
                    fetch(`/pressupostos/ajax/get_dades_recurs/?recurso=${recursoId}`)
                        .then(response => response.json())
                        .then(data => {
                            const preuTancat = data.preu_tancat;
                            const preuHora = parseFloat(data.preu_hora) || 0;

                            setValue(row, 'preu_tancat', preuTancat);
                            setValue(row, 'cost_hores', preuTancat ? 0 : preuHora);
                            setValue(row, 'cost_tancat', preuTancat ? 0 : getValue(row, 'cost_tancat'));

                            let hores = parseFloat(horesId) || 0;
                            let horesTotales = preuTancat ? 0 : (hores + increment) * quantitat;
                            let costHoresTotals = preuTancat ? 0 : preuHora * horesTotales;
                            let subtotal = parseFloat(row.querySelector("input[id$='-cost_tancat']").value) || 0;

                            subtotal += costHoresTotals;
                            const benefici = (beneficiPercent / 100) * subtotal;
                            const total = subtotal + benefici;

                            setValue(row, 'hores_totales', horesTotales);
                            setValue(row, 'cost_hores_totals', costHoresTotals);
                            setValue(row, 'subtotal_linea', subtotal);
                            setValue(row, 'total_linea', total);
                        });
                });
        }
    }

    function getValue(row, name) {
        const input = row.querySelector(`[id$='-${name}']`);
        return input ? input.value : "";
    }

    function setValue(row, name, value) {
        const input = row.querySelector(`[id$='-${name}']`);
        if (input) input.value = (Math.round(value * 10000) / 10000).toFixed(4);
    }
});

// static/js/pressupostos_total.js

document.addEventListener('DOMContentLoaded', function () {
    const formsetPrefix = 'pressupostoslineas_set';

    function getValue(name, row) {
        const el = row.querySelector(`[name*='${name}']`);
        return el ? el.value : null;
    }

    function setValue(name, row, value) {
        const el = row.querySelector(`[name*='${name}']`);
        if (el) el.value = value;
    }

    function disableField(name, row, disable = true) {
        const el = row.querySelector(`[name*='${name}']`);
        if (el) el.readOnly = disable;
    }

    function fetchIncrement(row) {
        const parroquia = document.querySelector('#id_id_parroquia')?.value;
        const ubicacio = document.querySelector('#id_id_ubicacio')?.value;
        const tasca = getValue('id_tasca', row);

        if (parroquia && ubicacio && tasca) {
            fetch(`/pressupostos/ajax/get_increment_hores/?parroquia=${parroquia}&ubicacio=${ubicacio}&tasca=${tasca}`)
                .then(response => response.json())
                .then(data => {
                    setValue('increment_hores', row, data.increment);
                    calcTotals(row);
                });
        }
    }

    function fetchRecurs(row) {
        const recurso = getValue('id_recurso', row);
        if (recurso) {
            fetch(`/pressupostos/ajax/get_dades_recurs/?recurso=${recurso}`)
                .then(response => response.json())
                .then(data => {
                    setValue('preu_tancat', row, data.preu_tancat);

                    if (data.preu_tancat == 1) {
                        setValue('increment_hores', row, 0);
                        setValue('hores_totales', row, 0);
                        setValue('cost_hores', row, 0);
                        setValue('cost_hores_totals', row, 0);
                        disableField('cost_tancat', row, false);
                    } else {
                        disableField('cost_tancat', row, true);
                        const preu_hora = data.preu_hora;
                        setValue('cost_hores', row, preu_hora);
                        calcTotals(row);
                    }
                });
        }
    }

    function calcTotals(row) {
        const hores = parseFloat(getValue('id_hora', row)) || 0;
        const increment = parseFloat(getValue('increment_hores', row)) || 0;
        const quantitat = parseInt(getValue('quantitat', row)) || 1;
        const cost_hores = parseFloat(getValue('cost_hores', row)) || 0;
        const cost_tancat = parseFloat(getValue('cost_tancat', row)) || 0;
        const benefici = parseFloat(getValue('benefici_linea', row)) || 0;

        const hores_totales = (hores + increment) * quantitat;
        const cost_hores_total = hores_totales * cost_hores;
        const subtotal = cost_hores_total + cost_tancat;
        const total = subtotal * (1 + (benefici / 100));

        setValue('hores_totales', row, hores_totales.toFixed(2));
        setValue('cost_hores_totals', row, cost_hores_total.toFixed(4));
        setValue('subtotal_linea', row, subtotal.toFixed(4));
        setValue('total_linea', row, total.toFixed(4));

        updatePressupostTotal();
    }

    function updatePressupostTotal() {
        const totalFields = document.querySelectorAll(`[name*='total_linea']`);
        let sum = 0;
        totalFields.forEach(field => {
            const val = parseFloat(field.value);
            if (!isNaN(val)) sum += val;
        });
        let totalDisplay = document.getElementById('pressupost-total');
        if (!totalDisplay) {
            totalDisplay = document.createElement('div');
            totalDisplay.id = 'pressupost-total';
            totalDisplay.style = 'margin-top:1rem;font-weight:bold;font-size:1.2rem;';
            const inlineGroup = document.querySelector('.inline-group');
            inlineGroup?.parentNode?.insertBefore(totalDisplay, inlineGroup);
        }
        totalDisplay.innerHTML = `Total pressupost estimat: ${sum.toFixed(2)} €`;
    }

    function filterTascaOptions(row) {
        const treball = getValue('id_treball', row);
        const tascaField = row.querySelector(`[name*='id_tasca']`);

        if (treball && tascaField) {
            fetch(`/pressupostos/ajax/get_tasques_treball/?treball=${treball}`)
                .then(res => res.json())
                .then(data => {
                    const selected = tascaField.value;
                    tascaField.innerHTML = ''; // Clear
                    data.forEach(t => {
                        const option = document.createElement('option');
                        option.value = t.id;
                        option.text = t.tasca;
                        if (t.id == selected) option.selected = true;
                        tascaField.add(option);
                    });
                });
        }
    }

    document.querySelectorAll('.dynamic-pressupostoslineas_set').forEach(row => {
        row.addEventListener('change', e => {
            const name = e.target.name;
            if (!name) return;

            if (name.includes('id_recurso')) fetchRecurs(row);
            if (name.includes('id_tasca')) fetchIncrement(row);
            if (name.includes('id_treball')) filterTascaOptions(row);
            if (name.includes('quantitat') || name.includes('benefici_linea') || name.includes('id_hora')) calcTotals(row);
        });
    });
});
