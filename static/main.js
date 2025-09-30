// Búsqueda usando la API simple
const buscador = document.getElementById('buscador');
const resultados = document.getElementById('resultados');


if (buscador) {
let timer = null;
buscador.addEventListener('input', function(e){
clearTimeout(timer);
const q = e.target.value.trim();
if (!q) { resultados.innerHTML = ''; return }
timer = setTimeout(()=>{
fetch(`/api/search?q=${encodeURIComponent(q)}`)
.then(r=>r.json())
.then(data=>{
if (!data.results || data.results.length===0){
resultados.innerHTML = '<div>No hay resultados</div>';
return;
}
const html = data.results.map(r=>{
if (r.type === 'curso'){
return `<div class="res"><a href="/curso/${r.curso_slug}">${r.titulo} (curso)</a></div>`
} else {
return `<div class="res"><a href="/curso/${r.curso_slug}/tema/${r.tema_slug}">${r.titulo} (tema)</a></div>`
}
}).join('')
resultados.innerHTML = html;
})
}, 300)
})
}