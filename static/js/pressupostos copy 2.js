document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#pressupost-form");
  if (!form) return;
  console.log("✅ Formulario de pressupost cargado");

  const clientField = document.querySelector("#id_id_client");
  clientField?.addEventListener("change", function () {
    const clientId = this.value;
    const projectSelect = document.querySelector("#id_id_projecte");
    console.log("🔄 Cambio en clientId:", clientId);
    if (!clientId || clientId === "0") {
      projectSelect.innerHTML = '<option value="">Seleccioni Projecte</option>';
      return;
    }
    fetch(`/pressupostos/get_projectes/${clientId}/`)
      .then((response) => response.json())
      .then((data) => {
        console.log("📦 Projectes cargados:", data);
        projectSelect.innerHTML = '<option value="">Seleccioni Projecte</option>';
        data.forEach((item) => {
          const option = document.createElement("option");
          option.value = item.id;
          option.textContent = item.nom;
          projectSelect.appendChild(option);
        });
      })
      .catch((error) => {
        console.error("❌ Error carregant projectes:", error);
      });
  });

  document.querySelectorAll(".pressupost-linea").forEach((linea, index) => {
    console.log(`🔧 Inicializando línea ${index}`);
    setupLinea(linea, index);
  });

  const addBtn = document.querySelector("#add-linea");
  if (addBtn) {
    addBtn.addEventListener("click", function () {
      const totalForms = document.querySelector('input[name$="-TOTAL_FORMS"]');
      const currentIndex = parseInt(totalForms.value);
      const container = document.querySelector("#lineas-container");
      const emptyForm = document.querySelector("#empty-form");
      if (!emptyForm) return;

      const newLinea = emptyForm.cloneNode(true);
      newLinea.style.display = "";
      newLinea.id = "";
      newLinea.classList.add("pressupost-linea");

      newLinea.querySelectorAll("input, select, textarea, label").forEach((el) => {
        if (el.name) el.name = el.name.replace(/__prefix__/, currentIndex);
        if (el.id) el.id = el.id.replace(/__prefix__/, currentIndex);
        if (el.tagName !== "LABEL") {
          if (el.type === "checkbox" || el.type === "radio") {
            el.checked = false;
          } else {
            el.value = "";
          }
        }
      });

      newLinea.querySelectorAll("input[readonly]").forEach((el) => el.value = "");

      const idField = newLinea.querySelector(`[name$="-id"]`);
      if (idField) idField.value = "";

      const deleteField = newLinea.querySelector(`[name$="-DELETE"]`);
      if (deleteField) deleteField.checked = false;

      const deleteBtn = newLinea.querySelector(".eliminar-linea");
      if (deleteBtn) {
        deleteBtn.addEventListener("click", () => {
          if (!idField || !idField.value) {
            newLinea.remove();
          } else if (deleteField) {
            deleteField.checked = true;
            newLinea.style.display = "none";
          }
          calcularTotalPressupost();
        });
      }

      totalForms.value = currentIndex + 1;
      container.appendChild(newLinea);

      console.log(`➕ Nueva línea añadida: ${currentIndex}`);
      setupLinea(newLinea, currentIndex);
    });
  }

  function setupLinea(linea, index) {
    const treballSelect = linea.querySelector(`[id$="-id_treball"]`);
    const tascaSelect = linea.querySelector(`[id$="-id_tasca"]`);
    const recursoSelect = linea.querySelector(`[id$="-id_recurso"]`);
    const preuTancatCheck = linea.querySelector(`[id$="-preu_tancat"]`);
    const horesField = linea.querySelector(`[id$="-id_hora"]`);
    const incrementField = linea.querySelector(`[id$="-increment_hores"]`);
    const horesTotalsField = linea.querySelector(`[id$="-hores_totales"]`);
    const costHoresField = linea.querySelector(`[id$="-cost_hores"]`);
    const costTotalsField = linea.querySelector(`[id$="-cost_hores_totals"]`);
    const costTancatField = linea.querySelector(`[id$="-cost_tancat"]`);
    const subtotalField = linea.querySelector(`[id$="-subtotal_linea"]`);
    const quantitatField = linea.querySelector(`[id$="-quantitat"]`);
    const beneficiField = linea.querySelector(`[id$="-benefici_linea"]`);
    const totalLineaField = linea.querySelector(`[id$="-total_linea"]`);
    const deleteField = linea.querySelector(`[id$="-DELETE"]`);

    treballSelect?.addEventListener("change", function () {
      const idTreball = this.value;
      tascaSelect.innerHTML = '<option value="">Seleccioni Tasca</option>';
      console.log("📌 Treball cambiado:", idTreball);
      if (idTreball) {
        fetch(`/pressupostos/get_tasques/${idTreball}/`)
          .then((res) => res.json())
          .then((data) => {
            console.log("📦 Tasques cargadas:", data);
            const tasques = Array.isArray(data) ? data : data.tasques;
            if (Array.isArray(tasques)) {
              tasques.forEach((item) => {
                const option = document.createElement("option");
                option.value = item.id;
                option.textContent = item.tasca;
                tascaSelect.appendChild(option);
              });
            } else {
              console.error("⚠️ Formato inesperado de tasques:", data);
            }
          })
          .catch(err => console.error("❌ Error carregant tasques:", err));
      }
    });

    recursoSelect?.addEventListener("change", function () {
      const idRecurso = this.value;
      console.log("🔁 Recurso seleccionado:", idRecurso);
      if (!idRecurso) return;
      fetch(`/pressupostos/get_recurso/${idRecurso}/`)
        .then((res) => res.json())
        .then((data) => {
          console.log("📦 Datos del recurso:", data);
          if (data.PreuTancat) {
            preuTancatCheck.checked = true;
            horesField.value = "";
            incrementField.value = "0";
            horesTotalsField.value = "0";
            costHoresField.value = "";
            costTotalsField.value = "";
          } else {
            preuTancatCheck.checked = false;
            costHoresField.value = data.PreuHora || "0";
          }
          calcularSubtotal();
        });
    });

    [document.querySelector("#id_id_parroquia"), document.querySelector("#id_id_ubicacio"), tascaSelect].forEach((el) => {
      el?.addEventListener("change", function () {
        const id_parroquia = document.querySelector("#id_id_parroquia").value;
        const id_ubicacio = document.querySelector("#id_id_ubicacio").value;
        const id_tasca = tascaSelect.value;
        console.log("🔄 Verificando increment hores para:", { id_parroquia, id_ubicacio, id_tasca });
        if (id_parroquia && id_ubicacio && id_tasca) {
          fetch(`/pressupostos/get_increment_hores/?id_parroquia=${id_parroquia}&id_ubicacio=${id_ubicacio}&id_tasca=${id_tasca}`)
            .then((res) => res.json())
            .then((data) => {
              console.log("📦 Increment hores:", data);
              if (data.increment_hores !== undefined) {
                incrementField.value = data.increment_hores;
                calcularSubtotal();
              }
            });
        }
      });
    });

    [horesField, incrementField, costHoresField, quantitatField, costTancatField].forEach((el) =>
      el?.addEventListener("input", calcularSubtotal)
    );

    beneficiField?.addEventListener("input", calcularSubtotal);

    if (deleteField) {
      deleteField.addEventListener("change", calcularTotalPressupost);
    }

    function calcularSubtotal() {
      const q = parseFloat(quantitatField.value) || 0;
      const h = parseFloat(horesField?.value) || 0;
      const inc = parseFloat(incrementField?.value) || 0;
      const cost = parseFloat(costHoresField?.value) || 0;
      const costTancat = parseFloat(costTancatField?.value) || 0;
      const preuTancat = preuTancatCheck?.checked;

      const totalHores = h + inc;
      const totalCostHores = totalHores * cost;
      const subtotal = preuTancat ? q * costTancat : q * totalCostHores;

      horesTotalsField.value = totalHores.toFixed(2);
      costTotalsField.value = totalCostHores.toFixed(4);
      subtotalField.value = subtotal.toFixed(4);

      const beneficiPercent = parseFloat(beneficiField.value) || 0;
      const benefici = subtotal * (beneficiPercent / 100);
      const total = subtotal + benefici;

      totalLineaField.value = total.toFixed(2);

      console.log("💰 Subtotal calculado:", {
        totalHores, totalCostHores, subtotal, beneficiPercent, benefici, total
      });

      calcularTotalPressupost();
    }
  }

  function calcularTotalPressupost() {
    let total = 0;
    document.querySelectorAll(".pressupost-linea").forEach((linea) => {
      const isDeleted = linea.querySelector(`[id$="-DELETE"]`)?.checked;
      if (isDeleted) return;
      const totalLineaField = linea.querySelector(`[id$="-total_linea"]`);
      total += parseFloat(totalLineaField?.value || "0");
    });
    const totalPressupostElement = document.getElementById("total-pressupost");
    if (totalPressupostElement) {
      totalPressupostElement.textContent = total.toFixed(2);
    }
    console.log("🧮 Total pressupost actualizado:", total);
  }

  calcularTotalPressupost();
});
