const MENSAJES = [
    "La cuerda espera...",
    "Se acerca el peligro...",
    "El destino se acerca...",
    "No te queda mucho tiempo...",
    "Casi es demasiado tarde...",
    "¡Último aviso!",
    "¡GAME OVER!"
];

const FILAS = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"];

function tokenCsrf() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
}

async function leerError(res) {
    const cuerpo = await res.json().catch(() => ({}));
    return cuerpo.error || `Error ${res.status}`;
}

function mostrarPantalla(id) {
    document.querySelectorAll(".seccion").forEach(s => s.classList.remove("activa"));
    document.getElementById(id).classList.add("activa");

    if (id === "ver") {
        cargarPalabras().catch(error => console.error("Error al cargar las palabras:", error));
    }
}

async function iniciarJuego(dificultad) {
    const res = await fetch("/api/jugar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": tokenCsrf()
        },
        body: JSON.stringify({ dificultad })
    });

    if (!res.ok) {
        alert(await leerError(res));
        return;
    }

    const data = await res.json();
    document.getElementById("info-categoria").textContent = data.categoria.toUpperCase();
    document.getElementById("info-dificultad").textContent = data.dificultad.toUpperCase();
    document.getElementById("palabra").textContent = data.palabra_oculta;
    document.getElementById("mensaje").textContent = MENSAJES[0];
    document.getElementById("fallos").textContent = `Fallos: 0 / ${data.max_fallos}`;

    crearTeclado();
    dibujar(0);
    mostrarPantalla("juego");
}

function crearTeclado() {
    const cont = document.getElementById("teclado");
    cont.innerHTML = "";

    FILAS.forEach(fila => {
        const div = document.createElement("div");
        div.className = "tecla-fila";

        for (const letra of fila) {
            const btn = document.createElement("button");
            btn.textContent = letra;
            btn.className = "tecla";
            btn.onclick = () => intentar(letra.toLowerCase(), btn);
            div.appendChild(btn);
        }
        cont.appendChild(div);
    });
}

async function intentar(letra, btn) {
    btn.disabled = true;

    const res = await fetch("/api/intentar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": tokenCsrf()
        },
        body: JSON.stringify({ letra })
    });

    if (!res.ok) {
        alert(await leerError(res));
        btn.disabled = false;
        return;
    }

    const data = await res.json();

    if (data.error) {
        alert(data.error);
        btn.disabled = false;
        return;
    }

    if (data.correctas.includes(letra)) {
        btn.classList.add("correcta");
    } else {
        btn.classList.add("fallida");
    }

    document.getElementById("palabra").textContent = data.palabra_oculta;
    document.getElementById("fallos").textContent = `Fallos: ${data.fallos} / ${data.max_fallos}`;
    document.getElementById("mensaje").textContent = MENSAJES[Math.min(data.fallos, 6)];

    dibujar(data.fallos);

    if (data.terminado) {
        // Deshabilitar todas las teclas
        document.querySelectorAll(".tecla").forEach(b => b.disabled = true);

        setTimeout(() => {
            const titulo = document.getElementById("resultado-titulo");
            const palabra = document.getElementById("resultado-palabra");
            const fallos = document.getElementById("resultado-fallos");

            if (data.resultado === "victoria") {
                titulo.textContent = "🏆 ¡VICTORIA! 🏆";
                titulo.className = "victoria";
            } else {
                titulo.textContent = "💀 DERROTA 💀";
                titulo.className = "derrota";
            }

            palabra.textContent = `La palabra era: ${data.palabra_completa}`;
            fallos.textContent = `Fallos: ${data.fallos} / ${data.max_fallos}`;

            mostrarPantalla("resultado");
        }, 800);
    }
}

function dibujar(nf) {
    const c = document.getElementById("canvas");
    const ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);

    ctx.strokeStyle = "#8B7355";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(30, 260);
    ctx.lineTo(270, 260);
    ctx.stroke();

    ctx.strokeStyle = "#8B4513";
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(80, 260);
    ctx.lineTo(80, 30);
    ctx.stroke();

    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(80, 30);
    ctx.lineTo(200, 30);
    ctx.stroke();

    ctx.strokeStyle = "#D2B48C";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(200, 30);
    ctx.lineTo(200, 60);
    ctx.stroke();

    ctx.strokeStyle = "#8B4513";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(80, 70);
    ctx.lineTo(120, 30);
    ctx.stroke();

    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3;

    if (nf >= 1) {
        ctx.beginPath();
        ctx.arc(200, 85, 25, 0, Math.PI * 2);
        ctx.stroke();
        // Ojos
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(190, 80); ctx.lineTo(195, 85); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(205, 80); ctx.lineTo(210, 85); ctx.stroke();
        // Boca
        ctx.beginPath(); ctx.moveTo(192, 98); ctx.lineTo(208, 98); ctx.stroke();
    }

    if (nf >= 2) {
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(200, 110);
        ctx.lineTo(200, 180);
        ctx.stroke();
    }

    if (nf >= 3) {
        ctx.beginPath();
        ctx.moveTo(200, 130);
        ctx.lineTo(160, 160);
        ctx.stroke();
    }

    if (nf >= 4) {
        ctx.beginPath();
        ctx.moveTo(200, 130);
        ctx.lineTo(240, 160);
        ctx.stroke();
    }

    if (nf >= 5) {
        ctx.beginPath();
        ctx.moveTo(200, 180);
        ctx.lineTo(165, 230);
        ctx.stroke();
    }

    if (nf >= 6) {
        ctx.beginPath();
        ctx.moveTo(200, 180);
        ctx.lineTo(235, 230);
        ctx.stroke();
    }
}

async function anadirPalabra() {
    const palabra = document.getElementById("nueva-palabra").value.trim();
    const categoria = document.getElementById("nueva-categoria").value.trim();
    const dificultad = document.getElementById("nueva-dificultad").value;
    const msg = document.getElementById("anadir-msg");

    if (!palabra || !categoria || !dificultad) {
        msg.style.color = "#ff8c7a";
        msg.textContent = "Rellena todos los campos";
        return;
    }

    const res = await fetch("/api/anadir", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": tokenCsrf()
        },
        body: JSON.stringify({ palabra, categoria, dificultad })
    });

    const data = await res.json();

    if (data.ok) {
        msg.style.color = "#2ecc71";
        msg.textContent = data.mensaje;
        document.getElementById("nueva-palabra").value = "";
        document.getElementById("nueva-categoria").value = "";
        document.getElementById("nueva-dificultad").value = "";
    } else {
        msg.style.color = "#ff8c7a";
        msg.textContent = data.error || (await leerError(res));
    }
}

async function cargarPalabras() {
    const res = await fetch("/api/palabras");
    if (!res.ok) {
        throw new Error(await leerError(res));
    }
    const palabras = await res.json();
    const cont = document.getElementById("lista-palabras");

    if (palabras.length === 0) {
        cont.innerHTML = "<p>No hay palabras registradas.</p>";
        return;
    }

    let html = "";
    let catActual = "";

    for (const p of palabras) {
        if (p.categoria !== catActual) {
            catActual = p.categoria;
            html += `<div class="cat-titulo">⚔ ${catActual.toUpperCase()} ⚔</div>`;
        }
        html += `<div class="palabra-item dif-${p.dificultad}">• ${p.palabra} [${p.dificultad}]</div>`;
    }

    cont.innerHTML = html;
}
