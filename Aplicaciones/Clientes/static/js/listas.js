let rutaVista = "../../../";
let vista = document.getElementById('vista').value;
let idRegistro = document.getElementById('idRegistro').value;
let idPais = document.getElementById('idPais').value;
let pais = document.getElementById('Pais').value;
let idRegion = document.getElementById('idRegion').value;
let region = document.getElementById('Region').value;
let idCodDomFis = document.getElementById('idCodDomFis').value;
let idCodPos = document.getElementById('idCodPos').value;
let iniDistrito = document.getElementById('iniDistrito').value;
let coddomfis = document.getElementById('CodDomFis').value;

window.addEventListener("load", async () => {
    await cargaInicial();
});

const cargaInicial = async() => {
    await ListarPaises();
    await ListarEstados(idPais, true);
    if(idPais=="MX") {
        await ListarCodPos(idRegion, true);        
        if(idRegistro > 0) {
            await ListarColonias(idCodPos, true);   }
    }

    PaisRegion.addEventListener("change", (event) => {

        let tagNac = document.getElementById('dataNac');
        let tagInt = document.getElementById('dataInt');
        var tagUS = false
        if(vista=="Cliente") {
            tagUS = document.getElementById('dataUS');  }

        if(event.target.value != "MX") {
            tagNac.setAttribute("hidden", true);
            tagInt.removeAttribute("hidden");
            if(vista=="Cliente") {
                if(event.target.value == "US") {
                    tagUS.removeAttribute("hidden"); }                
                else {
                    tagUS.setAttribute("hidden", true); }
            }
        }
        else {
            tagInt.setAttribute("hidden", true);
            tagNac.removeAttribute("hidden");
        }
        ListarEstados(event.target.value, false);   
    });

    Estado.addEventListener("change", (event) => {
        ListarCodPos(event.target.value);
        clearColonias();
    });

    CodigoPostal.addEventListener("change", (event) => {
        ListarColonias(event.target.value);
    });
};

const ListarPaises = async() => {
    try {
        const response = await fetch(`${rutaVista}paises/`);
        const data = await response.json();
        console.log(data);
        if(data.message == "Success") {
            opciones = `<option value='${idPais}'>${pais}</option>`;
            data.paises.forEach((pais)=> {
                opciones += `<option value='${pais.CodeId}'>${pais.Descrip}</option>`;
            });
            PaisRegion.innerHTML = opciones;
        }
        else {
            alert("Países no encontrados");
        }

    } catch (error) {
        console.log(error);
    }
};

const ListarEstados = async(idPais, inival) => {
    let opciones = ``;
    try {
        const response = await fetch(`${rutaVista}estados/${idPais}`);
        const data = await response.json();
        console.log(data);
        if(data.message == "Success") {            
            if (inival) {
                opciones = `<option value='${idRegion}'>${region}</option>`;
            } else {
                if(idPais=="MX") {
                    opciones = `<option value='CMX'>Ciudad de México</option>`;
                    ListarCodPos('CMX');
                }    
            }

            estados = data.estados;
            estados.forEach((estado)=> {
                opciones += `<option value='${estado.CodeId}'>${estado.Descrip}</option>`;
            });
            Estado.innerHTML = opciones;

            if(vista=='Cliente') {
                if(idPais=="US") {
                    CodigoDomFiscal.innerHTML = opciones;   }
                else {
                    opciones = ``;
                    CodigoDomFiscal.innerHTML = opciones;   }
            }
        }
        else {
            Estado.innerHTML = opciones;
            alert("Estados no encontrados");
        }
    } catch (error) {
        console.log(error);
    }
};

const ListarCodPos = async(idRegion, inival) => {
    try {
        const response = await fetch(`${rutaVista}codigos/${idRegion}`);
        const data = await response.json();
        console.log(data);
        if(data.message == "Success") {
            let opciones = ``;
            if(inival) {
                if( idCodPos != "")
                opciones = `<option value='${idCodPos}'>${idCodPos}</option>`;            
            }
            codigos = data.codigos;
            codigos.forEach((codigo)=> {
                opciones += `<option value='${codigo.D_codigo}'>${codigo.D_codigo}</option>`;
            });
            CodigoPostal.innerHTML = opciones;
        }
        else {
            if(!inival)
                alert("Códigos Postales no encontrados");
        }

    } catch (error) {
        console.log(error); }
};

const ListarColonias = async(CodPos, inival) => {
    try {
        const response = await fetch(`${rutaVista}colonias/${CodPos}`);
        const data = await response.json();
        console.log(data);
        var counter=0;
        if(data.message == "Success") {
            let opciones = ``;
            if (inival) {
                if( iniDistrito != "")
                opciones = `<option value='${iniDistrito}'>${iniDistrito}</option>`;
            }
            colonias = data.colonias;
            colonias.forEach((colonia)=> {
                if(counter==0)
                    mnpio = colonia.D_mnpio;
                opciones += `<option value='${colonia.D_asenta}'>${colonia.D_asenta}</option>`;
            });
            Distrito.innerHTML = opciones;
            getCiudad(mnpio);
        }
        else {
            alert("Colonias no encontrados");
        }

    } catch (error) {
        console.log(error);
    }
};

const clearColonias = async() => {
    let opciones = ``;
    Distrito.innerHTML = opciones;
    getCiudad("")
};

const clearInternacional = async() => {
    $("#IntCodigoPostal").val("");
    $("#IntCiudad").val("");
    $("#IntDistrito").val("");
};

const clearNacional = async() => {
    let opciones = ``;
    CodigoPostal.innerHTML = opciones;
    Distrito.innerHTML = opciones;
    $("#Ciudad").val("");
};

const getCiudad = async(mnpio) => {
    $("#Ciudad").val(mnpio);
};


