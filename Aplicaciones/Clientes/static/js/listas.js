const ListarPaises = async () => {
    try {
        const response = await fetch("./paises");
        const data = await response.json();
        
        if(data.message == "Success") {
            let opciones = ``;
            data.paises.foreach((pais)=> {
                opciones += `<option value='${pais.IdCliente}'>${pais.NombreCliente}</option>`;
            });
        }
        else {
            alert("Países no encontrados");
        }
    }
    catch (error) {
        console.log(error);
    }
}

const cargaInicial = async() => {
    await ListarPaises();
}

window.addEventListener("load", async () => {
    await cargaInicial();
})