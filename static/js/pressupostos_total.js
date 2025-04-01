
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
                    tascaField.innerHTML = '';
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
        const selects = row.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', e => handleChange(row, e));
            $(select).on('select2:select', e => handleChange(row, e));
        });

        row.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', () => calcTotals(row));
        });
    });

    function handleChange(row, e) {
        const name = e.target.name;
        if (!name) return;

        if (name.includes('id_recurso')) fetchRecurs(row);
        if (name.includes('id_tasca')) fetchIncrement(row);
        if (name.includes('id_treball')) filterTascaOptions(row);
        if (name.includes('quantitat') || name.includes('benefici_linea') || name.includes('id_hora')) calcTotals(row);
    }
});